"""
Prompt templates for FocusFlow AI productivity capabilities.

This module isolates all prompt engineering and system instructions from UI and service logic.
"""

from typing import Optional


# Capability Identifiers
MODE_SUMMARIZE = "Summarize"
MODE_ASK_AI = "Ask AI"
MODE_GENERATE_CONTENT = "Generate Content"
MODE_ANALYZE_TEXT = "Analyze Text"
MODE_SMART_SUGGESTIONS = "Smart Suggestions"

SYSTEM_INSTRUCTION = """You are FocusFlow AI, an intelligent, highly structured productivity assistant.
Your goal is to help users work with text, documents, questions, and content efficiently.
Always deliver well-formatted, professional, clear Markdown output without fluff.
Use headings, bullet points, bold text, and numbered lists where appropriate for readability.
"""


def build_summarize_prompt(text: str, summary_style: str = "Bullet Points") -> str:
    """Build prompt for Text Summarization mode."""
    style_guidance = {
        "Bullet Points": "Provide 3-5 high-impact bullet points highlighting the core messages.",
        "Executive Summary": "Write a formal 2-paragraph Executive Summary tailored for quick reading.",
        "Key Takeaways": "List the key takeaways grouped into main themes with bold headings.",
        "Short Paragraph": "Provide a clean, concise paragraph summary in 3-4 sentences.",
    }.get(summary_style, "Provide a clear and concise summary.")

    return f"""Task: Summarize the following text.

Summary Style: {summary_style}
Guidance: {style_guidance}

--- TEXT TO SUMMARIZE ---
{text}
------------------------

Format the output clearly using Markdown.
"""


def build_ask_ai_prompt(question: str, context: Optional[str] = None) -> str:
    """Build prompt for Question Answering mode."""
    context_block = (
        f"--- REFERENCE CONTEXT ---\n{context}\n------------------------\n"
        if context and context.strip()
        else ""
    )

    return f"""Task: Answer the user's question accurately, directly, and comprehensively.

{context_block}
Question: {question}

Provide a direct answer first, followed by key explanations or supporting details if needed. Use clear formatting.
"""


def build_generate_content_prompt(
    instructions: str, content_type: str = "Email", tone: str = "Professional"
) -> str:
    """Build prompt for Content Generation mode."""
    return f"""Task: Generate {content_type} content.

Tone: {tone}
Instructions/Topic: {instructions}

Generate a complete, high-quality draft for the specified content type. Include appropriate headings, subject lines (if applicable), and structure.
"""


def build_analyze_text_prompt(text: str, analysis_type: str = "Comprehensive Analysis") -> str:
    """Build prompt for Text/Document Analysis mode."""
    type_guidance = {
        "Comprehensive Analysis": "Analyze key themes, tone, readability, structural strengths, and areas for improvement.",
        "Tone & Sentiment": "Identify the primary tone, underlying sentiment, language formality, and emotional nuance.",
        "Readability & Clarity": "Evaluate reading level, sentence structure, clarity, and suggest specific edits for better flow.",
        "Key Entities & Themes": "Extract core entities, key topics, primary arguments, and essential terms.",
    }.get(analysis_type, "Analyze the text thoroughly.")

    return f"""Task: Perform text analysis.

Analysis Type: {analysis_type}
Focus: {type_guidance}

--- TEXT TO ANALYZE ---
{text}
----------------------

Present your analysis in structured Markdown sections with clear headers and actionable insights.
"""


def build_smart_suggestions_prompt(text: str, focus_area: str = "Actionable Next Steps") -> str:
    """Build prompt for Intelligent Suggestions mode."""
    focus_guidance = {
        "Actionable Next Steps": "Provide a prioritized list of clear, actionable next steps based on the provided text.",
        "Work Breakdown Structure": "Break down the content into logical sub-tasks with estimated priority (High/Medium/Low).",
        "Follow-up Questions": "Generate insightful follow-up questions to identify risks, missing details, or strategic alignment.",
        "Priority Recommendations": "Provide top strategic recommendations to optimize efficiency and impact.",
    }.get(focus_area, "Provide practical and intelligent suggestions.")

    return f"""Task: Generate intelligent productivity suggestions.

Focus Area: {focus_area}
Guidance: {focus_guidance}

--- SOURCE TEXT/CONTEXT ---
{text}
---------------------------

Format the recommendations as actionable, structured bullet points with brief rationales.
"""
