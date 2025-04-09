# Kiến trúc hệ thống và mô hình ứng dụng dự đoán đa bệnh

## Kiến trúc hệ thống

Ứng dụng dự đoán đa bệnh được xây dựng theo kiến trúc module hóa với mô hình MVC (Model-View-Controller) đơn giản hóa:

### 1. Tổng quan kiến trúc

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  Giao diện       |     |  Xử lý logic     |     |  Mô hình         |
|  người dùng      +---->+  ứng dụng        +---->+  học máy         |
|  (Streamlit)     |     |  (Python)        |     |  (ML Models)     |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
         ^                        ^                        ^
         |                        |                        |
         v                        v                        v
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  Thành phần      |     |  Module hỗ trợ   |     |  Dữ liệu         |
|  hiển thị        |     |  (code/)         |     |  (data/)         |
|  (app.py)        |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
```

### 2. Các lớp kiến trúc

#### Lớp giao diện (Presentation Layer)
- **Công nghệ**: Streamlit
- **Thành phần chính**: app.py
- **Chức năng**: Hiển thị giao diện người dùng, thu thập dữ liệu đầu vào, hiển thị kết quả

#### Lớp logic (Business Logic Layer)
- **Công nghệ**: Python
- **Thành phần chính**: 
  - Các hàm xử lý trong app.py
  - Module DiseaseModel.py (cho dự đoán bệnh tổng quát)
  - Module helper.py (hàm tiện ích)
- **Chức năng**: Xử lý dữ liệu đầu vào, gọi mô hình học máy, xử lý kết quả

#### Lớp dữ liệu (Data Layer)
- **Công nghệ**: Pandas, NumPy, Scikit-learn, XGBoost
- **Thành phần chính**: 
  - Các mô hình học máy (.sav, .json)
  - Dữ liệu trong thư mục data/
- **Chức năng**: Lưu trữ và cung cấp dữ liệu, thực hiện dự đoán

### 3. Luồng dữ liệu

```
+----------------+     +----------------+     +----------------+     +----------------+
|                |     |                |     |                |     |                |
| Người dùng     +---->+ Nhập dữ liệu   +---->+ Xử lý dữ liệu  +---->+ Mô hình ML     |
| chọn bệnh      |     | y tế           |     | đầu vào        |     | dự đoán        |
|                |     |                |     |                |     |                |
+----------------+     +----------------+     +----------------+     +----------------+
                                                                            |
                                                                            v
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
| Hiển thị       |<----+ Xử lý kết quả  |<----+ Kết quả        |
| kết quả        |     | dự đoán        |     | dự đoán        |
|                |     |                |     |                |
+----------------+     +----------------+     +----------------+
```

## Mô hình học máy được sử dụng

Ứng dụng sử dụng nhiều mô hình học máy khác nhau cho từng loại bệnh:

### 1. Dự đoán bệnh tổng quát
- **Mô hình**: XGBoost (eXtreme Gradient Boosting)
- **File**: xgboost_model.json
- **Đặc điểm**: 
  - Mô hình dựa trên cây quyết định tăng cường (gradient boosting)
  - Hiệu suất cao trong các bài toán phân loại
  - Xử lý được dữ liệu có nhiều đặc trưng (133 triệu chứng)
- **Đầu vào**: Mảng nhị phân 133 chiều (mỗi chiều tương ứng với một triệu chứng)
- **Đầu ra**: Loại bệnh dự đoán và xác suất

### 2. Dự đoán tiểu đường
- **Mô hình**: Có thể là Random Forest hoặc Logistic Regression
- **File**: diabetes_model.sav
- **Đặc điểm**: Mô hình phân loại nhị phân (có/không có tiểu đường)
- **Đầu vào**: 8 đặc trưng (số lần mang thai, đường huyết, huyết áp, v.v.)
- **Đầu ra**: Dự đoán nhị phân (0/1)

### 3. Dự đoán bệnh tim
- **Mô hình**: Có thể là SVM hoặc Random Forest
- **File**: heart_disease_model.sav
- **Đặc điểm**: Mô hình phân loại nhị phân
- **Đầu vào**: Các đặc trưng về tim mạch (tuổi, giới tính, loại đau ngực, v.v.)
- **Đầu ra**: Dự đoán nhị phân (0/1)

### 4. Dự đoán Parkinson
- **Mô hình**: Có thể là SVM hoặc Random Forest
- **File**: parkinsons_model.sav
- **Đặc điểm**: Mô hình phân loại nhị phân
- **Đầu vào**: Các đặc trưng âm thanh giọng nói
- **Đầu ra**: Dự đoán nhị phân (0/1)

### 5. Dự đoán bệnh gan
- **Mô hình**: Có thể là Logistic Regression hoặc Random Forest
- **File**: liver_model.sav
- **Đặc điểm**: Mô hình phân loại nhị phân
- **Đầu vào**: Các chỉ số xét nghiệm máu
- **Đầu ra**: Dự đoán nhị phân (0/1)

### 6. Dự đoán viêm gan
- **Mô hình**: Tương tự mô hình bệnh gan
- **File**: hepititisc_model.sav
- **Đặc điểm**: Mô hình phân loại nhị phân
- **Đầu vào**: Các chỉ số xét nghiệm máu và chỉ số bổ sung
- **Đầu ra**: Dự đoán nhị phân (0/1)

### 7. Dự đoán ung thư phổi
- **Mô hình**: Có thể là Random Forest hoặc Gradient Boosting
- **File**: lung_cancer_model.sav
- **Đặc điểm**: Mô hình phân loại nhị phân
- **Đầu vào**: Các yếu tố nguy cơ và triệu chứng
- **Đầu ra**: Dự đoán nhị phân (0/1)

### 8. Dự đoán bệnh thận mãn tính
- **Mô hình**: Có thể là Random Forest hoặc SVM
- **File**: chronic_model.sav
- **Đặc điểm**: Mô hình phân loại nhị phân
- **Đầu vào**: Nhiều chỉ số y tế (tuổi, huyết áp, albumin, v.v.)
- **Đầu ra**: Dự đoán nhị phân (0/1)

### 9. Dự đoán ung thư vú
- **Mô hình**: Có thể là SVM hoặc Random Forest
- **File**: breast_cancer.sav
- **Đặc điểm**: Mô hình phân loại nhị phân
- **Đầu vào**: Các đặc điểm của tế bào (bán kính, kết cấu, chu vi, v.v.)
- **Đầu ra**: Dự đoán nhị phân (0/1)

## Tích hợp mô hình vào ứng dụng

### 1. Tải mô hình

Tất cả các mô hình được tải khi khởi động ứng dụng:

```python
# Tải mô hình dự đoán bệnh tổng quát
disease_model = DiseaseModel()
disease_model.load_xgboost('models/xgboost_model.json')

