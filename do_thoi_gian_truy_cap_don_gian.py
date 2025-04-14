import requests
import time
import statistics

def do_thoi_gian_truy_cap(url, so_lan):
    """
    Đo thời gian truy cập vào một URL
    
    Args:
        url: Địa chỉ web cần đo
        so_lan: Số lần thực hiện đo
    """
    thoi_gian_truy_cap = []
    
    print(f"Đang đo thời gian truy cập vào {url} ({so_lan} lần)...")
    
    for i in range(so_lan):
        try:
            bat_dau = time.time()
            response = requests.get(url, timeout=30)
            ket_thuc = time.time()
            
            thoi_gian = ket_thuc - bat_dau
            thoi_gian_truy_cap.append(thoi_gian)
            
            if (i + 1) % 100 == 0:
                print(f"Đã hoàn thành {i + 1}/{so_lan} lần truy cập")
                
            # Tạm dừng nhỏ để tránh quá tải máy chủ
            time.sleep(0.1)
            
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối lần {i+1}: {e}")
    
    # Tính toán thống kê cơ bản
    if thoi_gian_truy_cap:
        thoi_gian_nhanh_nhat = min(thoi_gian_truy_cap)
        thoi_gian_cham_nhat = max(thoi_gian_truy_cap)
        thoi_gian_trung_binh = sum(thoi_gian_truy_cap) / len(thoi_gian_truy_cap)
        
        print("\nKết quả:")
        print(f"Số lần truy cập thành công: {len(thoi_gian_truy_cap)}/{so_lan}")
        print(f"Thời gian truy cập nhanh nhất: {thoi_gian_nhanh_nhat:.18f} giây")
        print(f"Thời gian truy cập chậm nhất: {thoi_gian_cham_nhat:.6f} giây")
        print(f"Thời gian truy cập trung bình: {thoi_gian_trung_binh:.6f} giây")
    else:
        print("Không có dữ liệu truy cập thành công để phân tích")

if __name__ == "__main__":
    url = "http://192.168.1.101:8501"
    so_lan = 100
    
    do_thoi_gian_truy_cap(url, so_lan)