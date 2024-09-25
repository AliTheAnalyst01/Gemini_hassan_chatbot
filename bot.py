import streamlit as st
import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
key = os.getenv('GOOGLE_API_KEY')

# Configure the Generative AI API
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-pro')

# Initialize chat
chat = model.start_chat(history=[])

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_gemini_response(question):
    try:
        # Send the message to the chat model
        response = chat.send_message(question, stream=True)
        
        # Initialize an empty response text
        response_text = ""

        # Extract text from response, checking for 'text' attribute
        for chunk in response:
            if hasattr(chunk, 'text'):
                response_text += chunk.text

        return response_text
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return "An error occurred while processing your request."

# Set up Streamlit page configuration
st.set_page_config(page_title='Q&A Demo')

# Header for the chatbot
st.header('Hassan chatbot 💬 💬')

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Text input for user queries
input_query = st.text_input('Input your query: ', key='input')

# Submit button
submit = st.button('Submit the query')

# Process the input when submitted
if submit and input_query:
    response = get_gemini_response(input_query)
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
