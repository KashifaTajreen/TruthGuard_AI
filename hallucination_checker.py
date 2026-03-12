import streamlit as st
import requests
import re

def check_real_time(query):
    """Uses Tavily API for real-time fact-checking beyond 2023 knowledge."""
    try:
        api_key = st.secrets["TAVILY_API_KEY"]
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 3
        }
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Combine snippets from multiple sources for a broader truth base
            combined_text = " ".join([res['content'] for res in data.get('results', [])])
            source_urls = [res['url'] for res in data.get('results', [])]
            return {"text": combined_text, "sources": source_urls}
    except Exception as e:
        st.error(f"Search Engine Error: {e}")
    return None

def hallucination_score(ai_answer, source_text):
    if not source_text or not ai_answer: return 0
    
    # Extract key entities (Names, Years, Organizations)
    ai_entities = set(re.findall(r'\b[A-Z][a-zA-Z]+\b|\b\d{4}\b', ai_answer))
    source_entities = set(re.findall(r'\b[A-Z][a-zA-Z]+\b|\b\d{4}\b', source_text))
    
    if not ai_entities: return 50 # Neutral if no specific facts found
    
    matches = ai_entities.intersection(source_entities)
    score = (len(matches) / len(ai_entities)) * 100
    return min(round(score), 100)
# import requests
# import re

# def check_wikipedia(query):
#     # Clean the query to be just one or two words for best results
#     url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
#     try:
#         r = requests.get(url, timeout=5)
#         if r.status_code == 200:
#             data = r.json()
#             return {
#                 "text": data.get("extract", ""),
#                 "source": data.get("content_urls", {}).get("desktop", {}).get("page", "")
#             }
#     except:
#         return None
#     return None

# def hallucination_score(ai_answer, wiki_text):
#     if not wiki_text: return 0
    
#     # Logic: Look for unique "Fact Words" (Capitalized words or numbers)
#     facts_in_ai = set(re.findall(r'\b[A-Z][a-z]+|\b\d+\b', ai_answer))
#     facts_in_wiki = set(re.findall(r'\b[A-Z][a-z]+|\b\d+\b', wiki_text))
    
#     if not facts_in_ai:
#         # Fallback to general word overlap
#         ai_words = set(ai_answer.lower().split())
#         wiki_words = set(wiki_text.lower().split())
#         overlap = ai_words.intersection(wiki_words)
#         return min(round((len(overlap)/len(ai_words)) * 100), 100)

#     matches = facts_in_ai.intersection(facts_in_wiki)
#     score = (len(matches) / len(facts_in_ai)) * 100
#     return round(score)

#     score = (len(matches) / len(ai_keys)) * 100
    
#     return min(round(score), 100)
