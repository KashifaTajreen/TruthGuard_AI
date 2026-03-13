import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_real_time, hallucination_score
import time

st.set_page_config(page_title="TRUTHGUARD AI", layout="wide")

# MODERN CYBER-GLASS UI
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
    query = st.text_input("ENTER INTEL QUERY:", placeholder="e.g. Current status of Galgotias University AI Summit 2026")
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
                    context = real_data['text'] if real_data else "No source found."
                    response = get_ai_response(f"Ref: {context}. Query: {query}")
                
                st.markdown("### 📡 SYSTEM OUTPUT")
                st.info(response)
                
                if real_data:
                    score = hallucination_score(response, real_data['text'])
                    st.subheader("📊 CREDIBILITY ANALYSIS")
                    c1, c2 = st.columns(2)
                    c1.metric("TRUTH INDEX", f"{score}%")
                    c2.write("**VERIFIED SOURCES:**")
                    for url in real_data['sources']: st.write(f"- [Source Link]({url})")

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
                # Replace your existing metrics/sources display with this clean version:
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
                # if real_data:
                #     score = hallucination_score(audit_text, real_data['text'])
                #     st.metric("EXTERNAL TRUTH INDEX", f"{score}%")
                #     st.progress(score/100)
                #     st.write("**VERIFIED SOURCES FOUND:**")
                #     for url in real_data['sources']: st.write(f"- [Reference]({url})")
                # else:
                #     st.error("COULD NOT FIND LIVE SOURCES FOR THIS TOPIC.")
# import streamlit as st
# from prompt_detector import detect_prompt_injection
# from llm_handler import get_ai_response
# from hallucination_checker import check_real_time, hallucination_score
# import time

# st.set_page_config(page_title="TRUTHGUARD AI", layout="wide")

# # MODERN CYBER-GLASS UI
# st.markdown("""
#     <style>
#     .stApp {
#         background: radial-gradient(circle at top right, #001a1a, #000000);
#         color: #e0e0e0;
#     }
#     /* Glassmorphism Cards */
#     div[data-testid="stVerticalBlock"] > div:has(div.stMetric) {
#         background: rgba(255, 255, 255, 0.05);
#         backdrop-filter: blur(10px);
#         border: 1px solid rgba(0, 255, 65, 0.2);
#         border-radius: 15px;
#         padding: 20px;
#     }
#     .stButton>button {
#         background: linear-gradient(45deg, #004d00, #00cc00);
#         color: white; border: none; border-radius: 8px;
#         font-weight: bold; text-transform: uppercase;
#     }
#     .stTextInput>div>div>input {
#         background: rgba(0,0,0,0.5); border: 1px solid #00ff41; color: #00ff41;
#     }
#     h1 { text-shadow: 0 0 10px #00ff41; color: #00ff41 !important; }
#     </style>
#     """, unsafe_allow_html=True)

# st.title("🛡️ TRUTHGUARD AI")
# st.write("REAL-TIME AI VETTING // NEURAL DEFENSE ACTIVE")

# # Main Interface
# query = st.text_input("ENTER INTEL QUERY:", placeholder="e.g. What is happening in 2026?")

# if st.button("EXECUTE SCAN"):
#     if query:
#         # 1. Security Analysis
#         is_attack, pattern = detect_prompt_injection(query)
#         if is_attack:
#             st.error(f"❌ SECURITY BREACH: {pattern.upper()} DETECTED")
#         else:
#             st.success("✅ PROMPT CLEARANCE GRANTED")
            
#             # 2. Real-Time Fact Fetching (Crucial for 2026 events)
#             with st.spinner("FETCHING REAL-TIME ARCHIVES..."):
#                 real_data = check_real_time(query)
            
#             # 3. AI Response
#             with st.spinner("QUERYING LLM..."):
#                 # We feed the real-time data into the prompt to fix the "2023 limit"
#                 context_prompt = f"Using this verified data: {real_data['text'] if real_data else 'None'}. Answer: {query}"
#                 response = get_ai_response(context_prompt)
            
