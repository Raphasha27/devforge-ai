"""
Zero-Cost Bootstrap Engine
Automatically falls back to free-tier APIs (Groq / HuggingFace) when premium capital (OpenAI) is unavailable.
"""
import os
import requests
import logging

logger = logging.getLogger(__name__)

class ZeroCostEngine:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        
    def generate_code(self, prompt: str) -> str:
        """Attempts to generate code using completely free tiers."""
        if self.groq_api_key:
            return self._call_groq(prompt)
        elif self.hf_api_key:
            return self._call_huggingface(prompt)
        else:
            return "# SYSTEM STANDBY: Awaiting FREE Groq API key in .env file to begin zero-cost operations."
            
    def _call_groq(self, prompt: str) -> str:
        logger.info("[*] Utilizing Zero-Cost Architecture: Groq API")
        try:
            # We use Llama 3 8B or 70B which are blazing fast and free on Groq
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.groq_api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}]
            }
            res = requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
            else:
                return f"# Groq API Error: {res.status_code}"
        except Exception as e:
            return f"# Exception using Groq: {e}"

    def _call_huggingface(self, prompt: str) -> str:
        logger.info("[*] Utilizing Zero-Cost Architecture: HuggingFace Inference API")
        try:
            url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
            headers = {"Authorization": f"Bearer {self.hf_api_key}", "Content-Type": "application/json"}
            payload = {"inputs": prompt}
            res = requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                return res.json()[0]["generated_text"]
            else:
                return f"# HuggingFace API Error: {res.status_code}"
        except Exception as e:
            return f"# Exception using HuggingFace: {e}"

zero_cost_llm = ZeroCostEngine()
