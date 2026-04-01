# 🎓 BTree Quản Lý Sinh Viên

Dự án ứng dụng web quản lý sinh viên sử dụng cấu trúc dữ liệu **B-Tree (Bậc 3)** làm chỉ mục để tối ưu tốc độ tìm kiếm. 

Ứng dụng được xây dựng bằng **Python Flask** (Backend) và **HTML/CSS/JS thuần** (Frontend) với thiết kế giao diện Glassmorphism hiện đại.

## ✨ Tính Năng Nổi Bật
- **Thêm Sinh Viên**: Điền thông tin (Mã SV, Họ và Tên, Giới tính) để thêm sinh viên mới.
- **Xóa Sinh Viên**: Xóa trực tiếp thông tin sinh viên để quan sát sự cân bằng lại (re-balancing) của chỉ mục B-Tree.
- **Tìm Kiếm Nhanh**: Tìm kiếm sinh viên theo "Mã SV" hoặc "Họ Tên".
- **Trực Quan Hóa B-Tree**: Ứng dụng vẽ và minh họa sự thay đổi cấu trúc của cây B-Tree Bậc 3 trực quan trên web sau mỗi giao dịch cập nhật bảng.

## 🚀 Cấu trúc dữ liệu B-Tree (Order 3)
Cây B-Tree trong ứng dụng có cấu hình như sau:
- Node nhánh có tối đa **3 con** (children) và tối đa **2 khóa** (keys).
- Cấu trúc tự động điều chỉnh cân bằng để đảm bảo thời gian truy xuất hiệu quả.
- Tự động gộp / chia nhỏ (split root, merge nodes) chuẩn chỉ theo thuật toán bậc 3.
- Xử lý các khóa trùng lặp (ví dụ: tìm qua Họ tên) thông qua việc phân vùng một mảng kết quả ID trên từng node.

## 🛠 Hướng Dẫn Cài Đặt Và Khởi Chạy

1. **Tải mã nguồn (Clone repository)**
   ```bash
   git clone https://github.com/dpduy123/BTreeQuanLySinhVien.git
   cd BTreeQuanLySinhVien
   ```

2. **Cài đặt thư viện môi trường cần thiết**
   Ứng dụng yêu cầu `Python 3` trở lên:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Khởi động server ứng dụng REST API**
   ```bash
   python3 app.py
   ```

4. **Trải nghiệm ứng dụng**
   Mở trình duyệt web của bạn và truy cập trực tiếp bằng địa chỉ theo mặc định: 
   👉 **[http://127.0.0.1:8888](http://127.0.0.1:8888)**

## 📁 Cấu Trúc Mã Nguồn Cơ Bản
```text
.
├── app.py              # File chạy ứng dụng backend xử lý routing
├── btree.py            # Code cấu trúc cốt lõi BTree order 3
├── requirements.txt    # Danh sách các thư viện Python cài đặt
├── templates/          # Chứa file cấu trúc HTML
│   └── index.html      # Giao diện chính của ứng dụng
└── static/             # Chứa CSS & JS tĩnh
    ├── script.js       # Xử lý logic thao tác DOM và vẽ cây BTree
    └── style.css       # File CSS dùng kiến trúc màu gradient hiện đại
```
