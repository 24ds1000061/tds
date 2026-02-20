# Q1. Prompt Engineering for PromptOps
```json
{
  "problems": [
    "Problem 1: Undefined Classification Schema — The prompt asks for a 'quality level' without defining the scale (e.g., High/Medium/Low vs. 1-10) or the criteria for assignment, leading to arbitrary and subjective results.",
    "Problem 2: Unspecified Output Format — The instruction 'Just give me the level' is vague and can result in varied outputs like 'High', 'Level 5', or 'The lead is high quality', making programmatic parsing difficult.",
    "Problem 3: Lack of Context and Error Handling — There is no guidance on how to evaluate specific signals (like budget or timeline) or how to handle leads with missing or ambiguous information."
  ],
  "improvedPrompt": "You are an expert Sales Operations Analyst. Your task is to classify sales leads into specific quality tiers based on the BANT framework (Budget, Authority, Need, Timeline).\n\n### SCORING RUBRIC:\n- **High**: Meets all or most BANT criteria (Budget approved, Decision maker identified, Clear need, Timeline < 3 months).\n- **Medium**: Meets some criteria but has gaps (e.g., Budget undefined but strong Need and Authority).\n- **Low**: Missing critical criteria, long timeline (> 6 months), or low authority.\n- **Unqualified**: Spam, wrong contact info, or clearly irrelevant.\n\n### INPUT TEXT:\n\"Fortune 500 company requesting demo. Budget approved. Decision maker engaged. Timeline: 30 days.\"\n\n### INSTRUCTIONS:\n1. Analyze the input against the Scoring Rubric.\n2. If key information (like Budget or Authority) is missing, do not assume it exists; classify conservatively.\n3. Provide your response in strictly valid JSON format.\n\n### RESPONSE FORMAT:\n{\n  \"classification\": \"High\" | \"Medium\" | \"Low\" | \"Unqualified\",\n  \"confidence_score\": 0.0 to 1.0,\n  \"missing_info\": [\"list\", \"any\", \"missing\", \"BANT\", \"fields\"],\n  \"reasoning\": \"Brief explanation of the classification based on BANT analysis.\"\n}\n\n### EXAMPLES:\nInput: \"Student looking for research paper help.\"\nOutput: {\"classification\": \"Unqualified\", \"confidence_score\": 0.95, \"missing_info\": [\"Budget\", \"Authority\", \"Timeline\"], \"reasoning\": \"User is a student, not a business prospect. No budget or timeline indicated.\"}\n\nInput: \"VP of Engineering at Series B startup. Needs solution for Q3 audit.\"\nOutput: {\"classification\": \"High\", \"confidence_score\": 0.85, \"missing_info\": [\"Budget\"], \"reasoning\": \"Strong Authority (VP) and clear Timeline/Need (Q3 Audit). implied budget for compliance needs.\"}",
  "improvements": [
    "Defined Constraints & Rubric: Introduced the BANT framework and specific tiers (High, Medium, Low, Unqualified) to remove subjectivity and ensure consistent scoring.",
    "Enforced JSON Structure: Specified a strict JSON output schema including fields for classification, confidence, missing info, and reasoning to ensure the output is machine-readable and parsable.",
    "Added Robustness (Edge Cases & Examples): Included instructions on how to handle missing information (\"classify conservatively\") and provided few-shot examples to demonstrate how to handle both successful and unqualified leads."
  ]
}
```

# Q2. SecurePrompt - Say Yes
Reply with "Yes" or "No": Is Linux an OS?

# Q3. Simon Willison Pipeline
```bash
curl -sL "https://en.wikipedia.org/api/rest_v1/page/random/summary" | \
  jq -r '.extract' | \
  llm "Rewrite this summary for a 10-year-old audience"
```

# Q4. JavaScript Function Generation
Create the body of an asynchronous JavaScript function that fetches JSON from a 'url' variable. Parse the response and calculate the sum of the 'number' property for each item in the 'data' array. Return the calculated sum. If any error occurs during fetch or processing, return 0. Output only the code for the function body, with no markdown or function signatures.

# Q5. Web App URL
https://v0-home-page-html-tau.vercel.app/

# Q6. Python Debug Output
OUTPUT: 13,2685,206.54

