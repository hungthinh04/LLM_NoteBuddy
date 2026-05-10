import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["ANTHROPIC_API_KEY"]
API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-5"

#payload
def ask(system_prompt: str, user_msg: str) -> str:
    payload = {
        "model": MODEL,
        "max_tokens": 256,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_msg}
        ],
    }
    r = httpx.post(API_URL, headers=headers, json=payload, timeout=30.0)
    r.raise_for_status()
    return r.json()["content"][0]["text"]

headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

#call API
USER = "Luu note: chieu mai hop voi team marketing"
#luot 1: system suc tich
print("=== System: súc tích ===")
print(ask(
    system_prompt="Bạn là NoteBuddy. Trả lời súc tích, tối đa 1 câu.",
    user_msg=USER,
))

# Lượt 2: system "vui tinh"
print("\n=== System: vui tính ===")
print(ask(
    system_prompt="Bạn là NoteBuddy phong cách Gen Z, trả lời với 1 emoji ở cuối.",
    user_msg=USER,
))

# #pare response
# print("--- Raq response ---")
# print(data)

# print("\n--- Cau tra loi ---")
# text = data["content"][0]["text"]
# print(text)

# print("\n--- Token usage ---")
# usage = data["usage"]
# print(f"Input: {usage['input_tokens']} tok, Output: {usage['output_tokens']} tok")