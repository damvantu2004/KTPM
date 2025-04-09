
# Ứng dụng dự đoán đa bệnh

## Tổng quan

Ứng dụng dự đoán đa bệnh là một hệ thống hỗ trợ chẩn đoán y tế sử dụng các mô hình học máy để dự đoán khả năng mắc nhiều loại bệnh khác nhau dựa trên các chỉ số y tế, triệu chứng và yếu tố nguy cơ. Ứng dụng được xây dựng bằng Streamlit, cung cấp giao diện người dùng trực quan và dễ sử dụng.

## Kiến trúc tổng quan

### 1. Cấu trúc thư mục

```
├── app.py                  # File chính của ứng dụng
├── code/                   # Thư mục chứa các module hỗ trợ
│   ├── DiseaseModel.py     # Lớp xử lý dự đoán bệnh tổng quát
│   └── helper.py           # Các hàm tiện ích
├── data/                   # dataset.csv, clean_dataset.tsv chỉ dùng cho phần dự đoán bệnh tổng quát.
│   ├── clean_dataset.tsv   # Dữ liệu đã làm sạch
│   ├── dataset.csv         # Dữ liệu gốc
│   ├── lung_cancer.csv     # Dữ liệu ung thư phổi
│   ├── symptom_Description.csv  # Mô tả các triệu chứng
│   └── symptom_precaution.csv   # Biện pháp phòng ngừa
├── models/                 # Thư mục chứa các mô hình đã huấn luyện
│   ├── breast_cancer.sav   # Mô hình dự đoán ung thư vú
│   ├── chronic_model.sav   # Mô hình dự đoán bệnh thận mãn tính
│   ├── diabetes_model.sav  # Mô hình dự đoán tiểu đường
│   ├── heart_disease_model.sav  # Mô hình dự đoán bệnh tim
│   ├── hepititisc_model.sav     # Mô hình dự đoán viêm gan
│   ├── liver_model.sav     # Mô hình dự đoán bệnh gan
│   ├── lung_cancer_model.sav    # Mô hình dự đoán ung thư phổi
│   ├── parkinsons_model.sav     # Mô hình dự đoán Parkinson
│   └── xgboost_model.json  # Mô hình XGBoost cho dự đoán bệnh tổng quát
└── [các file hình ảnh]     # Hình ảnh minh họa (positive.jpg, negative.jpg, v.v.)
```

### 2. Thành phần chính

1. **Giao diện người dùng (UI)**: Xây dựng bằng Streamlit, cung cấp các trang dự đoán riêng biệt cho từng loại bệnh.
2. **Mô hình học máy**: Các mô hình đã được huấn luyện trước, được lưu dưới dạng file `.sav` hoặc `.json`.
3. **Lớp DiseaseModel**: Xử lý dự đoán bệnh tổng quát, cung cấp các phương thức để mô tả bệnh và biện pháp phòng ngừa.
4. **Hàm tiện ích**: Hỗ trợ chuyển đổi dữ liệu đầu vào thành định dạng phù hợp với mô hình.

## Mô hình code

### 1. Cấu trúc app.py

File `app.py` là file chính của ứng dụng, được tổ chức theo cấu trúc sau:

1. **Import thư viện**: Nhập các thư viện cần thiết như Streamlit, Pandas, NumPy, Plotly, PIL, v.v.
2. **Tải mô hình**: Tải tất cả các mô hình học máy đã được huấn luyện trước.
3. **Tạo thanh điều hướng**: Sử dụng `option_menu` để tạo thanh điều hướng bên trái.
4. **Các phần dự đoán bệnh**: Mỗi loại bệnh có một phần riêng biệt với các thành phần:
   - Tiêu đề và hình ảnh minh họa
   - Các trường nhập liệu (text input, slider, selectbox)
   - Nút dự đoán
   - Xử lý dự đoán và hiển thị kết quả

### 2. Lớp DiseaseModel