# Tải các mô hình khác
diabetes_model = joblib.load('models/diabetes_model.sav')
heart_disease_model = joblib.load('models/heart_disease_model.sav')
parkinsons_model = joblib.load('models/parkinsons_model.sav')
liver_model = joblib.load('models/liver_model.sav')
hepititisc_model = joblib.load('models/hepititisc_model.sav')
lung_cancer_model = joblib.load('models/lung_cancer_model.sav')
chronic_disease_model = joblib.load('models/chronic_model.sav')
breast_cancer_model = joblib.load('models/breast_cancer.sav')
```

### 2. Sử dụng mô hình

#### Dự đoán bệnh tổng quát (XGBoost)

```python
# Chuyển đổi triệu chứng thành mảng đầu vào
symptoms_array = prepare_symptoms_array(selected_symptoms)

# Dự đoán bệnh
disease, probability = disease_model.predict(symptoms_array)

# Lấy mô tả và biện pháp phòng ngừa
description = disease_model.describe_disease(disease)
precautions = disease_model.disease_precautions(disease)
```

#### Dự đoán các bệnh cụ thể

```python
# Tạo DataFrame với dữ liệu đầu vào
user_input = pd.DataFrame({
    'feature1': [value1],
    'feature2': [value2],
    # ...
})

# Dự đoán
prediction = specific_model.predict(user_input)

# Hiển thị kết quả
if prediction[0] == 1:
    result = "Có khả năng mắc bệnh"
else:
    result = "Không mắc bệnh"
```

## Kiến trúc phần mềm

### 1. Mô hình thiết kế

Ứng dụng sử dụng mô hình thiết kế đơn giản hóa từ MVC:
- **Model**: Các mô hình học máy và lớp DiseaseModel
- **View**: Giao diện Streamlit trong app.py
- **Controller**: Các hàm xử lý trong app.py và helper.py

### 2. Nguyên tắc thiết kế

- **Tách biệt mối quan tâm (Separation of Concerns)**: Mỗi phần dự đoán bệnh được tách biệt rõ ràng
- **Đơn giản hóa (Simplicity)**: Giao diện người dùng trực quan, dễ sử dụng
- **Mô-đun hóa (Modularity)**: Phần dự đoán bệnh tổng quát được tách thành module riêng
- **Khả năng mở rộng (Extensibility)**: Dễ dàng thêm các loại bệnh mới vào ứng dụng

### 3. Mẫu thiết kế (Design Patterns)

- **Factory Method**: Tạo các mô hình dự đoán khác nhau
- **Strategy**: Mỗi loại bệnh có chiến lược dự đoán riêng
- **Facade**: Lớp DiseaseModel cung cấp giao diện đơn giản cho việc dự đoán bệnh tổng quát

## Tóm tắt

Ứng dụng dự đoán đa bệnh được xây dựng với kiến trúc module hóa, sử dụng nhiều mô hình học máy khác nhau cho từng loại bệnh. Phần dự đoán bệnh tổng quát sử dụng mô hình XGBoost phức tạp hơn và được tách thành module riêng, trong khi các phần dự đoán bệnh cụ thể sử dụng các mô hình đơn giản hơn và được triển khai trực tiếp trong file app.py. Kiến trúc này cho phép dễ dàng bảo trì và mở rộng ứng dụng trong tương lai.