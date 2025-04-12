# Tạo file benchmark_full.py
import subprocess
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import signal
import sys
import logging
import joblib
from code.DiseaseModel import DiseaseModel

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def measure_startup_time(attempts=10):
    startup_times = []
    successful_runs = 0
    
    # Đảm bảo đường dẫn tuyệt đối đến app.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")
    
    # Thêm dấu ngoặc kép cho đường dẫn
    app_path = f'"{app_path}"'
    
    logging.info(f"Bắt đầu đo {attempts} lần khởi động...")
    logging.info(f"App path: {app_path}")
    
    if not os.path.exists(app_path):
        logging.error(f"File không tồn tại: {app_path}")
        return np.array([])
    
    for i in range(attempts):
        logging.info(f"Đang chạy lần thứ {i+1}/{attempts}...")
        
        # Khởi động ứng dụng Streamlit
        start_time = time.time()
        
        # Sử dụng shell=True để đảm bảo lệnh chạy đúng
        command = f"streamlit run {app_path} --server.headless=true"
        logging.info(f"Thực thi lệnh: {command}")
        
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            bufsize=1
        )
        
        # Thêm timeout để tránh chờ vô hạn
        timeout = 30  # 30 giây
        server_started = False
        server_ready_time = None
        start_time_proc = time.time()
        
        # Các mẫu cần tìm (thêm nhiều pattern khác nhau)
        patterns = [
            re.compile(r"You can now view your Streamlit app"),
            re.compile(r"Local URL: http://localhost"),
            re.compile(r"Network URL: http://")
        ]
        
        while time.time() - start_time_proc < timeout:
            line = proc.stdout.readline().strip()
            if line:
                logging.debug(f"Output: {line}")
                
                # Kiểm tra nếu server đã sẵn sàng
                for pattern in patterns:
                    if pattern.search(line):
                        server_started = True
                        server_ready_time = time.time()
                        logging.info(f"Server đã sẵn sàng: {line}")
                        break
                
                # Kiểm tra thông tin thời gian khởi động
                if "Thời gian khởi động:" in line:
                    ui_duration_match = re.search(r"Thời gian khởi động: (\d+\.\d+) giây", line)
                    if ui_duration_match:
                        ui_duration = float(ui_duration_match.group(1))
                        logging.info(f"UI thông báo thời gian khởi động: {ui_duration} giây")
            
            # Thoát nếu tìm thấy pattern
            if server_started:
                break
            
            # Kiểm tra nếu process đã kết thúc
            if proc.poll() is not None:
                logging.warning("Process kết thúc trước khi server sẵn sàng!")
                break
        
        # Xử lý kết quả
        if server_started and server_ready_time is not None:
            duration = server_ready_time - start_time
            startup_times.append(duration)
            successful_runs += 1
            logging.info(f"Lần {i+1}: Thời gian khởi động: {duration:.2f}s")
        else:
            logging.error(f"Lần {i+1}: Không phát hiện server khởi động trong {timeout} giây!")
            
            # In ra stderr để debug
            stderr_output = proc.stderr.read()
            if stderr_output:
                logging.error(f"stderr: {stderr_output}")
        
        # Dừng Streamlit process
        try:
            if proc.poll() is None:  # Nếu process vẫn đang chạy
                proc.terminate()
                proc.wait(timeout=5)
                if proc.poll() is None:
                    proc.kill()
                    logging.warning("Process bị kill vì không terminate được")
        except Exception as e:
            logging.error(f"Lỗi khi dừng process: {e}")
        
        # Thêm thời gian chờ dài hơn để đảm bảo port được giải phóng
        time.sleep(3)
    
    logging.info(f"Hoàn thành {successful_runs}/{attempts} lần chạy thành công")
    return np.array(startup_times)

def simulate_startup():
    """Mô phỏng quá trình khởi động mô hình"""
    start_time = time.time()
    
    # 1. Thời gian tải models (chi phí chính)
    diabetes_model = joblib.load("models/diabetes_model.sav")
    heart_model = joblib.load("models/heart_disease_model.sav")
    parkinson_model = joblib.load("models/parkinsons_model.sav")
    lung_cancer_model = joblib.load('models/lung_cancer_model.sav')
    breast_cancer_model = joblib.load('models/breast_cancer.sav')
    chronic_disease_model = joblib.load('models/chronic_model.sav')
    hepatitis_model = joblib.load('models/hepititisc_model.sav')
    liver_model = joblib.load('models/liver_model.sav')
    
    # 2. Thời gian tải XGBoost model
    disease_model = DiseaseModel()
    disease_model.load_xgboost('model/xgboost_model.json')
    
    # Tổng thời gian
    total_duration = time.time() - start_time
    
    return total_duration

if __name__ == "__main__":
    attempts = 10  # Đặt thành 1000 cho bài tập thực tế
    
    startup_times = measure_startup_time(attempts)
    
    # Phân tích kết quả
    if len(startup_times) > 0:
        mean_time = np.mean(startup_times)
        std_time = np.std(startup_times)
        median_time = np.median(startup_times)
        min_time = np.min(startup_times)
        max_time = np.max(startup_times)
        
        # Lưu kết quả
        pd.DataFrame({
            'Run': range(1, len(startup_times) + 1),
            'Duration': startup_times
        }).to_csv('full_startup_benchmark.csv', index=False)
        
        # In kết quả
        print(f"\nKết quả đo {len(startup_times)} lần khởi động (bao gồm UI):")
        print(f"Thời gian trung bình: {mean_time:.4f} giây")
        print(f"Độ lệch chuẩn: {std_time:.4f} giây")
        print(f"Thời gian tối thiểu: {min_time:.4f} giây")
        print(f"Thời gian tối đa: {max_time:.4f} giây")
        print(f"Thời gian trung vị: {median_time:.4f} giây")
        print(f"Tổng thời gian: {np.sum(startup_times):.2f} giây")
        
        # Vẽ biểu đồ
        plt.figure(figsize=(10, 6))
        plt.hist(startup_times, bins=min(30, len(startup_times)), alpha=0.7, color='blue')
        plt.axvline(mean_time, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_time:.4f}s')
        plt.axvline(median_time, color='green', linestyle='dashed', linewidth=2, label=f'Median: {median_time:.4f}s')
        plt.title('Phân phối thời gian khởi động (bao gồm UI)')
        plt.xlabel('Thời gian (giây)')
        plt.ylabel('Tần suất')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('full_startup_benchmark.png')
        plt.show()
    else:
        print("Không có lần chạy nào thành công!")