"""
Prompt templates for FocusFlow AI productivity capabilities.

This module isolates all prompt engineering, system instructions, and input delimiting from UI and service logic.
"""

from typing import Optional


# Capability Identifiers
MODE_SUMMARIZE = "Summarize"
MODE_ASK_AI = "Ask AI"
MODE_GENERATE_CONTENT = "Generate Content"
MODE_ANALYZE_TEXT = "Analyze Text"
MODE_SMART_SUGGESTIONS = "Smart Suggestions"

SYSTEM_INSTRUCTION = """You are FocusFlow AI, an intelligent, highly structured productivity assistant.
Your goal is to help users work with text, documents, questions, and content creation efficiently.
Always deliver well-formatted, professional, clear Markdown output without unnecessary fluff or conversational filler.
Use headings, bold key terms, bullet points, and numbered lists for optimal readability.
Do not invent unverified facts, and clearly state any limitations when context is insufficient.
"""


def build_summarize_prompt(text: str, summary_style: str = "Bullet Points") -> str:
    """
    Build prompt for Text Summarization mode.
    
    Supported styles:
    - Bullet Points: 3-5 concise, high-impact bullet points highlighting core messages.
    - Concise Summary: A single focused, well-written paragraph (3-4 sentences).
    - Executive Summary: A formal multi-paragraph overview with key findings and conclusion.
    """
    style_guidance = {
        "Bullet Points": (
            "Summarize the text into 3-5 concise, high-impact bullet points. "
            "Highlight the most critical insights using bold text for key terms."
        ),
        "Concise Summary": (
            "Provide a single focused, high-density paragraph summary (3-4 sentences). "
            "Capture the main point and immediate takeaways without filler."
        ),
        "Executive Summary": (
            "Write a formal Executive Summary. Include an Overview section, "
            "a Key Findings section with bullet points, and a Strategic Conclusion."
        ),
    }.get(
        summary_style,
        "Provide a clear, accurate, and structured summary of the text."
    )

    return f"""Task: Summarize the user-provided text.

Target Summary Style: {summary_style}
Instructions: {style_guidance}

<<<USER_TEXT>>>
{text}
<<<END_USER_TEXT>>>

Formatting Guidelines:
- Respond in clean Markdown.
- Keep the summary focused directly on the provided text.
"""


def build_ask_ai_prompt(question: str, context: Optional[str] = None) -> str:
    """
    Build prompt for Question Answering mode.
    
    Guidelines:
    - Directly answer the question first.
    - Provide concise supporting explanations if useful.
    - Avoid pretending to know unavailable information; state uncertainty clearly.
    """
    context_block = ""
    if context and context.strip():
        context_block = f"""<<<REFERENCE_CONTEXT>>>
{context.strip()}
<<<END_REFERENCE_CONTEXT>>>
"""

    return f"""Task: Answer the user's question accurately and directly.

{context_block}
<<<USER_QUESTION>>>
{question}
<<<END_USER_QUESTION>>>

Answering Guidelines:
1. Provide a direct, clear answer in the opening paragraph.
2. If context is provided, ground your answer primarily in that context.
3. If the context does not contain enough information to fully answer, explicitly state what is missing rather than guessing.
4. Use Markdown formatting (headings, bullet points, code blocks) where helpful.
"""


def build_generate_content_prompt(
    instructions: str,
    content_type: str = "Email",
    tone: str = "Professional",
    length: str = "Medium",
) -> str:
    """
    Build prompt for Content Generation mode.
    
    Supported Content Types:
    - Email
    - Study Notes
    - Blog Outline
    - Social Media Post
    - Professional Description
    """
    length_guidance = {
        "Short": "Keep the content brief and concise (approx. 100-150 words).",
        "Medium": "Provide a well-developed draft (approx. 250-400 words).",
        "Detailed": "Provide a comprehensive, highly thorough document (approx. 500+ words).",
    }.get(length, "Provide a standard length draft.")

    return f"""Task: Generate structured content based on user instructions.

Target Content Type: {content_type}
Desired Tone: {tone}
Target Length: {length} ({length_guidance})

<<<CONTENT_INSTRUCTIONS>>>
{instructions}
<<<END_CONTENT_INSTRUCTIONS>>>

Generation Rules:
- Include appropriate structural elements (e.g., Subject line for Email, Section headers for Study Notes / Blog Outlines, Hashtags for Social Media Posts).
- Adhere strictly to the requested tone ({tone}) and length ({length}).
- Output ready-to-use, polished Markdown text.
"""


def build_analyze_text_prompt(text: str, analysis_type: str = "Comprehensive Analysis") -> str:
    """
    Build prompt for Text & Document Analysis mode.
    
    Output strictly includes:
    1. Main Topic
    2. Key Points
    3. Important Observations
    4. Strengths or Positive Aspects
    5. Areas for Improvement
    6. Overall Assessment
    """
    return f"""Task: Perform a structured analysis of the provided text.

Analysis Focus: {analysis_type}

<<<TEXT_TO_ANALYZE>>>
{text}
<<<END_TEXT_TO_ANALYZE>>>

Required Output Structure:
Provide your analysis using the exact Markdown headers below:

### 📌 Main Topic
(Identify the primary topic and core intent of the text in 1-2 sentences.)

### 🔑 Key Points
(List 3-5 main arguments, assertions, or central ideas as bullet points.)

### 🔍 Important Observations
(Highlight notable structural patterns, tone nuances, or implicit assumptions.)

### 💪 Strengths & Positive Aspects
(Point out effective phrasing, clarity, or strong logical elements.)

### 🛠️ Areas for Improvement
(Provide constructive feedback on readability, word choice, organization, or missing context.)

### 📊 Overall Assessment
(Summarize the quality, impact, and effectiveness of the text in a short concluding paragraph.)
"""


def build_smart_suggestions_prompt(text: str, focus_area: str = "Actionable Next Steps") -> str:
    """
    Build prompt for Intelligent Suggestions mode.
    
    Generates actionable, relevant, concise, and clearly categorized recommendations.
    """
    focus_guidance = {
        "Actionable Next Steps": "Focus on immediate, concrete tasks that should be executed next.",
        "Work Breakdown Structure": "Break the input down into logical task modules with priority markers (High/Medium/Low).",
        "Follow-up Questions": "List strategic follow-up questions to uncover risks, missing specs, or dependencies.",
        "Priority Recommendations": "Provide strategic top recommendations to maximize productivity and outcome quality.",
    }.get(focus_area, "Provide practical and actionable recommendations.")

    return f"""Task: Generate intelligent, actionable productivity suggestions based on user context.

Focus Area: {focus_area}
Guidance: {focus_guidance}

<<<USER_CONTEXT>>>
{text}
<<<END_USER_CONTEXT>>>

Output Requirements:
- Structure recommendations into clear, distinct sections:
  - ### ⚡ Immediate Action Items
  - ### 🎯 Strategic Recommendations
  - ### ❓ Key Follow-up Questions / Risks to Address
- Format each recommendation as a concise bullet point starting with a bold action verb.
- Keep suggestions realistic, specific, and directly relevant to the user context.
"""
