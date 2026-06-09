import streamlit as st
import asyncio
import os
import time
from uuid import uuid4
import httpx

from dotenv import load_dotenv

# Import A2A modules
from a2a.types import AgentCard, Message, Part, Role, TextPart, MessageSendParams, SendMessageRequest
from a2a.client import A2AClient

load_dotenv()

CUSTOMER_AGENT_URL = os.getenv("CUSTOMER_AGENT_URL", "http://localhost:10100")

st.set_page_config(page_title="Multi-Agent Legal Assistant", page_icon="⚖️", layout="wide")

st.title("⚖️ Multi-Agent Legal Assistant (A2A Protocol)")
st.markdown("Hệ thống bao gồm các Agent chuyên sâu (Law, Tax, Compliance, Privacy) chạy độc lập qua giao thức A2A.")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "latency" in message:
            st.caption(f"⏱️ Thời gian xử lý: {message['latency']:.2f}s")

async def call_customer_agent(question: str) -> str:
    """Gọi HTTP Request đến Customer Agent bằng giao thức A2A"""
    async with httpx.AsyncClient(timeout=300.0) as http_client:
        card_url = f"{CUSTOMER_AGENT_URL}/.well-known/agent.json"
        try:
            card_resp = await http_client.get(card_url)
            card_resp.raise_for_status()
        except Exception as e:
            return f"❌ Không thể kết nối tới Customer Agent. Vui lòng đảm bảo bạn đã chạy `./start_all.sh`.\n\nChi tiết lỗi: {e}"

        agent_card = AgentCard.model_validate(card_resp.json())
        client = A2AClient(httpx_client=http_client, agent_card=agent_card)

        # Cấu trúc message
        message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text=question))],
            message_id=str(uuid4()),
        )
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(message=message),
        )

        try:
            # Gửi request
            response = await client.send_message(request)
            
            # Parse kết quả trả về
            result_text = ""
            if hasattr(response, "root") and hasattr(response.root, "result"):
                result = response.root.result
                if hasattr(result, "artifacts") and result.artifacts:
                    for artifact in result.artifacts:
                        for part in artifact.parts:
                            p = part.root if hasattr(part, "root") else part
                            if hasattr(p, "text"):
                                result_text += p.text
                elif hasattr(result, "parts") and result.parts:
                    for part in result.parts:
                        p = part.root if hasattr(part, "root") else part
                        if hasattr(p, "text"):
                            result_text += p.text
                elif hasattr(result, "status") and hasattr(result.status, "message") and hasattr(result.status.message, "parts"):
                    for part in result.status.message.parts:
                        p = part.root if hasattr(part, "root") else part
                        if hasattr(p, "text"):
                            result_text += p.text
            
            return result_text if result_text else "⚠️ Không nhận được câu trả lời dạng văn bản từ hệ thống."
            
        except Exception as e:
            return f"❌ Đã xảy ra lỗi kết nối: {e}"

# Form nhập tin nhắn
if prompt := st.chat_input("Nhập câu hỏi pháp lý phức tạp (VD: Công ty trốn thuế và rò rỉ dữ liệu sẽ bị phạt thế nào?)"):
    # Lưu tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot trả lời
    with st.chat_message("assistant"):
        start_time = time.time()
        
        # Cập nhật real-time bằng cách liên tục đọc file log trong một tiến trình async
        with st.status("🧠 Hệ thống Multi-Agent đang xử lý...", expanded=True) as status:
            log_container = st.container()
            
            async def run_and_monitor():
                from common.ui_logger import clear_agent_events, LOG_FILE
                import json
                
                # Xóa log cũ
                clear_agent_events()
                
                # Bắt đầu gọi Agent
                agent_task = asyncio.create_task(call_customer_agent(prompt))
                
                # Vòng lặp theo dõi file log
                last_lines = 0
                while not agent_task.done():
                    if os.path.exists(LOG_FILE):
                        try:
                            with open(LOG_FILE, "r", encoding="utf-8") as f:
                                lines = f.readlines()
                                if len(lines) > last_lines:
                                    for line in lines[last_lines:]:
                                        try:
                                            data = json.loads(line.strip())
                                            agent = data["agent"]
                                            action = data["action"]
                                            details = data.get("details", "")
                                            
                                            # Thêm UI expander ngay lập tức
                                            with log_container.expander(f"**{agent}** ➔ {action}", expanded=False):
                                                st.markdown(details)
                                        except Exception:
                                            pass
                                    last_lines = len(lines)
                        except Exception:
                            pass
                    await asyncio.sleep(0.5)
                
                return agent_task.result()

            # Chạy hàm async
            answer = asyncio.run(run_and_monitor())
            
            latency = time.time() - start_time
            status.update(label=f"Hoàn tất phân tích trong {latency:.2f} giây!", state="complete", expanded=False)
        
        # Hiển thị câu trả lời chính
        st.markdown("### Kết quả Tổng hợp")
        st.markdown(answer)

        # Lưu tin nhắn bot
        st.session_state.messages.append({
            "role": "assistant", 
            "content": answer,
            "latency": latency
        })
