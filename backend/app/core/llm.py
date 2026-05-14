import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
from app.core import quota_manager

def get_client():
    """Returns a lazily-initialized OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def call_llm(prompt: str, json_mode: bool = False):
    """
    Unified LLM wrapper for DevForge AI Agents.
    """
    if not quota_manager.is_within_quota():
        print("[QUOTA] Daily budget exceeded. Throttling request.")
        return "{}" if json_mode else "Quota exceeded."

    # Record estimated cost
    quota_manager.record_request(0.01) # Mock $0.01 per call
    client = get_client()
    if not client:
        return "Error: OPENAI_API_KEY not set. Please configure your environment."
    response_format = {"type": "json_object"} if json_mode else None
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior open-source architect and product manager for DevForge AI."},
            {"role": "user", "content": prompt}
        ],
        response_format=response_format
    )

    return response.choices[0].message.content
