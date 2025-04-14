import subprocess
import time
import os
import psutil  # Thêm thư viện để kiểm tra process tốt hơn

# Cấu hình đường dẫn
THU_MUC_APP = r"D:\Study university\nam 3\kien truc phan mem\aaa\Frontend"
LENH = [
    "streamlit", "run", "app.py","--server.headless=false"    
]


os.chdir(THU_MUC_APP)
print("Đường dẫn làm việc hiện tại:", os.getcwd())

so_lan_chay = 300
tong_thoi_gian = 0.0

def is_streamlit_running():
    """Kiểm tra xem có process Streamlit đang chạy không"""
    for proc in psutil.process_iter(['name']):
        if 'streamlit' in proc.info['name'].lower():
            return True
    return False

def kill_streamlit():
    """Dừng tất cả các process Streamlit đang chạy"""
    if os.name == 'nt':  # Windows
        os.system('taskkill /f /im streamlit.exe >nul 2>&1')
    else:  # Linux/Mac
        os.system('pkill -f streamlit')
    
    # Đợi cho đến khi process thực sự dừng, tối đa 1 giây
    start_time = time.time()
    while time.time() - start_time < 1:
        if not is_streamlit_running():
            return
        time.sleep(0.1)

def kill_browser():
    """Dừng tất cả các process trình duyệt phổ biến đang chạy"""
    browser_list = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'opera.exe', 'brave.exe']
    
    for browser in browser_list:
        try:
            if os.name == 'nt':  # Windows
                os.system(f'taskkill /f /im {browser} >nul 2>&1')
            else:  # Linux/Mac
                browser_name = browser.replace('.exe', '')
                os.system(f'pkill -f {browser_name}')
        except:
            continue
    
    # Đợi cho đến khi tất cả trình duyệt đóng hoàn toàn
    start_time = time.time()
    while time.time() - start_time < 2:  # Timeout sau 2 giây
        browsers_running = False
        for proc in psutil.process_iter(['name']):
            if any(browser.lower() in proc.info['name'].lower() for browser in browser_list):
                browsers_running = True
                break
        if not browsers_running:
            return
        time.sleep(0.1)

def run_single_test():
    """Chạy một lần test và trả về thời gian khởi động"""
    # Xóa file cũ nếu tồn tại
    try:
        os.remove("startup_time.txt")
    except FileNotFoundError:
        pass
    
    # Khởi động Streamlit
    process = subprocess.Popen(
        LENH,
        cwd=THU_MUC_APP,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        # env=dict(os.environ, STREAMLIT_SERVER_HEADLESS="true")
    )
    
    # Đợi và đọc kết quả
    start_wait = time.time()
    while time.time() - start_wait < 30:  # Timeout sau 30 giây
        try:
            with open("startup_time.txt", "r") as file:
                thoi_gian = float(file.readline().strip())
                time.sleep(0.3)
                return thoi_gian, process
        except (FileNotFoundError, ValueError):
            time.sleep(0.1)  # Giảm thời gian sleep
    
    return None, process

# Bắt đầu với môi trường sạch
kill_streamlit()
kill_browser()

# Chạy test nhiều lần
for i in range(so_lan_chay):
    print(f"\nLần chạy thứ {i+1}...")
    
    # Đảm bảo môi trường sạch trước mỗi lần chạy
    kill_streamlit()
    kill_browser()
    try:
        os.remove("startup_time.txt")
    except FileNotFoundError:
        pass
    
    # Chạy test
    thoi_gian, process = run_single_test()
    
    # Xử lý kết quả
    if thoi_gian is not None:
        print(f"Thời gian khởi động: {thoi_gian:.2f} giây")
        tong_thoi_gian += thoi_gian
    else:
        print("Không thể đo thời gian trong lần chạy này")
    
    # Dọn dẹp
    if process:
        process.terminate()
        try:
            process.wait(timeout=1)  # Đợi tối đa 1 giây
        except subprocess.TimeoutExpired:
            process.kill()  # Force kill nếu quá thời gian
    kill_streamlit()
    kill_browser()
    
    # # Đợi một khoảng thời gian ngắn trước lần chạy tiếp theo
    # if i < so_lan_chay - 1:
    #     time.sleep(0.5)  # Giảm xuống 0.5 giây

# In kết quả cuối cùng
print("\nKết quả cuối cùng:")
print(f"Tổng thời gian khởi động sau {so_lan_chay} lần chạy: {tong_thoi_gian:.2f} giây")
print(f"Thời gian khởi động trung bình: {tong_thoi_gian/so_lan_chay:.2f} giây")
