import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import sys
from pathlib import Path

# Thêm Lab_Assignment vào path
sys.path.append(str(Path(__file__).resolve().parent))
from graph import app_graph

load_dotenv()

st.set_page_config(page_title="Supervisor - Workers Architecture", page_icon="🏢", layout="wide")
st.title("🏢 Multi-Agent Supervisor-Workers (Day 09 Assignment)")
st.markdown("Hệ thống nâng cấp Day 08 với 1 Supervisor điều phối 3 Workers độc lập: **Legal Worker**, **News Worker**, và **General Worker**.")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Form nhập tin nhắn
if prompt := st.chat_input("Nhập câu hỏi (VD: Xin chào / Tội buôn ma túy đi tù bao năm? / Có nghệ sĩ nào bị bắt không?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.info("👨‍💼 Supervisor đang phân tích câu hỏi để tìm đúng chuyên gia...")
        
        # Chạy đồ thị LangGraph
        inputs = {"messages": [HumanMessage(content=prompt)]}
        
        final_answer = ""
        try:
            for s in app_graph.stream(inputs, stream_mode="updates"):
                if "Supervisor" in s:
                    next_node = s["Supervisor"]["next"]
                    if next_node != "FINISH":
                        status_placeholder.warning(f"👨‍💼 Supervisor đã quyết định giao việc này cho chuyên gia: **{next_node}**")
                    else:
                        status_placeholder.success("✅ Nhiệm vụ đã hoàn thành!")
                elif "LegalWorker" in s:
                    final_answer = s["LegalWorker"]["messages"][-1].content
                    status_placeholder.success("🧑‍⚖️ Legal Worker đã phân tích xong pháp lý!")
                elif "NewsWorker" in s:
                    final_answer = s["NewsWorker"]["messages"][-1].content
                    status_placeholder.success("📰 News Worker đã lấy xong thông tin thực tế!")
                elif "GeneralWorker" in s:
                    final_answer = s["GeneralWorker"]["messages"][-1].content
                    status_placeholder.success("🤖 General Worker đã trả lời!")
        except Exception as e:
            final_answer = f"❌ Lỗi hệ thống: {e}"
            status_placeholder.error("Đã xảy ra lỗi!")
            
        st.markdown(final_answer)
        st.session_state.messages.append({"role": "assistant", "content": final_answer})
