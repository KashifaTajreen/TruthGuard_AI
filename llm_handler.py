import streamlit as st
from groq import Groq

def get_ai_response(prompt, context=""):
    try:
        # Attempt to use Groq for a detailed, high-quality response
        key = st.secrets.get("GROQ_API_KEY")
        if key:
            client = Groq(api_key=key)
            # We explicitly ask for a detailed 4-5 sentence report
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a professional intelligence officer. Provide a detailed, 4-5 sentence report based ONLY on the provided context. If context is missing, use your internal knowledge but stay factual."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
                ],
                temperature=0.3
            )
            return completion.choices[0].message.content
    except Exception:
        pass # If Groq fails, fall back to the context summary below
    
    # FALLBACK: If Groq fails, we manually combine context snippets so it's not just 2 lines
    if context and len(context) > 100:
        return f"DETAILED REPORT: {context[:500]}..." 
    return "ERROR: Intelligence nodes unreachable. Please check API keys."
# import streamlit as st
# import requests

# def get_ai_response(prompt):
#     # If Groq is failing, we pull the 'answer' directly from Tavily's AI search
#     try:
#         api_key = st.secrets.get("TAVILY_API_KEY")
#         url = "https://api.tavily.com/search"
#         payload = {
#             "api_key": api_key,
#             "query": prompt,
#             "include_answer": True, # This makes Tavily act like an LLM
#             "search_depth": "advanced"
#         }
#         response = requests.post(url, json=payload, timeout=10)
#         if response.status_code == 200:
#             return response.json().get("answer", "No summarized answer available.")
#     except Exception as e:
#         return f"ERROR: Unified API Failure - {str(e)}"
#     return "ERROR: Could not connect to Intel Node."
