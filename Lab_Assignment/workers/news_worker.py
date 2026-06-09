from langchain_core.messages import AIMessage
import os
from langchain_openai import ChatOpenAI

def news_worker_node(state):
    """Worker chuyên cập nhật tin tức (Sử dụng LLM Search hoặc LLM prompt)"""
    messages = state["messages"]
    last_user_msg = messages[-1].content
    
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENROUTER_API_KEY", "dummy"),
        base_url="https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else None,
        temperature=0.5
    )
    
    prompt = f"Bạn là một nhà báo. Hãy trả lời câu hỏi sau dựa trên kiến thức thực tế và tin tức xã hội: {last_user_msg}"
    try:
        response = llm.invoke(prompt)
        answer = response.content
    except Exception as e:
        answer = f"Lỗi News Worker: {e}"
        
    return {"messages": [AIMessage(content=f"**[📰 News Worker]**\n\n{answer}")]}
