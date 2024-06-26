import os

from django.conf import settings
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from pymongo import MongoClient

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

import json


def get_mongo_client():
    client = MongoClient('mongodb://admin:admin@localhost:27017/')
    db = client['moviedb']
    return db

@api_view(['POST'])
def short_form(request):
    query = request.POST.get('query')
    if query is None:
        return Response({'error': 'Query not provided'}, status=400)

    embeddings = OpenAIEmbeddings()
    synopses_vectordb = FAISS.load_local(os.path.join(settings.BASE_DIR, '..', 'synopses_vectordb'), embeddings, allow_dangerous_deserialization=True)
    synopses_retriever = synopses_vectordb.as_retriever(search_kwargs={"k": 1})
    synopsis_doc = synopses_retriever.invoke(query)

    db = get_mongo_client()
    scenes_collection = db.scenes
    scene_id = synopsis_doc[0].metadata["id"]
    scene = scenes_collection.find_one({"id": scene_id})

    synopsis = synopsis_doc[0].page_content
    scene_timestamp = {"timestamp": scene["timestamp"], "synopsis": synopsis}

    return Response(scene_timestamp)

@api_view(['POST'])
def video_qa(request):
    query = request.POST.get('query')
    if query is None:
        return Response({'error': 'Query not provided'}, status=400)

    embeddings = OpenAIEmbeddings()
    synopses_vectordb = FAISS.load_local(os.path.join(settings.BASE_DIR, '..', 'synopses_vectordb'), embeddings, allow_dangerous_deserialization=True)

    synopses_retriever = synopses_vectordb.as_retriever(search_kwargs={"k": 5})
    synopses_docs = synopses_retriever.invoke(query)

    synopses = "\n\n".join([synopsis_doc.page_content for synopsis_doc in synopses_docs])

    llm = ChatOpenAI(model="gpt-4-turbo-preview")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You answer questions about a movie."),
        ("user", "Relevant Movie Scenes: {synopses}\n\nAnswer the followig question. {input}")
    ])

    llm_chain = prompt | llm
    answer = llm_chain.invoke({"input": query, "synopses": synopses}).content

    return Response({"answer": answer})

@api_view(['POST'])
def avatar_chat(request):
    query = request.POST.get('query')
    character = request.POST.get('character')
    if query is None or character is None:
        return Response({'error': 'Query or character not provided'}, status=400)

    embeddings = OpenAIEmbeddings()
    synopses_vectordb = FAISS.load_local(os.path.join(settings.BASE_DIR, '..', 'synopses_vectordb'), embeddings, allow_dangerous_deserialization=True)
    synopses_retriever = synopses_vectordb.as_retriever(search_kwargs={"k": 5})
    synopses_docs = synopses_retriever.invoke(query)

    db = get_mongo_client()
    scenes_collection = db.scenes
    scenes_data = []

    for synopsis_doc in synopses_docs:
        scene = scenes_collection.find_one({"id": synopsis_doc.metadata["id"]})
        if scene:
            synopsis = synopsis_doc.page_content
            dialogue = scene["subtitles"]
            scenes_data.append(f"Scene Synopsis: {synopsis}\n\nDialogue:\n\n{dialogue}")

    if not scenes_data:
        return Response({'error': 'No relevant scenes found'}, status=404)

    dialogues = "\n\n####\n\n".join(scenes_data)

    llm = ChatOpenAI(model="gpt-4-turbo-preview")
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a role-playing chatbot. Act as if you are the movie character {character} and answer the question. You must imitate the character's style of speech."),
        ("user", "{dialogues}\n\nAnswer the following question: {input}")
    ])

    llm_chain = prompt | llm
    answer = llm_chain.invoke({"input": query, "dialogues": dialogues}).content

    return Response({"answer": answer})

