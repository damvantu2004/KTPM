import time
import subprocess
import statistics
# import matplotlib.pyplot as plt
# import numpy as np

def measure_startup_time(num_runs=10):
    startup_times = []
    total_start_time = time.time()
    
    for i in range(num_runs):
        print(f"Lần chạy {i+1}/{num_runs}")
        
        # Bắt đầu đo thời gian
        start_time = time.time()
        
        # Chạy ứng dụng Streamlit với tùy chọn headless
        process = subprocess.Popen(
            ["streamlit", "run", "app1.py", "--server.headless", "true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Đợi cho đến khi ứng dụng khởi động
        while True:
            line = process.stdout.readline().decode('utf-8')
            if "You can now view your Streamlit app in your browser." in line:
                break
            # if not line or process.poll() is not None:
            #     break
        
        # Kết thúc đo thời gian
        end_time = time.time()
        elapsed_time = end_time - start_time
        startup_times.append(elapsed_time)
        
        # Kết thúc tiến trình
        process.terminate()
    
    # Tính tổng thời gian
    total_time = time.time() - total_start_time
    
    # Phân tích kết quả
    avg_time = statistics.mean(startup_times)
    
    # In kết quả
    print(f"\nKết quả sau {num_runs} lần chạy:")
    print(f"Tổng thời gian: {total_time:.2f} giây")
    print(f"Thời gian trung bình: {avg_time:.2f} giây")
    
    # # Vẽ biểu đồ
    # plt.figure(figsize=(10, 6))
    # plt.hist(startup_times, bins=10, alpha=0.7, color='blue')
    # plt.axvline(avg_time, color='red', linestyle='dashed', linewidth=1, label=f'Trung bình: {avg_time:.2f}s')
    # plt.xlabel('Thời gian khởi động (giây)')
    # plt.ylabel('Số lần chạy')
    # plt.title(f'Phân phối thời gian khởi động sau {num_runs} lần chạy')
    # plt.legend()
    # plt.grid(True, alpha=0.3)
    # plt.savefig('startup_time_distribution.png')
    # plt.show()
    
    return startup_times

if __name__ == "__main__":
    measure_startup_time(num_runs=10)