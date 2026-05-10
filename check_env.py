import os
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("ANTHROPIC_API_KEY")
if not key:
    print("Lỗi: chưa có ANTHROPIC_API_KEY trong .env")
elif not key.startswith("sk-ant-"):
    print("Lỗi: key sai format, phải bắt đầu bằng sk-ant-")
else:
    print(f"Ok: key load được, prefix = {key[:12]}...")