import asyncio
import streamlit as st
import os
from src.authenticator import Authenticator
from src.analyse_chat import AnalyseChat
from src.connection import Connection
from pyaudio import PyAudio, paInt16

st.set_page_config(page_title="Chillbert - Mood-Driven Voice Assistant", layout="wide")

# Constants
FORMAT = paInt16
CHANNELS = 1
SAMPLE_WIDTH = 2
CHUNK_SIZE = 1024
INPUT_DEVICE_INDEX = 0
OUTPUT_DEVICE_INDEX = 1
SAMPLE_RATE = 48000

if "task" not in st.session_state:
    st.session_state.task = None
if "loop" not in st.session_state:
    st.session_state.loop = asyncio.new_event_loop()

def get_access_token() -> str:

    # Retrieve API key and Secret key from environment variables
    HUME_API_KEY = os.getenv("HUME_API_KEY")
    HUME_SECRET_KEY = os.getenv("HUME_SECRET_KEY")

    if HUME_API_KEY is None or HUME_SECRET_KEY is None:
        st.error("HUME_API_KEY and HUME_SECRET_KEY must be set in environment variables.")
        st.stop()

    authenticator = Authenticator(HUME_API_KEY, HUME_SECRET_KEY)
    return authenticator.fetch_access_token()


async def main():
    pyaudio = PyAudio()
    audio_stream = pyaudio.open(
        format=FORMAT,
        channels=CHANNELS,
        frames_per_buffer=CHUNK_SIZE,
        rate=SAMPLE_RATE,
        input=True,
        output=True,
        input_device_index=INPUT_DEVICE_INDEX,
        output_device_index=OUTPUT_DEVICE_INDEX,
    )
    access_token = get_access_token()
    socket_url = f"wss://api.hume.ai/v0/assistant/chat?access_token={access_token}&config_id=9a7e6382-efba-4cff-9dd2-1d16eceefce2"
    
    try:
        await Connection.connect(socket_url, audio_stream, SAMPLE_RATE, SAMPLE_WIDTH, CHANNELS, CHUNK_SIZE)
    except asyncio.CancelledError:
        st.write("Conversation ended.")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pyaudio.terminate()


if "user" not in st.session_state:
    st.error("Please Login to continue")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="col1-background"></div>', unsafe_allow_html=True)
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.markdown("![chillbert.gif](https://cdn.dribbble.com/users/7421625/screenshots/18722183/media/57f4bd5aea84c23e226069f65e417704.gif)")
            
    with col2:
        loop = st.session_state.loop
        st.markdown('<h4>Your emotional sidekick with cool vibes!</h4>', unsafe_allow_html=True)
        if st.button("Say Hello"):
            st.session_state.task = loop.create_task(main())
            loop.run_until_complete(st.session_state.task)
        if st.button("Say Bye"):
            ac = AnalyseChat(st.session_state['user'])
            ac.store_ac()
            # st.session_state['ac'] = ac
            # print("AC UPDATED")
            try:
                if st.session_state.task is not None and not st.session_state.task.done():
                    st.session_state.task.cancel()  # Cancel the WebSocket connection task
                    try:
                        loop.run_until_complete(st.session_state.task)  # Ensure it's fully canceled
                    except asyncio.CancelledError:
                        print("Connection closed successfully.")
            # st.write(response)
            except BaseException as e:
                print(e)
        st.markdown('</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.image("ChillbertLogo-removebg-preview.png", use_container_width=True)
# page = st.sidebar.radio("Navigate", ["Start Conversation", "For Practitioners"])

# # Page navigation logic
# if page == "Start Conversation":
#     start_conversation.render_page()
# elif page == "For Practitioners":
#     practitioner_dashboard.render_page()

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.write("© 2024 Made with Love by Team Powerpuff Girls | Powered by Streamlit")
st.markdown('</div>', unsafe_allow_html=True)