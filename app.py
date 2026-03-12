# import streamlit as st
# from prompt_detector import detect_prompt_injection
# from llm_handler import get_ai_response
# from hallucination_checker import check_wikipedia, hallucination_score
# import time

# st.set_page_config(page_title="TRUTHGUARD: AI FIREWALL", layout="wide")

# # Professional Multinational UI
# st.markdown("""
#     <style>
#     .main { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
#     .stTextInput>div>div>input { background-color: #111; color: #00FF41; border: 1px solid #00FF41; }
#     .stButton>button { background-color: #003300; color: #00FF41; border: 1px solid #00FF41; font-weight: bold; }
#     .stMetric { border-left: 5px solid #00FF41; background-color: #0a0a0a; }
#     .status-box { padding: 20px; border: 1px solid #00FF41; background: #051a05; margin-bottom: 20px; }
#     </style>
#     """, unsafe_allow_html=True)

# st.title("🛡️ TRUTHGUARD OS v3.0")
# st.write("SECURE AI GATEWAY // HALLUCINATION DETECTION // THREAT NEUTRALIZATION")

# tab1, tab2 = st.tabs(["[ SHADOW SCAN ]", "[ DATA ARCHIVE ]"])

# with tab1:
#     user_input = st.text_input("ENTER INTEL REQUEST:", placeholder="e.g., Explain Quantum Computing")
    
#     if st.button("EXECUTE ANALYSIS"):
#         if user_input:
#             # STEP 1: SECURITY SCAN
#             is_attack, threat_type = detect_prompt_injection(user_input)
            
#             st.markdown("### 🛡️ SECURITY LAYER")
#             if is_attack:
#                 st.error(f"🚨 CRITICAL THREAT: {threat_type.upper()} DETECTED. EXECUTION HALTED.")
#             else:
#                 st.success("🟢 STATUS: PROMPT SECURE. NO INJECTION DETECTED.")
                
#                 # STEP 2: AI GENERATION
#                 with st.spinner("QUERYING LLM NODES..."):
#                     ai_response = get_ai_response(user_input)
                
#                 st.markdown("### 🤖 AI RESPONSE")
#                 st.info(ai_response)
                
#                 # STEP 3: HALLUCINATION CHECKING
#                 st.markdown("### 🔍 FACT-CHECKING ENGINE")
#                 # Automatically pick the best word for Wikipedia (The last noun usually)
#                 search_word = user_input.split()[-1].strip("?") 
#                 wiki_data = check_wikipedia(search_word)
                
#                 if wiki_data:
#                     score = hallucination_score(ai_response, wiki_data["text"])
#                     col1, col2 = st.columns(2)
#                     col1.metric("TRUTH SCORE", f"{score}%", help="Higher is more factual")
#                     col2.write(f"**SOURCE FOUND:** {wiki_data['source']}")
#                     st.progress(score/100)
#                 else:
#                     st.warning("⚠️ VETTING FAILED: No independent source found in Wikipedia for this subject.")
import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_wikipedia, hallucination_score
import time

st.set_page_config(page_title="TRUTHGUARD OS", layout="wide")

# Theme logic
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #111; color: #00FF41; border: 1px solid #00FF41; }
    .stButton>button { background-color: #003300; color: #00FF41; border: 1px solid #00FF41; width: 100%; }
    .stButton>button:hover { background-color: #00FF41 !important; color: black !important; }
    h1, h2, h3 { color: #00FF41 !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. FIXED: SESSION STATE FOR HISTORY & PURGE
if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.title("📂 ARCHIVES")
    if st.button("PURGE ALL DATA"):
        st.session_state.history = []
        st.success("CLEARED")
        time.sleep(0.5)
        st.rerun()
    
    for entry in reversed(st.session_state.history):
        st.info(f"TIME: {entry['time']}\nSCORE: {entry['score']}%")

st.title("🕵️ PROTOCOL: TRUTHGUARD V2.1")

tab1, tab2 = st.tabs(["[ INTEL DISPATCH ]", "[ EXTERNAL VERIFICATION ]"])

# ---------------- TAB 1 ---------------- #
with tab1:
    user_prompt = st.text_input("ENTER TARGET QUERY:", key="dispatch_input")
    
    if st.button("EXECUTE SYSTEM SCAN"):
        if user_prompt:
            # 2. FIXED: INJECTION CHECKER BLOCK
            is_attack, pattern = detect_prompt_injection(user_prompt)
            
            if is_attack:
                st.error(f"⚠️ SECURITY BREACH: {pattern.upper()} DETECTED. SCAN TERMINATED.")
            else:
                with st.status("SECURITY CLEARANCE GRANTED", state="complete"):
                    st.write("Neutralizing malicious layers... Complete.")
                    ai_answer = get_ai_response(user_prompt)
                
                if "ERROR" in ai_answer:
                    st.error(ai_answer)
                else:
                    st.subheader("📡 INTEL REPORT")
                    st.info(ai_answer)
                    
                    # 3. FIXED: HALLUCINATION LOGIC
                    search_key = " ".join(user_prompt.split()[:2])
                    wiki_data = check_wikipedia(search_key)
                    if wiki_data:
                        score = hallucination_score(ai_answer, wiki_data["text"])
                        st.metric("TRUTH INDEX", f"{score}%")
                        st.session_state.history.append({"time": time.strftime("%H:%M"), "score": score})
                    else:
                        st.warning("SOURCE ARCHIVE UNREACHABLE.")

# ---------------- TAB 2 ---------------- #
with tab2:
    st.subheader("VERIFY EXTERNAL DATA")
    ext_topic = st.text_input("SUBJECT TOPIC:", key="ext_topic")
    ext_intel = st.text_area("PASTE UNVERIFIED TEXT:", key="ext_intel")
    
    if st.button("VERIFY TRUTH"):
        if ext_topic and ext_intel:
            with st.spinner("CROSS-REFERENCING ARCHIVES..."):
                wiki_data = check_wikipedia(ext_topic)
                if wiki_data:
                    score = hallucination_score(ext_intel, wiki_data["text"])
                    st.metric("CREDIBILITY SCORE", f"{score}%")
                    st.progress(score/100)
                    st.write(f"Verified via: {wiki_data['source']}")
                else:
                    st.error("NO MATCHING ARCHIVES FOUND.")
