import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["ANTHROPIC_API_KEY"]
API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-5"

#payload
payload = {
    "model": MODEL,
    "max_tokens": 512,
    "messages": [
        {
            "role": "user",
            "content": "Tóm tắt giúp tôi note này thành 1 câu: "
                       "'Sáng nay tôi gặp khách hàng A, họ muốn thêm tính năng "
                       "xuất file PDF, deadline cuối tháng.'",
        }
    ],
}

headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

#call API
response = httpx.post(API_URL, headers=headers, json=payload, timeout=30.0)
response.raise_for_status() #raise neu http 4xx/5xx
data = response.json()

#pare response
print("--- Raq response ---")
print(data)

print("\n--- Cau tra loi ---")
text = data["content"][0]["text"]
print(text)

print("\n--- Token usage ---")
usage = data["usage"]
print(f"Input: {usage['input_tokens']} tok, Output: {usage['output_tokens']} tok")