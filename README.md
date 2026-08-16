# FocusFlow AI ⚡

> **AI-Powered Productivity Assistant** — Built for the Innovation Hacks AI Internship 2026 (Week 1).

FocusFlow AI is a professional, modular web application designed to help students, professionals, and general users analyze, summarize, create, and interact with text far more efficiently.

---

## 📌 Problem Being Solved

In today's information-heavy environment, users waste significant time manually digesting long documents, drafting repetitive communications, analyzing document tone, or figuring out actionable next steps from raw meeting notes. 

**FocusFlow AI** addresses this productivity bottleneck by offering a single, focused assistant exposed through five tailored capabilities rather than a generic chatbot interface.

---

## ✨ Core Capabilities (Week 1)

1. **📝 Text Summarization**: Generate high-impact `Bullet Points`, a single tight `Concise Summary`, or a multi-paragraph `Executive Summary`.
2. **❓ Question Answering (Ask AI)**: Get accurate, direct answers to general questions or ground answers using optional reference context. States limitations clearly when information is missing.
3. **✍️ Content Generation**: Draft `Email`, `Study Notes`, `Blog Outline`, `Social Media Post`, or `Professional Description` with customizable Tone (`Professional`, `Casual`, `Academic`, `Concise`, `Persuasive`) and Target Length (`Short`, `Medium`, `Detailed`).
4. **🔍 Text & Document Analysis**: Receive structured critique including `Main Topic`, `Key Points`, `Important Observations`, `Strengths`, `Areas for Improvement`, and `Overall Assessment`.
5. **💡 Intelligent Suggestions**: Turn raw context into actionable, prioritized recommendations categorized into `Immediate Action Items`, `Strategic Recommendations`, and `Follow-up Questions`.

---

## 🛠️ Technology Stack

- **Language**: Python 3.10+
- **Frontend Framework**: [Streamlit](https://streamlit.io/)
- **AI SDK**: Official [Google GenAI SDK](https://pypi.org/project/google-genai/) (`google-genai`) / Gemini API
- **Environment Management**: `python-dotenv`
- **Version Control**: Git & GitHub

---

## 📁 Project Architecture & Directory Structure

FocusFlow AI follows a clean, modular architecture separating UI logic, AI service integration, and prompt engineering:

```
focusflow-ai/
│
├── app.py                  # Main Streamlit application UI & control flow
├── requirements.txt        # Application dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules for secrets and build files
├── README.md               # Project documentation
│
├── services/
│   ├── __init__.py
│   └── ai_service.py       # Gemini API client, API wrapper & error handling
│
├── prompts/
│   ├── __init__.py
│   └── prompts.py          # Structured prompt templates for all 5 capabilities
│
└── utils/
    ├── __init__.py
    └── helpers.py          # Environment checks, validation & text helpers
```

---

## 🚀 Local Setup & Installation

### 1. Prerequisites
Ensure you have **Python 3.10 or higher** installed.

### 2. Clone Repository & Navigate
```bash
git clone <repository-url>
cd focusflow-ai
```

### 3. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variable Setup & Security

1. Obtain a **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).
2. Copy `.env.example` to create `.env`:
   ```bash
   cp .env.example .env   # On Windows PowerShell: copy .env.example .env
   ```
3. Open `.env` and paste your API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

> ⚠️ **SECURITY WARNING**: 
> **NEVER commit your `.env` file or hardcode API keys anywhere in your codebase.** `.gitignore` is configured to exclude `.env` automatically. Always inspect `git status` before committing.

---

## 💻 How to Run the Application

Start the Streamlit development server:

```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 📊 Current Development Status

- [x] **Week 1 (Current)**: Project foundation setup, modular architecture, Gemini API service layer, prompt template isolation, Streamlit UI, error handling, loading states, secure `.env` integration, documentation, and Git initialization.
- [ ] **Week 2**: Advanced file uploading (PDF/TXT processing) & enhanced document analytics.
- [ ] **Week 3**: Custom workflow templates & persistent history storage.
- [ ] **Week 4**: Final performance optimization, testing suite, and production deployment.

---

## 📄 License
Created for **Innovation Hacks AI Internship 2026**.
