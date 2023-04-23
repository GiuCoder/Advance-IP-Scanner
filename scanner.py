import socket
import struct
import threading
import math
import colorama
from colorama import Fore, Style
import sys
import time
import ipaddress
import signal
import pyfiglet
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
os.system("clear")
# Install missing modules
try:
    import colorama
except ImportError:
    print("Installing colorama module...")
    os.system("pip install colorama")
    import colorama

try:
    import pyfiglet
except ImportError:
    print("Installing pyfiglet module...")
    os.system("pip install pyfiglet")
    import pyfiglet
os.system("clear")

# Print ASCII art
ascii_art = pyfiglet.figlet_format("Advance IP Scanner")
print(f"{Fore.BLUE}{ascii_art}{Style.RESET_ALL}")
print("\nCreator - GiuCoder\n\n")

# Flag to indicate if the program should stop
stop_flag = False

# Signal handler for SIGINT


def signal_handler(sig, frame):
    global stop_flag
    print("\nStopping program...")
    stop_flag = True


signal.signal(signal.SIGINT, signal_handler)


def scan(ip, port, output_file):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            sock.connect((ip, port))
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(
                f"{Fore.GREEN}[+] {ip}:{port} is open ({current_time}){Style.RESET_ALL}")
            with open(output_file, 'a') as f:
                f.write(f"{ip}:{port} is open\n")
            return True
        except (ConnectionRefusedError, socket.timeout):
            return False


def scan_range(start_ip, end_ip, port, output_file):
    global stop_flag
    open_count = 0
    for i in range(struct.unpack('>I', socket.inet_aton(start_ip))[0], struct.unpack('>I', socket.inet_aton(end_ip))[0]):
        if stop_flag:
            break  # Stop scanning if stop_flag is set
        ip = socket.inet_ntoa(struct.pack('>I', i))
        if scan(ip, port, output_file):
            open_count += 1
    return open_count


if __name__ == '__main__':
    try:
        start_ip = input("[*] Enter the start IP address: ")
        end_ip = input("[*] Enter the end IP address: ")
        port = int(input("[*] Enter the port number to scan: "))
        output_file = input("[*] Enter the output file name: ")

        # Check if start and end IP addresses are valid
        start_ip_addr = ipaddress.IPv4Address(start_ip)
        end_ip_addr = ipaddress.IPv4Address(end_ip)

        if start_ip_addr > end_ip_addr:
            print("Error: Start IP address cannot be greater than end IP address")
            sys.exit()

        # Calculate the number of IP addresses to scan
        start_octet = int(start_ip.split('.')[2])
        end_octet = int(end_ip.split('.')[2])
        num_ips = (end_octet - start_octet + 1) * 254

        open_count = 0
        threads = []
        for i in range(1, 255):
            t = threading.Thread(target=scan_range, args=(
                f"{start_ip.split('.')[0]}.{start_ip.split('.')[1]}.{i}.1", f"{end_ip.split('.')[0]}.{end_ip.split('.')[1]}.{i}.255", port, output_file))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        # Estimate the time it will take to scan each IP address (in seconds)
        scan_time = 1.5

        # Calculate the estimated time it will take to complete the scan (in minutes)
        est_time = math.ceil(num_ips * scan_time / 60)
        print(
            f"\n\nScan complete.\n Open IP Address{open_count}nEstimated time: {est_time} minutes.\nSaved To : " + output_file)

    except ValueError:
        print("Error: Invalid IP address")
        sys.exit()

    except KeyboardInterrupt:
        print(f"\nScan interrupted by user.")
        sys.exit()
