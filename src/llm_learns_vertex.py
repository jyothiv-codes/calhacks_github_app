
import streamlit as st
#Gen AI code 
import markdown
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.

model = genai.GenerativeModel('gemini-pro')

genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

with st.form("get_recommendation"):
   
   st.write("What would you like to watch today?")
   search = st.text_input('', '')
   submitted = st.form_submit_button("Submit")
   if submitted:
       
       confirm=model.generate_content("is the following sentence asking for movie recommendation "+search+".If yes, then is the confidence percentage greater than or equal to 90. Only say yes or no")
       print("Related to movies, yes or no?",confirm.text)
       percentage=confirm.text
       if percentage=="yes":
        response = model.generate_content(search)
        answer=response.text
        markdown.markdown(answer)
        st.write(answer)
       else:
          st.write("I'm not sure if what you are searching for is related to movies? Could you please check again?")
    
    
if submitted:
    st.write("Hope you like these recommendations! Enjoy with popcorn and a soda!")
