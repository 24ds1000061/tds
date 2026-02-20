import requests
import time

BASE_URL = "http://localhost:8082/validate"

# Test different spacings to find what works
print("Finding the right spacing for 12 'normal' requests...")
print("Rate: 37 req/min = 1.62s per token refill\n")

for delay in [1.7, 1.8, 1.9, 2.0]:
    user = f"test-delay-{delay}"
    passed = blocked = 0
    
    # First use burst
    for i in range(9):
        r = requests.post(BASE_URL, json={"userId": user, "category": "Rate Limiting"})
    
    # Then try 12 more with spacing
    for i in range(12):
        r = requests.post(BASE_URL, json={"userId": user, "category": "Rate Limiting"})
        if r.status_code == 200:
            passed += 1
        elif r.status_code == 429:
            blocked += 1
        if i < 11:
            time.sleep(delay)
    
    print(f"Delay {delay}s: {passed} passed, {blocked} blocked")
    time.sleep(3)  # Reset between tests
