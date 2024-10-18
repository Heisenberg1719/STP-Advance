import psutil, json, requests
from datetime import datetime
from zoneinfo import ZoneInfo

def get_system_details():
    try:
        # Get public IP
        public_ip = requests.get('https://ifconfig.me').text.strip() if requests.get('https://ifconfig.me').status_code == 200 else '0'
    except requests.RequestException:
        public_ip = 'Unavailable'

    # Get CPU details
    cpu_count = psutil.cpu_count(logical=False)  # Physical cores
    logical_cpu_count = psutil.cpu_count(logical=True)  # Logical cores (including hyperthreading)
    cpu_freq = psutil.cpu_freq().current  # Current CPU frequency in MHz

    # Get RAM details
    ram_info = psutil.virtual_memory()
    total_ram = ram_info.total / (1024 ** 3)  # Convert bytes to GB
    available_ram = ram_info.available / (1024 ** 3)  # Convert bytes to GB

    # Get the current process's thread information
    current_process = psutil.Process()
    thread_count = current_process.num_threads()  

    # Return as a Python dictionary
    system_details = {
        "public_ip": public_ip,
        "current_time_ist": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "cpu_info": {
            "physical_cores": cpu_count,
            "logical_cores": logical_cpu_count,
            "current_frequency_mhz": cpu_freq
        },
        "ram_info": {
            "total_ram_gb": f"{total_ram:.2f} GB",
            "available_ram_gb": f"{available_ram:.2f} GB"
        },
        "thread_info": {
            "thread_count": thread_count  
        }
    }

    return system_details