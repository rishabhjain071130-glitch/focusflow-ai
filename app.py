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
# Custom Styling (Vanilla CSS for Premium Dark Mode Aesthetic)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Gradient Header & Typography */
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 1.8rem;
    }
    
    /* Sidebar styling */
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
    }
    .status-badge-ok {
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .status-badge-err {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }

    /* Output Card Container */
    .output-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    /* Counter Badge */
    .metric-badge {
        font-size: 0.82rem;
        color: #64748B;
        text-align: right;
        margin-top: -0.8rem;
        margin-bottom: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Sidebar Navigation & Status
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/flash-on.png", width=64)
    st.markdown('<div class="sidebar-title">FocusFlow AI</div>', unsafe_allow_html=True)
    st.caption("AI-Powered Productivity Assistant")

    st.divider()

    # API Key Configuration Status
    is_api_valid, api_status_msg = validate_api_key()
    if is_api_valid:
        st.markdown(
            '<div class="status-badge-ok">🟢 API Key: Active</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-badge-err">🔴 API Key: Action Required</div>',
            unsafe_allow_html=True,
        )
        st.warning(api_status_msg)

    st.divider()

    # Capability Selection
    st.subheader("Productivity Modes")
    selected_mode = st.radio(
        "Choose Mode:",
        options=[
            MODE_SUMMARIZE,
            MODE_ASK_AI,
            MODE_GENERATE_CONTENT,
            MODE_ANALYZE_TEXT,
            MODE_SMART_SUGGESTIONS,
        ],
        index=0,
        help="Select an AI capability to optimize your workflow.",
    )

    st.divider()
    st.info("💡 **Tip**: Configure your `GEMINI_API_KEY` in the `.env` file to enable live AI responses.")


# -----------------------------------------------------------------------------
# Main Application Content Area
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">FocusFlow AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Streamline your workflow with AI-powered summarization, Q&A, content creation, text analysis, and smart suggestions.</div>',
    unsafe_allow_html=True,
)

# Initialize AI Service Layer
ai_service = AIService()

# -----------------------------------------------------------------------------
# MODE 1: SUMMARIZE
# -----------------------------------------------------------------------------
if selected_mode == MODE_SUMMARIZE:
    st.header("📝 Text Summarization")
    st.write("Extract core ideas, key bullet points, or executive summaries from lengthy documents.")

    col1, col2 = st.columns([3, 1])
    with col2:
        summary_style = st.selectbox(
            "Summary Style",
            options=["Bullet Points", "Executive Summary", "Key Takeaways", "Short Paragraph"],
            index=0,
        )

    with col1:
        text_input = st.text_area(
            "Input Text to Summarize:",
            height=250,
            placeholder="Paste your article, meeting notes, report, or essay here...",
        )
        st.markdown(
            f'<div class="metric-badge">Words: {count_words(text_input)} | Characters: {count_characters(text_input)}</div>',
            unsafe_allow_html=True,
        )

    if st.button("✨ Summarize Text", type="primary", use_container_width=True):
        if not text_input.strip():
            st.warning("Please provide input text to summarize.")
        else:
            with st.spinner("Analyzing text and generating summary..."):
                try:
                    result = ai_service.summarize(text=text_input, summary_style=summary_style)
                    st.success("Summary Generated!")
                    st.markdown("### Summary Output")
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(f"Error: {e}")

# -----------------------------------------------------------------------------
# MODE 2: ASK AI
# -----------------------------------------------------------------------------
elif selected_mode == MODE_ASK_AI:
    st.header("❓ Question Answering")
    st.write("Ask questions directly or provide context text for precise answers.")

    question_input = st.text_input(
        "Your Question:",
        placeholder="What are the key differences between synchronous and asynchronous execution?",
    )

    with st.expander("📌 Optional Reference Context (Paste document/code here)", expanded=False):
        context_input = st.text_area(
            "Reference Context:",
            height=180,
            placeholder="Paste background text, document excerpt, or code snippet to ground the AI's answer...",
        )
        st.markdown(
            f'<div class="metric-badge">Context Words: {count_words(context_input)}</div>',
            unsafe_allow_html=True,
        )

    if st.button("🚀 Ask AI", type="primary", use_container_width=True):
        if not question_input.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Finding answer..."):
                try:
                    result = ai_service.ask_ai(
                        question=question_input, context=context_input
                    )
                    st.success("Answer Ready!")
                    st.markdown("### Response")
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(f"Error: {e}")

# -----------------------------------------------------------------------------
# MODE 3: GENERATE CONTENT
# -----------------------------------------------------------------------------
elif selected_mode == MODE_GENERATE_CONTENT:
    st.header("✍️ Content Generation")
    st.write("Draft professional emails, blog posts, outlines, study guides, and reports.")

    col1, col2 = st.columns([1, 1])
    with col1:
        content_type = st.selectbox(
            "Content Type",
            options=["Email", "Blog Post", "Executive Brief", "Study Guide", "Task Outline"],
            index=0,
        )
    with col2:
        tone = st.selectbox(
            "Tone & Style",
            options=["Professional", "Casual", "Academic", "Concise", "Persuasive"],
            index=0,
        )

    instructions_input = st.text_area(
        "Topic / Instructions:",
        height=200,
        placeholder="e.g., Write a project launch announcement email to stakeholders highlighting key features and launch date...",
    )

    if st.button("🎨 Generate Content", type="primary", use_container_width=True):
        if not instructions_input.strip():
            st.warning("Please enter topic or instructions for content generation.")
        else:
            with st.spinner("Generating draft content..."):
                try:
                    result = ai_service.generate_content(
                        instructions=instructions_input,
                        content_type=content_type,
                        tone=tone,
                    )
                    st.success("Draft Generated!")
                    st.markdown("### Generated Content")
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(f"Error: {e}")

# -----------------------------------------------------------------------------
# MODE 4: ANALYZE TEXT
# -----------------------------------------------------------------------------
elif selected_mode == MODE_ANALYZE_TEXT:
    st.header("🔍 Text & Document Analysis")
    st.write("Analyze text structure, tone, readability, sentiment, or key entities.")

    col1, col2 = st.columns([3, 1])
    with col2:
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

    with col1:
        text_to_analyze = st.text_area(
            "Text to Analyze:",
            height=250,
            placeholder="Paste your draft, communication, or document to analyze...",
        )
        st.markdown(
            f'<div class="metric-badge">Words: {count_words(text_to_analyze)}</div>',
            unsafe_allow_html=True,
        )

    if st.button("🔬 Analyze Text", type="primary", use_container_width=True):
        if not text_to_analyze.strip():
            st.warning("Please provide text to analyze.")
        else:
            with st.spinner("Analyzing text structure and tone..."):
                try:
                    result = ai_service.analyze_text(
                        text=text_to_analyze, analysis_type=analysis_type
                    )
                    st.success("Analysis Complete!")
                    st.markdown("### Insights & Breakdown")
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(f"Error: {e}")

# -----------------------------------------------------------------------------
# MODE 5: SMART SUGGESTIONS
# -----------------------------------------------------------------------------
elif selected_mode == MODE_SMART_SUGGESTIONS:
    st.header("💡 Smart Productivity Suggestions")
    st.write("Get actionable next steps, work breakdown structures, or follow-up recommendations.")

    col1, col2 = st.columns([3, 1])
    with col2:
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

    with col1:
        suggestion_input = st.text_area(
            "Project Context / Meeting Notes / Goals:",
            height=250,
            placeholder="Paste raw notes, project brief, or email thread to turn into structured next steps...",
        )
        st.markdown(
            f'<div class="metric-badge">Words: {count_words(suggestion_input)}</div>',
            unsafe_allow_html=True,
        )

    if st.button("⚡ Get Suggestions", type="primary", use_container_width=True):
        if not suggestion_input.strip():
            st.warning("Please provide context or text to generate suggestions.")
        else:
            with st.spinner("Formulating intelligent recommendations..."):
                try:
                    result = ai_service.suggest_improvements(
                        text=suggestion_input, focus_area=focus_area
                    )
                    st.success("Suggestions Ready!")
                    st.markdown("### Intelligent Recommendations")
                    st.markdown(result)
                except AIServiceException as e:
                    st.error(f"Error: {e}")
