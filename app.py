import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os, sys, json


# Load environment va   riables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


st.set_page_config(
    page_title="Work Buddy - Your AI Assistant",
    page_icon=":robot:",
    layout="wide",
)



def ai_sales_coach(user_input):
    if not user_input:
        return "Please provide a valid question or request."
    elif "!persona" in user_input:
        return f"""As an expert in sales and marketing, create a detailed buyer's persona based on the following input:

{user_input}

Include the following aspects in your persona:
1. Demographics (age, gender, income, education, etc.)
2. Professional background
3. Goals and challenges
4. Preferred communication channels
5. Decision-making process
6. Key pain points  
7. Objections they might have
8. Potential solutions your product/service offers"""
    elif "!script" in user_input:
        return f"""As an expert in sales and marketing, create a detailed sales script based on the following input:
{user_input}

Include the following aspects in your script:
1. Introduction
2. Problem identification
3. Solution presentation
4. Objections handling
5. Closing the sale"""
    elif "!leads" in user_input:
        return f"""
How can I find leads who are interested in {user_input}?

Please provide specific, actionable strategies for lead generation, including:
1. Ideal customer profile
2. Effective channels for outreach
3. Content marketing ideas
4. Networking opportunities
5. Digital marketing tactics
6. Any industry-specific recommendations
"""
    else:
        return "Please provide a valid question or request."

        llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
        response = llm.generate_text(user_input, max_length=150)
        return response




with st.sidebar:
    #clear chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
    
# Don't show Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []  # Initialize chat history
    #clear chat history
    st.session_state.messages = []
    # Welcome message
    st.session_state.messages.append({"role": "assistant", "content": "Welcome! Type a message to get started."})


# Display chat messages
with st.container():  # Use container for styling
    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
# User Input
if prompt := st.chat_input("Your message"):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display "Sales Coach is typing..."
    with st.chat_message("assistant"):
        message_placeholder = st.empty() 
        message_placeholder.markdown("Assstiant is typing...")

    # Get and append AI response (with a delay to simulate typing)
    time.sleep(1)  # Adjust the delay as needed
    response = ai_sales_coach(prompt)
    message_placeholder.markdown(response)  # Update the placeholder
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear user input after sending message
    st.session_state.messages = st.session_state.messages[-100:]  # Limit chat history to last 100 messages
