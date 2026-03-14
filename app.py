import streamlit as st
from prompt_detector import detect_prompt_injection
from llm_handler import get_ai_response
from hallucination_checker import check_real_time, split_claims, claim_score

st.set_page_config(page_title="TRUTHGUARD AI", layout="wide")

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#0a0f24,#000000);
color:#e2e8f0;
}

h1{
color:#22c55e;
text-shadow:0 0 15px #22c55e;
}

.panel{
background: rgba(20,20,40,0.6);
backdrop-filter: blur(15px);
border:1px solid rgba(168,85,247,0.4);
border-radius:14px;
padding:20px;
box-shadow:0 0 25px rgba(168,85,247,0.35);
}

.stButton>button{
background:linear-gradient(45deg,#9333ea,#22c55e);
color:white;
border:none;
border-radius:8px;
font-weight:bold;
box-shadow:0 0 10px #22c55e;
}

.stTextInput input{
background:rgba(0,0,0,0.6);
border:1px solid #9333ea;
color:#22c55e;
}

.sourcecard{
background:rgba(0,0,0,0.5);
backdrop-filter: blur(10px);
border:1px solid rgba(34,197,94,0.4);
padding:12px;
border-radius:8px;
margin-bottom:10px;
}

.green{color:#22c55e;font-weight:bold;}
.red{color:#ef4444;font-weight:bold;}

</style>
""", unsafe_allow_html=True)

st.title("🛡️ TRUTHGUARD AI")
st.caption("PROMPT INJECTION FIREWALL & HALLUCINATION DETECTOR")

t1, t2 = st.tabs(["[ SHADOW SCAN ]", "[ EXTERNAL AUDIT ]"])

with t1:

    query = st.text_input("ENTER QUERY")

    if st.button("EXECUTE SCAN"):

        is_attack, pattern = detect_prompt_injection(query)

        if is_attack:

            st.markdown(f'<p class="red">🚨 PROMPT ATTACK DETECTED: {pattern}</p>', unsafe_allow_html=True)

        else:

            st.markdown('<p class="green">✔ PROMPT SECURE</p>', unsafe_allow_html=True)

            real_data = check_real_time(query)
            ai_response = get_ai_response(query)

            st.subheader("📡 SYSTEM OUTPUT")

            st.markdown(f'<div class="panel">{ai_response}</div>', unsafe_allow_html=True)

            if real_data:

                claims = split_claims(ai_response)

                score, results = claim_score(claims, real_data["text"])

                st.subheader("📊 TRUTH ANALYSIS")

                st.metric("TRUTH INDEX", f"{score}%")
                st.progress(score/100)

                st.subheader("🧠 CLAIM VERIFICATION")

                for c, res in results:

                    if res:
                        st.markdown(f'<p class="green">✔ {c}</p>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<p class="red">⚠ {c}</p>', unsafe_allow_html=True)

                st.subheader("📚 SOURCES")

                for s in real_data["sources"]:

                    st.markdown(
                        f"""
                        <div class="sourcecard">
                        🟢 <b>{s['title']}</b><br>
                        <a href="{s['url']}" target="_blank">Open Source</a>
                        </div>
                        """,
                        unsafe_allow_html=True)
                    

with t2:

    st.subheader("AUDIT EXTERNAL TEXT")

    topic = st.text_input("TOPIC")
    text = st.text_area("PASTE TEXT")

    if st.button("RUN AUDIT"):

        if topic and text:

            real_data = check_real_time(topic)

            if real_data:

                claims = split_claims(text)

                score, results = claim_score(claims, real_data["text"])

                st.metric("TRUTH INDEX", f"{score}%")
                st.progress(score/100)

                st.subheader("🧠 CLAIM VERIFICATION")

                for c, res in results:

                    if res:
                        st.markdown(f'<p class="green">✔ {c}</p>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<p class="red">⚠ {c}</p>', unsafe_allow_html=True)

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
