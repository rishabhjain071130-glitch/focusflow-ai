"""
Utility helper functions for FocusFlow AI.

Includes environment configuration, API key verification, and text utilities.
"""

import os
from typing import Tuple
from dotenv import load_dotenv


def load_environment() -> None:
    """Load environment variables from .env file if available."""
    load_dotenv()


def get_api_key() -> str:
    """Retrieve Gemini API key from environment variables."""
    load_environment()
    return os.getenv("GEMINI_API_KEY", "").strip()


def validate_api_key() -> Tuple[bool, str]:
    """
    Check if GEMINI_API_KEY is configured in environment.
    
    Returns:
        Tuple[bool, str]: (is_valid, status_message)
    """
    api_key = get_api_key()
    if not api_key:
        return False, "AI Service Unavailable"
    if api_key == "your_gemini_api_key_here":
        return False, "AI Service Unavailable"
    return True, "AI Connected"


def count_words(text: str) -> int:
    """Count words in a string."""
    if not text:
        return 0
    return len(text.strip().split())


def count_characters(text: str) -> int:
    """Count characters in a string."""
    if not text:
        return 0
    return len(text)


def truncate_preview(text: str, max_chars: int = 100) -> str:
    """Return a short preview snippet of text."""
    if not text:
        return ""
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars] + "..."
