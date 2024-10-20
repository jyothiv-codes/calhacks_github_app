import streamlit as st
import asyncio
import os
import streamlit as st  # Streamlit framework
from authenticator import Authenticator
from connection import Connection
from dotenv import load_dotenv
from pyaudio import PyAudio, paInt16


# Audio format and parameters
FORMAT = paInt16
CHANNELS = 1
SAMPLE_WIDTH = 2  # PyAudio.get_sample_size(pyaudio, format=paInt16)
CHUNK_SIZE = 1024

# Hardcoded audio device indices and sample rate
INPUT_DEVICE_INDEX = 0  # Replace with correct input device index if needed
OUTPUT_DEVICE_INDEX = 1  # Replace with correct output device index if needed
SAMPLE_RATE = 48000  # Set your desired sample rate

if "task" not in st.session_state:
    st.session_state.task = None
if "loop" not in st.session_state:
    st.session_state.loop = asyncio.new_event_loop()


# Main asynchronous function
async def main():
    """
    Main asynchronous function to set up audio devices, authenticate, and connect to the Hume AI websocket.
    """
    # Initialize PyAudio instance
    pyaudio = PyAudio()

    # Open the audio stream with the selected parameters
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

    # Fetch the access token for authentication
    access_token = get_access_token()

    # Construct the websocket URL with the access token
    socket_url = (
        "wss://api.hume.ai/v0/assistant/chat?"
        f"access_token={access_token}&"
        f"config_id=9a7e6382-efba-4cff-9dd2-1d16eceefce2"
    )

    try:
        # Connect to the websocket and start the audio stream
        await Connection.connect(
            socket_url,
            audio_stream,
            SAMPLE_RATE,
            SAMPLE_WIDTH,
            CHANNELS,
            CHUNK_SIZE,
        )
    except asyncio.CancelledError:
        st.write("Conversation ended.")
    finally:
        # Close the PyAudio stream and terminate PyAudio
        audio_stream.stop_stream()
        audio_stream.close()
        pyaudio.terminate()


def get_access_token() -> str:
    load_dotenv()

    # Retrieve API key and Secret key from environment variables
    #HUME_API_KEY = os.getenv("HUME_API_KEY")
    #HUME_SECRET_KEY = os.getenv("HUME_SECRET_KEY")
    HUME_CONFIG_ID="9a7e6382-efba-4cff-9dd2-1d16eceefce2"
    HUME_API_KEY="g9YCR9LZyFnRlAPuiVrjn0AO3GUGJUXdhftMq2zQDMFVOA6G"
    HUME_SECRET_KEY="ibojNQZAAo756z1rvxBGUS3YGtU4nWvopMh6BjQFLyWEaW3YWA4NIGZQMAgD4gbv"

    if HUME_API_KEY is None or HUME_SECRET_KEY is None:
        st.error("HUME_API_KEY and HUME_SECRET_KEY must be set in environment variables.")
        st.stop()

    authenticator = Authenticator(HUME_API_KEY, HUME_SECRET_KEY)
    return authenticator.fetch_access_token()
def chillbert_response():
    #return "Hello! I'm Chillbert, how can I help you today?"
    """ = st.session_state.loop
    st.session_state.task = loop.create_task(main())
    loop.run_until_complete(st.session_state.task)"""
    return

# Streamlit layout
st.set_page_config(page_title="Chillbert - Mood-Driven Voice Assistant", layout="wide")


# Add custom CSS for background color and other styles
st.markdown("""
    <style>
    #      [data-testid=stSidebar] {
    #     background-color:rgb(11 87 137);
    #     opacity: 0.1
    #     color:white
    # } 
            
    /* Full background color for the first column behind the image */
    .col1-background {
        background-color: #F0F8FF; /* Light blue color */
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 50%; /* Adjust depending on the column width */
        z-index: -1; /* Put the background behind the content */
    }

    /* Flexbox to keep the image centered */
    .image-container {
        display: flex;
        align-items: center;
        justify-content: center;
        /* height: 100vh; Full height to ensure vertical centering */
    }

    /* Button hover effect */
    .stButton > button:hover {
        background-color: #FF5733;
        color: white;
    }

    /* Button style */
    .stButton > button {
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


# Sidebar for navigation
#st.sidebar.title("Chillbert")
st.sidebar.markdown('<h1 style="text-align:center; color:white">Chillbert</h1>', unsafe_allow_html=True)
page = st.sidebar.radio("Navigate", ["Start Conversation", "For Practitioners"])

# First Page: Start Conversation with Chillbert
if page == "Start Conversation":
    st.title("Welcome to Chillbert!")
    
    # Layout with two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Apply background color to the whole column without affecting the image
        st.markdown('<div class="col1-background"></div>', unsafe_allow_html=True)
        
        # Flexbox to center the image properly
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image("chillbert3.png", caption="Chillbert", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # Create a centered container
        st.markdown('<div class="centered-text">', unsafe_allow_html=True)
        st.write("### Ask Chillbert Anything!")
        if st.button("Say Hello"):
            loop = st.session_state.loop
            st.session_state.task = loop.create_task(main())
            loop.run_until_complete(st.session_state.task)
        st.markdown('</div>', unsafe_allow_html=True)

# Second Page: For Practitioners
if page == "For Practitioners":
    st.title("Practitioner Dashboard")
    
    # Layout with two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Apply background color to the whole column without affecting the image
        st.markdown('<div class="col1-background"></div>', unsafe_allow_html=True)
        
        # Flexbox to center the image properly
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image("chillbert3.png", caption="Chillbert", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # Create a centered container for the question and button
        st.markdown('<div class="centered-text">', unsafe_allow_html=True)
        st.write("### Ask a Question to Chillbert")
        question = st.text_input("Enter your question here")
        if st.button("Submit"):
            response = chillbert_response()  # Replace with llm_response(question)
            st.write(response)
        st.markdown('</div>', unsafe_allow_html=True)
