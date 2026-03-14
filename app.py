import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_real_time, split_claims, claim_score
import time

st.set_page_config(page_title="TRUTHGUARD AI",layout="wide")

st.markdown("""
<style>
.stApp{
background:linear-gradient(135deg,#0f172a,#020617);
color:#e2e8f0;
}

.panel{
background:rgba(15,23,42,0.8);
padding:20px;
border-radius:10px;
border:1px solid rgba(0,255,200,0.2);
box-shadow:0 0 20px rgba(0,255,200,0.15);
}
</style>
""",unsafe_allow_html=True)

st.title("🛡️ TRUTHGUARD AI")
st.caption("PROMPT INJECTION FIREWALL & HALLUCINATION DETECTOR")

t1,t2 = st.tabs(["[ SHADOW SCAN ]","[ EXTERNAL AUDIT ]"])

with t1:

    query = st.text_input("ENTER QUERY")

    if st.button("EXECUTE SCAN"):

        is_attack,pattern = detect_prompt_injection(query)

        if is_attack:

            st.error(f"🚨 PROMPT ATTACK DETECTED: {pattern}")

        else:

            st.success("✅ PROMPT SECURE")

            with st.spinner("Fetching real time data..."):
                real_data = check_real_time(query)

            with st.spinner("Generating AI response..."):
                ai_response = get_ai_response(query)

            st.subheader("📡 SYSTEM OUTPUT")

            st.markdown(f'<div class="panel">{ai_response}</div>',unsafe_allow_html=True)

            if real_data:

                claims = split_claims(ai_response)

                score,results = claim_score(claims,real_data["text"])

                st.subheader("📊 CREDIBILITY ANALYSIS")

                st.metric("TRUTH INDEX",f"{score}%")

                st.progress(score/100)

                st.subheader("🧠 CLAIM VERIFICATION")

                for c,res in results:

                    if res:
                        st.success(c)
                    else:
                        st.warning(c)

                st.subheader("📚 SOURCES")

                for s in real_data["sources"]:

                    st.markdown(f"🟢 **{s['title']}**")

                    st.markdown(f"[Open Source]({s['url']})")

                    st.caption(s["content"][:200]+"...")


with t2:

    st.subheader("AUDIT EXTERNAL TEXT")

    topic = st.text_input("TOPIC")

    text = st.text_area("PASTE TEXT")

    if st.button("RUN AUDIT"):

        if topic and text:

            real_data = check_real_time(topic)

            if real_data:

                claims = split_claims(text)

                score,results = claim_score(claims,real_data["text"])

                st.metric("TRUTH INDEX",f"{score}%")

                st.progress(score/100)

                st.subheader("🧠 CLAIM VERIFICATION")

                for c,res in results:

                    if res:
                        st.success(c)
                    else:
                        st.warning(c)

                st.subheader("📚 SOURCES")

                for s in real_data["sources"]:

                    st.markdown(f"🟢 **{s['title']}**")

                    st.markdown(f"[Open Source]({s['url']})")
# import streamlit as st
# from prompt_detector import detect_prompt_injection
# from llm_handler import get_ai_response
# from hallucination_checker import check_real_time, hallucination_score, split_claims
# import time

# st.set_page_config(page_title="TRUTHGUARD AI", layout="wide")

# st.markdown("""
# <style>
# .stApp { background: radial-gradient(circle at top right, #001a1a, #000000); color:#e0e0e0; }
# .stButton>button { background: linear-gradient(45deg,#004d00,#00cc00); color:white; font-weight:bold; }
# .stTextInput>div>div>input { background:black; border:1px solid #00ff41; color:#00ff41; }
# h1 { color:#00ff41 !important; text-shadow:0 0 10px #00ff41; }
# </style>
# """, unsafe_allow_html=True)

# st.title("🛡️ TRUTHGUARD AI")
# st.caption("PROMPT INJECTION FIREWALL & HALLUCINATION DETECTOR")

# t1, t2 = st.tabs(["[ SHADOW SCAN ]","[ EXTERNAL AUDIT ]"])

# with t1:

#     query = st.text_input("ENTER QUERY")

#     if st.button("EXECUTE SCAN"):

#         with st.spinner("🔎 SCANNING PROMPT SECURITY..."):
#             time.sleep(1)

#         is_attack, pattern = detect_prompt_injection(query)

#         if is_attack:

#             st.error(f"🚨 PROMPT ATTACK DETECTED: {pattern}")

#             st.progress(90)

#         else:

#             st.success("✅ PROMPT SECURE")

#             with st.spinner("🌐 FETCHING REAL TIME DATA..."):
#                 real_data = check_real_time(query)

#             with st.spinner("🧠 GENERATING AI RESPONSE..."):
#                 ai_response = get_ai_response(query)

#             st.subheader("📡 SYSTEM OUTPUT")

#             st.info(ai_response)

#             if real_data:

#                 score = hallucination_score(ai_response, real_data["text"])

#                 st.subheader("📊 CREDIBILITY ANALYSIS")

#                 st.metric("TRUTH INDEX", f"{score}%")

#                 st.progress(score/100)

#                 st.subheader("🧠 CLAIM VERIFICATION")

#                 claims = split_claims(ai_response)

#                 for c in claims:

#                     if c.lower() in real_data["text"].lower():

#                         st.success(f"✔ {c}")

#                     else:

#                         st.warning(f"⚠ {c}")

#                 st.subheader("📚 SOURCES")

#                 for s in real_data["sources"]:

#                     st.markdown(f"🟢 **{s['title']}**")

#                     st.markdown(f"[Open Source]({s['url']})")

#                     st.caption(s["content"][:200]+"...")


# with t2:

#     st.subheader("AUDIT EXTERNAL TEXT")

#     topic = st.text_input("TOPIC")

#     text = st.text_area("PASTE TEXT")

#     if st.button("RUN AUDIT"):

#         if topic and text:

#             with st.spinner("VERIFYING..."):

#                 real_data = check_real_time(topic)

#                 if real_data:

#                     score = hallucination_score(text, real_data["text"])

#                     st.metric("TRUTH INDEX", f"{score}%")

#                     st.progress(score/100)

#                     for s in real_data["sources"]:

#                         st.markdown(f"🟢 {s['title']}")

#                         st.markdown(f"[Source]({s['url']})")
