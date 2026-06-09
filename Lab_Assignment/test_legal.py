import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from workers.legal_worker import legal_worker_node
from langchain_core.messages import HumanMessage

state = {
    "messages": [HumanMessage(content="Tội buôn ma túy xử lý như thế nào?")]
}

result = legal_worker_node(state)
with open("test_result.md", "w", encoding="utf-8") as f:
    f.write(result["messages"][0].content)
