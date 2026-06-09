import sys
import os
from pathlib import Path
from langchain_core.messages import AIMessage

# Thêm đường dẫn tới source Day08
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent / "DAY8" / "Day08_RAG_pipeline_cohort2"
sys.path.append(str(project_root))

try:
    from src.task10_generation import generate_with_citation
except ImportError:
    # Nếu không tìm thấy, tạo hàm mock
    def generate_with_citation(query, **kwargs):
        return {"answer": "Đây là câu trả lời pháp lý từ Legal Worker (Mock do không tìm thấy module).", "sources": []}

def legal_worker_node(state):
    """Worker chuyên tư vấn pháp luật (Sử dụng RAG Day 08)"""
    messages = state["messages"]
    last_user_msg = messages[-1].content
    
    # Gọi hàm RAG
    try:
        result = generate_with_citation(last_user_msg)
        answer = result.get("answer", "Lỗi khi lấy dữ liệu RAG.")
    except Exception as e:
        answer = f"Lỗi Legal Worker: {e}"
        
    return {"messages": [AIMessage(content=f"**[🧑‍⚖️ Legal Worker]**\n\n{answer}")]}
