import platform
import psutil
import subprocess
import json
import shutil

def get_system_info():
    """
    Lấy thông tin cơ bản của hệ điều hành
    """
    return {
        "system": platform.system(),      # Tên hệ điều hành (Windows / Linux / Darwin...)
        "release": platform.release(),    # Phiên bản phát hành (VD: 10, 11 cho Windows, 5.15 cho Linux)
        "version": platform.version()     # Chuỗi version chi tiết
    }

def get_resource_usage():
    """
    Lấy thông tin về tài nguyên: CPU, RAM, Disk
    """
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),           # % CPU đang sử dụng (1 giây lấy mẫu)
        "memory_percent": psutil.virtual_memory().percent,       # % RAM đang sử dụng
        "disk_usage_percent": psutil.disk_usage('/').percent     # % dung lượng ổ đĩa root (Linux: '/', Windows: ổ C:/)
    }

def check_firewall_status():
    """
    Kiểm tra trạng thái Firewall (khác nhau giữa Windows và Linux)
    """
    system = platform.system()

    if system == "Windows":
        try:
            # Chạy lệnh kiểm tra firewall trên Windows
            output = subprocess.check_output(
                ["netsh", "advfirewall", "show", "allprofiles"],
                stderr=subprocess.STDOUT,
                text=True
            )
            if "ON" in output.upper():
                return "On"
            else:
                return "Off"
        except Exception:
            return "Unknown"

    elif system == "Linux":
        try:
            # Chạy lệnh kiểm tra UFW trên Linux
            output = subprocess.check_output(
                ["ufw", "status"],
                stderr=subprocess.STDOUT,
                text=True
            )
            if "active" in output.lower():
                return "Active"
            else:
                return "Inactive"
        except Exception:
            return "Unknown"
    else:
        return "Unsupported OS"

def system_health_check():
    """
    Hàm chính: tập hợp toàn bộ thông tin hệ thống
    """
    health_data = {
        "os_info": get_system_info(),
        "resources": get_resource_usage(),
        "services": {
            "firewall": check_firewall_status()
        }
    }
    return health_data

if __name__ == "__main__":
    # Gọi hàm kiểm tra sức khỏe hệ thống
    result = system_health_check()

    # In ra kết quả dưới dạng JSON đẹp (indent=4 để dễ đọc)
    print(json.dumps(result, indent=4))
