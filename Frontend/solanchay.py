import subprocess
import pandas as pd
import time
import os
from pathlib import Path

# Cấu hình
SO_LAN_CHAY = 5  # Số lần chạy, có thể thay đổi
THU_MUC_APP = r"D:\Study university\nam 3\kien truc phan mem\aaa\Frontend"
FILE_EXCEL = os.path.join(THU_MUC_APP, "startup_times.xlsx")
LENH = ["streamlit", "run", "app.py"]
THOI_GIAN_CHO_TOI_DA = 60  # Thời gian tối đa chờ mỗi lần chạy (giây)

# Đảm bảo đúng thư mục làm việc
os.chdir(THU_MUC_APP)
print("Đường dẫn làm việc hiện tại:", os.getcwd())

def dem_so_dong_excel():
    """Đếm số dòng trong file Excel."""
    try:
        if not os.path.exists(FILE_EXCEL):
            print(f"File {FILE_EXCEL} chưa tồn tại.")
            return 0
        df = pd.read_excel(FILE_EXCEL, engine="openpyxl")
        so_dong = len(df)
        print(f"Số dòng Excel: {so_dong}")
        return so_dong
    except Exception as e:
        print(f"Lỗi đọc Excel: {e}")
        return -1

def chay_streamlit_mot_lan(so_dong_ban_dau):
    """Chạy Streamlit, dừng khi có dòng mới trong Excel."""
    print(f"Chạy: {' '.join(LENH)}")
    process = subprocess.Popen(
        LENH,
        cwd=THU_MUC_APP,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    )

    # Chờ dòng mới trong Excel
    thoi_gian_bat_dau = time.time()
    while time.time() - thoi_gian_bat_dau < THOI_GIAN_CHO_TOI_DA:
        so_dong_hien_tai = dem_so_dong_excel()
        if so_dong_hien_tai == -1:
            print("Dừng do lỗi đọc Excel.")
            process.terminate()
            process.wait()
            return False
        if so_dong_hien_tai > so_dong_ban_dau:
            print("Có dòng mới, dừng Streamlit...")
            process.terminate()
            process.wait()
            return True
        time.sleep(0.2)  # Kiểm tra mỗi 0.2 giây

    print("Cảnh báo: Không có dòng mới trong thời gian tối đa.")
    process.terminate()
    process.wait()
    return False



# Kiểm tra thư mục và file
THU_MUC_APP = Path(THU_MUC_APP).resolve()
FILE_EXCEL = Path(FILE_EXCEL).resolve()
if not THU_MUC_APP.exists():
    print(f"Lỗi: Thư mục {THU_MUC_APP} không tồn tại.")
    exit(1)

app_path = os.path.join(THU_MUC_APP, "app.py")
if not os.path.exists(app_path):
    print(f"Lỗi: File {app_path} không tồn tại.")
    exit(1)

# Kiểm tra Excel ban đầu
print("Kiểm tra Excel...")
so_dong_ban_dau = dem_so_dong_excel()
if so_dong_ban_dau == -1:
    print("Lỗi: Không đọc được Excel. Kiểm tra app.py hoặc cài openpyxl.")
    exit(1)

# Chạy số lần yêu cầu
for i in range(SO_LAN_CHAY):
    print(f"Lần chạy thứ {i+1}")
    so_dong_ban_dau = dem_so_dong_excel()
    thanh_cong = chay_streamlit_mot_lan(so_dong_ban_dau)
    if not thanh_cong:
        print(f"Lần chạy thứ {i+1} thất bại, thử lại...")
    time.sleep(1)  # Đợi tiến trình dừng hoàn toàn
