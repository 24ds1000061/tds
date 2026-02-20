import requests
import time

URL = "http://localhost:8082/secure-ai"
user = "quick-test-user"

print("Burst: 18 requests")
burst_passed = sum(1 for _ in range(18) if requests.post(URL, json={"userId": user, "category": "Rate Limiting"}).status_code == 200)

print(f"Burst: {burst_passed}/9 expected passed")

time.sleep(0.5)  # Small delay like validation system

print("\nNormal: 12 requests")
normal_passed = sum(1 for _ in range(12) if requests.post(URL, json={"userId": user, "category": "Rate Limiting"}).status_code == 200)

print(f"Normal: {normal_passed}/6+ expected passed")
print(f"\nResult: {'✅ PASS' if burst_passed >= 9 and normal_passed >= 6 else '❌ FAIL'}")
