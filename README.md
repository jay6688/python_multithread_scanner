# 🕵️‍♂️ Python Multi-Threaded Port Scanner

A professional-grade, high-performance TCP port scanner built with Python. This tool leverages **Multithreading** and **Thread-Safe Queueing** to identify open ports and grab service banners in seconds—significantly faster than standard sequential scanners.

---

## 🚀 Features

* **Lightning Fast:** Uses 100 concurrent threads to scan hundreds of ports simultaneously.
* **CLI Powered:** Built with `argparse` to allow dynamic target and port range selection from the terminal.
* **Service Identification:** Features "Banner Grabbing" to retrieve information about the software running on open ports (e.g., SSH versions, Web Server headers).
* **Smart DNS:** Automatically resolves hostnames (e.g., `google.com`) to IPv4 addresses.
* **Robust Error Handling:** Designed to handle timeouts and connection resets gracefully.

---

## 🛠️ How It Works

The scanner uses the **TCP 3-Way Handshake** method. It attempts to connect to a target IP and port:
1.  **SYN:** Script sends a synchronization request.
2.  **SYN/ACK:** If the port is open, the server responds.
3.  **Result:** The script logs the port as `OPEN` and attempts to read the service banner.



---

## 💻 Installation & Usage

### 1. Requirements
* Python 3.x
* No external dependencies (Standard Library only).

### 2. Run the Scanner
Navigate to your project folder and use the following commands:

```bash
# Basic scan (Default: 1024 ports)
python port_scanner.py <target_ip_or_domain>

# Custom port range scan
python port_scanner.py <target_ip_or_domain> -p 500

# View the help menu
python port_scanner.py -h