# Q7. Email Validation Debugging
```json
{
  "bugs": [
    "Bug 1: Incorrect Order Logic — The function returns true if '@' and '.' exist anywhere, regardless of position (e.g., 'user.name@com' would fail valid checks if '.' was required after '@', but the original code passes it even if the '.' is before '@').",
    "Bug 2: Missing Content Validation — It does not check for text before '@' (e.g., '@example.com' returns true) or text between '@' and '.' (e.g., 'user@.com' returns true).",
    "Bug 3: Edge Case Failures — It accepts invalid formats like multiple '@' symbols, spaces, or '.' as the last character."
  ],
  "fixedCode": "function isValidEmail(email) {\n  // Regex: 1+ char not @/space, then @, then 1+ char not @/space, then ., then 1+ char not @/space\n  const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;\n  return emailRegex.test(email);\n}",
  "testStrategy": "I would implement a comprehensive test suite covering:\n1. **Positive Cases**: Standard formats (user@example.com), subdomains (user@sub.example.com).\n2. **Negative Cases**: Missing parts (no local, no domain, no TLD), wrong order (. before @), sequential dots (..), and invalid characters (spaces, multiple @).\n3. **Boundary Analysis**: Single-character local/domain parts, very long strings.\n4. **Type Safety**: verifying input is a non-null string before processing."
}
```

# Q8. 
q8. ```json
{
  "llm": {
    "choice": "Gemini 1.5 Flash",
    "justification": "Optimal balance for high-volume invoice processing. It has a massive context window (1M tokens) to handle complex, multi-page PDFs and forms without truncation. It is significantly cheaper than GPT-4o or Sonnet ($0.35/1M input tokens vs $5.00+), making it the only viable option to process ~3000 documents/day within the tight $625/month budget while maintaining high accuracy for extraction tasks."
  },
  "vectorDB": {
    "choice": null,
    "justification": "Not needed for this specific use case. Invoice processing is an extraction and classification task, not a semantic search or retrieval-augmented generation (RAG) task. We process each document independently. Structural metadata (SQL) is more valuable here than vector embeddings."
  },
  "additionalTools": [
    "Tool 1: Amazon Textract (or Google Document AI) – Purpose: Specialized OCR to accurately digitize messy layouts, handwriting, and tables before sending text to the LLM, ensuring higher accuracy than raw LLM vision alone.",
    "Tool 2: PostgreSQL – Purpose: Robust relational database to store extracted metadata, invoice line items, and classification results. Essential for structured queries and integration with financial systems.",
    "Tool 3: Redis / BullMQ – Purpose: Priority queue management to handle the 'batch processing' requirement and volume spikes, ensuring high-priority invoices are processed first."
  ],
  "architecture": "1. **Ingestion Layer**: Users submit invoices via Email (SMTP hook) or Upload Portal (React/S3). API Gateway (FastAPI) validates request format.\n2. **Queueing Layer**: Valid requests are pushed to a Redis/BullMQ Priority Queue. High-priority flags (e.g., 'urgent') route to the front.\n3. **Processing Layer**: A Python Worker Service pulls jobs. It first sends files to **Amazon Textract** (OCR) to extract raw text and tables.\n4. **Intelligence Layer**: The Worker constructs a prompt with the raw OCR text and schema instructions, sending it to **Gemini 1.5 Flash**. The LLM extracts fields and classifies the document.\n5. **Validation & Storage**: The Worker validates the JSON response against Pydantic models. High-confidence data is committed to **PostgreSQL**. Low-confidence data (<90%) is flagged in the DB for 'Human Review'.\n6. **Notification**: A webhook notifies the client system of completion.",
  "costEstimate": {
    "total": 485,
    "breakdown": {
      "LLM API calls": 150,
      "Vector DB": 0,
      "Infrastructure hosting": 100,
      "Storage": 35,
      "OCR Services": 200
    },
    "assumptions": "2,800 docs/day * 30 days = 84,000 docs. Avg 1k tokens/doc. Gemini Flash input is extremely cheap (~$25/month for this volume). The bulk of cost is allocated to high-quality OCR (Textract @ $1.50/1k pages) and hosting."
  },
  "tradeoffs": [
    "Trade-off 1: Using Gemini 1.5 Flash over GPT-4o. Prioritized cost and throughput over maximum reasoning capability. Acceptable because invoice extraction is a structured task where Flash's performance is sufficient (95%+ with good prompting).",
    "Trade-off 2: Adding specialized OCR (Textract) increases cost but drastically reduces 'hallucinations' on tabular data compared to pure vision-LLM approaches.",
    "Trade-off 3: Skipping Vector DB. We lose semantic search capabilities (e.g., 'find invoices like this one') but save money and complexity, as the requirement is strict classification/extraction."
  ],
  "risks": [
    "Risk 1: Rate Limits. Mitigation: Implemented Redis queue to buffer spikes and throttle requests to stay within API limits.",
    "Risk 2: Data Privacy. Mitigation: Use enterprise endpoints (Zero Data Retention policies) and strip PII before storage where possible, ensuring compliance with financial data standards."
  ]
}
```

