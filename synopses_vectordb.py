from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

import json


with open('./data/synopses.json', 'r') as f:
    synopses_data = [json.loads(synopsis) for synopsis in f.readlines()]
f.close()

synopses_docs = [Document(page_content=synopsis["synopsis"], metadata={"id":synopsis["id"]}) for synopsis in synopses_data]

embeddings = OpenAIEmbeddings()
vector_db = FAISS.from_documents(synopses_docs, embeddings)

vector_db.save_local("synopses_vectordb")
