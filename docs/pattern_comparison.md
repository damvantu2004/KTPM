# So sánh Kiến Trúc Eager Loading và Lazy Loading

## Tổng quan

| Tiêu chí | Kiến trúc Eager Loading (Cũ) | Kiến trúc Lazy Loading (Mới) |
|----------|----------------------------|----------------------------|
| **Định nghĩa** | Tải tất cả mô hình khi khởi động ứng dụng | Tải mô hình theo yêu cầu khi cần sử dụng |
| **Các mẫu thiết kế chính** | - Module Pattern<br>- Procedural Programming | - Singleton Pattern<br>- Lazy Loading Pattern<br>- Cache Pattern<br>- Factory Method Pattern |
| **Quản lý mô hình** | Phân tán, không tập trung | Tập trung qua ModelManager |

## Các mẫu thiết kế được sử dụng

### Kiến trúc Eager Loading (Cũ)

1. **Module Pattern**
   - Mỗi mô hình được tải và sử dụng như một module riêng biệt
   - Không có sự phối hợp giữa các module

2. **Procedural Programming**
   - Code được tổ chức theo thứ tự thực hiện
   - Thiếu tính trừu tượng và đóng gói

3. **Direct Access Pattern**
   - Truy cập trực tiếp đến các mô hình
   - Không có lớp trung gian

### Kiến trúc Lazy Loading (Mới)

1. **Singleton Pattern**
   - Đảm bảo chỉ có một instance của ModelManager
   - Cung cấp điểm truy cập toàn cục

2. **Lazy Loading Pattern**
   - Trì hoãn việc tải mô hình cho đến khi cần thiết
   - Tối ưu hóa tài nguyên hệ thống

3. **Cache Pattern**
   - Lưu trữ mô hình đã tải để tái sử dụng
   - Tránh tải lại mô hình không cần thiết

4. **Factory Method Pattern**
   - ModelManager hoạt động như một factory tạo ra các instance của mô hình
   - Che giấu logic khởi tạo mô hình

5. **Repository Pattern**
   - Trừu tượng hóa việc truy cập dữ liệu
   - Cung cấp giao diện thống nhất để truy cập mô hình

## So sánh chi tiết

### 1. Cách triển khai

#### Kiến trúc Eager Loading (Cũ)
```python
# Tải tất cả mô hình khi khởi động
diabetes_model = joblib.load('models/diabetes_model.sav')
heart_disease_model = joblib.load('models/heart_disease_model.sav')
parkinsons_model = joblib.load('models/parkinsons_model.sav')
liver_model = joblib.load('models/liver_model.sav')
hepititisc_model = joblib.load('models/hepititisc_model.sav')
lung_cancer_model = joblib.load('models/lung_cancer_model.sav')
chronic_disease_model = joblib.load('models/chronic_model.sav')
breast_cancer_model = joblib.load('models/breast_cancer.sav')

# Sử dụng mô hình trực tiếp
prediction = diabetes_model.predict(input_data)
```

#### Kiến trúc Lazy Loading (Mới)
```python
# Singleton Pattern + Factory Method Pattern
class ModelManager:
    _instance = None
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance
    
    # Lazy Loading Pattern + Cache Pattern
    @lru_cache(maxsize=None)
    def get_model(self, model_name):
        if model_name not in self._models:
            # Factory Method Pattern
            self._models[model_name] = self._load_model(model_name)
        return self._models[model_name]
    
    # Repository Pattern
    def _load_model(self, model_name):
        model_paths = {
            "diabetes": "models/diabetes_model.sav",
            # Các mô hình khác...
        }
        return joblib.load(model_paths[model_name])

# Sử dụng
model_manager = ModelManager()
diabetes_model = model_manager.get_model('diabetes')
prediction = diabetes_model.predict(input_data)
```

### 2. Hiệu năng và tài nguyên

