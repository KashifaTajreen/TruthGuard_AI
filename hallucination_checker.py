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
            ).lower()

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

    claims = []

    for s in sentences:

        s = s.strip()

        if len(s) > 25:
            claims.append(s)

    return claims[:8]


def claim_score(claims, source_text):

    results = []
    verified = 0

    source_words = set(re.findall(r'\b\w+\b', source_text.lower()))

    for claim in claims:

        claim_words = set(re.findall(r'\b\w+\b', claim.lower()))

        overlap = claim_words.intersection(source_words)

        similarity = len(overlap) / max(len(claim_words), 1)

        if similarity > 0.3:

            verified += 1
            results.append((claim, True))

        else:

            results.append((claim, False))

    if len(claims) == 0:
        score = 0
    else:
        score = round((verified / len(claims)) * 100)

    return score, results
