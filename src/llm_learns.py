import openai

# Set your OpenAI API key

from openai import OpenAI

# Sample content to include in the system prompt
with open("audio_responses_cleaned.txt", "r", encoding="utf-8") as file:
    sample_content = file.read()

def fetch_answer(user_input):
    # Initialize the OpenAI client
    client = OpenAI(
    # This is the default and can be omitted
    api_key=openai.api_key
)
    # Creating the chat completion request
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Model selection
        messages=[
            {
                "role": "system",
                "content": f"You will be provided with a question, and you have to fetch insights for the same from {sample_content}"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.2,  # Controls randomness: lower values make output more focused
        max_tokens=1000,   # Limits the response length
        top_p=1.0,         # Nucleus sampling; 1.0 means no filtering
    )
   

    # Print the model's response
    print(response.choices[0].message.content)

user_input=input("Enter your question: ")
fetch_answer(user_input)
