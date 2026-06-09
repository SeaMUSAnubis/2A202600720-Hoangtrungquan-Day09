# Giải thích Code Stage 3

### Sự khác nhau giữa Stage 2 và Stage 3
- **Stage 2 (Thủ công / Manual):** Bạn phải tự viết một vòng lặp (`loop`) hoặc luồng xử lý bằng code (như đoạn kiểm tra `if response.tool_calls: ...`). Hệ thống gọi LLM -> LLM bảo cần dùng tool -> Code của bạn thực thi tool -> Nạp kết quả lại cho LLM -> Trả về câu trả lời cuối. Luồng này có tính tĩnh và chỉ chạy theo một quy trình lập trình sẵn.
- **Stage 3 (Tự động / Autonomous):** Sử dụng **ReAct Agent** (Reason + Act). Bạn giao toàn bộ danh sách `TOOLS` cho Agent thông qua hàm `create_react_agent` của thư viện LangGraph. Từ lúc này, Agent hoàn toàn tự quyết định:
  - Có nên dùng tool hay không?
  - Dùng tool nào? Có thể dùng nhiều tool cùng một lúc không?
  - Sau khi tool trả kết quả, nếu thấy chưa đủ thông tin, nó có thể tự gọi tiếp các tool khác cho đến khi nào phân tích (Reason) thấy đã đủ dữ kiện để trả lời user (Final Answer). 
  - Toàn bộ luồng tự động này được đóng gói bên trong cơ chế của `create_react_agent`.

---

### Kết quả phần thực hành thêm
Trong file `stages/stage_3_single_agent/main.py`, đã thực hiện thành công các bước:

1. **Thêm Tool `search_case_law`:** Đã tạo một tool mới tìm kiếm án lệ (case law) giả lập có sẵn dữ liệu của các vụ án như *Hadley v. Baxendale (1854)* (về vi phạm hợp đồng) và thêm nó vào mảng `TOOLS`.
2. **Cập nhật QUESTION:** Đã thay đổi câu hỏi thành *"What are the legal consequences and relevant case law if a software company commits a material breach of contract?"*.
3. **Thêm tham số Debug:** Đối với `create_react_agent` của thư viện LangGraph, cờ `debug=True` đã được thêm vào (tương đương với `verbose=True` của Langchain AgentExecutor cũ). Khi đặt cờ này, ta có thể theo dõi toàn bộ quá trình suy nghĩ bên trong của Agent.

**Kết quả khi chạy:**
Nhờ có ReAct loop và chế độ debug, ta thấy rõ Agent đã tự nhận thức được việc phải gọi song song cả hai tool:
- `search_legal_database` (để tìm quy định hợp đồng chung)
- `search_case_law` (để tìm án lệ cụ thể)

Sau đó nó gom đủ dữ kiện và phân tích thành câu trả lời cuối cùng xuất sắc về hậu quả pháp lý của hành vi vi phạm hợp đồng.
