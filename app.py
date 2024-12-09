import streamlit as st
import boto3
import os
from botocore.exceptions import ClientError
import webbrowser
from dotenv import load_dotenv

st.set_page_config(page_title="Chillbert - Mood-Driven Voice Assistant", layout="wide")
# Load environment variables
load_dotenv()

class Config:
    def __init__(self):
        """
        Configuration class that holds AWS Cognito settings.
        We no longer need S3 configuration since we're using a direct pre-signed URL.
        """
        self.USER_POOL_ID = os.getenv('USER_POOL_ID')
        self.CLIENT_ID = os.getenv('CONGNITO_CLIENT_ID')
        self.REGION = os.getenv('REGION', 'us-east-1')
        # Store the pre-signed URL as a constant
        self.MACOS_DOWNLOAD_URL = os.getenv('MACOS_DOWNLOAD_URL')


class CognitoAuth:
    def __init__(self, config):
        """
        Initialize Cognito client with configuration.
        """
        self.config = config
        self.client = boto3.client('cognito-idp', region_name=config.REGION)
    
    def sign_up(self, username, password, email, given_name, family_name):
        """
        Handle new user registration with required name attributes.
        The function now includes given_name and family_name as required by the schema.
        """
        try:
            response = self.client.sign_up(
                ClientId=self.config.CLIENT_ID,
                Username=username,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'given_name', 'Value': given_name},
                    {'Name': 'family_name', 'Value': family_name}
                ]
            )
            return True, "Registration successful! Please check your email for verification code."
        except ClientError as e:
            return False, e.response['Error']['Message']

    def verify_email(self, username, code):
        """
        Confirm user's email with verification code.
        """
        try:
            response = self.client.confirm_sign_up(
                ClientId=self.config.CLIENT_ID,
                Username=username,
                ConfirmationCode=code
            )
            return True, "Email verified successfully!"
        except ClientError as e:
            return False, e.response['Error']['Message']

    def login(self, username, password):
        """
        Handle user login using SRP authentication flow.
        """
        try:
            auth_response = self.client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                ClientId=self.config.CLIENT_ID,
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            return True, auth_response['AuthenticationResult']['AccessToken']
        except ClientError as e:
            return False, e.response['Error']['Message']

def main():
    """
    Main Streamlit application with OS download buttons.
    The macOS button now directly uses the pre-signed URL for downloads.
    """
    config = Config()
    auth = CognitoAuth(config)

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("Welcome to Chillbert!")
        st.markdown("<h3>Please Login to continue</h3>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.header("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login"):
                if login_username and login_password:
                    success, result = auth.login(login_username, login_password)
                    if success:
                        st.session_state.authenticated = True
                        st.success("Login successful!")
                        st.session_state['user']=login_username
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.error("Please enter both username and password")
        
        with tab2:
            st.header("Register")
            
            # Enhanced registration form with name fields
            reg_given_name = st.text_input("First Name", key="reg_given_name")
            reg_family_name = st.text_input("Last Name", key="reg_family_name")
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            
            # Password requirements helper text
            st.caption("""Password must contain:
            - At least 8 characters
            - Uppercase and lowercase letters
            - Numbers
            - Special characters""")
            
            if st.button("Register"):
                if all([reg_given_name, reg_family_name, reg_username, reg_email, reg_password]):
                    success, result = auth.sign_up(
                        reg_username, 
                        reg_password, 
                        reg_email,
                        reg_given_name,
                        reg_family_name
                    )
                    if success:
                        st.success(result)
                    else:
                        st.error(result)
                else:
                    st.error("Please fill in all fields")

            st.divider()
            st.subheader("Verify Email")
            verify_username = st.text_input("Username", key="verify_username")
            verification_code = st.text_input("Verification Code")
            
            if st.button("Verify"):
                if verify_username and verification_code:
                    success, result = auth.verify_email(verify_username, verification_code)
                    if success:
                        st.success(result)
                    else:
                        st.error(result)
                else:
                    st.error("Please enter both username and verification code")

   
    else:
        user = st.session_state['user']
        st.title(f"Hello {user}!")
        st.markdown("<h3>Please download the program</h3>", unsafe_allow_html=True)
        
        # Create a container for the logout button
        logout_container = st.container()
        with logout_container:
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()
        
        # Add a descriptive header for the download section
        st.write("### Download Chillbert")
        st.write("Select your operating system to download the application:")
        
        # Create three columns for better button spacing
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Windows", use_container_width=True):
                st.info("Windows version coming soon!")
        
        with col2:
            st.link_button("macOS",config.MACOS_DOWNLOAD_URL, use_container_width=True)

                # if st.button("macOS", use_container_width=True):
                #     # Create a direct download link using the pre-signed URL
                #     st.markdown(
                #         f'<a href="{config.MACOS_DOWNLOAD_URL}" target="_blank">Click here to download for macOS</a>', 
                #         unsafe_allow_html=True
                #     )
                # st.success("Your download should begin automatically. If it doesn't, click the link above.")
        
        with col3:
            if st.button("Ubuntu", use_container_width=True):
                st.info("Ubuntu version coming soon!")

if __name__ == "__main__":
    main()

st.sidebar.image("ChillbertLogo-removebg-preview.png", use_container_width=True)

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.write("© 2024 Made with Love by Team Powerpuff Girls | Powered by Streamlit")
st.markdown('</div>', unsafe_allow_html=True)
