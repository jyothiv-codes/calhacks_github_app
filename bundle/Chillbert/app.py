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
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="col1-background"></div>', unsafe_allow_html=True)
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.markdown("![chillbert.gif](https://cdn.dribbble.com/users/7421625/screenshots/18722183/media/57f4bd5aea84c23e226069f65e417704.gif)")
            
    with col2:
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
