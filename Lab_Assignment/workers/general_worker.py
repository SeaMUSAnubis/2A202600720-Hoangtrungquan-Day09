from langchain_core.messages import AIMessage
import os
from langchain_openai import ChatOpenAI

def general_worker_node(state):
    """Worker chuyên xử lý các câu hỏi chào hỏi thông thường."""
    messages = state["messages"]
    
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENROUTER_API_KEY", "dummy"),
        base_url="https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else None,
        temperature=0.7
    )
    
    try:
        response = llm.invoke([{"role": "system", "content": "Bạn là trợ lý ảo thân thiện. Hãy chào hỏi hoặc trả lời ngắn gọn các câu giao tiếp cơ bản."}] + messages)
        answer = response.content
    except Exception as e:
        answer = f"Lỗi General Worker: {e}"
        
    return {"messages": [AIMessage(content=f"**[🤖 General Worker]**\n\n{answer}")]}
