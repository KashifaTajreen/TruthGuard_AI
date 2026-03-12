import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_wikipedia, hallucination_score

st.set_page_config(page_title="AI TruthGuard", layout="centered")

st.title("AI TruthGuard")
st.caption("Prompt Injection + Hallucination Detection")

mode = st.radio(
    "Select Mode",
    ["Ask AI + Verify", "Verify External AI Response"]
)

st.divider()

# ---------------- MODE 1 ---------------- #

if mode == "Ask AI + Verify":

    user_prompt = st.text_input("Ask a question")

    if st.button("Analyze"):

        st.subheader("Prompt Injection Detector")

        attack, pattern = detect_prompt_injection(user_prompt)

        if attack:

            st.error("Prompt Injection Detected")
            st.write("Pattern:", pattern)

        else:

            st.success("Prompt looks safe")

            st.divider()

            st.subheader("AI Response")

            ai_answer = None

            try:
                ai_answer = get_ai_response(user_prompt)
                st.write(ai_answer)

            except Exception as e:
                st.error("AI response failed. Check API key.")

            # Only run verification if AI answer exists
            if ai_answer:

                st.divider()
                st.subheader("Hallucination Detector")

                wiki_data = check_wikipedia(user_prompt)

                if wiki_data is not None:

                    score = hallucination_score(ai_answer, wiki_data["text"])

                    st.metric("Truth Score", str(score) + "%")
                    st.progress(score/100)

                    st.subheader("Source")
                    st.write(wiki_data["source"])

                else:

                    st.warning("No trusted source found")


# ---------------- MODE 2 ---------------- #

if mode == "Verify External AI Response":

    topic = st.text_input("Topic / Question")
    ai_answer = st.text_area("Paste AI response")

    if st.button("Verify Response"):

        st.subheader("Hallucination Detector")

        if not ai_answer:
            st.warning("Paste an AI response first")

        else:

            wiki_data = check_wikipedia(topic)

            if wiki_data is not None:

                score = hallucination_score(ai_answer, wiki_data["text"])

                st.metric("Truth Score", str(score) + "%")
                st.progress(score/100)

                st.subheader("Source")
                st.write(wiki_data["source"])

            else:

                st.warning("No trusted source found")
# import streamlit as st

# from prompt_detector import detect_prompt_injection
# from llm_handler import get_ai_response
# from hallucination_checker import check_wikipedia, hallucination_score


# st.set_page_config(page_title="AI TruthGuard", layout="centered")

# st.markdown("""
# <style>

# .stApp {
#     background: linear-gradient(135deg,#0f172a,#1e293b);
#     color:white;
# }

# /* Fix radio button text */
# label, p, span {
#     color:white !important;
# }

# /* Buttons */
# button {
#     background:#22c55e !important;
#     color:white !important;
#     border-radius:10px;
#     padding:10px 20px;
# }

# /* Input fields */
# textarea, input {
#     background:#1f2937 !important;
#     color:white !important;
# }

# /* Metric box */
# div[data-testid="stMetric"] {
#     background:#111827;
#     padding:20px;
#     border-radius:10px;
# }

# </style>
# """, unsafe_allow_html=True)

# st.title("🛡 AI TruthGuard")
# st.caption("Prompt Injection + Hallucination Detection System")

# mode = st.radio(
#     "Select Mode",
#     ["Ask AI + Verify", "Verify External AI Response"]
# )

# st.divider()

# # MODE 1
# if mode == "Ask AI + Verify":

#     user_prompt = st.text_input("Ask a question")

#     if st.button("Analyze"):

#         st.subheader("🔐 Prompt Injection Detector")

#         attack, pattern = detect_prompt_injection(user_prompt)

#         if attack:

#             st.error("Prompt Injection Detected")
#             st.write("Pattern:", pattern)

#         else:

#             st.success("Prompt looks safe")

#             st.divider()

#             st.subheader("🤖 AI Response")
#             ai_answer = None

#         try:
#              with st.spinner("AI thinking..."):
#                  ai_answer = get_ai_response(user_prompt)

#                  st.write(ai_answer)

#         except Exception as e:
#              st.error("AI response failed. Check GROQ API key.")

# # Only verify if answer exists
#         if ai_answer:

#               st.divider()
#               st.subheader("🧠 Hallucination Detector")

#               wiki_data = check_wikipedia(user_prompt)

#         if wiki_data:

#              score = hallucination_score(ai_answer, wiki_data["text"])

#              st.metric("Truth Score", str(score) + "%")
#              st.progress(score/100)

#              st.subheader("📚 Evidence Source")
#              st.write(wiki_data["source"])

#         else:

#                st.warning("No trusted source found for this claim.")

           
# # MODE 2
# if mode == "Verify External AI Response":

#     topic = st.text_input("Topic / Question")

#     ai_answer = st.text_area("Paste AI response")

#     if st.button("Verify Response"):

#         st.subheader("🧠 Hallucination Detector")

#         wiki_data = check_wikipedia(topic)

#         if wiki_data:

#             score = hallucination_score(ai_answer, wiki_data["text"])

#             st.metric("Truth Score", str(score) + "%")
#             st.progress(score/100)

#             if score > 70:
#                 st.success("Likely factual")
#             else:
#                 st.warning("Possible hallucination")

#             st.subheader("📚 Source")
#             st.write(wiki_data["source"])

#         else:

#             score = 30

#             st.metric("Truth Score", str(score) + "%")
#             st.progress(score/100)

#             st.warning("No trusted source found")
