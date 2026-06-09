# Hướng Dẫn Sử Dụng - Lab Assignment (Day 09)

## 1. Giới Thiệu
Dự án trong thư mục `Lab_Assignment` này là bài tập thực hành nâng cấp dựa trên kiến thức Day 08. 
Mục tiêu là xây dựng một hệ thống đa tác nhân sử dụng mẫu thiết kế **Supervisor - Workers Pattern** bằng thư viện LangGraph. 
Mô hình bao gồm 1 Người điều phối (Supervisor) chịu trách nhiệm phân tích ý định của người dùng và điều phối nhiệm vụ cho 3 Chuyên gia (Workers) hoạt động độc lập.

## 2. Kiến Trúc Hệ Thống
Hệ thống bao gồm các tác nhân (Agents) sau:
- **Supervisor**: Nhận câu hỏi từ người dùng, đánh giá yêu cầu và định tuyến (routing) công việc cho đúng chuyên gia phù hợp nhất, hoặc kết thúc (FINISH) nếu đã hoàn thành.
- **Legal Worker**: Chuyên gia pháp lý. Phụ trách giải đáp các câu hỏi về quy định pháp luật, điều luật và mức hình phạt.
- **News Worker**: Chuyên gia tin tức. Xử lý các câu hỏi liên quan đến sự kiện thực tế, cập nhật vụ án, hoặc tin tức về người nổi tiếng.
- **General Worker**: Trợ lý đa năng. Nhận các tác vụ giao tiếp thông thường, chào hỏi hoặc các câu hỏi không thuộc chuyên môn của 2 chuyên gia trên.

## 3. Yêu Cầu Cài Đặt
Môi trường thực thi sử dụng chung với dự án mẹ (thư mục gốc):
- Đã cài đặt thư viện bằng lệnh `uv sync`.
- Tồn tại tệp `.env` chứa khóa `OPENROUTER_API_KEY`. (Ví dụ: `OPENROUTER_API_KEY=sk-or-...`).
- Mô hình mặc định (có thể thay đổi trong cấu hình): `gpt-4o-mini` hoặc `google/gemini-2.5-flash`.

## 4. Cách Khởi Chạy
Bài tập này được tích hợp sẵn một giao diện người dùng trực quan bằng **Streamlit**.

Di chuyển vào thư mục bài tập và khởi chạy:
```bash
# Đảm bảo bạn đang đứng ở thư mục gốc của project trước khi CD
cd Lab_Assignment
streamlit run app.py
```
Sau khi lệnh chạy thành công, một trình duyệt web sẽ tự động mở lên tại địa chỉ `http://localhost:8501`.

## 5. Hướng Dẫn Tương Tác Thử Nghiệm
Trên giao diện Streamlit, bạn hãy thử nhập các câu hỏi thuộc các lĩnh vực khác nhau để quan sát cách Supervisor làm việc. Giao diện có tích hợp UI theo dõi tiến trình (Real-time Flow tracking) giúp bạn thấy rõ quyết định của Supervisor.

Các mẫu câu hỏi bạn có thể thử:
1. *"Xin chào, bạn có thể giúp tôi được không?"* 
 **Kỳ vọng:** Supervisor sẽ giao nhiệm vụ cho **General Worker**.
2. *"Hành vi tàng trữ trái phép chất ma túy đi tù bao nhiêu năm?"*
 **Kỳ vọng:** Supervisor sẽ giao nhiệm vụ cho **Legal Worker**.
3. *"Gần đây có ca sĩ hay diễn viên nào dính líu đến pháp luật không?"*
 **Kỳ vọng:** Supervisor sẽ giao nhiệm vụ cho **News Worker**.

Chúc bạn thực hành vui vẻ!
