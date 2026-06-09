from typing import Literal
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import os

class Route(BaseModel):
    next_node: Literal["LegalWorker", "NewsWorker", "GeneralWorker", "FINISH"]

def supervisor_node(state):
    """Điều phối viên quyết định Worker nào xử lý."""
    messages = state["messages"]
    
    system_prompt = (
        "Bạn là một Supervisor (Người điều phối). Bạn quản lý 3 workers:\n"
        "- 'LegalWorker': Chuyên trả lời các câu hỏi về quy định pháp luật, điều luật, hình phạt (đặc biệt là luật ma tuý).\n"
        "- 'NewsWorker': Chuyên trả lời các sự kiện thực tế, vụ án, người nổi tiếng bị bắt.\n"
        "- 'GeneralWorker': Xử lý các câu hỏi chào hỏi, giao tiếp thông thường (ví dụ: xin chào, cảm ơn).\n"
        "Hãy dựa vào câu hỏi của người dùng để chọn worker phù hợp nhất. Nếu đã có đủ câu trả lời, chọn 'FINISH'."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Ai sẽ là người xử lý tiếp theo? Chọn 1 trong: LegalWorker, NewsWorker, GeneralWorker, FINISH.")
    ])
    
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENROUTER_API_KEY", "dummy"),
        base_url="https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else None,
        temperature=0
    )
    
    chain = prompt | llm.with_structured_output(Route)
    try:
        route = chain.invoke({"messages": messages})
        next_worker = route.next_node
    except Exception as e:
        # Nếu LLM bị lỗi (VD hết credits) thì fallback về General
        next_worker = "GeneralWorker"
        
    return {"next": next_worker}
