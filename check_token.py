import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()   # tự đọc ANTHROPIC_API_KEY từ env

result = client.messages.count_tokens(
    model="claude-sonnet-4-5",
    system="Bạn là NoteBuddy.",
    messages=[
        {"role": "user", "content": "Lưu note: mai họp lúc 9h."},
    ],
)
print(f"Token count: {result.input_tokens}")