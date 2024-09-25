import streamlit as st
import google.generativeai as genai

import os
from dotenv import load_dotenv
load_dotenv()

# Set up the API key
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)

# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-pro')

# Start a chat session with an empty history
chat = model.start_chat(history=[])

# Function to get a response from the Gemini model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    response_text = "".join(chunk.text for chunk in response)
    return response_text

# Set the page configuration
st.set_page_config(page_title='Q&A Demo')

# Header for the chatbot
st.header('Hassan chatbot 💬 💬')

# Initialize the chat history in session_state if it does not exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input for user query
input_query = st.text_input('Input your query:', key='input')

# Button to submit the query
submit = st.button('Submit the query')

# Process the user's input and get the bot's response
if submit and input_query:
    response = get_gemini_response(input_query)
    # Append the conversation to chat history
    st.session_state['chat_history'].append(('You', input_query, 'Hassan Bot', response))

# Display the chat history
st.subheader('Your chat history')

for user_role, user_text, bot_role, bot_text in st.session_state['chat_history']:
    with st.container():
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 10px; background-color: #f0f0f5; margin-bottom: 10px; color: #000;">
            <strong>{user_role}</strong>: {user_text}
        </div>
        <div style="padding: 10px; border-radius: 10px; background-color: #e0f7fa; margin-bottom: 10px; color: #000;">
            <strong>{bot_role}</strong>: {bot_text}
        </div>
        """, unsafe_allow_html=True)
