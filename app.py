import streamlit as st

from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_wikipedia, hallucination_score

st.title("AI TruthGuard")
st.subheader("Prompt Injection + Hallucination Detector")

user_prompt = st.text_input("Ask a question")

if st.button("Analyze"):

    attack, pattern = detect_prompt_injection(user_prompt)

    if attack:

        st.error("⚠ Prompt Injection Detected")
        st.write("Pattern detected:", pattern)

    else:

        st.info("Prompt looks safe")

        ai_answer = get_ai_response(user_prompt)

        st.subheader("AI Response")
        st.write(ai_answer)

        wiki_text = check_wikipedia(user_prompt)

        score = hallucination_score(ai_answer, wiki_text)

        st.subheader("Truth Score")

        st.write(str(score) + "%")

        if score > 70:
            st.success("Answer likely factual")

        else:
            st.warning("Possible hallucination")
