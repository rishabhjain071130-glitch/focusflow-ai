"""
AI Service Layer for FocusFlow AI.

Encapsulates all Google Gemini API interactions, client management, and error handling.
Keeps API integration isolated from Streamlit UI code.
"""

from typing import Optional
from utils.helpers import get_api_key, validate_api_key
from prompts.prompts import (
    SYSTEM_INSTRUCTION,
    build_summarize_prompt,
    build_ask_ai_prompt,
    build_generate_content_prompt,
    build_analyze_text_prompt,
    build_smart_suggestions_prompt,
)


class AIServiceException(Exception):
    """Custom exception raised when an AI service call fails."""
    pass


class AIService:
    """Service handling interactions with the Google Gemini API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AIService with a Gemini API key.
        If api_key is omitted, loads key from environment via get_api_key().
        """
        self.api_key = api_key if api_key else get_api_key()
        self.default_model = "gemini-2.5-flash"

    def _get_client(self):
        """
        Create and return an initialized Gemini API client.
        Supports official 'google-genai' SDK with fallback to 'google-generativeai'.
        """
        if not self.api_key:
            raise AIServiceException("AI Service Unavailable. Please check system configuration.")

        # Primary attempt: Official Google GenAI SDK (`google-genai`)
        try:
            from google import genai
            return ("genai", genai.Client(api_key=self.api_key))
        except ImportError:
            pass

        # Secondary attempt: Legacy Google Generative AI SDK (`google-generativeai`)
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=self.api_key)
            return ("legacy", legacy_genai)
        except ImportError:
            raise AIServiceException(
                "No Google Gemini SDK is installed. Please run: pip install google-genai"
            )

    def generate_response(self, prompt: str, system_instruction: str = SYSTEM_INSTRUCTION) -> str:
        """
        Send a prompt to the Gemini API and return the text response.

        Args:
            prompt (str): Main user prompt or constructed task text.
            system_instruction (str): System instruction guiding persona and behavior.

        Returns:
            str: Generated Markdown response text.

        Raises:
            AIServiceException: If API call fails or encounters an error.
        """
        is_valid, err_msg = validate_api_key()
        if not is_valid and not self.api_key:
            raise AIServiceException(err_msg)

        try:
            sdk_type, client = self._get_client()

            if sdk_type == "genai":
                from google.genai import types
                
                response = client.models.generate_content(
                    model=self.default_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    ),
                )
                return response.text if response.text else "No content returned from Gemini API."

            elif sdk_type == "legacy":
                model_name = "gemini-1.5-flash"
                model = client.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction
                )
                response = model.generate_content(prompt)
                return response.text if response.text else "No content returned from Gemini API."

            else:
                raise AIServiceException("Unsupported SDK configuration.")

        except AIServiceException:
            raise
        except Exception as e:
            err_str = str(e)
            if "API_KEY_INVALID" in err_str or "API key not valid" in err_str:
                raise AIServiceException("AI Service Unavailable. Authentication failed.")
            elif "RESOURCE_EXHAUSTED" in err_str or "QUOTA_EXCEEDED" in err_str or "429" in err_str:
                raise AIServiceException("AI Service rate limit or quota exceeded. Please try again shortly.")
            else:
                raise AIServiceException("AI Service Error occurred. Please try again.")

    # Mode-specific Service Methods
    def summarize(self, text: str, summary_style: str = "Bullet Points") -> str:
        """Summarize text using Gemini API."""
        prompt = build_summarize_prompt(text=text, summary_style=summary_style)
        return self.generate_response(prompt)

    def ask_ai(self, question: str, context: Optional[str] = None) -> str:
        """Answer user question with optional reference context."""
        prompt = build_ask_ai_prompt(question=question, context=context)
        return self.generate_response(prompt)

    def generate_content(
        self,
        instructions: str,
        content_type: str = "Email",
        tone: str = "Professional",
        length: str = "Medium",
    ) -> str:
        """Generate content based on instructions, content type, tone, and length."""
        prompt = build_generate_content_prompt(
            instructions=instructions,
            content_type=content_type,
            tone=tone,
            length=length,
        )
        return self.generate_response(prompt)

    def analyze_text(self, text: str, analysis_type: str = "Comprehensive Analysis") -> str:
        """Analyze text structure, tone, readability, or key themes."""
        prompt = build_analyze_text_prompt(text=text, analysis_type=analysis_type)
        return self.generate_response(prompt)

    def suggest_improvements(self, text: str, focus_area: str = "Actionable Next Steps") -> str:
        """Generate smart productivity suggestions for input text."""
        prompt = build_smart_suggestions_prompt(text=text, focus_area=focus_area)
        return self.generate_response(prompt)
