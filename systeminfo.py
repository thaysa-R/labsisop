import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

# --- Funções --- #

def get_datetime():
    with open("/proc/driver/rtc") as f:
        data = f.read()
        data = data.strip().split()
        for i, cmd in enumerate(data):
            if cmd == "rtc_time":
                time = data[i+2]
            if cmd == "rtc_date":
                date = data[i+2]

        return (f"{date} {time}")

def get_uptime():
    with open("/proc/uptime") as f:
        data = f.read()
        data = data.strip().split()
        uptime = float(data[0])
        return uptime

def get_cpu_info():
    return {
        "model": "TODO",
        "speed_mhz": 0,
        "usage_percent": 0.0
    }

def get_memory_info():
    return {
        "total_mb": 0,
        "used_mb": 0
    }

def get_os_version():
    version = []

    with open("/proc/version") as f:
        data = f.read()

    for c in enumerate(data):
        version.append(c)
        if c == ")":
            break

    version_str = "".join(version)

    smp_part = ""
    words = data.strip().split()
    for idx, word in enumerate(words):
        if word == "SMP":
            smp_part = " ".join(words[idx:])
            break

    final_version = f"{version_str} {smp_part}"
    return final_version

def get_process_list():
    result = []
    for entry in os.listdir("/proc"):
        if entry.isdigit():
            pid = int(entry)
            with open(f"/proc/{pid}/comm") as f:
                name = f.read().strip()
            result.append({"pid": pid, "name": name})
            
    return result  # lista de { "pid": int, "name": str }

def get_disks():
    result = []
    for entry in os.listdir("/sys/block"):
        if not entry.startswith("ram"):
            size_mb = -1
            with open(f"/sys/block/{entry}/size") as f:
                sectors_count = int(f.readline().strip())
                size_b = sectors_count + 512
                size_mb = size_b // (1024 * 1024) 
            result.append({"device": entry, "size_mb": size_mb})
            
    return result  # lista de { "device": str, "size_mb": int }

def get_usb_devices():
    # Não há dispositivos USB nesse caso
    result = []
    for entry in os.listdir("/sys/bus/usb/devices"):
        product = None
        manufacturer = None
        
        product_path = f"/sys/bus/usb/devices/{entry}/product"
        if os.path.exists(product_path):
            with open(f"/sys/bus/usb/devices/{entry}/product") as f:
                product = f.read().strip()
                
        manufacturer_path = f"/sys/bus/usb/devices/{entry}/manufacturer"
        if os.path.exists(manufacturer_path):
            with open(manufacturer_path) as f:
                manufacturer = f.read().strip()
                
        if product:
            description = f"{product}"
            if manufacturer:
                description = f"{description} from {manufacturer}"
                
            result.append({"port": entry, "description": description})
    
    return result  # lista de { "port": str, "description": str }

def get_network_adapters():
    result = []
    
    # Precisa dos IPs associadas às interfaces de rede
    routes = []
    with open("/proc/net/route") as f:
            routes = f.readlines()
    
    for entry in os.listdir("/sys/class/net"):
        if os.path.isdir(f"/sys/class/net/{entry}"):
            # Procura IP associado
            ip = ""
            for line in routes:
                fields = line.split()
                iface = fields[0].strip()
                if iface == entry:
                    ip = fields[1]
                    ip = ip.strip()
                    
                    # Está em HEX, converte para X.X.X.X
                    n = int(ip, 16)
                    b1 = (n)       & 0xFF
                    b2 = (n >> 8)  & 0xFF
                    b3 = (n >> 16) & 0xFF
                    b4 = (n >> 24) & 0xFF
                    ip = f"{b1}.{b2}.{b3}.{b4}"

                    result.append({"interface": entry, "ip_address": ip})
                    break
    
    return result  # lista de { "interface": str, "ip_address": str }

# --- Servidor HTTP --- #

class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/status":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        response = {
            "datetime": get_datetime(),
            "uptime_seconds": get_uptime(),
            "cpu": get_cpu_info(),
            "memory": get_memory_info(),
            "os_version": get_os_version(),
            "processes": get_process_list(),
            "disks": get_disks(),
            "usb_devices": get_usb_devices(),
            "network_adapters": get_network_adapters()
        }

        data = json.dumps(response, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

def run_server(port=8080):
    print(f"Servidor disponível em http://0.0.0.0:{port}/status")
    server = HTTPServer(("0.0.0.0", port), StatusHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()