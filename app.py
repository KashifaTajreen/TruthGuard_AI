import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_wikipedia, hallucination_score
import time

# Protocol Configuration
st.set_page_config(page_title="TRUTHGUARD OS", layout="wide", initial_sidebar_state="expanded")

# Professional Spy Theme (High Contrast)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { background-color: #111; color: #00FF41; border: 1px solid #00FF41; border-radius: 0px; }
    .stButton>button { background-color: #003300; color: #00FF41; border: 1px solid #00FF41; width: 100%; border-radius: 0px; transition: 0.3s; }
    .stButton>button:hover { background-color: #00FF41 !important; color: black !important; }
    .stSidebar { background-color: #0a0a0a; border-right: 1px solid #003300; }
    .stMetric { border: 1px solid #00FF41; background-color: #051a05; padding: 15px; }
    h1, h2, h3 { color: #00FF41 !important; text-transform: uppercase; letter-spacing: 2px; }
    .stProgress > div > div > div > div { background-color: #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - Session Archives
with st.sidebar:
    st.title("📂 ARCHIVES")
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    for i, entry in enumerate(st.session_state.history):
        st.info(f"REC: {entry['time']}\n\nSCORE: {entry['score']}%")
    
    if st.button("PURGE ALL DATA"):
        st.session_state.history = []
        st.rerun()

st.title("🕵️ PROTOCOL: TRUTHGUARD v2.1")
st.caption("AI VETTING & THREAT NEUTRALIZATION PLATFORM // ENCRYPTION: AES-256")

tab1, tab2 = st.tabs(["[ INTEL DISPATCH ]", "[ EXTERNAL VERIFICATION ]"])

with tab1:
    user_prompt = st.text_input("ENTER TARGET QUERY:", placeholder="Awaiting input...")
    
    if st.button("EXECUTE SYSTEM SCAN"):
        if not user_prompt:
            st.warning("SYSTEM IDLE: INPUT REQUIRED")
        else:
            # 1. Threat Assessment
            with st.status("Running Security Protocols...", expanded=True) as status:
                st.write("Checking for Prompt Injections...")
                is_attack, pattern = detect_prompt_injection(user_prompt)
                time.sleep(0.5)
                
                if is_attack:
                    status.update(label="THREAT DETECTED!", state="error")
                    st.error(f"CRITICAL BREACH: {pattern.upper()} PATTERN DETECTED")
                else:
                    status.update(label="SECURITY CLEARANCE GRANTED", state="complete")
                    
                    # 2. AI Intelligence Gathering
                    ai_answer = get_ai_response(user_prompt)
                    
                    if "ERROR" in ai_answer:
                        st.error(ai_answer)
                    else:
                        st.subheader("📡 AI INTELLIGENCE REPORT")
                        st.code(ai_answer, language=None)
                        
                        # 3. Verification Layer
                        st.divider()
                        st.subheader("🔍 VERIFICATION LAYER")
                        
                        # Extracting first 2 words for better Wiki matching
                        search_term = " ".join(user_prompt.split()[:2])
                        wiki_data = check_wikipedia(search_term)
                        
                        if wiki_data:
                            score = hallucination_score(ai_answer, wiki_data["text"])
                            col1, col2 = st.columns([1, 2])
                            
                            col1.metric("TRUTH INDEX", f"{score}%")
                            st.progress(score/100)
                            col2.write(f"**SOURCE ARCHIVE:** {wiki_data['source']}")
                            
                            # Log to Sidebar History
                            st.session_state.history.append({
                                "time": time.strftime("%H:%M:%S"),
                                "score": score
                            })
                            
                            # Professional Feature: Exporting
                            report = f"TRUTHGUARD REPORT\nQuery: {user_prompt}\nScore: {score}%\nResponse: {ai_answer}"
                            st.download_button("DOWNLOAD DOSSIER", report, file_name="intel_report.txt")
                        else:
                            st.warning("NO INDEPENDENT VERIFICATION DATA FOUND IN GLOBAL ARCHIVES.")
# import streamlit as st
# from prompt_detector import detect_prompt_injection
# from llm_handler import get_ai_response
# from hallucination_checker import check_wikipedia, hallucination_score

# # Spy UI Configuration
# st.set_page_config(page_title="PROTOCOL: TRUTHGUARD", layout="wide")

# # Custom CSS for Spy Aesthetic
# st.markdown("""
#     <style>
#     .main { background-color: #000000; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
#     .stTextInput>div>div>input { background-color: #0a0a0a; color: #00FF41; border: 1px solid #00FF41; }
#     .stButton>button { width: 100%; border-radius: 0px; background-color: #003300; color: #00FF41; border: 1px solid #00FF41; }
#     .stButton>button:hover { background-color: #00FF41 !important; color: black !important; }
#     .stMetric { border: 1px solid #00FF41; padding: 10px; background: #051a05; }
#     h1, h2, h3, p, span { color: #00FF41 !important; font-family: 'Courier New', monospace; }
#     .stTabs [data-baseweb="tab-list"] { background-color: #000000; }
#     .stTabs [data-baseweb="tab"] { color: #00FF41; }
#     </style>
#     """, unsafe_allow_html=True) # FIXED THE PARAMETER HERE

# st.title("📂 PROTOCOL: TRUTHGUARD")
# st.caption("SECURE INTEL VERIFICATION SYSTEM // ENCRYPTION ACTIVE")

# tabs = st.tabs(["[ DISPATCH ]", "[ ANALYZE EXTERNAL ]"])

# # ---------------- MODE 1: DISPATCH ---------------- #
# with tabs[0]:
#     user_prompt = st.text_input("ENTER QUERY FOR INTEL EXTRACTION:", placeholder="Ask the AI...")

#     if st.button("EXECUTE ANALYSIS"):
#         if not user_prompt:
#             st.warning("FIELD EMPTY. INPUT REQUIRED.")
#         else:
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.subheader("🛡️ THREAT ASSESSMENT")
#                 is_attack, pattern = detect_prompt_injection(user_prompt)
#                 if is_attack:
#                     st.error(f"CRITICAL: PROMPT INJECTION DETECTED\n\nPATTERN: {pattern.upper()}")
#                 else:
#                     st.success("CLEAN: NO MALICIOUS PAYLOAD DETECTED")

#             if not is_attack:
#                 with col2:
#                     st.subheader("🤖 AI RESPONSE")
#                     with st.spinner("DECRYPTING..."):
#                         ai_answer = get_ai_response(user_prompt)
#                         if "ERROR" in ai_answer:
#                             st.error(ai_answer)
#                         else:
#                             st.info(ai_answer)

#                 st.divider()

#                 if "ERROR" not in ai_answer:
#                     st.subheader("🔍 VERIFICATION LAYER")
#                     wiki_data = check_wikipedia(user_prompt)
                    
#                     if wiki_data:
#                         score = hallucination_score(ai_answer, wiki_data["text"])
#                         c1, c2 = st.columns([1, 2])
#                         c1.metric("CREDIBILITY SCORE", f"{score}%")
#                         c2.write(f"**SOURCE DATA:** {wiki_data['source']}")
#                         st.progress(score/100)
#                     else:
#                         st.warning("NO INDEPENDENT VERIFICATION DATA FOUND IN ARCHIVES.")

# # ---------------- MODE 2: EXTERNAL ---------------- #
# with tabs[1]:
#     topic = st.text_input("SUBJECT TOPIC")
#     ext_answer = st.text_area("PASTE UNVERIFIED INTEL")

#     if st.button("VERIFY TRUTH"):
#         if topic and ext_answer:
#             wiki_data = check_wikipedia(topic)
#             if wiki_data:
#                 score = hallucination_score(ext_answer, wiki_data["text"])
#                 st.metric("TRUTH INDEX", f"{score}%")
#                 st.progress(score/100)
#                 st.write(f"Verified via: {wiki_data['source']}")
#             else:
#                 st.error("SOURCE UNREACHABLE.")
