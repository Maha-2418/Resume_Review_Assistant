# 📄 AI Resume Review Assistant

An AI-powered Resume Review Assistant that analyzes resumes, provides ATS scores, identifies missing skills, suggests improvements, generates downloadable PDF reports, and allows users to interact with their resumes through an intelligent chatbot and voice assistant.

---

## 🚀 Features

- 📄 Upload Resume (PDF/DOCX)
- 🤖 AI-Powered Resume Analysis
- 📊 ATS Score Dashboard
- 📈 Interactive Charts & Visualizations
- 💪 Resume Strengths Detection
- ❌ Missing Skills Identification
- ⚠ Weakness Detection
- ✍ Grammar Suggestions
- 💼 Recommended Job Roles
- 💡 Personalized Improvement Suggestions
- 📥 Download Professional PDF Report
- 💬 AI Resume Chat Assistant
- 🎙 Speech-to-Text (ElevenLabs)
- 🔊 Text-to-Speech (ElevenLabs)
- 🎨 Modern Streamlit UI

---

## 🖼️ Project Preview

### Dashboard
- ATS Score Gauge
- Resume Metrics
- Skill Distribution Chart
- Category Analysis
- AI Suggestions

### Resume Chatbot
Ask questions like:

- "What are my strengths?"
- "Which skills are missing?"
- "Summarize my resume."
- "Suggest improvements."
- "Am I suitable for a Java Developer role?"

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI Model
- Google Gemma 4 26B (via OpenRouter)

### Voice AI
- ElevenLabs

### PDF Generation
- ReportLab

### Charts
- Plotly

### Resume Parsing
- PyPDF2
- python-docx

---

## 📂 Project Structure

```
Resume_Review_Assistant/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── backend/
│   ├── ats_scoring.py
│   ├── chatbot.py
│   ├── llm_engine.py
│   ├── parser.py
│   ├── prompts.py
│   ├── report_generator.py
│   └── voice.py
│
├── utils/
│   ├── text_cleaner.py
│   └── file_handler.py
│
├── static/
│   └── style.css
│
├── templates/
│   └── report_template.html
│
└── reports/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Maha-2418/Resume_Review_Assistant.git

cd Resume_Review_Assistant
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file inside the project folder.

```
QWEN_API_KEY=YOUR_OPENROUTER_API_KEY

ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY
```

---

## ▶ Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## 📊 Workflow

1. Upload Resume (PDF/DOCX)
2. Extract Resume Text
3. Clean Resume Content
4. AI Resume Analysis
5. ATS Score Calculation
6. Resume Insights Generation
7. Display Interactive Dashboard
8. Generate Professional PDF Report
9. Chat with Resume
10. Voice-based Resume Interaction

---

## 📸 Key Features

### ATS Analysis
- Overall ATS Score
- Resume Summary
- Strengths
- Weaknesses
- Missing Skills
- Grammar Issues
- Suggested Job Roles
- Improvement Tips

### AI Resume Chat
- Resume-based Question Answering
- Resume Summarization
- Resume Rewriting
- Skill Recommendations

### Voice Assistant
- Speech-to-Text
- Text-to-Speech

### PDF Report
- Professional Resume Report
- ATS Score
- Charts
- Suggestions
- Downloadable PDF

---

## 🎯 Future Enhancements

- Multi-language Resume Support
- Resume Comparison
- LinkedIn Profile Review
- Cover Letter Generator
- Resume Templates
- Job Description Matching
- Interview Question Generator
- AI Career Advisor

---

## 👩‍💻 Author

**Mahalakshmi G**

Final Year B.E. Computer Science and Engineering

Sri Ramakrishna Engineering College

GitHub: https://github.com/Maha-2418

---

## ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub!
