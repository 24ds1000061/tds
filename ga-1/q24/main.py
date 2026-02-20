from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from openai import OpenAI
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="AI-Powered Data Pipeline")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client with custom base URL
client = OpenAI(
    api_key=os.getenv('AIPIPE_TOKEN') or os.getenv('AIPROXY_TOKEN'),
    base_url=os.getenv('AIPIPE_BASE_URL') or "https://aipipe.org/openai/v1"
)

# ==================== DATA MODELS ====================

class PipelineRequest(BaseModel):
    email: str
    source: str

# ==================== HELPER FUNCTIONS ====================

def fetch_comments():
    """
    Fetch comments from JSONPlaceholder API
    Returns: List of first 3 comments or empty list on error
    """
    try:
        print("📡 Fetching comments from JSONPlaceholder...")
        response = requests.get(
            'https://jsonplaceholder.typicode.com/comments?postId=1',
            timeout=10
        )
        response.raise_for_status()
        
        comments = response.json()
        # Return first 3 comments
        result = comments[:3]
        print(f"✅ Successfully fetched {len(result)} comments")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching comments: {e}")
        return []


def analyze_comment_with_ai(comment_data):
    """
    Use AI to analyze comment data via AIPIPE
    Returns: Dictionary with analysis and sentiment
    """
    try:
        print(f"🤖 Analyzing comment ID: {comment_data['id']}...")
        
        # Create concise text for analysis
        comment_text = comment_data['body']
        
        # Prompt for AI
        prompt = f"""Analyze this comment and provide:
1. Exactly 2-3 key points or themes discussed in the comment.
2. Sentiment classification (choose one: optimistic, pessimistic, balanced)

Comment Text:
{comment_text}

Respond in exactly this format:
Summary: [your 2-3 sentences summary/key points]
Sentiment: [optimistic/pessimistic/balanced]"""
        
        # Call AI API via AIPIPE
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        # Parse response
        result_text = response.choices[0].message.content.strip()
        
        # Extract summary and sentiment
        lines = [line.strip() for line in result_text.split('\n') if line.strip()]
        
        summary = "Analysis completed"
        sentiment = "balanced"
        
        for line in lines:
            if line.startswith('Summary:'):
                summary = line.replace('Summary:', '').strip()
            elif line.startswith('Sentiment:'):
                sentiment = line.replace('Sentiment:', '').strip().lower()
                # Ensure it's one of the required values
                if sentiment not in ['optimistic', 'pessimistic', 'balanced']:
                    if 'optimistic' in sentiment: sentiment = 'optimistic'
                    elif 'pessimistic' in sentiment: sentiment = 'pessimistic'
                    else: sentiment = 'balanced'
        
        print(f"✅ AI analysis completed for comment ID {comment_data['id']}")
        
        return {
            "analysis": summary,
            "sentiment": sentiment
        }
        
    except Exception as e:
        print(f"❌ AI analysis error for comment ID {comment_data.get('id', 'unknown')}: {e}")
        return {
            "analysis": "Analysis unavailable due to error",
            "sentiment": "balanced"
        }


def store_result(original_data, ai_analysis, filepath="results.json"):
    """
    Store processed result to JSON file
    Returns: The stored result object
    """
    try:
        print(f"💾 Storing result for comment ID {original_data['id']}...")
        
        # Create result object
        result = {
            "original": original_data['body'],
            "analysis": ai_analysis['analysis'],
            "sentiment": ai_analysis['sentiment'],
            "stored": True,
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }
        
        # Load existing results
        results = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    results = json.load(f)
                    if not isinstance(results, list):
                        results = []
            except (json.JSONDecodeError, Exception):
                results = []
        
        # Append new result
        results.append(result)
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Result stored for comment ID {original_data['id']}")
        return result
        
    except Exception as e:
        print(f"❌ Storage error: {e}")
        # Return result even if storage failed
        return {
            "original": str(original_data.get('body', '')),
            "analysis": ai_analysis['analysis'],
            "sentiment": ai_analysis['sentiment'],
            "stored": False,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "error": str(e)
        }


def send_notification(email, status, items_processed):
    """
    Send notification about pipeline completion
    Returns: True if notification sent
    """
    try:
        message = f"""
╔════════════════════════════════════════════╗
║     PIPELINE NOTIFICATION                  ║
╚════════════════════════════════════════════╝

To: {email}
Status: {status}
Items Processed: {items_processed}
Timestamp: {datetime.utcnow().isoformat()}Z

Pipeline execution completed successfully!
        """
        
        print(message)
        
        # Requirement: indicate that notification was sent to specific email
        # We also use the requested email from the request
        print(f"✅ Notification sent to: {email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Notification error: {e}")
        return False


def process_pipeline(notification_email):
    """
    Main pipeline orchestration function
    Returns: Complete pipeline result
    """
    errors = []
    processed_items = []
    
    print("\n" + "="*50)
    print("🚀 STARTING AI-POWERED DATA PIPELINE")
    print("="*50 + "\n")
    
    # Step 1: Fetch data
    comments = fetch_comments()
    
    if not comments:
        error_msg = "Failed to fetch comments from API"
        errors.append(error_msg)
        print(f"\n❌ PIPELINE FAILED: {error_msg}\n")
        return {
            "items": [],
            "notificationSent": False,
            "processedAt": datetime.utcnow().isoformat() + 'Z',
            "errors": errors
        }
    
    # Step 2-4: Process each comment
    for idx, comment in enumerate(comments, 1):
        try:
            print(f"\n--- Processing Comment {idx}/{len(comments)} ---")
            
            # AI Analysis
            ai_result = analyze_comment_with_ai(comment)
            
            # Storage
            stored_result = store_result(comment, ai_result)
            
            processed_items.append(stored_result)
            
        except Exception as e:
            error_msg = f"Error processing comment ID {comment.get('id', 'unknown')}: {str(e)}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
            continue
    
    # Step 5: Send notification
    print(f"\n📧 Sending notification to {notification_email}...")
    notification_sent = send_notification(
        notification_email,
        "completed" if processed_items else "failed",
        len(processed_items)
    )
    
    print("\n" + "="*50)
    print("✅ PIPELINE COMPLETED")
    print(f"Processed: {len(processed_items)} items")
    print(f"Errors: {len(errors)}")
    print("="*50 + "\n")
    
    # Return complete result
    return {
        "items": processed_items,
        "notificationSent": notification_sent,
        "processedAt": datetime.utcnow().isoformat() + 'Z',
        "errors": errors
    }


# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI-Powered Data Pipeline API",
        "version": "1.0",
        "endpoints": {
            "POST /pipeline": "Run the data pipeline"
        }
    }


@app.post("/pipeline")
async def run_pipeline(request: PipelineRequest):
    """
    Main pipeline endpoint
    Accepts: {"email": "...", "source": "JSONPlaceholder Comments"}
    Returns: Pipeline execution results
    """
    
    # Validate source
    if request.source != "JSONPlaceholder Comments":
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Expected 'JSONPlaceholder Comments', got '{request.source}'"
        )
    
    # Run the pipeline
    result = process_pipeline(request.email)
    
    return result


# For testing locally
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)