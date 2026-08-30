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
# Custom Styling (Modern Dark Productivity Interface)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top Hero Header */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 1.0rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* Selected Tool Header Banner */
    .tool-banner {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.75rem;
    }
    .tool-banner-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 0.25rem;
    }
    .tool-banner-desc {
        font-size: 0.9rem;
        color: #94A3B8;
    }

    /* Sidebar Styling */
    .sidebar-brand {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: 0.05em;
        margin-bottom: 0.15rem;
        text-transform: uppercase;
    }
    .sidebar-subbrand {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-bottom: 1rem;
    }
    .status-badge-ok {
        background-color: rgba(34, 197, 94, 0.1);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.25);
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .status-badge-err {
        background-color: rgba(239, 68, 68, 0.1);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.25);
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .nav-header {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .sidebar-footer {
        font-size: 0.78rem;
        color: #64748B;
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #1E293B;
    }

    /* Metric Counters */
    .metric-text {
        font-size: 0.8rem;
        color: #64748B;
        text-align: right;
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
    }

    /* Output Section */
    .output-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #334155;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Sidebar Navigation & Status
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-brand">FOCUSFLOW AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subbrand">AI-powered productivity assistant</div>', unsafe_allow_html=True)

    # Status Indicator
    is_api_valid, _ = validate_api_key()
    if is_api_valid:
        st.markdown('<div class="status-badge-ok">● AI Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge-err">● AI Service Unavailable</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-header">PRODUCTIVITY TOOLS</div>', unsafe_allow_html=True)

    selected_mode = st.radio(
        "Select Tool",
        options=[
            MODE_SUMMARIZE,
            MODE_ASK_AI,
            MODE_GENERATE_CONTENT,
            MODE_ANALYZE_TEXT,
            MODE_SMART_SUGGESTIONS,
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-footer">Powered by Gemini</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Main Dashboard Header
# -----------------------------------------------------------------------------
st.markdown('<div class="hero-title">FocusFlow AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Your intelligent workspace for understanding, creating, and improving content.</div>',
    unsafe_allow_html=True,
)

# Tool Descriptions for Header Banner
TOOL_DESCRIPTIONS = {
    MODE_SUMMARIZE: ("Summarize", "Extract bullet points, concise summaries, or executive overviews from articles, notes, and documents."),
    MODE_ASK_AI: ("Ask AI", "Get direct answers to questions with optional document reference context for grounded responses."),
    MODE_GENERATE_CONTENT: ("Generate Content", "Draft emails, study notes, blog outlines, social media posts, and descriptions tailored by tone and length."),
    MODE_ANALYZE_TEXT: ("Analyze Text", "Receive structured document critiques covering key points, strengths, improvements, and overall assessment."),
    MODE_SMART_SUGGESTIONS: ("Smart Suggestions", "Convert raw project notes or goals into actionable next steps, work breakdowns, and priority items."),
}

tool_title, tool_desc = TOOL_DESCRIPTIONS.get(selected_mode, (selected_mode, ""))

st.markdown(
    f"""
    <div class="tool-banner">
        <div class="tool-banner-title">{tool_title}</div>
        <div class="tool-banner-desc">{tool_desc}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize Service Layer
ai_service = AIService()

# -----------------------------------------------------------------------------
# MODE 1: SUMMARIZE
# -----------------------------------------------------------------------------
if selected_mode == MODE_SUMMARIZE:
    text_input = st.text_area(
        "Input Text",
        height=220,
        placeholder="Paste article text, meeting notes, reports, or document content here...",
    )

    st.markdown(
        f'<div class="metric-text">Words: {count_words(text_input)} | Characters: {count_characters(text_input)}</div>',
        unsafe_allow_html=True,
    )

    summary_style = st.selectbox(
        "Summary Style",
        options=["Bullet Points", "Concise Summary", "Executive Summary"],
        index=0,
    )

    st.write("")
    if st.button("Summarize", type="primary", use_container_width=True):
        if not text_input.strip():
            st.warning("Please enter some text before continuing.")
        else:
            with st.spinner("Thinking..."):
                try:
                    result = ai_service.summarize(text=text_input, summary_style=summary_style)
                    st.markdown('<div class="output-header">Summary Output</div>', unsafe_allow_html=True)
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))

# -----------------------------------------------------------------------------
# MODE 2: ASK AI
# -----------------------------------------------------------------------------
elif selected_mode == MODE_ASK_AI:
    question_input = st.text_input(
        "Your Question",
        placeholder="e.g., What are the core advantages of microservices architecture?",
    )

    with st.expander("Optional Reference Context", expanded=False):
        context_input = st.text_area(
            "Reference Document / Context",
            height=160,
            placeholder="Paste reference text, code snippet, or article to ground the AI answer...",
        )
        st.markdown(
            f'<div class="metric-text">Context Words: {count_words(context_input)}</div>',
            unsafe_allow_html=True,
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
                    st.markdown('<div class="output-header">AI Response</div>', unsafe_allow_html=True)
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))

# -----------------------------------------------------------------------------
# MODE 3: GENERATE CONTENT
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

    instructions_input = st.text_area(
        "Topic / Instructions",
        height=180,
        placeholder="Describe the content topic, target audience, key points to cover...",
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
                    st.markdown('<div class="output-header">Generated Content</div>', unsafe_allow_html=True)
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))

# -----------------------------------------------------------------------------
# MODE 4: ANALYZE TEXT
# -----------------------------------------------------------------------------
elif selected_mode == MODE_ANALYZE_TEXT:
    text_to_analyze = st.text_area(
        "Text to Analyze",
        height=220,
        placeholder="Paste document draft, proposal, email, or article snippet to analyze...",
    )

    st.markdown(
        f'<div class="metric-text">Words: {count_words(text_to_analyze)} | Characters: {count_characters(text_to_analyze)}</div>',
        unsafe_allow_html=True,
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
                    st.markdown('<div class="output-header">Structured Document Analysis</div>', unsafe_allow_html=True)
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))

# -----------------------------------------------------------------------------
# MODE 5: SMART SUGGESTIONS
# -----------------------------------------------------------------------------
elif selected_mode == MODE_SMART_SUGGESTIONS:
    suggestion_input = st.text_area(
        "Situation / Content",
        height=220,
        placeholder="Paste meeting notes, project status update, or task outline to generate recommendations...",
    )

    st.markdown(
        f'<div class="metric-text">Words: {count_words(suggestion_input)} | Characters: {count_characters(suggestion_input)}</div>',
        unsafe_allow_html=True,
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
                    st.markdown('<div class="output-header">Actionable Recommendations</div>', unsafe_allow_html=True)
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(str(e))
