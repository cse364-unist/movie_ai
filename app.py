import streamlit as st
import requests
import time


def get_scene(query):
    response = requests.post(
        'http://localhost:8000/movieapi/short_form',
        data={'query': query},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Error: ' + response.text)
        return None

def get_video_qa_answer(query):
    response = requests.post(
        'http://localhost:8000/movieapi/video_qa',
        data={'query': query},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Error: ' + response.text)
        return None

def get_avatar_chat(query, character):
    response = requests.post(
        'http://localhost:8000/movieapi/avatar_chat',
        data={'query': query, 'character': character},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Error: ' + response.text)
        return None

def handle_input(user_input):
    if user_input.startswith('/scene'):
        query = user_input.replace('/scene', '').strip()
        scene_info = get_scene(query)
        if scene_info:
            start = scene_info['timestamp']['start']
            end = scene_info['timestamp']['end']
            synopsis = scene_info['synopsis']
            st.session_state.messages.append(('system', synopsis))
            st.session_state.messages.append(('system', "Enter /revert to revert."))

            start_time = int(start.split(':')[0]) * 60 + int(start.split(':')[1])
            end_time = int(end.split(':')[0]) * 60 + int(end.split(':')[1])
            st.session_state.video_start_time = start_time
            st.session_state.video_end_time = end_time

    elif user_input.startswith('/qa'):
        query = user_input.replace('/qa', '').strip()
        answer_info = get_video_qa_answer(query)
        if answer_info:
            st.session_state.messages.append(('system', answer_info['answer']))

    elif user_input.startswith('/chat'):
        parts = user_input.replace('/chat', '').strip().split('--avatar')
        query = parts[0].strip()
        character = parts[1].strip() if len(parts) > 1 else None
        if character:
            chat_info = get_avatar_chat(query, character)
            if chat_info:
                st.session_state.messages.append(('system', f"{character} says - {chat_info['answer']}"))
        else:
            st.error("Character not specified. Use the format `/chat query --avatar character`.")

    elif user_input.strip() == '/revert':
        st.session_state.messages.append(('system', "Video player reverted to original full mode."))
        st.session_state.video_start_time = 0
        st.session_state.video_end_time = None

def highlight_commands(message):
    message = message.replace('/scene', '<span style="color: blue;">/scene</span>')
    message = message.replace('/qa', '<span style="color: blue;">/qa</span>')
    message = message.replace('/chat', '<span style="color: blue;">/chat</span>')
    message = message.replace('--avatar', '<span style="color: blue;">--avatar</span>')
    message = message.replace('/revert', '<span style="color: blue;">/revert</span>')
    return message

def stream_message(message):
    for word in message.split():
        yield word + " "
        time.sleep(0.02)

st.title('Movie Understanding Web App')

video_path = "./data/movie.mp4"
if "video_start_time" not in st.session_state:
    st.session_state.video_start_time = None
if "video_end_time" not in st.session_state:
    st.session_state.video_end_time = None

if st.session_state.video_start_time is not None and st.session_state.video_end_time is not None:
    st.video(video_path, start_time=st.session_state.video_start_time, end_time=st.session_state.video_end_time)
else:
    st.video(video_path)

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, message in st.session_state.messages:
    with st.chat_message(role):
        if role == 'system':
            st.markdown(message)
        else:
            highlighted_message = highlight_commands(message)
            st.markdown(highlighted_message, unsafe_allow_html=True)

if prompt := st.chat_input("Enter messages. Available commands: `/scene`, `/qa`, `/chat`"):

    st.session_state.messages.append(('user', prompt))
    handle_input(prompt)

    with st.chat_message("user"):
        highlighted_message = highlight_commands(prompt)
        st.markdown(highlighted_message, unsafe_allow_html=True)

    for role, message in st.session_state.messages[-2:]:
        if role == 'system':
            with st.chat_message(role):
                st.write_stream(stream_message(message))

