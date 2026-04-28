# Phân Tích Chu Trình Đồ Thị (Euler & Hamilton)

## 📖 Giới thiệu chung
Đây là một ứng dụng giao diện web tương tác được xây dựng bằng **Streamlit** kết hợp với Python. Ứng dụng hỗ trợ người dùng tự tay xây dựng mạng lưới đồ thị thông qua ma trận kề và tự động giải quyết hai bài toán kinh điển trong Lý thuyết đồ thị:
*   **Chu trình Euler:** Tìm kiếm một đường đi khép kín đi qua toàn bộ các cạnh của đồ thị, trong đó mỗi cạnh được đi qua chính xác một lần.
*   **Chu trình Hamilton:** Tìm kiếm một đường đi khép kín (vòng lặp) đi qua toàn bộ các đỉnh của đồ thị, mỗi đỉnh được ghé thăm chính xác một lần trước khi quay về điểm xuất phát.

## ✨ Các tính năng nổi bật
1. **Khởi tạo động:** Cho phép tùy chỉnh số lượng đỉnh của đồ thị (từ 3 đến 20 đỉnh). Ma trận kề sẽ tự động được khởi tạo với các giá trị 0.
2. **Xây dựng cạnh linh hoạt:** Hỗ trợ đồ thị vô hướng và có hướng (tùy chỉnh cạnh 1 chiều hoặc 2 chiều) trực tiếp vào đồ thị bằng cách chỉ định đỉnh nguồn và đỉnh đích.
3. **Trực quan hóa Ma trận kề:** Bảng ma trận kề được hiển thị và cập nhật liên tục theo thời gian thực mỗi khi có một cạnh mới được ghi nhận.
4. **Hệ thống Lọc thông minh:** Ứng dụng tự động đánh giá các điều kiện tồn tại của đồ thị và **chỉ hiển thị các đỉnh đạt tiêu chuẩn** để làm điểm xuất phát (Ví dụ: Đối với chu trình Euler, mọi đỉnh trong đồ thị liên thông bắt buộc phải có bậc chẵn đối với đồ thị vô hướng, hoặc bậc vào bằng bậc ra đối với đồ thị có hướng).
5. **Thuật toán chuẩn tối ưu:** 
   * Sử dụng thuật toán **Hierholzer** để tìm chu trình Euler với độ phức tạp thời gian tuyến tính, đảm bảo hiệu suất cao.
   * Sử dụng thuật toán **Quay lui (Backtracking)** kết hợp cắt tỉa nhánh để dò tìm chính xác chu trình Hamilton.

## 💻 Yêu cầu hệ thống
Trước khi chạy ứng dụng, vui lòng đảm bảo máy tính của bạn đã được cài đặt:

- Python 3.7 trở lên
- Các thư viện Python được liệt kê trong file `requirements.txt`

Các thư viện chính bao gồm:

```txt
streamlit
pandas
```
## 🚀 Hướng dẫn cài đặt và chạy ứng dụng

### Bước 1: Tải các tệp mã nguồn 
Tải các tệp mã nguồn vào chung một thư mục trên máy tính.

### Bước 2: Mở cửa sổ dòng lệnh

Mở cửa sổ dòng lệnh phù hợp với hệ điều hành:

- Windows: Command Prompt hoặc PowerShell
- macOS/Linux: Terminal

Sau đó di chuyển đến thư mục chứa mã nguồn bằng lệnh:

```bash
cd duong-dan-den-thu-muc-du-an
```

### Bước 3: Cài đặt các thư viện cần thiết

Cài đặt các thư viện cần thiết bằng lệnh:

```bash
pip install -r requirements.txt
```

### Bước 4: Khởi chạy ứng dụng Streamlit

Khởi chạy ứng dụng Streamlit bằng lệnh:

```bash
streamlit run app.py
```

Ngay sau khi chạy lệnh, trình duyệt web của bạn sẽ tự động mở một tab mới, thường ở địa chỉ:

```text
http://localhost:8501
```

Đây là giao diện của ứng dụng.

---

## 🛠 Hướng dẫn Sử dụng (Workflow)

### Bước 1: Khởi tạo

Chọn dạng đồ thị và nhập số đỉnh của đồ thị bạn muốn phân tích.

### Bước 2: Nối cạnh

Lựa chọn đỉnh xuất phát `U` và đỉnh đến `V`.

Bấm **Thêm Cạnh Vào Đồ Thị**. Bạn có thể quan sát bảng ma trận kề bên dưới tự động thay đổi các giá trị.

### Bước 3: Phân tích

Lựa chọn bài toán bạn muốn giải:

- Chu trình Euler
- Chu trình Hamilton

Lựa chọn đỉnh bắt đầu. Nếu đồ thị của bạn vi phạm điều kiện, danh sách chọn đỉnh sẽ bị khóa lại và hiển thị cảnh báo để bạn bổ sung thêm cạnh.

Bấm **Kết Xuất Kết Quả** để hệ thống tính toán và in ra lộ trình di chuyển chi tiết.