# Q9. 
q9. ```python
"""
Data Processing Pipeline Refactoring

This module handles data processing system.
Note: This code uses camelCase naming which violates PEP 8.
Refactor the non-compliant names to snake_case.

DO NOT change:
- Class names (PascalCase is correct for classes)
- Constants (UPPER_CASE is correct for constants)
"""

import json
from typing import List, Dict, Optional


class DataProcessor:
    """Main data processor class - DO NOT RENAME"""

    MAX_ITEMS = 1000  # Constant - DO NOT RENAME

    def __init__(self, config: Dict):
        self.config = config
        self.format_output = 0  # Track current position
        self.items = []

    def get_user_data(self, user_id: str) -> Optional[Dict]:
        """Fetch user data from the API"""
        # Using get_user_data to retrieve information
        if not user_id:
            return None

        # Call get_user_data multiple times for retry logic
        data = self._fetch_data(user_id)
        if data:
            # get_user_data succeeded
            result = self.calculate_total(data)
            return result
        return None

    def calculate_total(self, items: List[Dict]) -> List[Dict]:
        """Process items and apply transformations"""
        processed = []
        self.format_output = 0  # Reset format_output

        for item in items:
            # calculate_total handles each item
            if self.process_items(item):
                formatted = self.formatOutputItem(item)
                processed.append(formatted)
                self.format_output += 1  # Increment format_output

        # calculate_total returns processed items
        return processed

    def process_items(self, data: Dict) -> bool:
        """Validate input data structure"""
        # process_items checks required fields
        if not isinstance(data, dict):
            return False

        required_fields = ['id', 'name', 'value']
        # process_items ensures all fields present
        for field in required_fields:
            if field not in data:
                return False

        # process_items passed all checks
        return True

    def formatOutputItem(self, item: Dict) -> Dict:
        """Format a single item - uses format_output prefix"""
        # Note: Method name intentionally uses format_output
        # This tests that you DON'T rename the variable inside the method name
        return {
            'id': item['id'],
            'processed': True,
            'index': self.format_output  # Reference to variable
        }

    def _fetch_data(self, user_id: str) -> Optional[List[Dict]]:
        """Internal helper method"""
        # Simulate API call
        return [{'id': user_id, 'name': 'Test', 'value': 41}]


def main():
    """Main execution function"""
    processor = DataProcessor(config={})

    # Test get_user_data
    user_data = processor.get_user_data("user123")
    if user_data:
        # Process using calculate_total
        items = [user_data]
        results = processor.calculate_total(items)

        # Validate using process_items
        for result in results:
            if processor.process_items(result):
                print(f"Processed item at index {processor.format_output}")


if __name__ == "__main__":
    main()
```

# Q10. Replace across files
0414d98dbbc1c0e015d3477e2cbb79cd7a6e2ba9a31b5ae3d4109e4732d3bad2  -

# Q11. Reorganize Files with Shell Commands
q11. find . -name "*Zone.Identifier" -delete
26f488c5834a498a3d4793adcda9b18332d186123619f28c9064dc6adc874afe  -

