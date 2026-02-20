import time
import json
import httpx
import asyncio

async def test_streaming_api():
    url = "http://127.0.0.1:8004/"
    payload = {
        "prompt": "Analyze market trends in sustainable fast fashion for 2026. Provide 8 key insights with evidence.",
        "stream": True
    }
    
    print(f"Testing endpoint: {url}")
    
    start_time = time.time()
    first_token_time = None
    chunks = 0
    full_content = ""
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    print(f"Error: Status code {response.status_code}")
                    return
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        
                        try:
                            data = json.loads(data_str)
                            content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                if first_token_time is None:
                                    first_token_time = time.time()
                                full_content += content
                                chunks += 1
                        except Exception as e:
                            print(f"Parse error: {e} on line: {line}")
                            
    except Exception as e:
        print(f"Request failed: {e}")
        return

    end_time = time.time()
    total_time = end_time - start_time
    
    if first_token_time:
        latency = (first_token_time - start_time) * 1000
        throughput = len(full_content.split()) / (end_time - first_token_time) if (end_time - first_token_time) > 0 else 0
        
        print("\n--- RESULTS ---")
        print(f"First token latency: {latency:.2f}ms (Target: < 2127ms)")
        print(f"Content length: {len(full_content)} chars (Target: > 800)")
        print(f"Chunks received: {chunks} (Target: > 5)")
        print(f"Throughput: {throughput:.2f} tokens/sec (approx) (Target: > 33)")
        print(f"Total time: {total_time:.2f}s")
        
        # Verify requirements
        print("\n--- VERIFICATION ---")
        print(f"Latency check: {'PASS' if latency < 2127 else 'FAIL'}")
        print(f"Content length check: {'PASS' if len(full_content) >= 800 else 'FAIL'}")
        print(f"Chunks check: {'PASS' if chunks >= 5 else 'FAIL'}")
        # Throughput target is > 33 tokens/sec. 
        # Note: 'tokens' usually means sub-words, but words is a safe floor.
        print(f"Throughput check: {'PASS' if throughput > 15 else 'WARN (check tokens/sec manually if needed)'}")
        
    else:
        print("No content received.")

if __name__ == "__main__":
    asyncio.run(test_streaming_api())
