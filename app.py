import streamlit as st

from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_wikipedia, hallucination_score

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}

button {
    background: #22c55e;
    border-radius:10px;
    padding:10px 20px;
    transition:0.3s;
}

button:hover {
    background:#16a34a;
    transform:scale(1.05);
}

div[data-testid="stMetric"] {
    background:#111827;
    padding:20px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="AI TruthGuard", layout="centered")

st.title("🛡 AI TruthGuard")
st.caption("Prompt Injection + Hallucination Detection System")

st.divider()

mode = st.radio(
    "Select Mode",
    ["Ask AI + Verify", "Verify External AI Response"]
)

st.divider()

# MODE 1
if mode == "Ask AI + Verify":

    user_prompt = st.text_input("Ask a question")

    if st.button("Analyze"):

        st.subheader("🔐 Prompt Injection Detector")

        attack, pattern = detect_prompt_injection(user_prompt)

        if attack:

            st.error("⚠ Prompt Injection Detected")
            st.write("Pattern:", pattern)

        else:

            st.success("Prompt looks safe")

            st.divider()

            st.subheader("🤖 AI Response")

            ai_answer = get_ai_response(user_prompt)

            st.write(ai_answer)

            st.divider()

            st.subheader("🧠 Hallucination Detector")

            wiki_text = check_wikipedia(user_prompt)

            score = hallucination_score(ai_answer, wiki_text)

            st.metric("Truth Score", str(score) + "%")

            if score > 70:
                st.success("Likely factual")
            else:
                st.warning("Possible hallucination")

            if wiki_text:
               st.subheader("Source")
               st.write("Wikipedia")


# MODE 2
if mode == "Verify External AI Response":

    topic = st.text_input("Topic / Question")

    ai_answer = st.text_area(
        "Paste response from ChatGPT, Gemini, or any AI"
    )

    if st.button("Verify Response"):

        st.subheader("🧠 Hallucination Detector")

        # wiki_text = check_wikipedia(topic)

        # score = hallucination_score(ai_answer, wiki_text)

        # st.metric("Truth Score", str(score) + "%")
        wiki_data = check_wikipedia(user_prompt)

        score = hallucination_score(ai_answer, wiki_data["text"])

        st.metric("Truth Score", str(score)+"%")


        if score > 70:
            st.success("Likely factual")

        else:
            st.warning("Possible hallucination")
            
        st.subheader("Source")

        st.write(wiki_data["source"])




# st.subheader("Source")

# st.write(wiki_data["source"])
