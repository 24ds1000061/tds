# Semantic Search with Re-ranking API

This project implements a two-stage semantic search pipeline for legal documents using FastAPI. 

- **Stage 1**: Fast vector retrieval using cosine similarity and local embeddings.
- **Stage 2**: Re-ranking for improved precision using semantic relevance logic.

## Prerequisites

- Python 3.8+
- [ngrok](https://ngrok.com/) (installed and authenticated)

## Setup Instructions

### 1. Create Project Directory
```bash
mkdir -p ~/tds/ga-1/q18_semantic_search
cd ~/tds/ga-1/q18_semantic_search
```

### 2. Setup Virtual Environment
Create and activate a Python virtual environment to manage dependencies locally.

**On Linux/WSL/Ubuntu:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install fastapi uvicorn sentence-transformers numpy
```
*(Note: If torch dependencies take too long to download, the script has a built-in fallback to mock embeddings for testing the API logic.)*

### 4. Start the Application
Run the FastAPI server on port 5000:
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 5000
```

### 5. Expose with Ngrok
In a **new terminal tab**, expose the local server to the internet using your persistent ngrok URL:
```bash
ngrok http 5000 --url=choleric-zana-dentally.ngrok-free.dev
```

## Testing the API
You can test the search endpoint using `curl`:

```bash
curl -X POST "https://choleric-zana-dentally.ngrok-free.dev/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "climate change", "k": 12, "rerank": true, "rerankK": 7}'
```

## Response Format
The API returns results with the following structure:
- `results`: List of objects containing `id`, `score`, `content`, and `metadata`.
- `reranked`: Boolean indicating if re-ranking was applied.
- `metrics`: Latency and total document count.
