import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["ANTHROPIC_API_KEY"]
API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-5"

SYSTEM_PROMPT = (
    "Bạn là NoteBuddy — trợ lý ghi note thân thiện, tiếng Việt. "
    "Trả lời ngắn gọn 1-2 câu. Khi user xin lưu note, xác nhận đã ghi."
)

messages: list[dict] = []

def chat(user_input: str) -> str:
    messages.append({"role":"user", "content": user_input})

    #2. Goi API voi toan bo lich su hoi thoai
    payload = {
        "model": MODEL,
        "max_tokens": 512,
        "system": SYSTEM_PROMPT,
        "messages": messages,
    }
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    r = httpx.post(API_URL, headers=headers, json=payload, timeout=30.0)
    r.raise_for_status()
    data = r.json()

    #3. lay text reply, append vao lich su de LLM nho
    reply = data["content"][0]["text"]
    messages.append({"role":"assistant","content":reply})
    return reply

def main():
    print("NoteBuddy san sang. Go /exit de thoat, /reset de hoa lich su. \n")
    while True:
        try:
            user_input = input("Ban: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n tam biet!")
            break
        if not user_input:
            continue
        if user_input == "/exit":
            print("Tạm biệt!")
            break
        if user_input == "/reset":
            messages.clear()
            print("(đã xoá lịch sử)")
            continue
        reply = chat(user_input)
        print(f"NoteBuddy: {reply}\n")

if __name__ == "__main__":
    main()