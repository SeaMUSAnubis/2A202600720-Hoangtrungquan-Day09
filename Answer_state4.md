# Giải thích Code Stage 4 (Multi-Agent System)

### 1. Giải thích các khái niệm trong LangGraph:
- **`class State(TypedDict)` là state dùng chung:** Đóng vai trò như "bộ nhớ trung tâm" (Shared Memory) của toàn bộ hệ thống. Bất kỳ node (agent) nào chạy cũng sẽ đọc dữ liệu từ State này (ví dụ: lấy `question`) và khi chạy xong sẽ trả về một phần dữ liệu để cập nhật lại vào State (ví dụ: `tax_result`). Các trường dùng hàm reducer như `Annotated[str, _last_wins]` để chỉ định cách ghi đè dữ liệu (giữ lại giá trị mới nhất).
- **Các node agent (law_agent, tax_agent, compliance_agent, privacy_agent):** Mỗi node thực chất là một hàm Python đại diện cho một chuyên gia. Bên trong node này có thể tự chứa một LLM gọi các tools riêng biệt để phục vụ cho một chuyên môn cụ thể.
- **`Send()` API dùng để dispatch task song song:** Thay vì dùng `add_edge()` tĩnh rẽ nhánh 1-1 thông thường, `Send("tên_node", payload)` cho phép ta trả về **một danh sách các node** cần chạy tại thời điểm runtime (dynamic routing). LangGraph sẽ tự động lấy danh sách này và kích hoạt các node (như tax, compliance, privacy) chạy **cùng lúc (in parallel)**. Việc này giúp tiết kiệm tối đa thời gian chờ kết quả API.
- **`graph.add_node()` và `graph.add_edge()`:** `add_node` dùng để đăng ký một trạm xử lý (một bước/node) vào đồ thị, còn `add_edge` và `add_conditional_edges` dùng để vẽ các mũi tên nối các trạm lại với nhau, tạo thành luồng đi của dữ liệu từ lúc bắt đầu (`entry_point`) cho đến khi kết thúc (`END`).

---

### 2. Kết quả phần thực hành:
Trong file `stages/stage_4_milti_agent/main.py`, đã thực hiện thành công toàn bộ các yêu cầu của bài tập:

1. Thêm trường `needs_privacy` và `privacy_result` vào `LegalState`.
2. Tạo tool `search_privacy_law` chứa kiến thức cơ bản về GDPR.
3. Tạo node `call_privacy_specialist` chuyên môn xử lý luật về quyền riêng tư.
4. Cập nhật node Router (`check_routing`) để ép kiểu hệ thống: nếu câu hỏi chứa các từ khoá **data, privacy, gdpr, dữ liệu**, biến `needs_privacy = True` sẽ được kích hoạt. Lệnh `route_to_specialists` sẽ dispatch `Send("call_privacy_specialist", state)`.
5. Bổ sung node này vào luồng đồ thị qua `add_node` và nối mũi tên vào bộ gom kết quả qua `add_edge("call_privacy_specialist", "aggregate")`.
6. Sửa câu hỏi mẫu thành câu tiếng Việt: *"Nếu một công ty vi phạm hợp đồng, trốn thuế và rò rỉ dữ liệu người dùng vi phạm GDPR, thì hậu quả pháp lý và quy định là gì?"*

**Kết quả khi chạy đồ thị:**
Log hệ thống báo về cho thấy Router đã phân tích thành công:
```text
[Node: check_routing] needs_tax=True, needs_compliance=True, needs_privacy=True
```
Sau đó, thay vì chạy tuần tự, cả 3 Agents đã được kích hoạt chạy song song:
```text
  [Node: call_tax_specialist] Tax specialist agent starting...
  [Node: call_compliance_specialist] Compliance specialist agent starting...
  [Node: call_privacy_specialist] Privacy specialist agent starting...

  [Node: call_privacy_specialist] Done (1325 chars)
  [Node: call_tax_specialist] Done (635 chars)
  [Node: call_compliance_specialist] Done (708 chars)
```

Ở bước cuối cùng, `aggregate` (Luật sư trưởng) đã tổng hợp kết quả của cả 3 cấp dưới thành một văn bản báo cáo cuối cùng hoàn chỉnh bằng tiếng Việt (nếu model sinh ra tiếng Việt).
