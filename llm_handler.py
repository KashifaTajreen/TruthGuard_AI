import streamlit as st
from groq import Groq

def get_ai_response(prompt):
    try:
        # Direct retrieval to ensure no variable mismatch
        key = st.secrets.get("GROQ_API_KEY")
        if not key:
            return "ERROR: GROQ_API_KEY not found in secrets."
            
        client = Groq(api_key=key)
        
        # We use a try-except specifically for the API call to catch Auth errors
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional intelligence officer. Use context to provide factual intel."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        return completion.choices[0].message.content
    except Exception as e:
        # This will tell you if it's an Invalid API Key or a Rate Limit
        return f"ERROR: LLM GATEWAY FAILURE - {str(e)}"
# import streamlit as st
# from groq import Groq

# def get_ai_response(prompt):
#     try:
#         # Check if secrets exist
#         if "GROQ_API_KEY" not in st.secrets:
#             return "ERROR: GROQ_API_KEY not found in Streamlit Secrets."
            
#         # Initialize client with the key directly
#         client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
#         # Using the exact stable model ID
#         completion = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": "You are a professional intelligence AI. Provide concise, factual intel based on context."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.1
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         return f"ERROR: API AUTHENTICATION FAILED - {str(e)[:100]}"

#         return f"ERROR: SYSTEM FAILURE - {str(e)[:50]}"
