import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_real_time, split_claims, claim_score
import time

st.set_page_config(page_title="TRUTHGUARD AI",layout="wide")

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#020617,#000000);
color:#e2e8f0;
}

.panel{
background:rgba(15,23,42,0.9);
padding:20px;
border-radius:12px;
border:1px solid rgba(168,85,247,0.4);
box-shadow:0 0 25px rgba(168,85,247,0.3);
}

.green{
color:#22c55e;
font-weight:bold;
}

.red{
color:#ef4444;
font-weight:bold;
}

.sourcecard{
background:rgba(2,6,23,0.8);
padding:12px;
border-radius:8px;
border:1px solid rgba(34,197,94,0.3);
margin-bottom:10px;
}

</style>
""",unsafe_allow_html=True)

st.title("🛡 TRUTHGUARD AI")
st.caption("Prompt Injection Firewall + Hallucination Detector")

t1,t2 = st.tabs(["[ SHADOW SCAN ]","[ EXTERNAL AUDIT ]"])

with t1:

    query = st.text_input("ENTER QUERY")

    if st.button("EXECUTE SCAN"):

        is_attack,pattern = detect_prompt_injection(query)

        if is_attack:

            st.markdown(f'<p class="red">🚨 PROMPT ATTACK DETECTED: {pattern}</p>',unsafe_allow_html=True)

        else:

            st.markdown('<p class="green">✔ PROMPT SECURE</p>',unsafe_allow_html=True)

            with st.spinner("Collecting intelligence..."):
                real_data = check_real_time(query)

            with st.spinner("Generating response..."):
                ai_response = get_ai_response(query)

            st.subheader("📡 SYSTEM OUTPUT")

            st.markdown(f'<div class="panel">{ai_response}</div>',unsafe_allow_html=True)

            if real_data:

                claims = split_claims(ai_response)

                score,results = claim_score(claims,real_data["text"])

                st.subheader("📊 TRUTH ANALYSIS")

                st.metric("TRUTH INDEX",f"{score}%")

                st.progress(score/100)

                st.subheader("🧠 CLAIM VERIFICATION")

                for c,res in results:

                    if res:
                        st.markdown(f'<p class="green">✔ {c}</p>',unsafe_allow_html=True)
                    else:
                        st.markdown(f'<p class="red">⚠ {c}</p>',unsafe_allow_html=True)

                st.subheader("📚 SOURCES")

                for s in real_data["sources"]:

                    st.markdown(
                        f"""
                        <div class="sourcecard">
                        🟢 <b>{s['title']}</b><br>
                        <a href="{s['url']}" target="_blank">Open Source</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

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
                        st.markdown(f'<p class="green">✔ {c}</p>',unsafe_allow_html=True)
                    else:
                        st.markdown(f'<p class="red">⚠ {c}</p>',unsafe_allow_html=True)

                st.subheader("📚 SOURCES")

                for s in real_data["sources"]:

                    st.markdown(
                        f"""
                        <div class="sourcecard">
                        🟢 <b>{s['title']}</b><br>
                        <a href="{s['url']}" target="_blank">Open Source</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
# import streamlit as st
# from prompt_detector import detect_prompt_injection
# from llm_handler import get_ai_response
# from hallucination_checker import check_real_time, split_claims, claim_score
# import time

# st.set_page_config(page_title="TRUTHGUARD AI",layout="wide")

# st.markdown("""
# <style>
# .stApp{
# background:linear-gradient(135deg,#0f172a,#020617);
# color:#e2e8f0;
# }

# .panel{
# background:rgba(15,23,42,0.8);
# padding:20px;
# border-radius:10px;
# border:1px solid rgba(0,255,200,0.2);
# box-shadow:0 0 20px rgba(0,255,200,0.15);
# }
# </style>
# """,unsafe_allow_html=True)

# st.title("🛡️ TRUTHGUARD AI")
# st.caption("PROMPT INJECTION FIREWALL & HALLUCINATION DETECTOR")

# t1,t2 = st.tabs(["[ SHADOW SCAN ]","[ EXTERNAL AUDIT ]"])

# with t1:

#     query = st.text_input("ENTER QUERY")

#     if st.button("EXECUTE SCAN"):

#         is_attack,pattern = detect_prompt_injection(query)

#         if is_attack:

#             st.error(f"🚨 PROMPT ATTACK DETECTED: {pattern}")

#         else:

#             st.success("✅ PROMPT SECURE")

#             with st.spinner("Fetching real time data..."):
#                 real_data = check_real_time(query)

#             with st.spinner("Generating AI response..."):
#                 ai_response = get_ai_response(query)

#             st.subheader("📡 SYSTEM OUTPUT")

#             st.markdown(f'<div class="panel">{ai_response}</div>',unsafe_allow_html=True)

#             if real_data:

#                 claims = split_claims(ai_response)

#                 score,results = claim_score(claims,real_data["text"])

#                 st.subheader("📊 CREDIBILITY ANALYSIS")

#                 st.metric("TRUTH INDEX",f"{score}%")

#                 st.progress(score/100)

#                 st.subheader("🧠 CLAIM VERIFICATION")

#                 for c,res in results:

#                     if res:
#                         st.success(c)
#                     else:
#                         st.warning(c)

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

#             real_data = check_real_time(topic)

#             if real_data:

#                 claims = split_claims(text)

#                 score,results = claim_score(claims,real_data["text"])

#                 st.metric("TRUTH INDEX",f"{score}%")

#                 st.progress(score/100)

#                 st.subheader("🧠 CLAIM VERIFICATION")

#                 for c,res in results:

#                     if res:
#                         st.success(c)
#                     else:
#                         st.warning(c)

#                 st.subheader("📚 SOURCES")

#                 for s in real_data["sources"]:

#                     st.markdown(f"🟢 **{s['title']}**")

#                     st.markdown(f"[Open Source]({s['url']})")
