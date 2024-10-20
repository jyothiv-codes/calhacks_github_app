import asyncio
import os
import streamlit as st  # Streamlit framework
from authenticator import Authenticator
from connection import Connection
from dotenv import load_dotenv
from pyaudio import PyAudio, paInt16


# Apply custom CSS for white background and black text
st.markdown(
    """
    <style>
        body {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        .stButton button {
            background-color: #000000;
            color: #FFFFFF;
            font-size: 18px;
            border-radius: 10px;
            width: 200px;
            height: 50px;
        }
    </style>
    """,
    unsafe_allow_html=True,

)

# Streamlit Title
st.title("Hi! I'm Chillbert")

# Audio format and parameters
FORMAT = paInt16
CHANNELS = 1
SAMPLE_WIDTH = 2  # PyAudio.get_sample_size(pyaudio, format=paInt16)
CHUNK_SIZE = 1024

# Hardcoded audio device indices and sample rate
INPUT_DEVICE_INDEX = 0  # Replace with correct input device index if needed
OUTPUT_DEVICE_INDEX = 1  # Replace with correct output device index if needed
SAMPLE_RATE = 48000  # Set your desired sample rate

# Initialize session state variables
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
    """
    Load API credentials from environment variables and fetch an access token.
    """
    load_dotenv()

    # Retrieve API key and Secret key from environment variables
    HUME_API_KEY = os.getenv("HUME_API_KEY")
    HUME_SECRET_KEY = os.getenv("HUME_SECRET_KEY")
    HUME_CONFIG_ID=os.getenv("HUME_CONFIG_ID")
   

    if HUME_API_KEY is None or HUME_SECRET_KEY is None:
        st.error("HUME_API_KEY and HUME_SECRET_KEY must be set in environment variables.")
        st.stop()

    authenticator = Authenticator(HUME_API_KEY, HUME_SECRET_KEY)
    return authenticator.fetch_access_token()


# Start conversation button with a unique key
if st.button("Start Conversation", key="start_button"):
    st.write("Let's fetch your buddy!")
    
    # Run the async task using the custom event loop
    loop = st.session_state.loop
    st.session_state.task = loop.create_task(main())
    loop.run_until_complete(st.session_state.task)
