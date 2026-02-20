import requests
import json
import time

BASE_URL = "http://localhost:8081"

def test_caching():
    print("Testing Caching System...")
    
    # 1. First Request (Miss)
    print("\n--- Request 1: Original ---")
    payload = {"query": "Explain how a binary search tree works.", "application": "code review assistant"}
    r1 = requests.post(f"{BASE_URL}/", json=payload)
    print(r1.json())
    
    # 2. Second Request (Exact Hit)
    print("\n--- Request 2: Exact Match ---")
    r2 = requests.post(f"{BASE_URL}/", json=payload)
    print(r2.json())
    
    # 3. Third Request (Semantic Hit)
    print("\n--- Request 3: Semantic Match ---")
    payload_similar = {"query": "How does a BST work?", "application": "code review assistant"}
    r3 = requests.post(f"{BASE_URL}/", json=payload_similar)
    print(r3.json())
    
    # 4. Check Analytics
    print("\n--- Analytics ---")
    r_analytics = requests.get(f"{BASE_URL}/analytics")
    print(json.dumps(r_analytics.json(), indent=2))

if __name__ == "__main__":
    test_caching()