| Tiêu chí | Kiến trúc Eager Loading | Kiến trúc Lazy Loading |
|----------|---------------|--------------|
| **Thời gian khởi động** | Chậm (phải tải tất cả mô hình) | Nhanh (không tải mô hình khi khởi động) |
| **Sử dụng bộ nhớ** | Cao (tất cả mô hình luôn n��m trong bộ nhớ) | Tối ưu (chỉ tải mô hình cần thiết) |
| **Phản hồi người dùng** | Nhanh sau khi khởi động (mô hình đã được tải) | Lần đầu chậm hơn (phải tải mô hình), sau đó nhanh (nhờ cache) |
| **Tải CPU** | Cao khi khởi động, thấp sau đó | Phân bố đều khi người dùng truy cập tính năng |

### 3. Tổ chức code và bảo trì

| Tiêu chí | Kiến trúc Eager Loading | Kiến trúc Lazy Loading |
|----------|---------------|--------------|
| **Cấu trúc code** | Phân tán, không có cấu trúc rõ ràng | Tập trung, module hóa |
| **Khả năng mở rộng** | Khó (cần sửa nhiều nơi khi thêm mô hình) | Dễ (chỉ cần cập nhật ModelManager) |
| **Khả năng bảo trì** | Khó (logic tải mô hình lặp lại nhiều nơi) | Dễ (logic tập trung tại một nơi) |
| **Tái sử dụng code** | Thấp | Cao (ModelManager có thể tái sử dụng) |

### 4. Tính năng bổ sung

| Tính năng | Kiến trúc Eager Loading | Kiến trúc Lazy Loading |
|-----------|---------------|--------------|
| **Caching** | Không có | Có (sử dụng @lru_cache) |
| **Quản lý bộ nhớ** | Thủ công, không linh hoạt | Tự động, linh hoạt |
| **Xử lý lỗi** | Phân tán, khó kiểm soát | Tập trung, dễ kiểm soát |
| **Logging/Monitoring** | Khó triển khai | Dễ triển khai (tập trung tại ModelManager) |

## Ưu điểm và nhược điểm

### Kiến trúc Eager Loading

#### Ưu điểm:
- Đơn giản, dễ triển khai
- Không có độ trễ khi sử dụng mô hình (đã tải sẵn)
- Phù hợp với ứng dụng nhỏ, ít mô hình

#### Nhược điểm:
- Thời gian khởi động lâu
- Sử dụng nhiều bộ nhớ không cần thiết
- Khó mở rộng và bảo trì
- Không linh hoạt trong quản lý tài nguyên

### Kiến trúc Lazy Loading

#### Ưu điểm:
- Khởi động nhanh
- Sử dụng bộ nhớ hiệu quả
- Dễ mở rộng và bảo trì
- Linh hoạt trong quản lý tài nguyên
- Áp dụng các mẫu thiết kế tốt (Singleton, Cache)

#### Nhược điểm:
- Phức tạp hơn trong triển khai
- Có độ trễ khi lần đầu sử dụng mô hình
- Cần quản lý cache hợp lý

## Khi nào sử dụng

### Nên sử dụng Kiến trúc Eager Loading khi:
- Ứng dụng nhỏ với ít mô hình
- Tài nguyên hệ thống dồi dào
- Tất cả mô hình đều được sử dụng thường xuyên
- Độ trễ khi khởi động không phải vấn đề

### Nên sử dụng Kiến trúc Lazy Loading khi:
- Ứng dụng lớn với nhiều mô hình
- Tài nguyên hệ thống hạn chế
- Chỉ một số mô hình được sử dụng thường xuyên
- Cần tối ưu thời gian khởi động

## Kết luận

Việc chuyển từ Kiến trúc Eager Loading sang Kiến trúc Lazy Loading là một bước cải tiến quan trọng cho ứng dụng dự đoán đa bệnh. Kiến trúc mới không chỉ cải thiện hiệu năng và quản lý tài nguyên mà còn nâng cao chất lượng code, giúp ứng dụng dễ dàng mở rộng và bảo trì trong tương lai.

Kiến trúc Lazy Loading với ModelManager là một ví dụ điển hình về việc áp dụng các nguyên tắc thiết kế phần mềm tốt (SOLID, DRY) và các mẫu thiết kế phổ biến (Singleton, Factory Method, Cache) để giải quyết vấn đề thực tế.