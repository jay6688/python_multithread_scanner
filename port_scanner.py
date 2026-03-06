import socket
import threading
from queue import Queue
import argparse 

# ==========================================
# 1. COMMAND LINE INTERFACE (CLI) SETUP
# ==========================================
# argparse lets us pass commands from the terminal (like 'python scanner.py 10.10.10.10 -p 500')
parser = argparse.ArgumentParser(description="My Custom Python Port Scanner")

# Mandatory argument: The user MUST provide a target IP or domain
parser.add_argument("target", help="The IP address or domain you want to scan")

# Optional argument: The user CAN provide a specific number of ports, defaults to 1024 if left blank
parser.add_argument("-p", "--ports", type=int, default=1024, help="Number of ports to scan (default: 1024)")

# This actually reads what you typed in the terminal and stores it in the 'args' variable
args = parser.parse_args() 

# ==========================================
# 2. DNS RESOLUTION & TARGET SETUP
# ==========================================
target_domain = args.target
max_port = args.ports

# Computers route traffic using IPs, not domains. 
# gethostbyname acts like a phonebook, turning 'google.com' into '142.250.190.46'
target_ip = socket.gethostbyname(target_domain)

print("-" * 50)
print(f"[*] Scanning target: {target_ip}...")
print(f"[*] Scanning ports 1 through {max_port}...")
print("-" * 50)

# ==========================================
# 3. THE QUEUE (THE CHECKLIST)
# ==========================================
# The Queue is a thread-safe stack of "tickets". It stops two threads from scanning the same port.
queue = Queue()

# ==========================================
# 4. THE CORE ENGINE (THE NMAP PART)
# ==========================================
def scan_port(port):
    try:
        # AF_INET = IPv4 | SOCK_STREAM = TCP Protocol
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # If the port doesn't answer in 0.5 seconds, hang up and assume it's closed/filtered
        s.settimeout(0.5) 
        
        # connect_ex physically attempts the TCP 3-way handshake (SYN -> SYN/ACK -> ACK)
        # If it returns 0, the handshake succeeded and the port is OPEN.
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            print(f"[+] Port {port} is OPEN!")
            
            # BANNER GRABBING: Stay on the line and listen for up to 1024 bytes
            # This is how we find out WHAT service is running (e.g., "OpenSSH 8.2")
            try:
                banner = s.recv(1024).decode().strip()
                if banner:
                    print(f"    [>] Service Banner: {banner}")
            except:
                pass # If the server doesn't send a banner, just ignore and move on
                
        # Always close the socket to free up computer memory
        s.close()
    except:
        pass

# ==========================================
# 5. THE WORKERS (MULTITHREADING)
# ==========================================
def worker():
    # Keep working as long as there are still ports left in the queue
    while not queue.empty():
        port = queue.get() # Grab the next port number from the queue
        scan_port(port)    # Run our core engine on that port
        queue.task_done()  # Tell the queue we finished this ticket

# Fill the queue with the ports we want to scan (e.g., 1 through 1024)
for port in range(1, max_port + 1):
    queue.put(port)

# Spawn 100 threads (workers) to scan 100 ports at the exact same time
# This makes the scanner lightning fast
thread_list = []
for t in range(100):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)
    thread.start()

# Tell the script to wait here until the queue is completely empty before finishing
queue.join()

print("-" * 50)
print("[*] Scan Complete!")