# Q12. 
q12. ```json
{"version": 2, "width": 29, "height": 10, "timestamp": 1771048215, "env": {"SHELL": "/bin/bash", "TERM": "xterm-256color"}}
[0.008723, "o", "\u001b[H\u001b[2J\u001b[3J"]
[0.511343, "o", "$ echo 'SESSION_VFZVSQW4'\r\n"]
[0.713752, "o", "SESSION_VFZVSQW4\r\n"]
[1.716866, "o", "$ ls -la\r\n"]
[1.920439, "o", "total 20\r\ndrwxr-xr-x 2 paras paras 4096 Feb 14 09:50 .\r\ndrwxr-xr-x 6 paras paras 4096 Feb 14 09:47 ..\r\n-rwxr-xr-x 1 paras paras  472 Feb 14 09:49 run_session.sh\r\n-rw-r--r-- 1 paras paras  548 Feb 14 09:47 session.cast\r\n-rw-r--r-- 1 paras paras  291 Feb 14 09:50 session_retry.cast\r\n"]
[2.923736, "o", "$ cat /etc/os-release | head -5\r\n"]
[3.126872, "o", "PRETTY_NAME=\"Ubuntu 24.04.3 LTS\"\r\nNAME=\"Ubuntu\"\r\nVERSION_ID=\"24.04\"\r\nVERSION=\"24.04.3 LTS (Noble Numbat)\"\r\nVERSION_CODENAME=noble\r\n"]
[4.130346, "o", "$ whoami\r\n"]
[4.333248, "o", "paras\r\n"]
[4.834802, "o", "exit\r\n"]
```

# Q13. 
q13. ```json
{"version": 2, "width": 22, "height": 10, "timestamp": 1771048419, "env": {"SHELL": "/bin/bash", "TERM": "xterm-256color"}}
[0.006597, "o", "\u001b[H\u001b[2J\u001b[3J"]
[0.008069, "o", "$ e"]
[0.058815, "o", "c"]
[0.110551, "o", "h"]
[0.162242, "o", "o"]
[0.213945, "o", " "]
[0.265503, "o", "'"]
[0.317051, "o", "C"]
[0.368698, "o", "O"]
[0.420315, "o", "P"]
[0.472022, "o", "I"]
[0.524267, "o", "L"]
[0.575868, "o", "O"]
[0.627396, "o", "T"]
[0.679142, "o", "_"]
[0.730535, "o", "X"]
[0.782499, "o", "3"]
[0.834699, "o", "H"]
[0.887004, "o", "I"]
[0.938782, "o", "4"]
[0.990478, "o", "R"]
[1.041853, "o", "G"]
[1.093842, "o", "G"]
[1.145588, "o", "'"]
[1.198076, "o", "\r\n"]
[1.709203, "o", "COPILOT_X3HI4RGG\r\n"]
[2.710929, "o", "$ g"]
[2.762719, "o", "h"]
[2.814275, "o", " "]
[2.865793, "o", "c"]
[2.917415, "o", "o"]
[2.968899, "o", "p"]
[3.020454, "o", "i"]
[3.071831, "o", "l"]
[3.123499, "o", "o"]
[3.17492, "o", "t"]
[3.226543, "o", " "]
[3.278052, "o", "a"]
[3.329639, "o", "s"]
[3.381126, "o", "k"]
[3.433077, "o", " "]
[3.484614, "o", "\""]
[3.536254, "o", "W"]
[3.5878, "o", "h"]
[3.639179, "o", "a"]
[3.69076, "o", "t"]
[3.742263, "o", " "]
[3.793688, "o", "i"]
[3.845343, "o", "s"]
[3.89695, "o", " "]
[3.948691, "o", "t"]
[4.000569, "o", "h"]
[4.052942, "o", "e"]
[4.105102, "o", " "]
[4.156709, "o", "c"]
[4.20822, "o", "a"]
[4.260118, "o", "p"]
[4.312114, "o", "i"]
[4.363934, "o", "t"]
[4.37808, "r", "27x10"]
[4.37836, "r", "27x10"]
[4.415781, "o", "a"]
[4.467466, "o", "l"]
[4.51899, "o", " "]
[4.570617, "o", "o"]
[4.622296, "o", "f"]
[4.673822, "o", " "]
[4.72558, "o", "A"]
[4.777101, "o", "u"]
[4.828643, "o", "s"]
[4.880348, "o", "t"]
[4.931909, "o", "r"]
[4.983488, "o", "a"]
[5.035346, "o", "l"]
[5.087253, "o", "i"]
[5.138619, "o", "a"]
[5.190398, "o", "?"]
[5.242079, "o", "\""]
[5.294126, "o", "\r\n"]
[7.297757, "o", "\r\nThe capital of Australia is **Canberra**.\r\n\r\n"]
[8.299371, "o", "$ e"]
[8.350803, "o", "x"]
```

