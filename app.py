import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_real_time, hallucination_score
import time

st.set_page_config(page_title="TRUTHGUARD AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #001a1a, #000000); color: #e0e0e0; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 65, 0.2); border-radius: 15px; padding: 20px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #004d00, #00cc00); color: white; 
        border: none; border-radius: 8px; font-weight: bold; width: 100%;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(0,0,0,0.5); border: 1px solid #00ff41; color: #00ff41;
    }
    h1, h2 { text-shadow: 0 0 10px #00ff41; color: #00ff41 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ TRUTHGUARD AI")
st.write("SECURE AI GATEWAY // NEURAL DEFENSE ACTIVE")

tabs = st.tabs(["[ SHADOW SCAN ]", "[ EXTERNAL AUDIT ]"])
# --- TAB 1: SHADOW SCAN ---
with tabs[0]:
    query = st.text_input("ENTER INTEL QUERY:", placeholder="e.g. Current status of Galgotias University AI Summit 2026", key="shadow_q")
    if st.button("EXECUTE SYSTEM SCAN"):
        if query:
            is_attack, pattern = detect_prompt_injection(query)
            if is_attack:
                st.error(f"❌ SECURITY BREACH: {pattern.upper()} DETECTED")
            else:
                st.success("✅ PROMPT CLEARANCE GRANTED")
                
                with st.spinner("FETCHING REAL-TIME ARCHIVES..."):
                    real_data = check_real_time(query)
                
                with st.spinner("QUERYING LLM..."):
                    context = real_data['text'] if real_data else "No live web source found."
                    response = get_ai_response(f"Ref context: {context}. User Query: {query}")
                
                st.markdown("### 📡 SYSTEM OUTPUT")
                if "ERROR" in response:
                    st.error(response)
                else:
                    st.info(response)
                
                # UPDATED SOURCE DISPLAY FOR SHADOW SCAN
                if real_data:
                    score = hallucination_score(response, real_data['text'])
                    st.subheader("📊 CREDIBILITY ANALYSIS")
                    c1, c2 = st.columns(2)
                    c1.metric("TRUTH INDEX", f"{score}%")
                    
                    with c2:
                        st.write("**VERIFIED SOURCES:**")
                        for source in real_data['sources']:
                            # Shows: ✅ Wikipedia (with link)
                            st.markdown(f"✅ [{source['title']}]({source['url']})")
# with tabs[0]:
#     query = st.text_input("ENTER INTEL QUERY:", placeholder="e.g. Current status of Galgotias University AI Summit 2026")
#     if st.button("EXECUTE SYSTEM SCAN"):
#         if query:
#             is_attack, pattern = detect_prompt_injection(query)
#             if is_attack:
#                 st.error(f"❌ SECURITY BREACH: {pattern.upper()} DETECTED")
#             else:
#                 st.success("✅ PROMPT CLEARANCE GRANTED")
#                 with st.spinner("FETCHING REAL-TIME ARCHIVES..."):
#                     real_data = check_real_time(query)
#                 with st.spinner("QUERYING LLM..."):
#                     context = real_data['text'] if real_data else "No source found."
#                     response = get_ai_response(f"Ref: {context}. Query: {query}")
                
#                 st.markdown("### 📡 SYSTEM OUTPUT")
#                 st.info(response)
                
#                 if real_data:
#                     score = hallucination_score(response, real_data['text'])
#                     st.subheader("📊 CREDIBILITY ANALYSIS")
#                     c1, c2 = st.columns(2)
#                     c1.metric("TRUTH INDEX", f"{score}%")
#                     c2.write("**VERIFIED SOURCES:**")
#                     for url in real_data['sources']: st.write(f"- [Source Link]({url})")

# --- TAB 2: EXTERNAL AUDIT (PASTED TEXT) ---
with tabs[1]:
    st.subheader("VET EXTERNAL AI CONTENT")
    audit_topic = st.text_input("TOPIC (for source search):")
    audit_text = st.text_area("PASTE TEXT (from ChatGPT/Gemini):", height=200)
    
    if st.button("RUN AUDIT"):
        if audit_topic and audit_text:
            with st.spinner("VETTING AGAINST LIVE WEB..."):
                # Use same search engine as Tab 1
                real_data = check_real_time(audit_topic)
                if real_data:
                      score = hallucination_score(response if 'response' in locals() else audit_text, real_data['text'])
                      st.subheader("📊 CREDIBILITY ANALYSIS")
                      c1, c2 = st.columns(2)
                      c1.metric("TRUTH INDEX", f"{score}%")
    
                      with c2:
                              st.write("**VERIFIED SOURCES:**")
                              for source in real_data['sources']:
                            # This creates: Wikipedia (clickable link)
                                   st.markdown(f"✅ [{source['title']}]({source['url']})")
                
