import streamlit as st
from dotenv import load_dotenv
import boto3
import os
from botocore.exceptions import ClientError
# from pages import start_conversation

st.set_page_config(page_title="Chillbert - Mood-Driven Voice Assistant", layout="wide")
# Load environment variables
load_dotenv()

REGION = os.getenv('REGION', 'us-east-1')
COGNITO_CLIENT_ID = os.getenv('CONGNITO_CLIENT_ID')
USER_POOL_ID = os.getenv('USER_POOL_ID')
# Sidebar navigation
st.sidebar.image("ChillbertLogo-removebg-preview.png", use_container_width=True)
# page = st.sidebar.radio("Navigate", ["Start Conversation", "For Practitioners"])


## NOTE: Cognito
class CognitoAuth:
    def __init__(self):
        """
        Initialize Cognito client with configuration.
        """
        self.client = boto3.client('cognito-idp', region_name=REGION)

    def login(self, username, password):
        """
        Handle user login using SRP authentication flow.
        """
        try:
            auth_response = self.client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                ClientId=COGNITO_CLIENT_ID,
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            return True, auth_response['AuthenticationResult']['AccessToken']
        except ClientError as e:
            return False, e.response['Error']['Message']

# Login Page

auth = CognitoAuth()

if "user" not in st.session_state:

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="col1-background"></div>', unsafe_allow_html=True)
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.markdown("![chillbert.gif](https://cdn.dribbble.com/users/7421625/screenshots/18722183/media/57f4bd5aea84c23e226069f65e417704.gif)")
            
    with col2:
        st.title("Welcome to Chillbert!")
        st.markdown("<h3>Please Login to continue</h3>", unsafe_allow_html=True)
        
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if login_username and login_password:
                success, result = auth.login(login_username, login_password)
                if success:
                    st.success("Login successful!")
                    st.session_state['user']=login_username
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.error("Please enter both username and password")
else:
    st.title(f"Hello {st.session_state.user}! Start a Conversation")
    if st.button("Logout"):
        del st.session_state["user"]

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.write("© 2024 Made with Love by Team Powerpuff Girls | Powered by Streamlit")
st.markdown('</div>', unsafe_allow_html=True)
