import streamlit as st
from groq import Groq

def get_ai_response(prompt):
    try:
        # Pull key from Streamlit Secrets
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional Intelligence Officer. Provide strictly factual, concise, and structured intel reports. No small talk."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1, # Keep it professional and factual
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"SYSTEM ERROR: API_CONNECTION_FAILED - {str(e)}"
# import streamlit as st
# from groq import Groq

# def get_ai_response(prompt):
#     """
#     Fetches response from Groq using Streamlit Secrets.
#     """
#     # Pulling API Key from Streamlit Secrets
#     try:
#         api_key = st.secrets["GROQ_API_KEY"]
#     except KeyError:
#         return "ERROR: GROQ_API_KEY NOT FOUND IN SECRETS."

#     try:
#         # Initializing official Groq client
#         client = Groq(api_key=api_key)
        
#         # Creating completion with Llama 3
#         completion = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": "You are a secure intelligence AI. Provide concise, professional intel."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.3, # Lower temperature for less hallucination
#             max_tokens=1024
#         )
        
#         return completion.choices[0].message.content

#     except Exception as e:
#         # Professional error handling for the spy UI
#         return f"ERROR: ENCRYPTION FAILURE OR API OFFLINE - {str(e)}"
# from openai import OpenAI
# import os

# api_key = os.getenv("GROQ_API_KEY")

# client = OpenAI(
#     base_url="https://api.groq.com/openai/v1",
#     api_key=api_key
# )

# def get_ai_response(prompt):

#     if not api_key:
#         return "API key missing."

#     response = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )

#     return response.choices[0].message.content

