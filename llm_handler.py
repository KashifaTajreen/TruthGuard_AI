import streamlit as st
from groq import Groq

def get_ai_response(prompt):
    try:
        # Check if key exists before calling
        if "GROQ_API_KEY" not in st.secrets:
            return "ERROR: GROQ_API_KEY MISSING IN SECRETS"
            
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a secure intel AI. Use provided context to answer query concisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Returns the specific error to help you debug during the demo
        return f"ERROR: SYSTEM FAILURE - {str(e)[:50]}"
# import streamlit as st
# from groq import Groq

# def get_ai_response(prompt):
#     try:
#         api_key = st.secrets["TAVILY_API_KEY"]
#         client = Groq(api_key=api_key)
        
#         completion = client.chat.completions.create(
#             model="llama-3.1-8b-instant", # The most stable Groq model right now
#             messages=[
#                 {"role": "system", "content": "You are a top-secret intelligence AI. Give short, factual answers."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.1
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         return f"ERROR: SYSTEM FAILURE - {str(e)}"
