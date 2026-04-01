# BÁO CÁO BÀI TẬP / DỰ ÁN MÔN HỌC
**Tên đề tài:** Định tuyến Chỉ mục và Xây dựng ứng dụng Quản lý Sinh viên dùng Cấu trúc dữ liệu B-Tree
**Link ứng dụng (Live Demo):** [https://b-tree-quan-ly-sinh-vien.vercel.app/](https://b-tree-quan-ly-sinh-vien.vercel.app/)

---

## 1. Mục tiêu đề tài
Ứng dụng "Quản lý Sinh viên" được xây dựng nhằm hướng đến việc vận dụng những kiến thức lý thuyết về **Cấu trúc Dữ liệu và Giải thuật**, cụ thể là mô hình cây **B-Tree**, vào một bài toán lưu trữ dữ liệu thực tế.
Mục đích cốt lõi là minh họa quá trình **đánh chỉ mục (Indexing)** nhằm thay thế cho cách duyệt mảng thông thường (độ phức tạp O(N)), nâng cấp lên các hệ quản trị thuật toán tìm kiếm tối ưu với độ trễ thấp (O(logN)).

## 2. Yêu cầu đáp ứng
Dự án đã giải quyết và hiện thực hoá thành công các yêu cầu môn học đưa ra:
- **Thêm/Xoá một sinh viên:** Cập nhật thông tin trên cả cấu trúc bảng gốc (Base Table) và lập tức phản chiếu thuật toán lên các Indexing Nodes.
- **Tìm kiếm sinh viên:** Nhanh chóng định vị sinh viên bằng Mã SV hoặc Họ tên thông qua khả năng duyệt trên các nhánh B-Tree.
- **Mô phỏng B-Tree Bậc 3:** Đặt ràng buộc B-Tree ở **Bậc 3 (Order 3)** nhằm quan sát rõ nhất các điều kiện biên:
  - Tối đa 2 giá trị key / 1 node. Tối đa 3 nhánh con.
  - Xử lý các phép toán tách nút nhánh (Split Child) khi dôi dư lượng node.
  - Xử lý các thuật toán gộp nút nhánh (Merge) và mượn anh em (Borrow) khi một nút bị xoá rỗng nhưng chưa đạt chuẩn min keys.

## 3. Cấu trúc Công nghệ
- **Phân hệ thuật toán lõi (Backend):** 
  Lập trình toàn bộ thuật toán B-Tree từ căn bản (scratch) thông qua ngôn ngữ **Python** và thư viện **Flask**. Hệ thống chịu trách nhiệm giữ State dữ liệu nội bộ và tính toán Node.
- **Phân hệ Giao diện & Trực quan hóa (Frontend):**
  Sử dụng phong cách thiết kế UI Glassmorphism với **HTML / CSS / Javascript thuần**. Mã JS được thiết kế đặc biệt theo dạng Đệ quy DOM (Recursive DOM Rendering) để bóc tách tệp JSON và vẽ đồ thị mạng lưới Cây B-Tree ngay trên giao diện web.
- **Triển khai (Deployment):** 
  Phần mềm được đóng gói và tích hợp triển khai trên nền tảng **Vercel** giúp người dùng, giảng viên có thể test trực tiếp.

## 4. Hướng dẫn báo cáo và nghiệm thu
1. Thầy/Cô và các bạn truy cập link hệ thống Vercel: [https://b-tree-quan-ly-sinh-vien.vercel.app/](https://b-tree-quan-ly-sinh-vien.vercel.app/)
2. Tại màn hình chính, tiến hành Thêm 3-4 sinh viên bất kỳ.
3. Chú ý nửa dưới màn hình là 2 bộ mô phỏng cây **ID Index** và **Name Index** sẽ tự động trồi lên theo từng tầng phân nhánh của cây Bậc 3.
4. Kiểm thử tốc độ Tìm Kiếm và quan sát sự cân bằng lại của cây khi ấn Xoá học sinh trong Bảng dữ liệu.

---
### Lời cảm ơn
*Nhóm/Em xin chân thành cảm ơn thầy/cô đã trực tiếp giảng dạy và góp ý để ứng dụng được hoàn thiện hơn. Em rất mong nhận được những nhận xét, đánh giá từ thầy/cô về kết quả và thuật toán của bài tập ngày hôm nay!*
