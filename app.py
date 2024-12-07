import streamlit as st
from dotenv import load_dotenv
# from pages import start_conversation

st.set_page_config(page_title="Chillbert - Mood-Driven Voice Assistant", layout="wide")
# Load environment variables
load_dotenv()


# Sidebar navigation
st.sidebar.image("ChillbertLogo-removebg-preview.png", use_column_width=True)
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
