import time
import subprocess
import statistics
import matplotlib.pyplot as plt
import numpy as np
import argparse
import json
from datetime import datetime
import os
import sys
import shutil

class AppPerformanceMeasurer:
    def __init__(self, app_path="app.py", output_dir="performance_results"):
        self.app_path = app_path
        self.output_dir = output_dir
        self.ensure_output_dir()
        self.check_requirements()
        
    def ensure_output_dir(self):
        """Tạo thư mục output nếu chưa tồn tại"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def check_requirements(self):
        """Kiểm tra các yêu cầu cần thiết"""
        # Kiểm tra file app.py
        if not os.path.exists(self.app_path):
            raise FileNotFoundError(f"Không tìm thấy file {self.app_path}")

        # Kiểm tra Streamlit
        streamlit_path = shutil.which('streamlit')
        if not streamlit_path:
            print("Không tìm thấy Streamlit. Đang cài đặt Streamlit...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
                print("Đã cài đặt Streamlit thành công!")
            except subprocess.CalledProcessError:
                raise RuntimeError("Không thể cài đặt Streamlit. Vui lòng cài đặt thủ công: pip install streamlit")

    def measure_startup_time(self, num_runs=10):
        """Đo thời gian khởi động của ứng dụng"""
        startup_times = []
        total_start_time = time.time()
        
        print(f"Bắt đầu đo thời gian khởi động ({num_runs} lần)...")
        
        for i in range(num_runs):
            print(f"\nLần chạy {i+1}/{num_runs}")
            
            start_time = time.time()
            
            try:
                # Chạy ứng dụng Streamlit với đường dẫn đầy đủ
                python_executable = sys.executable
                streamlit_command = [python_executable, "-m", "streamlit", "run", 
                                   os.path.abspath(self.app_path), 
                                   "--server.headless", "true"]
                
                process = subprocess.Popen(
                    streamlit_command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Đợi cho đến khi ứng dụng khởi động
                while True:
                    line = process.stdout.readline()
                    if "You can now view your Streamlit app" in line:
                        break
                    if not line and process.poll() is not None:
                        raise RuntimeError("Ứng dụng không khởi động được")
                
                elapsed_time = time.time() - start_time
                startup_times.append(elapsed_time)
                
                print(f"Thời gian khởi động: {elapsed_time:.2f} giây")
                
            except Exception as e:
                print(f"Lỗi trong lần chạy {i+1}: {str(e)}")
                continue
            finally:
                # Kết thúc tiến trình
                if 'process' in locals():
                    process.terminate()
                    time.sleep(1)
        
        if not startup_times:
            raise RuntimeError("Không có lần chạy nào thành công")
            
        return self.analyze_results(startup_times, total_start_time)

    def analyze_results(self, startup_times, total_start_time):
        """Phân tích kết quả đo"""
        total_time = time.time() - total_start_time
        
        # Tính toán thống kê
        stats = {
            "total_time": total_time,
            "avg_time": statistics.mean(startup_times),
            "min_time": min(startup_times),
            "max_time": max(startup_times),
            "median_time": statistics.median(startup_times),
            "std_dev": statistics.stdev(startup_times) if len(startup_times) > 1 else 0
        }
        
        # Tạo timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Lưu kết quả
        self.save_results(stats, startup_times, timestamp)
        
        # Vẽ và lưu biểu đồ
        self.plot_results(startup_times, stats, timestamp)
        
        return stats, startup_times

    def save_results(self, stats, startup_times, timestamp):
        """Lưu kết quả vào file JSON"""
        results = {
            "timestamp": timestamp,
            "statistics": stats,
            "raw_data": startup_times
        }
        
        filename = f"{self.output_dir}/performance_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"\nKết quả chi tiết đã được lưu vào: {filename}")

    def plot_results(self, startup_times, stats, timestamp):
        """Vẽ biểu đồ kết quả"""
        plt.figure(figsize=(12, 8))
        
        # Subplot 1: Histogram
        plt.subplot(2, 1, 1)
        plt.hist(startup_times, bins=10, alpha=0.7, color='blue')
        plt.axvline(stats["avg_time"], color='red', linestyle='dashed', 
                   linewidth=1, label=f'Trung bình: {stats["avg_time"]:.2f}s')
        plt.xlabel('Thời gian khởi động (giây)')
        plt.ylabel('Số lần')
        plt.title('Phân phối thời gian khởi động')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Subplot 2: Line plot
        plt.subplot(2, 1, 2)
        plt.plot(range(1, len(startup_times) + 1), startup_times, 
                marker='o', linestyle='-', linewidth=2, markersize=6)
        plt.xlabel('Số lần chạy')
        plt.ylabel('Thời gian (giây)')
        plt.title('Thời gian khởi động theo từng lần chạy')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Lưu biểu đồ
        filename = f"{self.output_dir}/performance_plot_{timestamp}.png"
        plt.savefig(filename)
        print(f"Biểu đồ đã được lưu vào: {filename}")
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Đo thời gian khởi động ứng dụng Streamlit')
    parser.add_argument('--runs', type=int, default=10, help='Số lần chạy (mặc định: 10)')
    parser.add_argument('--app', type=str, default='app.py', help='Đường dẫn đến file ứng dụng (mặc định: app.py)')
    parser.add_argument('--output', type=str, default='performance_results', 
                       help='Thư mục lưu kết quả (mặc định: performance_results)')
    
    args = parser.parse_args()
    
    try:
        measurer = AppPerformanceMeasurer(app_path=args.app, output_dir=args.output)
        stats, _ = measurer.measure_startup_time(num_runs=args.runs)
        
        print("\nKết quả tổng quan:")
        print(f"Tổng thời gian chạy: {stats['total_time']:.2f} giây")
        print(f"Thời gian trung bình: {stats['avg_time']:.2f} giây")
        print(f"Thời gian ngắn nhất: {stats['min_time']:.2f} giây")
        print(f"Thời gian dài nhất: {stats['max_time']:.2f} giây")
        print(f"Độ lệch chuẩn: {stats['std_dev']:.2f} giây")
    
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