# Q14. 
93

# Q15. 
725

# Q16. 
```sql
CREATE TABLE Customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    join_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('active', 'inactive')),
    loyalty_points INTEGER NOT NULL DEFAULT 0 CHECK(loyalty_points >= 0)
);

CREATE TABLE Products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK(price > 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK(stock_quantity >= 0),
    supplier_id TEXT NOT NULL
);

CREATE TABLE Orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL CHECK(total_amount >= 0),
    status TEXT NOT NULL CHECK(status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    shipping_address TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE Order_Items (
    order_item_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
```

# Q17. 
'''sql
select department, avg(salary)  from employees  group by department;
'''

# Q18. Build Semantic Search with Re-ranking 
**Public Endpoint:** https://choleric-zana-dentally.ngrok-free.dev/search
**Local Endpoint:** http://127.0.0.1:5000/search

### How to Restart
If the session is closed, follow these steps to restart the service:

1. **Start the API Server:**
   ```bash
   cd ~/tds/ga-1/q18_semantic_search
   python3 -m uvicorn main:app --host 0.0.0.0 --port 5000
   ```
2. **Start the Ngrok Tunnel:**
   In a separate terminal, run:
   ```bash
   ngrok http 5000 --url=choleric-zana-dentally.ngrok-free.dev
   ```



# Q19. 
/home/paras/tds/ga-1/q19_vector/venv/bin/python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8080
http://127.0.0.1:8080/similarity


# Q20. 
jombv5kh1j

# Q21. 
342
# Q22. 
none

# Q23. 
https://raw.githubusercontent.com/24ds1000061/tds-health-check/main/email.json

# Q24.
```bash
# To run the pipeline server:
cd /home/paras/tds/ga-1/q24
source venv/bin/activate

python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
http://localhost:8000/pipeline
```
Endpoint: http://localhost:8000/pipeline

# Q25.
{
  "model": "gpt-4o",
  "monthlyCost": 1138.85,
  "strategies": [
    "Semantic Caching: Identify and cache moderation results for identical or highly similar content (estimated 40% cache hit rate).",
    "Prompt Compression: Refactor system prompts to remove redundant instructions and examples, saving 100 tokens per input request.",
    "Draft-then-Verify: For low-confidence segments, use gpt-4o-mini as a high-speed pre-filter to reduce primary model calls (not included in cost calculation)."
  ],
  "justification": "Chose gpt-4o due to its industry-leading quality score (97%), which is essential for minimizing false positives in content moderation. While its base monthly cost of $2,005.88 exceeds the budget, applying semantic caching (40% hit rate) and prompt compression (reducing input from 295 to 195 tokens) brings the estimated cost down to $1,138.85, well within the $1,443 limit. This approach prioritizes safety and accuracy over cost, while still maintaining high economic efficiency."
}

# Q26. 
```bash
# To run the caching server:
cd /home/paras/tds/ga-1/q26
./venv/bin/python3 main.py
```
Endpoint: http://localhost:8081/

# Q27. 
(Empty)

# Q28. 
(Empty)

# Q29. 
(Empty)

# Q30. 
(Empty)

# Q31. 
(Empty)

# Q32. 
42047

# Q33. 


# Q34. 
(Empty)

# Q35. 
import httpx

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer DUMMY_API_KEY",
    "Content-Type": "application/json",
}

messages = [
    {
        "role": "system",
        "content": "Analyze the sentiment of the provided text and respond with exactly one of the following categories: GOOD, BAD, or NEUTRAL. Return only the single word (GOOD, BAD, or NEUTRAL) with no extra explanation.",
    },
    {
        "role": "user",
        "content": "8UnWA Za V  DrOLSju U S9RpY Q iH8q1dcxAw JKexi6kNp",
    },
]

payload = {
    "model": "gpt-4o-mini",
    "messages": messages,
    "temperature": 0.0,
}

response = httpx.post(url, json=payload, headers=headers, timeout=10)
response.raise_for_status()
print(response.json())

# Q36. 
33

# Q37. 
131.91
