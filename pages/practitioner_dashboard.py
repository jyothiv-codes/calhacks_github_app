import streamlit as st
from src.analyse_chat import AnalyseChat

def ac_setup():
    if 'ac' not in st.session_state:
        ac = AnalyseChat()
        ac.setup()
        st.session_state['ac'] = ac


def chillbert_response(question):
    ac = st.session_state['ac']
    return ac.askChatbot(question)


col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="col1-background"></div>', unsafe_allow_html=True)
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.markdown("![chillbert.gif](https://cdn.dribbble.com/users/7421625/screenshots/18722183/media/57f4bd5aea84c23e226069f65e417704.gif)")

with col2:
    st.markdown('<h3>Ask a Question to Chillbert!</h3>', unsafe_allow_html=True)
    question = st.text_input("Enter your question here")
    if st.button("Submit"):
        response = chillbert_response(question)
        st.write(response)
