import psutil  # lấy thông tin tiến trình và kết nối mạng
import requests  # gọi API lấy thông tin IP
from colorama import Fore, Style, init  # tô màu terminal
import socket  # resolve IP sang domain

# Khởi tạo colorama
init(autoreset=True)

def get_country(ip):
    """
    Lấy thông tin quốc gia của một IP từ API ip-api.com
    """
    try:
        url = f"http://ip-api.com/json/{ip}"  # chỉ truyền IP
        response = requests.get(url, timeout=3)
        data = response.json()
        if data['status'] == 'success':
            return data['countryCode']  # ví dụ: US, VN, JP
        else:
            return "Unknown"
    except Exception:
        return "Unknown"

def get_my_ip():
    """
    Lấy IP public của máy bằng api.ipify.org
    """
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json().get("ip", "Unknown")
    except Exception as e:
        return f"Unknown ({e})"

def get_domain(ip):
    """
    Resolve IP thành domain (nếu có).
    """
    try:
        host = socket.gethostbyaddr(ip)[0]
        return host
    except Exception:
        return None

def is_whitelisted(ip):
    """
    Kiểm tra xem IP/domain có thuộc whitelist hay không
    """
    whitelist_keywords = ["google", "facebook", "openai", "microsoft", "github", "amazonaws","ip-api"]
    domain = get_domain(ip)
    if domain:
        for keyword in whitelist_keywords:
            if keyword in domain.lower():
                return True
    return False

def monitor_connections():
    # IP public hiện tại
    my_ip = get_my_ip()
    print(f"[+] Public IP của máy hiện tại: {my_ip}\n")

    # Danh sách tiến trình khả nghi
    suspicious_procs = ["python", "powershell", "cmd.exe", "bash", "sh"]

    # Liệt kê các kết nối mạng
    connections = psutil.net_connections(kind='inet')
    for conn in connections:
        if conn.raddr:  # nếu có địa chỉ remote
            ip = conn.raddr.ip
            port = conn.raddr.port
            country = get_country(ip)

            # Lấy tên process từ PID
            process_name = "Unknown"
            pid = conn.pid
            if pid:
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    process_name = "N/A"

            # Resolve domain
            domain = get_domain(ip)
            domain_str = f" ({domain})" if domain else ""

            # Xác định nghi ngờ
            is_suspicious = any(proc in process_name.lower() for proc in suspicious_procs)

            line = f"{process_name} (PID: {pid}) → {ip}:{port}{domain_str} [{country}]"

            # Quyết định hiển thị
            if is_whitelisted(ip):
                print(Fore.GREEN + f"[OK] {line} (Whitelisted)")
            elif is_suspicious or (country != "VN" and country != "Unknown"):
                print(Fore.RED + f"[!] {line}")
            else:
                print(Fore.GREEN + f"[+] {line}")

if __name__ == "__main__":
    monitor_connections()
