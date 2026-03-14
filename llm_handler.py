import streamlit as st
import requests

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
                content = r.get("content", "")
                if content:
                    paragraphs.append(content)

            answer = "\n\n".join(paragraphs)

            if answer:
                return answer[:1500]

        return "No detailed response found."

    except Exception as e:
        return f"ERROR: {str(e)}"
# import streamlit as st
# import requests

# def get_ai_response(prompt):
#     try:
#         api_key = st.secrets.get("TAVILY_API_KEY")
#         url = "https://api.tavily.com/search"

#         payload = {
#             "api_key": api_key,
#             "query": prompt,
#             "include_answer": True,
#             "search_depth": "advanced",
#             "max_results": 5
#         }

#         response = requests.post(url, json=payload, timeout=15)

#         if response.status_code == 200:

#             data = response.json()

#             # Tavily short answer
#             answer = data.get("answer", "")

#             # Extra content from search results
#             extra_content = " ".join(
#                 [r.get("content", "") for r in data.get("results", [])]
#             )

#             # Combine them to form longer paragraph output
#             full_answer = (answer + "\n\n" + extra_content).strip()

#             # limit extremely long outputs
#             return full_answer[:1200]

#     except Exception as e:
#         return f"ERROR: Unified API Failure - {str(e)}"

#     return "ERROR: Could not connect to Intel Node."