File `DiseaseModel.py` định nghĩa lớp `DiseaseModel` với các phương thức:

```python
class DiseaseModel:
    def __init__(self):
        self.all_symptoms = None
        self.symptoms = None
        self.pred_disease = None
        self.model = xgb.XGBClassifier()
        self.diseases = self.disease_list('data/dataset.csv')

    def load_xgboost(self, model_path):
        self.model.load_model(model_path)

    def save_xgboost(self, model_path):
        self.model.save_model(model_path)

    def predict(self, X):
        self.symptoms = X
        disease_pred_idx = self.model.predict(self.symptoms)
        self.pred_disease = self.diseases[disease_pred_idx].values[0]
        disease_probability_array = self.model.predict_proba(self.symptoms)
        disease_probability = disease_probability_array[0, disease_pred_idx[0]]
        return self.pred_disease, disease_probability

    def describe_disease(self, disease_name):
        # Đọc và trả về mô tả bệnh

    def describe_predicted_disease(self):
        # Trả về mô tả của bệnh đã dự đoán

    def disease_precautions(self, disease_name):
        # Đọc và trả về biện pháp phòng ngừa

    def predicted_disease_precautions(self):
        # Trả về biện pháp phòng ngừa cho bệnh đã dự đoán

    def disease_list(self, kaggle_dataset):
        # Đọc danh sách bệnh từ tập dữ liệu
```

### 3. Hàm tiện ích

File `helper.py` chứa các hàm tiện ích như `prepare_symptoms_array`:

```python
def prepare_symptoms_array(symptoms):
    '''
    Chuyển đổi danh sách triệu chứng thành mảng có kích thước phù hợp với
    mô hình học máy (trong trường hợp này là 133)
    '''
    symptoms_array = np.zeros((1,133))
    df = pd.read_csv('data/clean_dataset.tsv', sep='\t')
    
    for symptom in symptoms:
        symptom_idx = df.columns.get_loc(symptom)
        symptoms_array[0, symptom_idx] = 1

    return symptoms_array
```

## Luồng hoạt động

### 1. Khởi động ứng dụng

1. Tải tất cả các mô hình học máy đã được huấn luyện trước.
2. Hiển thị giao diện người dùng với thanh điều hướng bên trái.
3. Mặc định hiển thị trang "Dự Đoán Bệnh" (dự đoán bệnh tổng quát).

### 2. Dự đoán bệnh tổng quát

1. Người dùng chọn các triệu chứng từ danh sách.
2. Khi nhấn nút "Dự Đoán":
   - Chuyển đổi danh sách triệu chứng thành mảng đầu vào bằng hàm `prepare_symptoms_array`.
   - Gọi phương thức `predict` của lớp `DiseaseModel`.
   - Hiển thị kết quả dự đoán, mô tả bệnh và biện pháp phòng ngừa.

### 3. Dự đoán các bệnh cụ thể

1. Người dùng chọn loại bệnh cần dự đoán từ thanh điều hướng.
2. Nhập thông tin cá nhân (họ tên) và các chỉ số y tế liên quan.
3. Khi nhấn nút dự đoán:
   - Tạo DataFrame với dữ liệu đã nhập.
   - Gọi phương thức `predict` của mô hình tương ứng.
   - Hiển thị kết quả dự đoán với hình ảnh minh họa (positive.jpg hoặc negative.jpg).

## Các loại bệnh và đặc điểm

### 1. Dự đoán bệnh tổng quát
- Sử dụng mô hình XGBoost
- Cho phép người dùng chọn nhiều triệu chứng
- Hiển thị mô tả bệnh và biện pháp phòng ngừa

### 2. Dự đoán tiểu đường
- Sử dụng 8 chỉ số: số lần mang thai, đường huyết, huyết áp, độ dày da, insulin, BMI, chỉ số di truyền, tuổi

### 3. Dự đoán bệnh tim
- Sử dụng nhiều chỉ số như tuổi, giới tính, loại đau ngực, huyết áp, cholesterol, v.v.

