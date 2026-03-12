# hallucination_checker.py
import requests

def check_wikipedia(query):

    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query

    try:
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()

            return {
                "text": data.get("extract"),
                "source": data.get("content_urls",{}).get("desktop",{}).get("page")
            }

    except:
        return None


def hallucination_score(ai_answer, wiki_text):

    if not wiki_text:
        return 50

    ai_words = set(ai_answer.lower().split())
    wiki_words = set(wiki_text.lower().split())

    overlap = ai_words.intersection(wiki_words)

    score = len(overlap) / max(len(ai_words), 1)

    return round(score * 100)
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

