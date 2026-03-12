# hallucination_checker.py
import requests
import re

def check_wikipedia(query):
    # Sanitize query for API
    clean_query = re.sub(r'[^a-zA-Z0-9\s]', '', query).strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_query}"

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
    if not wiki_text or not ai_answer:
        return 0

    # Professional Logic: Compare meaningful keywords only
    def get_keywords(text):
        words = set(re.findall(r'\w+', text.lower()))
        stop_words = {'the', 'a', 'is', 'are', 'was', 'were', 'and', 'or', 'in', 'on', 'at', 'to', 'of'}
        return words - stop_words

    ai_keys = get_keywords(ai_answer)
    wiki_keys = get_keywords(wiki_text)

    if not ai_keys: return 0

    # Calculate overlap
    matches = ai_keys.intersection(wiki_keys)
    score = (len(matches) / len(ai_keys)) * 100
    
    return min(round(score), 100)

# def check_wikipedia(query):
#     # Format query for Wikipedia API (replaces spaces with %20)
#     formatted_query = query.replace(" ", "_")
#     url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_query}"

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

#     # Professional comparison: Look for key unique nouns/facts
#     ai_set = set(ai_answer.lower().split())
#     wiki_set = set(wiki_text.lower().split())
    
#     # Filter out common stop words for better accuracy
#     stop_words = {"the", "a", "is", "of", "and", "in", "to", "it"}
#     ai_set = ai_set - stop_words
#     wiki_set = wiki_set - stop_words

#     intersection = ai_set.intersection(wiki_set)
    
#     if not ai_set: return 0
#     score = (len(intersection) / len(ai_set)) * 100
#     return min(round(score), 100)
# import requests

# def check_wikipedia(query):

#     url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query

#     try:
#         r = requests.get(url)

#         if r.status_code == 200:
#             data = r.json()

#             return {
#                 "text": data.get("extract"),
#                 "source": data.get("content_urls",{}).get("desktop",{}).get("page")
#             }

#     except:
#         return None


# def hallucination_score(ai_answer, wiki_text):

#     if not wiki_text:
#         return 50

#     ai_words = set(ai_answer.lower().split())
#     wiki_words = set(wiki_text.lower().split())

#     overlap = ai_words.intersection(wiki_words)

#     score = len(overlap) / max(len(ai_words), 1)

#     return round(score * 100)
