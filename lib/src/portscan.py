import socket
import threading

def scan_port(host, port, results):
    """Threaded port scan."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            results.append(port)
            print(f"Port {port} is open on {host}.")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
    finally:
        sock.close()

def scan_ports(host, ports):
    """Scan multiple ports using threading."""
    results = []
    threads = []

    for port in ports:
        thread = threading.Thread(target=scan_port, args=(host, port, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results
