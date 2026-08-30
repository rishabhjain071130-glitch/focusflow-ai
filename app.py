"""
FocusFlow AI - Streamlit Application.

An AI-Powered Productivity Assistant helping users work with text, questions,
content creation, text analysis, and intelligent suggestions efficiently.
"""

import streamlit as st
from utils.helpers import validate_api_key, count_words, count_characters
from services.ai_service import AIService, AIServiceException
from prompts.prompts import (
    MODE_SUMMARIZE,
    MODE_ASK_AI,
    MODE_GENERATE_CONTENT,
    MODE_ANALYZE_TEXT,
    MODE_SMART_SUGGESTIONS,
)

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FocusFlow AI - Productivity Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Custom Styling (Deep Navy/Black SaaS AI Dashboard Aesthetic)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Body & Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0B0F19 !important;
        color: #F8FAFC;
    }

    /* Hide Default Streamlit Chrome & Headers */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0px;
    }
    footer {
        visibility: hidden;
        height: 0px;
    }
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2rem !important;
        max-width: 1280px;
    }

    /* Sidebar Base Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    .sidebar-brand {
        font-size: 1.35rem;
        font-weight: 800;
        background: linear-gradient(135deg, #A78BFA 0%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.01em;
        margin-bottom: 0.15rem;
    }
    .sidebar-subbrand {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-bottom: 1.1rem;
    }
    
    /* Status Badges */
    .status-badge-ok {
        background: rgba(34, 197, 94, 0.12);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.25);
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        margin-bottom: 1.25rem;
    }
    .status-badge-err {
        background: rgba(239, 68, 68, 0.12);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.25);
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        margin-bottom: 1.25rem;
    }

    /* Sidebar Navigation Header */
    .nav-header {
        font-size: 0.72rem;
        font-weight: 800;
        color: #64748B;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }

    /* Sidebar Promo Card */
    .promo-card {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.15) 0%, rgba(59, 130, 246, 0.12) 100%);
        border: 1px solid rgba(167, 139, 250, 0.25);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    .promo-card-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.3rem;
    }
    .promo-card-text {
        font-size: 0.78rem;
        color: #94A3B8;
        line-height: 1.4;
    }

    .sidebar-footer {
        font-size: 0.78rem;
        color: #64748B;
        text-align: center;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Hero Banner & Dashboard Header */
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        font-size: 0.98rem;
        color: #94A3B8;
        margin-bottom: 1.25rem;
    }

    /* Glassmorphism Hero Card */
    .hero-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(12px);
    }
    .hero-card::after {
        content: "";
        position: absolute;
        top: -40px;
        right: -40px;
        width: 180px;
        height: 180px;
        background: radial-gradient(circle, rgba(124, 58, 237, 0.25) 0%, rgba(59, 130, 246, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-welcome {
        font-size: 1.35rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.25rem;
    }
    .hero-subtext {
        font-size: 0.9rem;
        color: #94A3B8;
        margin-bottom: 1.25rem;
    }

    /* Metric Grid Cards inside Hero */
    .hero-stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.85rem;
    }
    .hero-stat-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 0.8rem 1rem;
    }
    .hero-stat-value {
        font-size: 1.05rem;
        font-weight: 700;
        color: #A78BFA;
        margin-bottom: 0.1rem;
    }
    .hero-stat-label {
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Tool Header Card */
    .tool-header-card {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        backdrop-filter: blur(8px);
    }
    .tool-icon-circle {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-right: 1.1rem;
        flex-shrink: 0;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35);
    }
    .tool-header-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.15rem;
    }
    .tool-header-desc {
        font-size: 0.86rem;
        color: #94A3B8;
    }

    /* Section Cards & Form Containers */
    .card-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 0.45rem;
    }

    /* Output Card styling */
    .output-card-container {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 1.35rem 1.6rem;
        margin-top: 1.25rem;
        backdrop-filter: blur(10px);
    }
    .output-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .output-placeholder {
        color: #64748B;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Primary Gradient Action Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button[kind="primary"]:hover {
        opacity: 0.92 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(124, 58, 237, 0.45) !important;
    }

    /* Inputs, Selectboxes, Textareas Override with Adaptive Sizing */
    .stTextArea textarea {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
        field-sizing: content;
        min-height: 100px !important;
        max-height: 280px !important;
        overflow-y: auto !important;
        resize: vertical !important;
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }
    .stTextInput input, div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
    }

    /* Hide Streamlit Helper Captions and Shortcut Hints (Ctrl+Enter) */
    .stTextArea [data-testid="stWidgetInstructions"],
    .stTextArea small,
    .stTextInput [data-testid="stWidgetInstructions"],
    div[data-testid="stWidgetInstructions"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Radio Options as Styled Selection Cards */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        gap: 0.5rem !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        background: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0.7rem 0.9rem !important;
        margin-bottom: 0.3rem !important;
        transition: all 0.18s ease-in-out !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        border-color: #8B5CF6 !important;
        background: rgba(139, 92, 246, 0.08) !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(59, 130, 246, 0.15) 100%) !important;
        border: 1.5px solid #8B5CF6 !important;
        box-shadow: 0 0 12px rgba(139, 92, 246, 0.25) !important;
    }

    /* Sidebar Navigation Hover */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        background: transparent !important;
        border: 1px solid transparent !important;
        box-shadow: none !important;
        padding: 0.45rem 0.75rem !important;
        margin-bottom: 0.2rem !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.05) !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.25) 0%, rgba(59, 130, 246, 0.2) 100%) !important;
        border: 1px solid rgba(139, 92, 246, 0.4) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Navigation Map (Icon Navigation items)
