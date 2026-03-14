import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_real_time, hallucination_score
import time

st.set_page_config(page_title="TRUTHGUARD AI", layout="wide")

# Modern Cyber UI
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #001a1a, #000000); color: #e0e0e0; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 65, 0.2); border-radius: 15px; padding: 20px;
    }
    .stButton>button { background: linear-gradient(45deg, #004d00, #00cc00); color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { background: rgba(0,0,0,0.5); border: 1px solid #00ff41; color: #00ff41; }
    h1 { text-shadow: 0 0 10px #00ff41; color: #00ff41 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ TRUTHGUARD AI")
st.caption("PROMPT INJECTION FIREWALL & HALLUCINATION DETECTOR")

def display_score(score):
    color = "#FF4B4B" if score < 50 else "#00FF41" # Red if < 50, Green if >= 50
    st.markdown(f"""
        <div style="padding:15px; border:2px solid {color}; border-radius:10px; background:rgba(0,0,0,0.5);">
            <p style="color:white; margin:0;">TRUTH INDEX</p>
            <h2 style="color:{color}; margin:0;">{score}%</h2>
        </div>
    """, unsafe_allow_html=True)

t1, t2 = st.tabs(["[ SHADOW SCAN ]", "[ EXTERNAL AUDIT ]"])

with t1:
    query = st.text_input("ENTER QUERY:", key="main_q")
    if st.button("EXECUTE SCAN"):
        is_attack, pattern = detect_prompt_injection(query)
        if is_attack:
            st.error(f"❌ SECURITY BREACH: {pattern.upper()} DETECTED")
        else:
            st.success("✅ PROMPT SECURE")
            with st.spinner("FETCHING REAL-TIME INTEL..."):
                # Use Tavily for the answer and the sources
                real_data = check_real_time(query)
                ai_response = get_ai_response(query)
            
            st.subheader("📡 SYSTEM OUTPUT")
            st.info(ai_response)
            
            if real_data and "ERROR" not in ai_response:
                score = hallucination_score(ai_response, real_data['text'])
                st.subheader("📊 CREDIBILITY ANALYSIS")
                c1, c2 = st.columns(2)
                c1.metric("TRUTH INDEX", f"{score}%")
                with c2:
                    st.write("**SOURCES:**")
                    for s in real_data['sources']:
                        st.markdown(f"✅ [{s['title']}]({s['url']})")

with t2:
    st.subheader("AUDIT EXTERNAL TEXT")
    topic = st.text_input("TOPIC:")
    text = st.text_area("PASTE TEXT:")
    if st.button("RUN AUDIT"):
        if topic and text:
            with st.spinner("VETTING..."):
                real_data = check_real_time(topic)
                
                if real_data:
                    score = hallucination_score(text, real_data['text'])
                    st.metric("TRUTH INDEX", f"{score}%")
                    for s in real_data['sources']:
                        st.markdown(f"✅ [{s['title']}]({s['url']})")


