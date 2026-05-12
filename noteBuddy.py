import os
import httpx
from dotenv import load_dotenv
import json as _json
from tool_dispatch import run_tool
from tools_schema import ALL_TOOLS

load_dotenv()

MAX_ITERATIONS = 10
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

def run_agent(user_input: str) -> str:
    # === BƯỚC 1: append user input vào history ===
    messages.append({"role": "user", "content": user_input})

    # === BƯỚC 2: vòng lặp ReAct ===
    for step in range(1, MAX_ITERATIONS + 1):
        resp = _call_api(messages)
        print(f"  [agent step {step}] stop_reason={resp['stop_reason']}")

        # 2a. Lưu nguyên content (text + tool_use) làm assistant turn
        messages.append({"role": "assistant", "content": resp["content"]})

        # 2b. Nếu không cần tool nữa → kết thúc
        if resp["stop_reason"] != "tool_use":
            return _extract_text(resp["content"])

        # 2c. Có tool_use → exec từng cái và append tool_result
        tool_results = []
        for block in resp["content"]:
            if block["type"] != "tool_use":
                continue
            print(f"    -> tool: {block['name']}({block['input']})")
            result = run_tool(block["name"], block["input"])
            print(f"    <- result: {result}")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block["id"],
                "content": _json.dumps(result, ensure_ascii=False),
            })
        messages.append({"role": "user", "content": tool_results})

    # === BƯỚC 3: hết max_iterations → thoát an toàn ===
    return f"(Đã đạt max_iterations={MAX_ITERATIONS}, có thể agent đang stuck loop.)"


def _extract_text(content_blocks: list) -> str:
    return "".join(b["text"] for b in content_blocks if b["type"] == "text")




# def chat(user_input: str) -> str:
#     messages.append({"role": "user", "content": user_input})

#     # Vòng API thứ nhất
#     resp = _call_api(messages)

#     # Nếu LLM trả thẳng text, xong.
#     if resp["stop_reason"] != "tool_use":
#         reply = resp["content"][0]["text"]
#         messages.append({"role": "assistant", "content": reply})
#         return reply

#     # === LLM muốn gọi tool ===
#     # Lưu nguyên content (gồm text + tool_use blocks) làm assistant turn
#     messages.append({"role": "assistant", "content": resp["content"]})

#     # Chạy từng tool_use block
#     tool_results = []
#     for block in resp["content"]:
#         if block["type"] != "tool_use":
#             continue
#         result = run_tool(block["name"], block["input"])
#         tool_results.append({
#             "type": "tool_result",
#             "tool_use_id": block["id"],
#             "content": _json.dumps(result, ensure_ascii=False),
#         })

#     # Gửi tool_results (role=user!) trở lại LLM
#     messages.append({"role": "user", "content": tool_results})

#     # Vòng API thứ 2 — LLM đọc kết quả tool và sinh reply cuối
#     resp2 = _call_api(messages)
#     reply = "".join(b["text"] for b in resp2["content"] if b["type"] == "text")
#     messages.append({"role": "assistant", "content": reply})
#     return reply

def main():
    print("NoteBuddy v2 (agent loop). /exit để thoát, /reset để xoá history.\n")
    while True:
        try:
            user_input = input("Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user_input == "/exit":
            break
        if user_input == "/reset":
            messages.clear()
            print("(reset)")
            continue
        if not user_input:
            continue
        reply = run_agent(user_input)
        print(f"NoteBuddy: {reply}\n")


if __name__ == "__main__":
    main()