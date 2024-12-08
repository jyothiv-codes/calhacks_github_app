import streamlit as st
from dotenv import load_dotenv
# from pages import start_conversation

st.set_page_config(page_title="Chillbert - Mood-Driven Voice Assistant", layout="wide")
# Load environment variables
load_dotenv()


# Sidebar navigation
st.sidebar.image("ChillbertLogo-removebg-preview.png", use_container_width=True)
# page = st.sidebar.radio("Navigate", ["Start Conversation", "For Practitioners"])

USERNAME = "admin"
PASSWORD = "pass123"

# # Initialize session state for login
# if "user" not in st.session_state:
#     st.session_state.user = False

# Login Page
if "user" not in st.session_state:
    st.title("Login to Chillbert")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.user = username
            st.success("Login successful!")
            # st.experimental_rerun()  # Refresh the app to show the main page
        else:
            st.error("Invalid username or password.")
else:
    st.title(f"Hello {st.session_state.user}! Start a Conversation or Analyse Chat")
    if st.button("Logout"):
        del st.session_state["user"]

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.write("© 2024 Made with Love by Team Powerpuff Girls | Powered by Streamlit")
st.markdown('</div>', unsafe_allow_html=True)
