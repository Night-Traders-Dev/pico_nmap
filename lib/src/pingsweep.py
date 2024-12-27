import socket
import time

def ping_host(host):
    """Ping a host to check if it is alive."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        start_time = time.time()
        sock.sendto(b"PING", (host, 1))
        sock.recvfrom(1024)
        end_time = time.time()
        print(f"Host {host} is alive. Response time: {round((end_time - start_time) * 1000)}ms")
        return True
    except socket.timeout:
        return False
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return False
    finally:
        sock.close()

def ping_sweep(network, start=1, end=254):
    """Perform a ping sweep on a network."""
    live_hosts = []
    for i in range(start, end + 1):
        host = f"{network}.{i}"
        if ping_host(host):
            live_hosts.append(host)
    return live_hosts
