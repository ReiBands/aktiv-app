"""
openai_client.py
----------------
Single responsibility: call the OpenAI API and return a plain string.
Never raises. Never crashes the app. All exceptions return a readable message.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI


def get_completion(prompt: str) -> str:
    """
    Send a prompt to gpt-4o-mini and return the response as a plain string.

    On ANY failure (auth error, timeout, rate limit, network, malformed response),
    returns a readable fallback string instead of raising an exception.
    """
    # Check for missing or empty API key before making a call
    try:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or not api_key.strip():
            return (
                "API key not configured. Add OPENAI_API_KEY to your Streamlit secrets."
            )
    except (KeyError, FileNotFoundError):
        return "API key not configured. Add OPENAI_API_KEY to your Streamlit secrets."

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()

    except Exception:
        return "Error generating response. Please try again."
