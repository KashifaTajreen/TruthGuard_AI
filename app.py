import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_wikipedia, hallucination_score

# Spy UI Configuration
st.set_page_config(page_title="PROTOCOL: TRUTHGUARD", layout="wide")

# Custom CSS for Spy Aesthetic
st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
    .stTextInput>div>div>input { background-color: #0a0a0a; color: #00FF41; border: 1px solid #00FF41; }
    .stButton>button { width: 100%; border-radius: 0px; background-color: #003300; color: #00FF41; border: 1px solid #00FF41; }
    .stButton>button:hover { background-color: #00FF41 !important; color: black !important; }
    .stMetric { border: 1px solid #00FF41; padding: 10px; background: #051a05; }
    h1, h2, h3, p, span { color: #00FF41 !important; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; }
    .stTabs [data-baseweb="tab"] { color: #00FF41; }
    </style>
    """, unsafe_allow_html=True) # FIXED THE PARAMETER HERE

st.title("📂 PROTOCOL: TRUTHGUARD")
st.caption("SECURE INTEL VERIFICATION SYSTEM // ENCRYPTION ACTIVE")

tabs = st.tabs(["[ DISPATCH ]", "[ ANALYZE EXTERNAL ]"])

# ---------------- MODE 1: DISPATCH ---------------- #
with tabs[0]:
    user_prompt = st.text_input("ENTER QUERY FOR INTEL EXTRACTION:", placeholder="Ask the AI...")

    if st.button("EXECUTE ANALYSIS"):
        if not user_prompt:
            st.warning("FIELD EMPTY. INPUT REQUIRED.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🛡️ THREAT ASSESSMENT")
                is_attack, pattern = detect_prompt_injection(user_prompt)
                if is_attack:
                    st.error(f"CRITICAL: PROMPT INJECTION DETECTED\n\nPATTERN: {pattern.upper()}")
                else:
                    st.success("CLEAN: NO MALICIOUS PAYLOAD DETECTED")

            if not is_attack:
                with col2:
                    st.subheader("🤖 AI RESPONSE")
                    with st.spinner("DECRYPTING..."):
                        ai_answer = get_ai_response(user_prompt)
                        if "ERROR" in ai_answer:
                            st.error(ai_answer)
                        else:
                            st.info(ai_answer)

                st.divider()

                if "ERROR" not in ai_answer:
                    st.subheader("🔍 VERIFICATION LAYER")
                    wiki_data = check_wikipedia(user_prompt)
                    
                    if wiki_data:
                        score = hallucination_score(ai_answer, wiki_data["text"])
                        c1, c2 = st.columns([1, 2])
                        c1.metric("CREDIBILITY SCORE", f"{score}%")
                        c2.write(f"**SOURCE DATA:** {wiki_data['source']}")
                        st.progress(score/100)
                    else:
                        st.warning("NO INDEPENDENT VERIFICATION DATA FOUND IN ARCHIVES.")

# ---------------- MODE 2: EXTERNAL ---------------- #
with tabs[1]:
    topic = st.text_input("SUBJECT TOPIC")
    ext_answer = st.text_area("PASTE UNVERIFIED INTEL")

    if st.button("VERIFY TRUTH"):
        if topic and ext_answer:
            wiki_data = check_wikipedia(topic)
            if wiki_data:
                score = hallucination_score(ext_answer, wiki_data["text"])
                st.metric("TRUTH INDEX", f"{score}%")
                st.progress(score/100)
                st.write(f"Verified via: {wiki_data['source']}")
            else:
                st.error("SOURCE UNREACHABLE.")
