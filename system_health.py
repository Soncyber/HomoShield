# system_health.py
# Module kiểm tra "sức khỏe hệ thống" trong HomoShield
# Hỗ trợ cả Windows và Linux

import platform
import psutil
import subprocess

def get_system_info():
    """
    Lấy thông tin cơ bản của hệ thống
    """
    return {
        "os": platform.system(),              # Tên hệ điều hành (Windows/Linux)
        "os_version": platform.version(),     # Phiên bản OS
        "machine": platform.machine(),        # Kiến trúc (x86_64, AMD64…)
        "cpu_percent": psutil.cpu_percent(interval=1),  # % CPU trung bình trong 1 giây
        "memory_percent": psutil.virtual_memory().percent,  # % RAM đang dùng
        "disk_usage": psutil.disk_usage('/').percent        # % dung lượng ổ đĩa root
    }

def get_service_status():
    """
    Kiểm tra trạng thái firewall cơ bản
    - Linux: dùng ufw (nếu có)
    - Windows: dùng netsh advfirewall
    """
    os_type = platform.system()
    status = "unknown"

    try:
        # if os_type == "Linux":
        #     # chạy lệnh "ufw status"
        #     output = subprocess.check_output(
        #         ["ufw", "status"],
        #         stderr=subprocess.STDOUT,
        #         text=True
        #     )
        #     if "active" in output.lower():
        #         status = "active"
        #     elif "inactive" in output.lower():
        #         status = "inactive"

        if os_type == "Linux":
        # chạy lệnh "ufw status"
                output = subprocess.check_output(
            ["ufw", "status"],
            stderr=subprocess.STDOUT,
            text=True
        )
                status = output.lower()

        elif os_type == "Windows":
            # chạy lệnh "netsh advfirewall show allprofiles"
            output = subprocess.check_output(
                ["netsh", "advfirewall", "show", "allprofiles"],
                stderr=subprocess.STDOUT,
                text=True,
                shell=True
            )
            # if "on" in output.lower():
            #     status = "active"
            # elif "off" in output.lower():
            #     status = "inactive"
            status = output.lower()
    except Exception as e:
        status = f"error: {e}"

    return {"firewall_status": status}

def run_system_health_check():
    """
    Hàm chính: gom tất cả thông tin lại và in ra màn hình
    """
    print("\n=== HomoShield: System Health Check ===")
    system_info = get_system_info()
    service_status = get_service_status()

    for k, v in system_info.items():
        print(f"{k}: {v}")

    for k, v in service_status.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    run_system_health_check()