#             st.markdown("### 📡AI Response")
#             st.info(response)
            
#             # 4. Score Calculation
#             if real_data:
#                 score = hallucination_score(response, real_data['text'])
#                 st.subheader("📊 CREDIBILITY ANALYSIS")
#                 c1, c2 = st.columns(2)
#                 c1.metric("TRUTH INDEX", f"{score}%")
#                 c2.write("**VERIFIED SOURCES:**")
#                 for url in real_data['sources']:
#                     st.write(f"- [Link]({url})")

# import streamlit as st
# from prompt_detector import detect_prompt_injection
# from llm_handler import get_ai_response
# from hallucination_checker import check_wikipedia, hallucination_score
# import time

# st.set_page_config(page_title="TRUTHGUARD OS", layout="wide")

# # Professional Dark UI
# st.markdown("""
#     <style>
#     .main { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
#     .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #111; color: #00FF41; border: 1px solid #00FF41; }
#     .stButton>button { background-color: #003300; color: #00FF41; border: 1px solid #00FF41; font-weight: bold; }
#     .stMetric { border-left: 5px solid #00FF41; background-color: #0a0a0a; padding: 10px; }
#     h1, h2, h3 { color: #00FF41 !important; }
#     </style>
#     """, unsafe_allow_html=True)

# st.title("📂 PROTOCOL: TRUTHGUARD v3.5")
# st.caption("AI FIREWALL & MULTI-SOURCE VERIFICATION ENGINE")

# tabs = st.tabs(["[ DISPATCH ]", "[ EXTERNAL AUDIT ]"])

# # --- TAB 1: AI Dispatch (Chat & Check) ---
# with tabs[0]:
#     user_input = st.text_input("ENTER INTEL QUERY:", key="dispatch")
#     if st.button("EXECUTE ANALYSIS"):
#         if user_input:
#             # 1. Security Check
#             is_attack, threat = detect_prompt_injection(user_input)
#             st.subheader("🛡️ SECURITY LAYER")
#             if is_attack:
#                 st.error(f"THREAT DETECTED: {threat.upper()}")
#             else:
#                 st.success("STATUS: SECURE")
                
#                 # 2. AI Response
#                 with st.spinner("COMMUNICATING WITH LLM..."):
#                     response = get_ai_response(user_input)
#                 st.subheader("🤖 AI RESPONSE")
#                 st.info(response)
                
#                 # 3. Fact Check
#                 st.subheader("🔍 FACT-CHECKING")
#                 # Clean query for better Wiki matching
#                 search_term = user_input.replace("Explain", "").replace("What is", "").strip()
#                 wiki_data = check_wikipedia(search_term)
                
#                 if wiki_data:
#                     score = hallucination_score(response, wiki_data["text"])
#                     st.metric("TRUTH SCORE", f"{score}%")
#                     st.progress(score/100)
#                     st.write(f"Source: {wiki_data['source']}")
#                 else:
#                     st.warning("Could not find a matching source to verify this response.")

# # --- TAB 2: External Audit (Verify other AI) ---
# with tabs[1]:
#     st.subheader("VERIFY EXTERNAL AI DATA")
#     topic = st.text_input("TOPIC OF THE TEXT:")
#     external_text = st.text_area("PASTE TEXT FROM ANOTHER AI (ChatGPT/Gemini):")
    
#     if st.button("RUN AUDIT"):
#         if topic and external_text:
#             with st.spinner("VETTING DATA..."):
#                 wiki_data = check_wikipedia(topic)
#                 if wiki_data:
#                     score = hallucination_score(external_text, wiki_data["text"])
#                     st.metric("EXTERNAL CREDIBILITY", f"{score}%")
#                     st.progress(score/100)
#                     st.info(f"Cross-referenced against: {wiki_data['source']}")
#                 else:
#                     st.error("SOURCE DATA NOT FOUND IN ARCHIVES.")
