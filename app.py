import streamlit as st
from backend.parser import extract_text_from_pdf, extract_text_from_docx
from backend.ats_scoring import analyze_resume
from backend.report_generator import generate_report
from backend.chatbot import chat_with_resume
from utils.text_cleaner import clean_text
import plotly.graph_objects as go
import plotly.express as px
from backend.voice import (
    speech_to_text,
    text_to_speech
)
import os

from streamlit_mic_recorder import mic_recorder

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Resume Review Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family:Arial, sans-serif;
}

.main{
    background:#F5F7FA;
}

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* Hero Banner */

.hero{
    background:linear-gradient(135deg,#2563EB,#4F46E5);
    padding:35px;
    border-radius:20px;
    color:white;
    text-align:center;
    margin-bottom:25px;
}

.hero h1{
    font-size:42px;
    margin-bottom:8px;
}

.hero p{
    font-size:18px;
    color:#E5E7EB;
}

/* Cards */

.card{
    background:white;
    border-radius:18px;
    padding:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom:20px;
}

.card-title{
    font-size:20px;
    font-weight:bold;
    color:#1E3A8A;
    margin-bottom:10px;
}

/* ATS Score */

.score-box{
    background:linear-gradient(135deg,#0F62FE,#2563EB);
    color:white;
    padding:35px;
    border-radius:20px;
    text-align:center;
    margin-bottom:20px;
}

.score-box h1{
    font-size:60px;
    margin:0;
}

.score-box h3{
    margin-top:10px;
}

/* Footer */

.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("🤖 Resume AI")

    st.markdown("---")

    st.success("📄 Resume Analysis")

    st.info("📊 ATS Score")

    st.info("💬 AI Feedback")

    st.info("📈 Skill Analysis")

    st.info("📄 PDF Report")

    st.markdown("---")

    st.subheader("Features")

    st.write("✅ ATS Resume Score")
    st.write("✅ Resume Summary")
    st.write("✅ Grammar Check")
    st.write("✅ Missing Skills")
    st.write("✅ Job Role Suggestions")
    st.write("✅ AI Improvement Tips")
    st.write("✅ Download PDF Report")

    st.markdown("---")

    st.caption("Made by Mahalakshmi ❤️")

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""

<div class="hero">

<h1>📄 Resume Review Assistant</h1>

<p>
AI-Powered ATS Resume Analyzer with Personalized Feedback,
Skill Analysis and Career Recommendations.
</p>

</div>

""", unsafe_allow_html=True)

# ---------------------------------------------------
# FILE UPLOADER
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload Resume",
    type=["pdf", "docx"]
)
# ---------------------------------------------------
# PROCESS RESUME
# ---------------------------------------------------

if uploaded_file:

    st.success("✅ Resume uploaded successfully!")

    # -----------------------------------------------
    # Extract Resume Text
    # -----------------------------------------------

    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)

    text = clean_text(text)

    # -----------------------------------------------
    # Candidate Information
    # -----------------------------------------------

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    candidate_name = lines[0] if lines else "Candidate"

    st.markdown("## 👤 Candidate Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Candidate",
            value=candidate_name
        )

    with col2:
        st.metric(
            label="Resume",
            value=uploaded_file.name
        )

    with col3:
        st.metric(
            label="Characters",
            value=f"{len(text):,}"
        )

    st.markdown("---")

    # -----------------------------------------------
    # Resume Preview
    # -----------------------------------------------

    with st.expander(
        "📄 Resume Preview",
        expanded=False
    ):

        st.text_area(
            label="Extracted Resume",
            value=text,
            height=350
        )

    st.markdown("---")

    # -----------------------------------------------
    # Analyze Button
    # -----------------------------------------------

    if st.button("🚀 Analyze Resume", use_container_width=True):

        with st.spinner("🤖 AI is analyzing your resume..."):

            result = analyze_resume(text)

        if result is None:
            st.error("⚠ AI service is busy.")
            st.stop()

        if "error" in result:
            st.error(result["error"])
            st.stop()

        st.session_state.analysis_result = result
        st.session_state.resume_text = text
        
    if st.session_state.analysis_result is not None:

        result = st.session_state.analysis_result
        if result is None or "ats_score" not in result:
            st.error("Analysis result is unavailable. Please analyze the resume again.")
            st.stop()
        text = st.session_state.resume_text
        # -----------------------------------------------
        # ATS SCORE DASHBOARD
        # -----------------------------------------------

        score = result["ats_score"]
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Overall ATS Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563EB"},
                "steps": [
                    {"range": [0, 40], "color": "#EF4444"},
                    {"range": [40, 70], "color": "#F59E0B"},
                    {"range": [70, 100], "color": "#10B981"}
                ]
            }
        ))

        st.markdown("## 📊 ATS Dashboard")

        st.markdown(
            f"""
            <div class="score-box">
                <h1>{score}/100</h1>
                <h3>Overall ATS Score</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        if score >= 80:
            st.success("🎉 Excellent Resume! Your resume is highly ATS-friendly.")
        elif score >= 60:
            st.warning("👍 Good Resume! A few improvements can increase your ATS score.")
        else:
            st.error("⚠ Your resume needs improvement before applying.")

        st.progress(score / 100)
        st.plotly_chart(gauge, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # -----------------------------------------------
        # QUICK METRICS
        # -----------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "ATS Score",
                f"{score}/100"
            )

        with col2:
            st.metric(
                "Strengths",
                len(result["strengths"])
            )

        with col3:
            st.metric(
                "Missing Skills",
                len(result["missing_skills"])
            )

        with col4:
            st.metric(
                "Suggestions",
                len(result["suggestions"])
            )

        st.markdown("---")
        
        matched = len(result["strengths"])
        missing = len(result["missing_skills"])
        partial = max(1, matched // 4)

        skill_chart = px.pie(
            values=[matched, missing, partial],
            names=["Matched", "Missing", "Partial"],
            hole=0.6,
            title="Skill Distribution"
        )

        st.plotly_chart(skill_chart, use_container_width=True)

        # -----------------------------------------------
        # RESUME SUMMARY
        # -----------------------------------------------
        categories = [
            "Skills",
            "Experience",
            "Education",
            "Keywords",
            "Formatting"
        ]

        scores = [90, 85, 80, 88, 75]

        bar_chart = px.bar(
            x=scores,
            y=categories,
            orientation="h",
            title="Category Scores",
            text=scores
        )

        st.plotly_chart(bar_chart, use_container_width=True)
        
        st.markdown(
            """
            <div class="card">
            <div class="card-title">
            📌 Resume Summary
            </div>
            """,
            unsafe_allow_html=True
        )
        

        st.write(result["summary"])

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        
        # -----------------------------------------------
        # STRENGTHS & MISSING SKILLS
        # -----------------------------------------------
        radar = go.Figure()

        radar.add_trace(
            go.Scatterpolar(
                r=scores,
                theta=categories,
                fill="toself",
                name="Resume"
            )
        )

        radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0,100]
                )
            ),
            showlegend=False,
            title="Resume Performance"
        )

        st.plotly_chart(radar, use_container_width=True)
        st.markdown("## 💪 Skills Analysis")

        left_col, right_col = st.columns(2)

        # -------------------------
        # Strengths Card
        # -------------------------

        with left_col:

            st.markdown("""
            <div class="card">
            <div class="card-title">
            💪 Strengths
            </div>
            """, unsafe_allow_html=True)

            if result["strengths"]:

                for item in result["strengths"]:

                    st.success(f"✅ {item}")

            else:

                st.info("No strengths identified.")

            st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # Missing Skills Card
        # -------------------------

        with right_col:

            st.markdown("""
            <div class="card">
            <div class="card-title">
            ❌ Missing Skills
            </div>
            """, unsafe_allow_html=True)

            if result["missing_skills"]:

                for item in result["missing_skills"]:

                    st.error(f"❌ {item}")

            else:

                st.success("No important skills missing.")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # -----------------------------------------------
        # WEAKNESSES
        # -----------------------------------------------

        st.markdown("## ⚠ Weaknesses")

        with st.expander(
            "View Weaknesses",
            expanded=True
        ):

            if result["weaknesses"]:

                for weakness in result["weaknesses"]:

                    st.warning(f"⚠ {weakness}")

            else:

                st.success("No weaknesses detected.")

        st.markdown("---")
        
                # -----------------------------------------------
        # GRAMMAR ISSUES
        # -----------------------------------------------

        st.markdown("## 📝 Grammar Analysis")

        with st.expander(
            "View Grammar Issues",
            expanded=False
        ):

            if result["grammar"]:

                for item in result["grammar"]:

                    st.info(f"📝 {item}")

            else:

                st.success("✅ No grammar issues detected.")

        st.markdown("---")

        # -----------------------------------------------
        # SUITABLE JOB ROLES
        # -----------------------------------------------

        st.markdown("## 💼 Recommended Job Roles")

        role_col1, role_col2 = st.columns(2)

        roles = result.get("job_roles", [])

        if roles:

            half = (len(roles) + 1) // 2

            with role_col1:

                for role in roles[:half]:

                    st.success(f"🎯 {role}")

            with role_col2:

                for role in roles[half:]:

                    st.success(f"🎯 {role}")

        else:

            st.info("No suitable job roles identified.")

        st.markdown("---")

        # -----------------------------------------------
        # IMPROVEMENT SUGGESTIONS
        # -----------------------------------------------

        st.markdown("## 📈 Improvement Suggestions")

        suggestions = result.get("suggestions", [])

        if suggestions:

            for index, suggestion in enumerate(suggestions, start=1):

                st.markdown(
                    f"""
                    <div class="card">
                        <b>Suggestion {index}</b><br><br>
                        {suggestion}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success("🎉 Your resume is already well optimized.")

        st.markdown("---")

        st.success("✅ Resume analysis completed successfully!")
        
                # -----------------------------------------------
        # GENERATE PDF REPORT
        # -----------------------------------------------

        st.markdown("## 📄 AI Resume Report")

        with st.spinner("Generating professional PDF report..."):

            pdf_file = generate_report(
                result=result,
                candidate_name=candidate_name
            )

        st.success("🎉 Your professional AI report is ready!")

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📥 Download Resume Report",
                data=file,
                file_name=f"{candidate_name.replace(' ','_')}_ATS_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        st.markdown("---")
        
        st.markdown("---")
        
        st.subheader("🎤 Voice Assistant")

        voice_question = None

        audio = mic_recorder(
            start_prompt="🎙 Start Recording",
            stop_prompt="⏹ Stop Recording",
            key="recorder"
        )

        if audio:

            os.makedirs("temp_audio", exist_ok=True)

            audio_path = "temp_audio/question.wav"

            with open(audio_path, "wb") as f:
                f.write(audio["bytes"])

            voice_question = speech_to_text(audio_path)

            st.success("Recognized Speech")

            st.write(voice_question)

        st.header("💬 Chat With Your Resume")

        st.caption("Ask anything about your uploaded resume.")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        typed_question = st.chat_input("Ask a question about your resume...")

        if voice_question:
            question = voice_question
        else:
            question = typed_question

        if question:

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message("user"):
                st.markdown(question)

            with st.spinner("Gemma is thinking..."):

                answer = chat_with_resume(
                    text,
                    str(result),
                    question
                )
                print("CHATBOT ANSWER:", answer)
            with st.chat_message("assistant"):
                st.markdown(answer)
                audio_path = text_to_speech(answer)
                st.audio(audio_path)
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        # -----------------------------------------------
        # THANK YOU SECTION
        # -----------------------------------------------

        st.markdown(
            """
            <div class="card" style="text-align:center">

            <h2>🎉 Analysis Completed</h2>

            <p>
            Your resume has been successfully analyzed using AI.
            Review the recommendations, improve your resume,
            and download the detailed report.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.balloons()

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div class="footer">

    <h4>🤖 Resume Review Assistant</h4>

    <p>
    AI-powered ATS Resume Analyzer built using
    <b>Python</b> • <b>Streamlit</b> • <b>OpenRouter</b> • <b>Gemma LLM</b>
    </p>

    <p>
    Developed by <b>Mahalakshmi</b>
    </p>

    </div>
    """,
    unsafe_allow_html=True
)