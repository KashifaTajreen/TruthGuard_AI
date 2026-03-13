import streamlit as st
import requests
import re
from urllib.parse import urlparse

def check_real_time(query):
    try:
        api_key = st.secrets["TAVILY_API_KEY"]
        url = "https://api.tavily.com/search"
        payload = {"api_key": api_key, "query": query, "search_depth": "advanced", "max_results": 3}
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            combined_text = " ".join([res['content'] for res in data.get('results', [])])
            
            sources_list = []
            for res in data.get('results', []):
                domain = urlparse(res['url']).netloc.replace('www.', '')
                site_name = domain.split('.')[0].capitalize() 
                sources_list.append({"title": site_name, "url": res['url']})
                
            return {"text": combined_text, "sources": sources_list}
    except:
        return None
    return None

def hallucination_score(ai_answer, source_text):
    if not source_text or not ai_answer: return 0
    
    # SCORING: Checks for specific facts, numbers, and key terms
    ai_words = set(re.findall(r'\b\w{4,}\b', ai_answer.lower())) 
    source_words = set(re.findall(r'\b\w{4,}\b', source_text.lower()))
    
    if not ai_words: return 0
    
    matches = ai_words.intersection(source_words)
    # Calculation that gives weight to matching information
    score = (len(matches) / len(ai_words)) * 100
    return min(round(score + 10), 100)
