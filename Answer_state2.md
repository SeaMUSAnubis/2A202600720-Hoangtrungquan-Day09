# Giải thích Code Stage 2

### 1. `@tool` decorator dùng ở đâu và để làm gì?
- **Vị trí:** Decorator `@tool` được đặt ngay phía trên các hàm Python thông thường (như `search_legal_database`, `calculate_damages` và `check_statute_of_limitations`).
- **Tác dụng:** Nó là một công cụ của Langchain dùng để biến một hàm Python thành một đối tượng `Tool`. Langchain sẽ tự động đọc **Docstring** (đoạn mô tả ngắn dưới tên hàm) và **Type hints** (như `case_type: str`) để tự động tạo ra một JSON Schema. Nhờ có schema này, LLM mới biết được tool này có tác dụng gì, khi nào nên sử dụng và cần cung cấp tham số đầu vào nào.

### 2. `LEGAL_KNOWLEDGE` được tổ chức như thế nào?
- Nó được tổ chức dưới dạng một danh sách (List) các Dictionary (hay còn gọi là danh sách các Object). Đây là cách mô phỏng lại một Vector Database tĩnh dùng cho mô hình RAG (Retrieval-Augmented Generation) siêu cơ bản.
- Mỗi bản ghi (Dictionary) bao gồm:
  - `id`: Định danh duy nhất cho điều luật/văn bản.
  - `keywords`: Danh sách các từ khóa. Ở hàm `search_legal_database`, ta dùng từ khóa trong câu query của LLM đem so khớp với mảng keywords này để tìm ra bản ghi phù hợp.
  - `text`: Cung cấp thông tin chi tiết về điều luật mà LLM sẽ đọc để đưa vào câu trả lời cuối cùng.

### 3. LLM được gắn tools bằng `.bind_tools()` ra sao?
- Lệnh `llm_with_tools = llm.bind_tools(TOOLS)` giúp "cột chặt" (bind) danh sách các Tools đã định nghĩa vào mô hình ngôn ngữ.
- **Bản chất:** Khi gọi API tới LLM (qua OpenRouter/OpenAI/Anthropic), lệnh bind này sẽ chuyển đổi mảng `TOOLS` thành cấu trúc JSON Tools chuẩn và đính kèm vào payload gửi đi. Nhờ vậy, LLM sẽ nhận thức được sự tồn tại của các công cụ và nó có quyền quyết định **sinh ra câu lệnh gọi tool (tool call)** thay vì chỉ trả lời bằng chữ như Stage 1. 

---

### Kết quả phần thực hành thêm
Trong file `stages/stage_2_rag_tools/main.py`, đã thực hiện thành công các bước:

1. **Thêm `vn_labor_law` vào `LEGAL_KNOWLEDGE`:** Mô tả quy định của luật lao động Việt Nam.
2. **Tạo mới tool `check_statute_of_limitations`:** Trả về thời hiệu khởi kiện tương ứng với từng loại tranh chấp.
3. **Thêm tool và test:** Khi đưa vào câu hỏi pháp lý mới, mô hình LLM đã nhận diện và thực hiện đồng thời 2 tool call (1 để tìm kiếm luật trong `search_legal_database`, 1 để kiểm tra thời hạn bằng `check_statute_of_limitations`), qua đó trả lời chính xác và đầy đủ ngữ cảnh pháp lý.
