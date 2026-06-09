import os
import json
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "agent_events.jsonl")

def log_agent_event(agent_name: str, action: str, details: str = ""):
    """Ghi lại hành động của Agent vào tệp log dùng chung để Streamlit hiển thị."""
    event = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "action": action,
        "details": details
    }
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Failed to write UI log: {e}")

def clear_agent_events():
    """Xóa tệp log cũ khi bắt đầu một phiên làm việc mới."""
    try:
        open(LOG_FILE, "w").close()
    except Exception:
        pass
