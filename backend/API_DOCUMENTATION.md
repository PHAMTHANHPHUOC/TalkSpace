# API Documentation - Hệ thống Quản lý Học viên

## Tổng quan
API này cung cấp các endpoint để quản lý học viên với đầy đủ các chức năng CRUD (Create, Read, Update, Delete) và các tính năng bổ sung như tìm kiếm, phân trang, và thống kê.

## Base URL
```
http://localhost:8000/api/
```

## Các Endpoint

### 1. Lấy danh sách học viên
**GET** `/api/hocvien/`

**Query Parameters:**
- `search` (optional): Tìm kiếm theo tên, email, số điện thoại, lớp
- `gioi_tinh` (optional): Lọc theo giới tính (0: Nam, 1: Nữ)
- `lop` (optional): Lọc theo lớp
- `da_dang_ky` (optional): Lọc theo trạng thái đăng ký (true/false)
- `page` (optional): Trang hiện tại (mặc định: 1)
- `page_size` (optional): Số lượng item mỗi trang (mặc định: 10)

**Ví dụ:**
```
GET /api/hocvien/?search=Nguyen&gioi_tinh=0&page=1&page_size=5
```

**Response:**
```json
{
    "status": "success",
    "message": "Lấy danh sách học viên thành công",
    "data": [
        {
            "id": 1,
            "ho_ten": "Nguyen Van A",
            "tuoi": 20,
            "gioi_tinh": 0,
            "lop": "Lop A",
            "da_dang_ky": true,
            "ngay_tao": "2024-01-01T10:00:00Z",
            "email": "nguyenvana@email.com",
            "so_dien_thoai": "0123456789"
        }
    ],
    "pagination": {
        "page": 1,
        "page_size": 10,
        "total_count": 25,
        "total_pages": 3
    }
}
```

### 2. Tạo học viên mới
**POST** `/api/hocvien/create/`

**Request Body:**
```json
{
    "ho_ten": "Nguyen Van A",
    "tuoi": 20,
    "gioi_tinh": 0,
    "lop": "Lop A",
    "da_dang_ky": true,
    "email": "nguyenvana@email.com",
    "so_dien_thoai": "0123456789"
}
```

**Validation Rules:**
- `ho_ten`: Bắt buộc, tối đa 100 ký tự
- `tuoi`: Bắt buộc, từ 5 đến 100
- `gioi_tinh`: Bắt buộc, 0 (Nam) hoặc 1 (Nữ)
- `lop`: Bắt buộc, tối đa 50 ký tự
- `da_dang_ky`: Mặc định false
- `email`: Tùy chọn, phải là email hợp lệ
- `so_dien_thoai`: Tùy chọn, phải có 10 chữ số

**Response:**
```json
{
    "status": "success",
    "message": "Tạo học viên thành công",
    "data": {
        "id": 1,
        "ho_ten": "Nguyen Van A",
        "tuoi": 20,
        "gioi_tinh": 0,
        "lop": "Lop A",
        "da_dang_ky": true,
        "ngay_tao": "2024-01-01T10:00:00Z",
        "email": "nguyenvana@email.com",
        "so_dien_thoai": "0123456789"
    }
}
```

### 3. Lấy thông tin chi tiết học viên
**GET** `/api/hocvien/{id}/`

**Response:**
```json
{
    "status": "success",
    "message": "Lấy thông tin học viên thành công",
    "data": {
        "id": 1,
        "ho_ten": "Nguyen Van A",
        "tuoi": 20,
        "gioi_tinh": 0,
        "lop": "Lop A",
        "da_dang_ky": true,
        "ngay_tao": "2024-01-01T10:00:00Z",
        "email": "nguyenvana@email.com",
        "so_dien_thoai": "0123456789"
    }
}
```

### 4. Cập nhật học viên
**PUT** `/api/hocvien/{id}/update/` (cập nhật toàn bộ)
**PATCH** `/api/hocvien/{id}/update/` (cập nhật một phần)

**Request Body (PUT):**
```json
{
    "ho_ten": "Nguyen Van A Updated",
    "tuoi": 21,
    "gioi_tinh": 0,
    "lop": "Lop B",
    "da_dang_ky": false,
    "email": "nguyenvana.updated@email.com",
    "so_dien_thoai": "0987654321"
}
```

**Request Body (PATCH):**
```json
{
    "tuoi": 21,
    "lop": "Lop B"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Cập nhật học viên thành công",
    "data": {
        "id": 1,
        "ho_ten": "Nguyen Van A Updated",
        "tuoi": 21,
        "gioi_tinh": 0,
        "lop": "Lop B",
        "da_dang_ky": false,
        "ngay_tao": "2024-01-01T10:00:00Z",
        "email": "nguyenvana.updated@email.com",
        "so_dien_thoai": "0987654321"
    }
}
```

### 5. Xóa học viên
**DELETE** `/api/hocvien/{id}/delete/`

**Response:**
```json
{
    "status": "success",
    "message": "Xóa học viên thành công"
}
```

### 6. Thống kê học viên
**GET** `/api/hocvien/stats/`

**Response:**
```json
{
    "status": "success",
    "message": "Lấy thống kê thành công",
    "data": {
        "total_hocvien": 25,
        "nam_count": 15,
        "nu_count": 10,
        "da_dang_ky_count": 20,
        "chua_dang_ky_count": 5,
        "lop_stats": {
            "Lop A": 10,
            "Lop B": 8,
            "Lop C": 7
        }
    }
}
```

## Error Responses

### Validation Error (400)
```json
{
    "status": "error",
    "message": "Dữ liệu không hợp lệ",
    "errors": {
        "tuoi": ["Tuổi phải từ 5 đến 100"],
        "gioi_tinh": ["Giới tính phải là 0 (Nam) hoặc 1 (Nữ)"]
    }
}
```

### Not Found Error (404)
```json
{
    "status": "error",
    "message": "Không tìm thấy học viên"
}
```

### Server Error (500)
```json
{
    "status": "error",
    "message": "Lỗi: [Chi tiết lỗi]"
}
```

## Cách sử dụng với cURL

### Lấy danh sách học viên
```bash
curl -X GET "http://localhost:8000/api/hocvien/?search=Nguyen&page=1&page_size=5"
```

### Tạo học viên mới
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

### Cập nhật học viên
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

### Xóa học viên
```bash
curl -X DELETE "http://localhost:8000/api/hocvien/1/delete/"
```

## Lưu ý
- Tất cả các endpoint đều trả về response với format JSON
- API sử dụng HTTP status codes chuẩn
- CORS đã được cấu hình để cho phép cross-origin requests
- Phân trang được áp dụng cho endpoint lấy danh sách
- Validation được thực hiện ở cả client và server side 