# -----------------------------------------------------------------------------
NAV_MAP = {
    "▣ Summarize": MODE_SUMMARIZE,
    "💬 Ask AI": MODE_ASK_AI,
    "✎ Generate Content": MODE_ANALYZE_TEXT if False else MODE_GENERATE_CONTENT,
    "◇ Analyze Text": MODE_ANALYZE_TEXT,
    "💡 Smart Suggestions": MODE_SMART_SUGGESTIONS,
}

# -----------------------------------------------------------------------------
# Sidebar Navigation & Status
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-brand">✨ FocusFlow AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subbrand">AI-powered productivity assistant</div>', unsafe_allow_html=True)

    # Connection Status
    is_api_valid, _ = validate_api_key()
    if is_api_valid:
        st.markdown('<div class="status-badge-ok">● AI Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge-err">● AI Service Unavailable</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-header">PRODUCTIVITY TOOLS</div>', unsafe_allow_html=True)

    selected_nav_label = st.radio(
        "Select Navigation",
        options=list(NAV_MAP.keys()),
        index=0,
        label_visibility="collapsed",
    )
    selected_mode = NAV_MAP[selected_nav_label]

    # Promotional Productivity Card
    st.markdown(
        """
        <div class="promo-card">
            <div class="promo-card-title">🚀 Boost your productivity</div>
            <div class="promo-card-text">Let AI handle the heavy lifting so you can focus on what matters most.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-footer">✦ Powered by Gemini</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Main Dashboard Hero Section
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">FocusFlow AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="main-subtitle">Your intelligent workspace for understanding, creating, and improving content.</div>',
    unsafe_allow_html=True,
)

# Glassmorphism Hero Card with Metrics
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-welcome">Welcome to FocusFlow AI</div>
        <div class="hero-subtext">Your intelligent workspace for understanding, creating, and improving content.</div>
        <div class="hero-stats-grid">
            <div class="hero-stat-card">
                <div class="hero-stat-value">5</div>
                <div class="hero-stat-label">Powerful Tools</div>
            </div>
            <div class="hero-stat-card">
                <div class="hero-stat-value">AI Powered</div>
                <div class="hero-stat-label">Gemini 2.5 Flash-Lite</div>
            </div>
            <div class="hero-stat-card">
                <div class="hero-stat-value">Secure</div>
                <div class="hero-stat-label">Your data is safe</div>
            </div>
            <div class="hero-stat-card">
                <div class="hero-stat-value">Fast & Smart</div>
                <div class="hero-stat-label">Instant results</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Tool Header Card
# -----------------------------------------------------------------------------
TOOL_HEADERS = {
    MODE_SUMMARIZE: (
        "▣",
        "Summarize Text",
        "Extract key insights, concise summaries, or executive overviews from articles, notes, and documents.",
    ),
    MODE_ASK_AI: (
        "💬",
        "Ask AI",
        "Get direct answers to questions with optional document reference context for grounded responses.",
    ),
    MODE_GENERATE_CONTENT: (
        "✎",
        "Generate Content",
        "Draft emails, study notes, blog outlines, social media posts, and descriptions tailored by tone and length.",
    ),
    MODE_ANALYZE_TEXT: (
        "◇",
        "Analyze Text",
        "Receive structured document critiques covering key points, strengths, improvements, and overall assessment.",
    ),
    MODE_SMART_SUGGESTIONS: (
        "💡",
        "Smart Suggestions",
        "Convert raw project notes or goals into actionable next steps, work breakdowns, and priority items.",
    ),
}

tool_icon, tool_title, tool_desc = TOOL_HEADERS.get(
    selected_mode, ("✨", selected_mode, "")
)

st.markdown(
    f"""
    <div class="tool-header-card">
        <div class="tool-icon-circle">{tool_icon}</div>
        <div>
            <div class="tool-header-title">{tool_title}</div>
            <div class="tool-header-desc">{tool_desc}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize AI Service Layer
ai_service = AIService()

# -----------------------------------------------------------------------------
# MODE 1: SUMMARIZE WORKSPACE
# -----------------------------------------------------------------------------
if selected_mode == MODE_SUMMARIZE:
    col_in, col_opt = st.columns([3, 2], gap="large")

    with col_in:
        st.markdown('<div class="card-label">1. Input Your Text</div>', unsafe_allow_html=True)
        text_input = st.text_area(
            "Input Text",
            height=110,
            placeholder="Paste your text here...",
            label_visibility="collapsed",
        )

    with col_opt:
        st.markdown('<div class="card-label">2. Summary Style</div>', unsafe_allow_html=True)
        summary_style = st.radio(
            "Select Style",
            options=["Bullet Points", "Concise Summary", "Executive Summary"],
            index=0,
            format_func=lambda x: {
                "Bullet Points": "Bullet Points — Key points in bulleted format",
                "Concise Summary": "Concise Summary — Brief and to the point summary",
                "Executive Summary": "Executive Summary — Detailed overview for decision makers",
            }[x],
        )

        st.write("")
        btn_summarize = st.button("✨ Summarize", type="primary", use_container_width=True)

    st.markdown('<div class="card-label" style="margin-top: 1.25rem;">3. Summary Output</div>', unsafe_allow_html=True)
    output_container = st.container()

    if btn_summarize:
        if not text_input.strip():
            st.warning("Please enter some text before continuing.")
        else:
            with st.spinner("Thinking..."):
                try:
                    result = ai_service.summarize(text=text_input, summary_style=summary_style)
                    with output_container:
                        st.markdown(
                            """
                            <div class="output-card-container">
                                <div class="output-card-title">Summary Result</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))
    else:
        with output_container:
            st.markdown(
                """
                <div class="output-card-container">
                    <div class="output-placeholder">📄 Your summarized content will appear here...</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# -----------------------------------------------------------------------------
# MODE 2: ASK AI WORKSPACE
# -----------------------------------------------------------------------------
elif selected_mode == MODE_ASK_AI:
    st.markdown('<div class="card-label">Your Question</div>', unsafe_allow_html=True)
    question_input = st.text_input(
        "Question",
        placeholder="e.g., What are the key principles of scalable system design?",
        label_visibility="collapsed",
    )

    with st.expander("📌 Optional Reference Context", expanded=False):
        context_input = st.text_area(
            "Reference Context",
            height=110,
            placeholder="Paste background document, code snippet, or article snippet to ground the AI answer...",
        )

    st.write("")
    if st.button("Ask AI", type="primary", use_container_width=True):
        if not question_input.strip():
            st.warning("Please enter some text before continuing.")
        else:
            with st.spinner("Thinking..."):
                try:
                    context_val = context_input if 'context_input' in locals() else None
                    result = ai_service.ask_ai(question=question_input, context=context_val)
                    st.markdown(
                        """
                        <div class="output-card-container">
                            <div class="output-card-title">AI Response</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))

# -----------------------------------------------------------------------------
# MODE 3: GENERATE CONTENT WORKSPACE
# -----------------------------------------------------------------------------
elif selected_mode == MODE_GENERATE_CONTENT:
    col1, col2, col3 = st.columns(3)
    with col1:
        content_type = st.selectbox(
            "Content Type",
            options=[
                "Email",
                "Study Notes",
                "Blog Outline",
                "Social Media Post",
                "Professional Description",
            ],
            index=0,
        )
    with col2:
        tone = st.selectbox(
            "Tone & Style",
            options=["Professional", "Casual", "Academic", "Concise", "Persuasive"],
            index=0,
        )
    with col3:
        length = st.selectbox(
            "Target Length",
            options=["Short", "Medium", "Detailed"],
            index=1,
        )

    st.markdown('<div class="card-label" style="margin-top: 1rem;">Topic / Instructions</div>', unsafe_allow_html=True)
    instructions_input = st.text_area(
        "Instructions",
        height=110,
        placeholder="Describe the content topic, key points to cover, or specific guidance...",
        label_visibility="collapsed",
    )

    st.write("")
    if st.button("Generate Content", type="primary", use_container_width=True):
        if not instructions_input.strip():
            st.warning("Please enter some text before continuing.")
        else:
            with st.spinner("Generating your response..."):
                try:
                    result = ai_service.generate_content(
                        instructions=instructions_input,
                        content_type=content_type,
                        tone=tone,
                        length=length,
                    )
                    st.markdown(
                        """
                        <div class="output-card-container">
                            <div class="output-card-title">Generated Content</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))

# -----------------------------------------------------------------------------
# MODE 4: ANALYZE TEXT WORKSPACE
# -----------------------------------------------------------------------------
elif selected_mode == MODE_ANALYZE_TEXT:
    st.markdown('<div class="card-label">Text to Analyze</div>', unsafe_allow_html=True)
    text_to_analyze = st.text_area(
        "Text to Analyze",
        height=110,
        placeholder="Paste draft, proposal, or document snippet to analyze...",
        label_visibility="collapsed",
    )

    analysis_type = st.selectbox(
        "Analysis Focus",
        options=[
            "Comprehensive Analysis",
            "Tone & Sentiment",
            "Readability & Clarity",
            "Key Entities & Themes",
        ],
        index=0,
    )

    st.write("")
    if st.button("Analyze Text", type="primary", use_container_width=True):
        if not text_to_analyze.strip():
            st.warning("Please enter some text before continuing.")
        else:
            with st.spinner("Thinking..."):
                try:
                    result = ai_service.analyze_text(
                        text=text_to_analyze, analysis_type=analysis_type
                    )
                    st.markdown(
                        """
                        <div class="output-card-container">
                            <div class="output-card-title">Structured Document Analysis</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))

# -----------------------------------------------------------------------------
# MODE 5: SMART SUGGESTIONS WORKSPACE
# -----------------------------------------------------------------------------
elif selected_mode == MODE_SMART_SUGGESTIONS:
    st.markdown('<div class="card-label">Situation / Content</div>', unsafe_allow_html=True)
    suggestion_input = st.text_area(
        "Situation / Content",
        height=110,
        placeholder="Paste meeting notes, project brief, or goal statement to generate recommendations...",
        label_visibility="collapsed",
    )

    focus_area = st.selectbox(
        "Focus Area",
        options=[
            "Actionable Next Steps",
            "Work Breakdown Structure",
            "Follow-up Questions",
            "Priority Recommendations",
        ],
        index=0,
    )

    st.write("")
    if st.button("Get Smart Suggestions", type="primary", use_container_width=True):
        if not suggestion_input.strip():
            st.warning("Please enter some text before continuing.")
        else:
            with st.spinner("Thinking..."):
                try:
                    result = ai_service.suggest_improvements(
                        text=suggestion_input, focus_area=focus_area
                    )
                    st.markdown(
                        """
                        <div class="output-card-container">
                            <div class="output-card-title">Actionable Recommendations</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))
