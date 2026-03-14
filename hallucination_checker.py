import streamlit as st
import requests
import re
from urllib.parse import urlparse

def check_real_time(query):
    try:
        api_key = st.secrets.get("TAVILY_API_KEY")

        if not api_key:
            return None

        url = "https://api.tavily.com/search"

        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 5
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:

            data = response.json()

            combined_text = " ".join(
                [r["content"] for r in data.get("results", [])]
            )

            sources = []

            for r in data.get("results", []):

                domain = urlparse(r["url"]).netloc.lower()

                name = domain.replace("www.", "").split(".")[0]

                if name == "en":
                    name = domain.split(".")[1]

                sources.append({
                    "title": name.capitalize(),
                    "url": r["url"],
                    "content": r["content"]
                })

            return {
                "text": combined_text,
                "sources": sources
            }

    except:
        return None

    return None


def split_claims(text):

    sentences = re.split(r'[.!?]', text)

    claims = [s.strip() for s in sentences if len(s.strip()) > 20]

    return claims


def hallucination_score(ai_answer, source_text):

    if not ai_answer or not source_text:
        return 0

    ai_words = set(re.findall(r'\b\w{4,}\b', ai_answer.lower()))

    source_words = set(re.findall(r'\b\w{4,}\b', source_text.lower()))

    if not ai_words:
        return 0

    matches = ai_words.intersection(source_words)

    score = (len(matches) / len(ai_words)) * 100

    return min(round(score), 100)
# import streamlit as st
# import requests
# import re
# from urllib.parse import urlparse

# def check_real_time(query):
#     try:
#         api_key = st.secrets.get("TAVILY_API_KEY")
#         if not api_key: return None
        
#         url = "https://api.tavily.com/search"
#         payload = {"api_key": api_key, "query": query, "search_depth": "advanced", "max_results": 3}
#         response = requests.post(url, json=payload, timeout=10)
        
#         if response.status_code == 200:
#             data = response.json()
#             combined_text = " ".join([res['content'] for res in data.get('results', [])])
            
#             sources_list = []
#             for res in data.get('results', []):
#                 # Smarter domain extraction
#                 domain = urlparse(res['url']).netloc.lower()
#                 name = domain.replace('www.', '').split('.')[0]
#                 if name == "en": # Fix for "en.wikipedia.org"
#                     name = domain.replace('www.', '').split('.')[1]
                
#                 sources_list.append({"title": name.capitalize(), "url": res['url']})
                
#             return {"text": combined_text, "sources": sources_list}
#     except:
#         return None
#     return None

# def hallucination_score(ai_answer, source_text):
#     # Fix: If AI hasn't responded or error occurred, score is 0
#     if not ai_answer or "ERROR" in ai_answer or not source_text:
#         return 0
    
#     ai_words = set(re.findall(r'\b\w{4,}\b', ai_answer.lower()))
#     source_words = set(re.findall(r'\b\w{4,}\b', source_text.lower()))
    
#     if not ai_words: return 0
    
#     matches = ai_words.intersection(source_words)
#     score = (len(matches) / len(ai_words)) * 100
#     return min(round(score), 100)
