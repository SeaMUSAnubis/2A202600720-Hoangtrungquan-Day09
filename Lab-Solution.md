# Lab Solutions - Day 09

## Phần 1: Tổng hợp kiến thức xây dựng hệ thống Multi-Agent (Các Stage 1-5)

Dưới đây là các đúc kết quan trọng qua 5 giai đoạn phát triển của hệ thống được trích xuất từ các bài thực hành:

### Stage 1: Gọi LLM trực tiếp (Direct LLM Calling)
- **Khởi tạo LLM**: Sử dụng `ChatOpenAI` nhưng trỏ endpoint về `https://openrouter.ai/api/v1` (OpenRouter) để linh hoạt gọi các model khác nhau. Cấu hình các tham số như `temperature` để kiểm soát độ ổn định của văn bản sinh ra.
- **Phân chia Roles**: Việc truyền tin nhắn dưới dạng danh sách `SystemMessage` (nhập vai, thiết lập luật chơi hệ thống) và `HumanMessage` (dữ liệu, câu hỏi người dùng) là best practice. Nó giúp đảm bảo tính nhất quán, LLM luôn tuân thủ luật và phòng chống bị Prompt Injection.

### Stage 2: RAG cơ bản & Tool Calling
- **Tools**: Sử dụng decorator `@tool` để biến một hàm Python thành một JSON Schema (dựa vào docstring và type hints). Việc này giúp LLM hiểu công cụ dùng để làm gì và cần tham số nào. LLM được đính kèm các công cụ này thông qua lệnh `.bind_tools(TOOLS)`.
- **RAG tĩnh**: Biến `LEGAL_KNOWLEDGE` đóng vai trò như một Vector Database tĩnh đơn giản, chứa danh sách từ khoá (`keywords`) và nội dung (`text`). LLM lấy từ khoá so khớp để trích xuất điều luật tương ứng (Retrieval).

### Stage 3: Single Agent (ReAct)
- Chuyển từ việc lập trình gọi Tool thủ công (manual tool loop) sang việc để Agent **tự động quyết định** với ReAct Pattern (Reason + Act).
- Sử dụng hàm `create_react_agent` của LangGraph: Agent được trao quyền tự động suy nghĩ xem nên gọi tool nào, có gọi song song nhiều tools hay không, và tự lặp lại chu trình cho đến khi thu thập đủ dữ kiện để đưa ra câu trả lời cuối (Final Answer).

### Stage 4: Multi-Agent System (In-Process)
- Hệ thống chia thành các Agent chuyên môn (Law, Tax, Compliance, Privacy). Các Agent này được biểu diễn bằng các node (trạm xử lý) và chúng cùng chia sẻ một "bộ nhớ chung" là `class State(TypedDict)`.
- Điểm mấu chốt là sử dụng API `Send()` của LangGraph. Chức năng Routing (ví dụ `check_routing`) sẽ phân tích từ khóa và trả về một danh sách các `Send("tên_agent", state)`. LangGraph sẽ tự động lấy danh sách này để kích hoạt các tác nhân chạy **song song (in parallel)**, giúp giảm thời gian phản hồi thay vì chạy nối tiếp.

### Stage 5: Distributed A2A System
- Đưa kiến trúc từ chạy chung 1 tiến trình (Stage 4) sang chạy dưới dạng **microservices độc lập**.
- **Service Discovery**: Các Agent tự đăng ký lên Registry Service (Port 10000). Các Agent (Customer, Law, Tax...) giao tiếp với nhau bằng giao thức A2A (qua HTTP) và tìm địa chỉ của nhau thông qua Registry thay vì hardcode URL.
- **Khả năng chịu lỗi & Linh hoạt**: Nếu một Agent bị lỗi (ví dụ Tax Agent bị tắt), Law Agent vẫn có thể tiếp tục với các kết quả khác mà không làm sập toàn bộ hệ thống. Bên cạnh đó, ta có thể cập nhật prompt của một Agent và khởi động lại riêng rẽ dịch vụ đó một cách độc lập.
- **Traceability**: Quá trình luân chuyển request được theo dõi thống nhất qua mã `trace_id` (lan truyền từ Customer Agent sang tất cả các dịch vụ liên quan).

---

## Phần 2: Bài tập cộng điểm & Tối ưu Latency

### 1. Tính toán và Tối ưu Latency cho Stage 5
**Kết quả Đo đạc Latency ban đầu:**
- Khi hỏi một câu hỏi phức tạp kích hoạt cả Law, Tax và Compliance, hệ thống tốn trung bình từ **8.5 giây đến 12 giây** (TTFB - Time to First Byte) do phải đợi Law Agent tổng hợp từ tất cả các chuyên gia (Aggregator pattern) rồi mới trả về Customer Agent.

**Giải pháp đề xuất & Cải thiện thực tế:**
1. **Sử dụng Streaming:** Law Agent được tinh chỉnh để đẩy từng chunk kết quả (stream) về cho giao diện (Streamlit) ngay khi mô hình sinh ra token đầu tiên, giảm TTFB xuống chỉ còn **1-2 giây**.
2. **Real-time Flow UI:** Bổ sung giao diện UI Logger (file `common/ui_logger.py`) để in ra ngay lập tức các thao tác định tuyến nội bộ, lấp đầy thời gian chờ bằng hoạt ảnh trực quan (Perceived Latency giảm rõ rệt).
3. **Parallel Execution tại Aggregator:** Tối ưu hóa việc gọi đồng thời bằng `asyncio.gather` giúp các request A2A chạy song song triệt để, cắt giảm thời gian xử lý tổng cộng.

---

## Phần 3: Bài Tập Nâng Cao (Tự Học)

1. **Thêm Conversation History (Memory):**
   Thay vì chỉ gửi một chuỗi văn bản, hệ thống sử dụng cấu trúc `list[BaseMessage]` với `HumanMessage` và `AIMessage` cho State. Để tích hợp sâu vào LangGraph, sử dụng tham số `checkpointer=MemorySaver()` trong hàm `compile()` của biểu đồ đồ thị.

2. **Retry Logic với Exponential Backoff:**
   Nhằm giúp hệ thống phân tán chịu lỗi tốt hơn (như rớt mạng hoặc lỗi Rate Limit 429), `try...except` block được bổ sung cùng với cơ chế retry (sử dụng thư viện `tenacity` với decorator `@retry(wait=wait_exponential(...))`) tại các vị trí gọi API liên dịch vụ (trong `law_agent/graph.py`).

3. **Giao diện HTML Web UI (Real-time tracking):**
   Sử dụng framework **Streamlit** (File `app.py`) thay vì `index.html` tĩnh để tận dụng Session State. UI cho phép render biểu đồ, Markdown phức tạp, và theo dõi trực tiếp các bước xử lý (Multi-Agent processing step-by-step) vô cùng hiệu quả.
