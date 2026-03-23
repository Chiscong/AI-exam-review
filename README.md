# AI Quiz Master - Hệ Thống Ôn Tập Trắc Nghiệm Thông Minh 🚀

Ứng dụng web cho phép người dùng tải lên các tệp tài liệu (Word hoặc PDF), sau đó sử dụng Trí tuệ nhân tạo (Google Gemini AI) để tự động trích xuất và tạo các câu hỏi trắc nghiệm tương tác.

## ✨ Tính năng nổi bật
- 📄 **Nhập liệu đa dạng:** Hỗ trợ đọc file `.docx` và `.pdf`.
- 🤖 **AI thông minh:** Tự động nhận diện câu hỏi, các lựa chọn và đáp án đúng (đặc biệt là các câu có dấu `*`).
- ⚡ **Phản hồi tức thì:** Hiển thị đáp án Đúng/Sai ngay sau khi chọn và giải thích đáp án đúng.
- 📊 **Tính điểm Real-time:** Theo dõi điểm số ngay trong quá trình làm bài.
- 🔄 **Điều hướng linh hoạt:** Cho phép xem lại các câu hỏi trước đó hoặc nhảy đến câu tiếp theo.
- 🖼️ **Hỗ trợ hình ảnh:** Hiển thị hình ảnh minh họa cho câu hỏi (nếu có trong tài liệu).
- 📱 **Giao diện hiện đại:** Thiết kế với Tailwind CSS, tối ưu cho cả máy tính và thiết bị di động.

## 🛠️ Công nghệ sử dụng
- **Backend:** Python, Flask
- **AI:** Google Gemini API
- **Document Processing:** python-docx, pdfplumber
- **Frontend:** HTML5, Tailwind CSS, JavaScript (ES6+)

## 🚀 Hướng dẫn cài đặt

### 1. Tải dự án về máy
```bash
git clone https://github.com/username/ai-quiz-master.git
cd ai-quiz-master
```
### 2. Tạo và kích hoạt môi trường ảo (Khuyên dùng)
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```
### 3. Cài đặt thư viện 
```
pip install -r requirements.txt
```
### 4. Cấu hình API key
tạo 1 file .env
```
GEMINI_API_KEY=<key của bạn>
```
Lấy API Key tại: https://aistudio.google.com/api-keys
### 5. Chạy ứng dụng
```
python app.py
```
## 5.1 Để thoát khỏi môi trường ảo: 
Khi bạn làm việc xong và muốn quay lại môi trường bình thường của máy tính, chỉ cần gõ:
```
deactivate
```
## 5.2 Lỗi "Execution Policy" trên Windows PowerShell:
Nếu bạn chạy lệnh activate trên PowerShell mà bị báo lỗi đỏ (Security Error), hãy chạy lệnh này trước:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Truy cập: http://127.0.0.1:5000 trên trình duyệt của bạn.
### 📁 Cấu trúc thư mục
├── app.py              # File xử lý logic chính (Backend)
├── .env                # Lưu trữ mã bí mật API Key
├── requirements.txt    # Danh sách thư viện cần cài đặt
├── static/             # Thư mục chứa hình ảnh và CSS
│   └── quiz_images/    # Hình ảnh trích xuất từ tài liệu
├── templates/          # Giao diện người dùng
│   └── index.html      # Trang chủ ứng dụng
└── uploads/            # Thư mục lưu file tạm thời khi người dùng upload
📝 Lưu ý
Để AI nhận diện tốt nhất, file tài liệu của bạn nên có cấu trúc:
Câu hỏi rõ ràng.
Các đáp án bắt đầu bằng A, B, C, D.
Đáp án đúng được đánh dấu bằng dấu sao (*) ở đầu.
🤝 Đóng góp
Mọi ý tưởng đóng góp hoặc báo lỗi vui lòng mở một Issue hoặc gửi Pull Request. Rất mong nhận được sự phản hồi từ bạn!
---

### Cách sử dụng các file này:
1. **requirements.txt:** Bạn copy nội dung trên, tạo file mới tên `requirements.txt` trong thư mục dự án. Để cài đặt, bạn gõ lệnh: `pip install -r requirements.txt`.
2. **README.md:** Bạn copy nội dung trên, tạo file mới tên `README.md`. Khi bạn tải lên GitHub, GitHub sẽ tự động hiển thị nội dung này thành một trang giới thiệu đẹp mắt bên dưới danh sách file. 

Bạn còn muốn bổ sung thêm thông tin gì cho dự án không?