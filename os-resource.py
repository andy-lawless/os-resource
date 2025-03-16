import psutil
import time
from datetime import datetime

def get_cpu_info():
    """Retrieve CPU-related information."""
    print("=== CPU Information ===")
    # Total CPU cores (physical and logical)
    print(f"Total CPU Cores: {psutil.cpu_count()}")
    print(f"Physical CPU Cores: {psutil.cpu_count(logical=False)}")
    
    # CPU usage percentage (overall and per core)
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"Overall CPU Usage: {cpu_usage}%")
    per_core_usage = psutil.cpu_percent(interval=1, percpu=True)
    for i, usage in enumerate(per_core_usage):
        print(f"Core {i}: {usage}%")
    
    # CPU frequency
    freq = psutil.cpu_freq()
    if freq:
        print(f"Current CPU Frequency: {freq.current:.2f} MHz")
        print(f"Min CPU Frequency: {freq.min:.2f} MHz")
        print(f"Max CPU Frequency: {freq.max:.2f} MHz")

def get_memory_info():
    """Retrieve memory-related information."""
    print("\n=== Memory Information ===")
    mem = psutil.virtual_memory()
    # Convert bytes to GB for readability
    total_gb = mem.total / (1024 ** 3)
    available_gb = mem.available / (1024 ** 3)
    used_gb = mem.used / (1024 ** 3)
    
    print(f"Total Memory: {total_gb:.2f} GB")
    print(f"Available Memory: {available_gb:.2f} GB")
    print(f"Used Memory: {used_gb:.2f} GB")
    print(f"Memory Usage: {mem.percent}%")

def get_disk_info():
    """Retrieve disk-related information."""
    print("\n=== Disk Information ===")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"Device: {partition.device}")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File System Type: {partition.fstype}")
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total_gb = usage.total / (1024 ** 3)
            used_gb = usage.used / (1024 ** 3)
            free_gb = usage.free / (1024 ** 3)
            print(f"  Total Space: {total_gb:.2f} GB")
            print(f"  Used Space: {used_gb:.2f} GB")
            print(f"  Free Space: {free_gb:.2f} GB")
            print(f"  Usage: {usage.percent}%")
        except PermissionError:
            print("  [Permission Denied]")

def get_network_info():
    """Retrieve network-related information."""
    print("\n=== Network Information ===")
    net_io = psutil.net_io_counters()
    bytes_sent_gb = net_io.bytes_sent / (1024 ** 3)
    bytes_recv_gb = net_io.bytes_recv / (1024 ** 3)
    
    print(f"Total Bytes Sent: {bytes_sent_gb:.3f} GB")
    print(f"Total Bytes Received: {bytes_recv_gb:.3f} GB")
    
    # Network interfaces
    interfaces = psutil.net_if_stats()
    for iface, stats in interfaces.items():
        print(f"Interface: {iface}")
        print(f"  Is Up: {stats.isup}")
        print(f"  Speed: {stats.speed} Mbps")

def get_process_info():
    """Retrieve information about running processes."""
    print("\n=== Top 5 Processes by CPU Usage ===")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            cpu = proc.info['cpu_percent']
            # Skip processes where cpu_percent is None
            if cpu is None:
                continue
            processes.append((proc.info['pid'], proc.info['name'], cpu, proc.info['memory_percent']))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if not processes:
        print("No process information available.")
        return
    
    # Sort by CPU usage (index 2) in descending order and take top 5
    top_processes = sorted(processes, key=lambda x: x[2], reverse=True)[:5]
    for pid, name, cpu, mem in top_processes:
        print(f"PID: {pid} | Name: {name or 'Unknown'} | CPU: {cpu:.1f}% | Memory: {mem:.2f}%")

def main():
    """Main function to display all system resource information."""
    print(f"System Resource Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    get_cpu_info()
    get_memory_info()
    get_disk_info()
    get_network_info()
    get_process_info()

if __name__ == "__main__":
    main()