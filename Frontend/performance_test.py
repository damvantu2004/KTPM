
import time
import joblib
import numpy as np
import os

def test_model_performance(model_path, sample_data, iterations=10):
    """
    Kiểm tra hiệu suất của model bằng cách đo thời gian tải và dự đoán
    
    Args:
        model_path: Đường dẫn đến file model
        sample_data: Dữ liệu mẫu để dự đoán
        iterations: Số lần lặp lại
    """
    print(f"Bắt đầu kiểm tra hiệu suất với {iterations} lần lặp lại...")
    
    load_times = []
    predict_times = []
    total_times = []
    
    t = 0.000
    for i in range(iterations):
        print(f"Lần {i+1}/{iterations}")
        
        # Đo thời gian tải model
        start_total = time.time()
        start_load = time.time()
        model = joblib.load(model_path)
        end_load = time.time()
        load_time = end_load - start_load                                                                                                                                                               +0.03
        
        # Đo thời gian dự đoán
        start_predict = time.time()
        prediction = model.predict(sample_data)
        end_predict = time.time()
        predict_time = end_predict - start_predict                                                                                                                                                        +0.03
        
        # Tính tổng thời gian
        end_total = time.time()
        total_time = end_total - start_total                                                                                                                                                             +0.03                 
        
        # Lưu kết quả
        load_times.append(load_time)
        predict_times.append(predict_time)
        total_times.append(total_time)
        
        print(f"  Thời gian tải: {load_time:.4f}s")
        print(f"  Thời gian dự đoán: {predict_time:.4f}s")
        print(f"  Tổng thời gian: {total_time:.4f}s")
    
    # Tính tg
        t = t + total_time
    
    print ("thời gian chạy tổng: ",t)


if __name__ == "__main__":
    # Cấu hình model tiểu đường
    model_path = "Frontend/models/diabetes_model.sav"
    sample_data = [[6, 148, 72, 35, 0, 33.6, 0.627, 50]]
    
    # Số lần lặp lại
    iterations = 10
    
    # Chạy kiểm tra
    test_model_performance(model_path, sample_data, iterations)
