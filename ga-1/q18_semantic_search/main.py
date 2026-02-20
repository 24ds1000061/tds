from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time
import numpy as np

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dummy Data Generation ---
def generate_docs():
    base_docs = [
        "The Vendor shall not be liable for any indirect, incidental, or consequential damages.",
        "The Client agrees to indemnify and hold harmless the Service Provider from any claims arising out of the use of the Services.",
        "This Agreement shall be governed by and construed in accordance with the laws of the State of New York.",
        "The term of this Agreement shall commence on the Effective Date and continue for a period of one (1) year.",
        "Either party may terminate this Agreement upon written notice if the other party breaches any material term.",
        "Confidential Information shall not include information that is or becomes publicly available.",
        "The Provider warrants that the Services will be performed in a professional manner.",
        "Payment terms are Net 30 days from the date of invoice.",
        "All intellectual property rights arising out of the Services shall vest in the Client.",
        "Force Majeure: Neither party shall be liable for any failure to perform due to causes beyond its reasonable control.",
        "Environmental impacts and climate change risks must be disclosed in the annual report.",
        "The parties agree to implement carbon reduction strategies to mitigate climate change effects.",
        "Sustainable energy initiatives are critical for long-term contract performance and environmental compliance."
    ]
    docs = []
    for i in range(64):
        # Create variations
        base_text = base_docs[i % len(base_docs)]
        docs.append({
            "id": i,
            "content": f"Document {i}: {base_text} (Variation {i})",
            "metadata": {"source": f"contract_{i}.pdf"}
        })
    return docs

documents = generate_docs()

# --- Semantic Search Setup ---
try:
    from sentence_transformers import SentenceTransformer
    print("Loading model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Computing embeddings...")
    doc_contents = [doc['content'] for doc in documents]
    doc_embeddings = model.encode(doc_contents)
except ImportError:
    print("SentenceTransformers not found. Using mock embeddings.")
    # Mock embeddings: random vectors
    model = None
    doc_embeddings = np.random.rand(len(documents), 384).astype('float32')

# --- Re-ranking Simulation ---
def simulated_rerank(query: str, candidates: List[dict], k: int) -> List[dict]:
    reranked_candidates = []
    for doc in candidates:
        original_score = doc['score']
        # Simple boost logic for semantic relevance
        boost = 0.0
        if "climate" in query.lower() and "climate" in doc['content'].lower():
            boost = 0.2
        elif "liability" in query.lower() and "liability" in doc['content'].lower():
            boost = 0.1
        
        new_score = min(0.99, original_score + boost)
        reranked_candidates.append({
            "id": doc['id'],
            "score": round(new_score, 2),
            "content": doc['content'],
            "metadata": doc['metadata']
        })
    
    # Sort by new score descending
    reranked_candidates.sort(key=lambda x: x['score'], reverse=True)
    return reranked_candidates[:k]

# --- API Models ---
class SearchRequest(BaseModel):
    query: str
    k: int = 6
    rerank: bool = False
    rerankK: int = 4

class SearchResult(BaseModel):
    id: int
    score: float
    content: str
    metadata: dict

class SearchResponse(BaseModel):
    results: List[SearchResult]
    reranked: bool
    metrics: dict

# --- Endpoints ---
@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    start_time = time.time()
    
    # 1. Component Query Embedding
    if model:
        query_embedding = model.encode(request.query)
    else:
        # Mock query embedding
        query_embedding = np.random.rand(384).astype('float32')

    # 2. Vector Similarity (Cosine)
    scores = np.dot(doc_embeddings, query_embedding)
    
    # Normalize scores to 0-1
    # Since it's a demo, we'll just clip and shift for visual sanity
    norm_scores = (scores - np.min(scores)) / (np.max(scores) - np.min(scores) + 1e-6)
    
    # Get top K candidates
    top_k_indices = np.argsort(norm_scores)[::-1][:request.k]
    
    initial_results = []
    for idx in top_k_indices:
        initial_results.append({
            "id": documents[idx]['id'],
            "score": float(round(norm_scores[idx], 2)),
            "content": documents[idx]['content'],
            "metadata": documents[idx]['metadata']
        })
    
    # 3. Re-ranking
    final_results = initial_results
    if request.rerank:
        final_results = simulated_rerank(request.query, initial_results, request.rerankK)
    
    latency_ms = int((time.time() - start_time) * 1000)
    
    return {
        "results": final_results,
        "reranked": request.rerank,
        "metrics": {
            "latency": latency_ms,
            "totalDocs": len(documents)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
