# Hướng Dẫn Sử Dụng Hệ Thống Pháp Lý Multi-Agent (A2A Protocol)

Đây là tài liệu hướng dẫn sử dụng cho hệ thống tư vấn pháp lý phân tán đa tác nhân. Hệ thống được xây dựng mô phỏng một quy trình tư vấn chuyên nghiệp, trong đó có một **Luật sư trưởng** (Law Agent) đóng vai trò điều phối, phân chia công việc cho các **chuyên gia chuyên ngành** (Tax Agent, Compliance Agent) theo hình thức song song, thông qua giao thức **Agent-to-Agent (A2A)** của Google.

## 1. Yêu Cầu Cài Đặt
Để chạy được hệ thống, máy tính của bạn cần có:
- **Python:** Phiên bản 3.11 trở lên.
- **Trình quản lý gói `uv`:** Cài đặt thông qua lệnh `pip install uv` 
- **API Key OpenRouter:** Cần có để gọi các mô hình LLM. Bạn có thể đăng ký miễn phí tại [OpenRouter](https://openrouter.ai).

## 2. Cài Đặt Ban Đầu

1. **Tải mã nguồn và cài đặt thư viện:**
   Mở terminal và gõ các lệnh sau:
   ```bash
   git clone <repo-url>
   cd legal_multiagent
   uv sync
   ```

2. **Thiết lập biến môi trường:**
   Tạo file `.env` bằng cách copy từ file mẫu:
   ```bash
   cp .env.example .env
   ```
   Sau đó, mở file `.env` vừa tạo và điền khóa API của bạn vào:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-... (Thay bằng key của bạn)
   ```

## 3. Khởi Động Hệ Thống Phân Tán (Microservices)

Hệ thống hoạt động dưới kiến trúc phân tán gồm 5 dịch vụ (microservices) chạy độc lập trên các cổng mạng khác nhau. 

Bạn chỉ cần chạy 1 tệp kịch bản để khởi động tất cả:
```bash
# Trên Linux/macOS hoặc Git Bash trên Windows:
bash ./start_all.sh
```

**Chi tiết các dịch vụ được chạy:**
- `Port 10000`: **Registry Service** (Trung tâm danh bạ, các Agent phải báo cáo có mặt tại đây).
- `Port 10100`: **Customer Agent** (Người tiếp tân nhận yêu cầu từ người dùng).
- `Port 10101`: **Law Agent** (Luật sư trưởng trực tiếp phân tích yêu cầu).
- `Port 10102`: **Tax Agent** (Chuyên gia giải quyết vấn đề về Thuế).
- `Port 10103`: **Compliance Agent** (Chuyên gia Tuân thủ luật lệ và quy định).

## 4. Tương Tác Với Hệ Thống

Để thử nghiệm tính năng, hệ thống cung cấp 2 cách thức giao tiếp. Hãy mở thêm một cửa sổ Terminal mới (không tắt terminal đang chạy `start_all.sh`).

### Cách 1: Tương tác qua Giao diện Web (Streamlit) - Khuyên dùng
Cung cấp giao diện chat chuyên nghiệp, có hiển thị quá trình Agent suy nghĩ và định tuyến luồng dữ liệu (Real-time tracking).
```bash
streamlit run app.py
```
Sau lệnh này, trình duyệt sẽ tự động mở trang web (thường là `http://localhost:8501`). Bạn có thể nhập câu hỏi của mình vào ô chat.
*Ví dụ: "Hậu quả pháp lý nếu công ty vi phạm hợp đồng và trốn thuế là gì?"*

### Cách 2: Tương tác qua Command Line (CLI)
Dành cho việc test nhanh luồng dữ liệu dưới dạng log thô:
```bash
uv run python test_client.py
```
Ứng dụng sẽ gửi sẵn một câu hỏi và in ra chi tiết các gói tin, `trace_id` cùng câu trả lời cuối cùng trên màn hình Terminal.

## 5. Đặc Trưng Của Hệ Thống Khi Vận Hành
- **Làm việc nhóm song song (Parallel Execution):** Nếu câu hỏi của bạn đụng đến nhiều chuyên ngành (ví dụ: vừa Thuế, vừa Quy định dữ liệu), Law Agent sẽ gửi yêu cầu hỏi các chuyên gia cùng một lúc thay vì phải đợi người này xong mới hỏi người kia.
- **Tự động tìm kiếm (Dynamic Discovery):** Các Agent tìm thấy nhau hoàn toàn tự động thông qua Registry Service, không bị gắn chết địa chỉ IP/Port trong mã nguồn.
- **Chịu lỗi linh hoạt (Fault Tolerance):** 
  - *Thử nghiệm:* Bạn hãy thử tắt (bấm Ctrl+C) riêng lẻ cửa sổ của `Tax Agent`. 
  - *Kết quả:* Hệ thống sẽ vẫn vận hành! Law Agent chỉ mất liên lạc với Tax Agent nhưng vẫn gộp các câu trả lời lấy được từ Compliance Agent để báo cáo lại cho bạn.

## 6. Lộ Trình Học Và Demo Cho Sinh Viên (Codelab)
Hệ thống này cũng là một bộ giáo trình thu nhỏ. Trong thư mục `stages/`, có các script tương đương 5 cấp độ tiến hóa của một ứng dụng LLM. Bạn có thể chạy riêng từng cấp độ (không cần khởi động `start_all.sh`) để học tập:

- **Stage 1 (Direct LLM):** Gọi AI đơn giản nhất: `uv run python stages/stage_1_direct_llm/main.py`
- **Stage 2 (RAG & Tools):** AI biết đọc tài liệu cơ bản: `uv run python stages/stage_2_rag_tools/main.py`
- **Stage 3 (ReAct Agent):** AI tự suy nghĩ để dùng tools: `uv run python stages/stage_3_single_agent/main.py`
- **Stage 4 (Multi-Agent - Chung file):** Chạy nhiều Agent bằng LangGraph StateGraph: `uv run python stages/stage_4_multi_agent/main.py`

## 7. Bài Tập Lab Assignment (Dành cho Day 09)
Bản nâng cấp sử dụng **Supervisor-Workers** (1 quản đốc - nhiều công nhân) đã được thiết kế sẵn.
Để kiểm tra bài tập này, bạn di chuyển vào thư mục `Lab_Assignment` và khởi động UI:
```bash
cd Lab_Assignment
streamlit run app.py
```

---
*Tham khảo thư mục `docs/` để xem các sơ đồ kiến trúc hệ thống (Architecture diagrams).*