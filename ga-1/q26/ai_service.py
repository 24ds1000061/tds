from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('AIPIPE_TOKEN') or os.getenv('AIPROXY_TOKEN'),
            base_url=os.getenv('AIPIPE_BASE_URL') or "https://aipipe.org/openai/v1"
        )

    def query(self, text: str) -> str:
        """Calls GPT-4o-mini for code review analysis"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful code review assistant."},
                    {"role": "user", "content": text}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM error: {e}")
            return f"Error: Could not process request. {str(e)}"

ai_service = AIService()
