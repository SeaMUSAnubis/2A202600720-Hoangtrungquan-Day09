# Hướng Dẫn Hoàn Thành Các Bài Tập Chưa Xong (Codelab)

Sau khi kiểm tra toàn bộ project của bạn, tôi thấy bạn đã xuất sắc hoàn thành tất cả các bài tập chính từ **Phần 1 đến Phần 5**, bao gồm cả việc viết file `Answer_state5.md` rất chi tiết! Tuy nhiên, bạn vẫn còn bỏ ngỏ phần **Bài Tập Nâng Cao (Tự Học)** và **Bài Tập Cộng Điểm**. 

Dưới đây là hướng dẫn chi tiết giúp bạn hoàn thiện nốt các phần này.

---

## 1. Bài Tập Cộng Điểm

### 1.1. Viết Code HTML File để demo tương tác của các Agent (Stage 4/5)
**Mục tiêu:** Tạo một giao diện UI (ví dụ sử dụng chat UI) để gọi tới Customer Agent (hoặc một API wrapper) thay vì dùng Terminal (`test_client.py`).

**Hướng dẫn thực hiện:**
- Bạn có thể tạo một file `index.html` trong thư mục gốc.
- Sử dụng framework như Bootstrap hoặc Tailwind CSS qua CDN để làm giao diện Chat đơn giản.
- Khởi tạo một HTTP Server nhỏ (có thể dùng FastAPI hoặc Flask) bọc lại lệnh gọi A2A Protocol. Thay vì `test_client.py` in ra màn hình, server này sẽ nhận API HTTP từ giao diện web (dùng `fetch()`) rồi gọi hệ thống Agent và trả kết quả về web.
- (Tùy chọn) Stream kết quả về web để tạo cảm giác "typing" chân thực giống ChatGPT.

### 1.2. Tính toán và Tối ưu Latency cho Stage 5
**Yêu cầu:** Trả lời 2 câu hỏi về độ trễ (Latency) và đề xuất phương án giảm độ trễ.

**Hướng dẫn thực hiện:**
1. **Đo Latency:**
   Mở file `test_client.py`, import thư viện `time`. Đặt `start_time = time.time()` trước khi gọi agent, và tính `total_time = time.time() - start_time` sau khi nhận kết quả. Chạy script và ghi nhận kết quả (VD: 8.5 giây).

2. **Đề xuất phương án giảm Latency:**
   - **Cách 1: Chuyển sang model nhỏ & nhanh hơn:** Đổi `OPENROUTER_MODEL` trong `.env` sang model tốc độ cao (ví dụ `gpt-4o-mini`, `claude-3-haiku` hoặc `llama-3.1-8b`).
   - **Cách 2: Bật tính năng Streaming:** Thay vì đợi Law Agent tổng hợp toàn bộ kết quả rồi mới trả về một cục lớn, bạn có thể triển khai Streaming để trả về từng chunk (từng chữ) ngay lập tức cho người dùng, làm giảm TTFB (Time to First Byte).
   - **Cách 3: Caching:** Lưu lại các câu hỏi pháp lý thường gặp. Nếu Customer Agent nhận được câu hỏi giống hệt, nó có thể lấy ngay kết quả từ Cache mà không cần gọi Law Agent.
   
   *Demo:* Sau khi đổi model sang model nhỏ hơn, chạy lại script và ghi nhận thời gian giảm được (ví dụ từ 8.5s xuống còn 3.2s). Ghi kết quả vào file markdown.

---

## 2. Bài Tập Nâng Cao (Tự Học)

### Challenge 1: Thêm memory / conversation history
**Mục tiêu:** Giúp Agent nhớ các câu hỏi trước.
**Hướng dẫn:** Thay vì chỉ truyền vào một string `question`, bạn cần thay đổi kiểu dữ liệu của `state` trong LangGraph để truyền vào một List các Messages (`list[BaseMessage]`). Khi trả lời, nối thêm `HumanMessage` và `AIMessage` vào mảng này. Trong LangGraph, bạn có thể truyền thêm `checkpointer=MemorySaver()` khi biên dịch (compile) graph để lưu trữ trạng thái hội thoại.

### Challenge 2: Add authentication
**Mục tiêu:** Thêm API key auth cho A2A endpoints.
**Hướng dẫn:** Trong mã nguồn A2A (ví dụ framework HTTP mà các agent đang chạy), bạn có thể thêm một Dependency/Middleware để kiểm tra Header `Authorization: Bearer <API_KEY>`. Khi các agent gọi lẫn nhau, yêu cầu chúng gắn thêm Header này vào request.

### Challenge 3: Implement retry logic
**Mục tiêu:** Tự động retry với exponential backoff khi một agent fail.
**Hướng dẫn:** Sử dụng thư viện `tenacity` của Python. Đặt decorator `@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))` lên trên hàm gọi HTTP request giữa các agent để khi kết nối bị lỗi hoặc timeout, agent tự động thử lại tối đa 3 lần.

### Challenge 4: Monitoring & Observability
**Mục tiêu:** Tích hợp LangSmith để theo dõi các tác vụ Agent.
**Hướng dẫn:** 
- Đăng ký tài khoản tại `smith.langchain.com`.
- Thêm các biến môi trường vào `.env`:
  ```env
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_API_KEY=your_langchain_api_key
  LANGCHAIN_PROJECT=MultiAgent_Project
  ```
- Khởi chạy lại project. Toàn bộ trace về các lời gọi LLM, độ trễ từng Node, tokens tiêu thụ sẽ được tự động đồng bộ và hiển thị trên dashboard LangSmith!
