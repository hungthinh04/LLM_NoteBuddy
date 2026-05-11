import os
import httpx
from dotenv import load_dotenv
import json as _json
from tool_dispatch import run_tool
from tools_schema import ALL_TOOLS

load_dotenv()

API_KEY = os.environ["ANTHROPIC_API_KEY"]
API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-5"

headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

SYSTEM_PROMPT = (
    "Bạn là NoteBuddy — trợ lý ghi note thân thiện, tiếng Việt. "
    "Trả lời ngắn gọn 1-2 câu. Khi user xin lưu note, xác nhận đã ghi."
)

messages: list[dict] = []

# def chat(user_input: str) -> str:
#     messages.append({"role":"user", "content": user_input})

#     #2. Goi API voi toan bo lich su hoi thoai
#     payload = {
#         "model": MODEL,
#         "max_tokens": 512,
#         "system": SYSTEM_PROMPT,
#         "messages": messages,
#     }
#     headers = {
#         "x-api-key": API_KEY,
#         "anthropic-version": "2023-06-01",
#         "content-type": "application/json",
#     }
#     r = httpx.post(API_URL, headers=headers, json=payload, timeout=30.0)
#     r.raise_for_status()
#     data = r.json()

#     #3. lay text reply, append vao lich su de LLM nho
#     reply = data["content"][0]["text"]
#     messages.append({"role":"assistant","content":reply})
#     return reply





def _call_api(messages: list[dict]) -> dict:
    payload = {
        "model": MODEL,
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "tools": ALL_TOOLS,
        "messages": messages,
    }
    r = httpx.post(API_URL, headers=headers, json=payload, timeout=60.0)
    r.raise_for_status()
    return r.json()

def chat(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})

    # Vòng API thứ nhất
    resp = _call_api(messages)

    # Nếu LLM trả thẳng text, xong.
    if resp["stop_reason"] != "tool_use":
        reply = resp["content"][0]["text"]
        messages.append({"role": "assistant", "content": reply})
        return reply

    # === LLM muốn gọi tool ===
    # Lưu nguyên content (gồm text + tool_use blocks) làm assistant turn
    messages.append({"role": "assistant", "content": resp["content"]})

    # Chạy từng tool_use block
    tool_results = []
    for block in resp["content"]:
        if block["type"] != "tool_use":
            continue
        result = run_tool(block["name"], block["input"])
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block["id"],
            "content": _json.dumps(result, ensure_ascii=False),
        })

    # Gửi tool_results (role=user!) trở lại LLM
    messages.append({"role": "user", "content": tool_results})

    # Vòng API thứ 2 — LLM đọc kết quả tool và sinh reply cuối
    resp2 = _call_api(messages)
    reply = "".join(b["text"] for b in resp2["content"] if b["type"] == "text")
    messages.append({"role": "assistant", "content": reply})
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