### 4. Dự đoán Parkinson
- Sử dụng các chỉ số âm thanh giọng nói (MDVP, Jitter, Shimmer, v.v.)

### 5. Dự đoán bệnh gan
- Sử dụng các chỉ số xét nghiệm máu như bilirubin, enzyme gan, protein

### 6. Dự đoán viêm gan
- Tương tự bệnh gan nhưng có thêm các chỉ số GGT và PROT

### 7. Dự đoán ung thư phổi
- Dựa trên các yếu tố nguy cơ và triệu chứng như hút thuốc, ho, khó thở, đau ngực

### 8. Dự đoán bệnh thận mãn tính
- Sử dụng nhiều chỉ số như tuổi, huyết áp, albumin, đường, hồng cầu, bạch cầu, v.v.

### 9. Dự đoán ung thư vú
- Sử dụng các đặc điểm của tế bào như bán kính, kết cấu, chu vi, độ lõm, v.v.

## Công nghệ sử dụng

1. **Streamlit**: Xây dựng giao diện người dùng web
2. **Pandas & NumPy**: Xử lý dữ liệu và tính toán số học
3. **Scikit-learn**: Cung cấp các mô hình học máy
4. **XGBoost**: Mô hình dự đoán bệnh tổng quát
5. **Plotly & Matplotlib**: Tạo biểu đồ và trực quan hóa (nếu cần)
6. **PIL (Pillow)**: Xử lý hình ảnh
7. **Joblib**: Tải và lưu mô hình học máy

## Quy trình xây dựng ứng dụng

### 1. Thu thập và chuẩn bị dữ liệu
- Thu thập dữ liệu từ nhiều nguồn khác nhau
- Tiền xử lý dữ liệu (làm sạch, chuẩn hóa)
- Chia dữ liệu thành tập huấn luyện và tập kiểm tra

### 2. Xây dựng và huấn luyện mô hình
- Lựa chọn thuật toán phù hợp cho từng loại bệnh
- Huấn luyện mô hình trên tập dữ liệu
- Đánh giá và điều chỉnh mô hình
- Lưu mô hình đã huấn luyện

### 3. Xây dựng giao diện người dùng
- Thiết kế cấu trúc ứng dụng với thanh điều hướng
- Tạo các trang dự đoán riêng biệt cho từng loại bệnh
- Kết nối giao diện với mô hình học máy

### 4. Việt hóa giao diện
- Chuyển đổi tất cả các nhãn, tiêu đề và thông báo sang tiếng Việt
- Đảm bảo các tùy chọn trong các hộp chọn cũng được dịch

### 5. Kiểm thử và triển khai
- Kiểm tra tất cả các chức năng của ứng dụng
- Đảm bảo tất cả các mô hình hoạt động chính xác
- Triển khai ứng dụng

## Hướng dẫn sử dụng

### Cài đặt

1. Clone repository:
```
git clone <repository-url>
```

2. Cài đặt các thư viện cần thiết:
```
pip install -r requirements.txt
```

3. Chạy ứng dụng:
```
streamlit run app.py
```

### Sử dụng ứng dụng

1. Chọn loại bệnh cần dự đoán từ thanh điều hướng bên trái.
2. Nhập thông tin cá nhân và các chỉ số y tế theo yêu cầu.
3. Nhấn nút dự đoán để xem kết quả.
4. Đối với dự đoán bệnh tổng quát, bạn có thể xem thêm mô tả bệnh và biện pháp phòng ngừa.

## Lưu ý

- Ứng dụng này chỉ cung cấp dự đoán ban đầu và không thay thế cho chẩn đoán y tế chuyên nghiệp.
- Luôn tham khảo ý kiến bác sĩ nếu bạn có bất kỳ lo ngại nào về sức khỏe.
- Độ chính xác của dự đoán phụ thuộc vào chất lượng dữ liệu đầu vào và hiệu suất của mô hình học máy.
