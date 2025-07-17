# Hướng dẫn sử dụng API - Hệ thống Quản lý Học viên

## Cài đặt và chạy dự án

### 1. Cài đặt dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Chạy migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Tạo superuser (tùy chọn)
```bash
python manage.py createsuperuser
```

### 4. Chạy server
```bash
python manage.py runserver
```

Server sẽ chạy tại: `http://localhost:8000`

## Cấu trúc API

### Base URL
```
http://localhost:8000/api/
```

### Các Endpoint chính

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/` | API home |
| GET | `/api/hocvien/` | Lấy danh sách học viên |
| POST | `/api/hocvien/create/` | Tạo học viên mới |
| GET | `/api/hocvien/{id}/` | Lấy thông tin chi tiết |
| PUT/PATCH | `/api/hocvien/{id}/update/` | Cập nhật học viên |
| DELETE | `/api/hocvien/{id}/delete/` | Xóa học viên |
| GET | `/api/hocvien/stats/` | Thống kê học viên |

## Test API

### Chạy test tự động
```bash
cd backend
python test_api.py
```

### Test thủ công với cURL

#### 1. Lấy danh sách học viên
```bash
curl -X GET "http://localhost:8000/api/hocvien/?page=1&page_size=5"
```

#### 2. Tạo học viên mới
```bash
curl -X POST "http://localhost:8000/api/hocvien/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "ho_ten": "Nguyen Van A",
    "tuoi": 20,
    "gioi_tinh": 0,
    "lop": "Lop A",
    "da_dang_ky": true,
    "email": "nguyenvana@email.com",
    "so_dien_thoai": "0123456789"
  }'
```

#### 3. Lấy thông tin chi tiết
```bash
curl -X GET "http://localhost:8000/api/hocvien/1/"
```

#### 4. Cập nhật học viên
```bash
curl -X PUT "http://localhost:8000/api/hocvien/1/update/" \
  -H "Content-Type: application/json" \
  -d '{
    "ho_ten": "Nguyen Van A Updated",
    "tuoi": 21,
    "gioi_tinh": 0,
    "lop": "Lop B",
    "da_dang_ky": false,
    "email": "nguyenvana.updated@email.com",
    "so_dien_thoai": "0987654321"
  }'
```

#### 5. Xóa học viên
```bash
curl -X DELETE "http://localhost:8000/api/hocvien/1/delete/"
```

#### 6. Thống kê
```bash
curl -X GET "http://localhost:8000/api/hocvien/stats/"
```

## Tính năng chính

### 1. CRUD Operations
- **Create**: Tạo học viên mới với validation
- **Read**: Lấy danh sách và chi tiết học viên
- **Update**: Cập nhật toàn bộ (PUT) hoặc một phần (PATCH)
- **Delete**: Xóa học viên

### 2. Tìm kiếm và Lọc
- Tìm kiếm theo tên, email, số điện thoại, lớp
- Lọc theo giới tính (Nam/Nữ)
- Lọc theo lớp
- Lọc theo trạng thái đăng ký

### 3. Phân trang
- Hỗ trợ phân trang với page và page_size
- Trả về thông tin pagination

### 4. Validation
- Validate tuổi (5-100)
- Validate giới tính (0/1)
- Validate email format
- Validate số điện thoại (10 chữ số)

### 5. Thống kê
- Tổng số học viên
- Số lượng nam/nữ
- Số lượng đã/chưa đăng ký
- Thống kê theo lớp

## Cấu trúc Response

### Success Response
```json
{
    "status": "success",
    "message": "Thông báo thành công",
    "data": {
        // Dữ liệu trả về
    }
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Thông báo lỗi",
    "errors": {
        // Chi tiết lỗi validation
    }
}
```

## Cấu hình Database

Dự án sử dụng MySQL với cấu hình trong `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'thenewmoon',
        'USER': 'root',
        'PASSWORD': 'Phuoc1512.',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

## CORS Configuration

API đã được cấu hình CORS để cho phép cross-origin requests:
```python
CORS_ALLOW_ALL_ORIGINS = True  # Chỉ dùng cho development
CORS_ALLOW_CREDENTIALS = True
```

## Lưu ý quan trọng

1. **Security**: Trong production, cần thay đổi `CORS_ALLOW_ALL_ORIGINS = False` và cấu hình cụ thể
2. **Database**: Đảm bảo MySQL server đang chạy và database `thenewmoon` đã được tạo
3. **Dependencies**: Cài đặt đầy đủ các thư viện trong `requirements.txt`
4. **Migrations**: Chạy migrations sau khi thay đổi model

## Troubleshooting

### Lỗi kết nối database
- Kiểm tra MySQL server có đang chạy không
- Kiểm tra thông tin kết nối trong `settings.py`
- Đảm bảo database `thenewmoon` đã được tạo

### Lỗi import
- Kiểm tra đã cài đặt đầy đủ dependencies
- Kiểm tra virtual environment có được activate không

### Lỗi CORS
- Kiểm tra cấu hình CORS trong `settings.py`
- Đảm bảo `corsheaders` đã được thêm vào `INSTALLED_APPS` và `MIDDLEWARE` 