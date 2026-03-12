import requests
import re

def check_wikipedia(query):
    # Clean the query to be just one or two words for best results
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return {
                "text": data.get("extract", ""),
                "source": data.get("content_urls", {}).get("desktop", {}).get("page", "")
            }
    except:
        return None
    return None

def hallucination_score(ai_answer, wiki_text):
    if not wiki_text: return 0
    
    # Logic: Look for unique "Fact Words" (Capitalized words or numbers)
    facts_in_ai = set(re.findall(r'\b[A-Z][a-z]+|\b\d+\b', ai_answer))
    facts_in_wiki = set(re.findall(r'\b[A-Z][a-z]+|\b\d+\b', wiki_text))
    
    if not facts_in_ai:
        # Fallback to general word overlap
        ai_words = set(ai_answer.lower().split())
        wiki_words = set(wiki_text.lower().split())
        overlap = ai_words.intersection(wiki_words)
        return min(round((len(overlap)/len(ai_words)) * 100), 100)

    matches = facts_in_ai.intersection(facts_in_wiki)
    score = (len(matches) / len(facts_in_ai)) * 100
    return round(score)
# # hallucination_checker.py
# import requests
# import re

# def check_wikipedia(query):
#     # Sanitize query for API
#     clean_query = re.sub(r'[^a-zA-Z0-9\s]', '', query).strip().replace(" ", "_")
#     url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_query}"

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
#     if not wiki_text or not ai_answer:
#         return 0

#     # Professional Logic: Compare meaningful keywords only
#     def get_keywords(text):
#         words = set(re.findall(r'\w+', text.lower()))
#         stop_words = {'the', 'a', 'is', 'are', 'was', 'were', 'and', 'or', 'in', 'on', 'at', 'to', 'of'}
#         return words - stop_words

#     ai_keys = get_keywords(ai_answer)
#     wiki_keys = get_keywords(wiki_text)

#     if not ai_keys: return 0

#     # Calculate overlap
#     matches = ai_keys.intersection(wiki_keys)
#     score = (len(matches) / len(ai_keys)) * 100
    
#     return min(round(score), 100)
