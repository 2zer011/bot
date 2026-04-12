# 2zer011 - Cày Thuê Manager

Ứng dụng quản lý đơn hàng cày thuê game dành cho Android, xây dựng bằng Flet (Python).  
Giao diện Dark Mode phong cách Cyberpunk / Glassmorphism.

## 🚀 Tính năng
- ✅ Thêm, sửa, xóa đơn hàng.
- ✅ Tìm kiếm theo tài khoản.
- ✅ Tổng doanh thu tự động cập nhật.
- ✅ Lưu trữ cục bộ an toàn, không mất dữ liệu khi tắt app.
- ✅ Xuất / Nhập dữ liệu JSON (Backup/Restore).
- ✅ Ẩn/hiện mật khẩu, nhập liệu có kiểm tra lỗi.

## 📲 Build APK bằng GitHub Actions
1. Fork hoặc tạo repository mới trên GitHub.
2. Upload toàn bộ file trong repo này lên.
3. Vào tab **Actions**, chọn workflow `Build APK`, nhấn `Run workflow`.
4. Sau khi build xong, tải file APK từ Artifacts.

## 🛠️ Chạy thử trên máy tính
```bash
pip install -r requirements.txt
flet run main.py
