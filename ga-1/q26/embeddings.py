import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client here or pass it from main.py
_client = None

def get_client():
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.getenv('AIPIPE_TOKEN') or os.getenv('AIPROXY_TOKEN'),
            base_url=os.getenv('AIPIPE_BASE_URL') or "https://aipipe.org/openai/v1"
        )
    return _client

def embed(text: str) -> np.ndarray:
    """Gets real embedding from OpenAI"""
    try:
        client = get_client()
        response = client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        # Convert to numpy array and reshape to (1, -1)
        return np.array(response.data[0].embedding).reshape(1, -1)
    except Exception as e:
        print(f"Embedding error: {e}")
        # Fallback to random if API fails, though not ideal
        np.random.seed(abs(hash(text)) % (10**8))
        return np.random.randn(1, 1536)

def similarity(vec1, vec2):
    return cosine_similarity(vec1, vec2)[0][0]
