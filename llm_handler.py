import streamlit as st
import requests
import re


def clean_text(text):

    text = re.sub(r"\[\.\.\.\]", "", text)
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"From Wikipedia.*", "", text)

    lines = text.split("\n")

    cleaned = []

    for l in lines:

        line = l.strip()

        if len(line) > 40:
            cleaned.append(line)

    return "\n\n".join(cleaned)


def get_ai_response(prompt):

    try:

        api_key = st.secrets.get("TAVILY_API_KEY")

        url = "https://api.tavily.com/search"

        payload = {
            "api_key": api_key,
            "query": prompt,
            "search_depth": "advanced",
            "max_results": 5
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:

            data = response.json()

            paragraphs = []

            for r in data.get("results", []):

                text = clean_text(r.get("content", ""))

                if text:
                    paragraphs.append(text)

            answer = "\n\n".join(paragraphs)

            if answer:
                return answer[:2000]

        return "No detailed answer found."

    except Exception as e:

        return f"ERROR: {str(e)}"
# import streamlit as st
# import requests
# import re

# def clean_text(text):

#     lines = text.split("\n")
#     cleaned = []

#     banned = ["edit","image","background","navigation","menu"]

#     for l in lines:
#         line = l.strip()

#         if len(line) < 40:
#             continue

#         bad = False
#         for b in banned:
#             if b in line.lower():
#                 bad = True
#                 break

#         if not bad:
#             cleaned.append(line)

#     return "\n\n".join(cleaned)


# def get_ai_response(prompt):

#     try:

#         api_key = st.secrets.get("TAVILY_API_KEY")

#         url = "https://api.tavily.com/search"

#         payload = {
#             "api_key": api_key,
#             "query": prompt,
#             "search_depth": "advanced",
#             "max_results": 5
#         }

#         response = requests.post(url,json=payload,timeout=10)

#         if response.status_code == 200:

#             data = response.json()

#             paragraphs = []

#             for r in data.get("results",[]):

#                 text = r.get("content","")

#                 text = clean_text(text)

#                 if text:
#                     paragraphs.append(text)

#             answer = "\n\n".join(paragraphs)

#             if answer:
#                 return answer[:2000]

#         return "No detailed answer found."

#     except Exception as e:

#         return f"ERROR: {str(e)}"
