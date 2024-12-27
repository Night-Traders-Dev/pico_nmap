import socket

def banner_grab(host, port):
    """
    Perform a low-level banner grab on a specific port.

    Args:
        host (str): The target host.
        port (int): The target port.

    Returns:
        str: The banner or service information.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        # Send a generic request to trigger a response
        sock.send(b"HELLO\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        return banner if banner else "No banner retrieved"
    except socket.timeout:
        return "Timeout: No response from port"
    except Exception as e:
        return f"Error: {e}"


def detect_service_low_level(host, port):
    """
    Detect the service running on a specific port using protocol probing.

    Args:
        host (str): The target host.
        port (int): The target port.

    Returns:
        str: The detected service name or "Unknown".
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))

        # Protocol-specific probes
        if port == 80 or port == 443:  # HTTP/HTTPS
            sock.send(b"GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host.encode()))
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "HTTP" in response:
                return "HTTP/HTTPS"

        elif port == 21:  # FTP
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "FTP" in response:
                return "FTP"

        elif port == 22:  # SSH
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "SSH" in response:
                return "SSH"

        elif port == 25:  # SMTP
            sock.send(b"EHLO test\r\n")
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "SMTP" in response:
                return "SMTP"

        return "Unknown Service"
    except socket.timeout:
        return "Timeout: No response"
    except Exception as e:
        return f"Error: {e}"
    finally:
        sock.close()


def detect_dns_service(host):
    """
    Detect if a DNS service is running on port 53.

    Args:
        host (str): The target host.

    Returns:
        str: "DNS" if a DNS service is detected, otherwise "Unknown".
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

        # Construct a basic DNS query packet
        query = b'\x12\x34'  # Transaction ID
        query += b'\x01\x00'  # Flags (standard query)
        query += b'\x00\x01'  # Questions
        query += b'\x00\x00'  # Answer RRs
        query += b'\x00\x00'  # Authority RRs
        query += b'\x00\x00'  # Additional RRs
        query += b'\x03www\x06google\x03com\x00'  # Query: www.google.com
        query += b'\x00\x01'  # Type: A (Host Address)
        query += b'\x00\x01'  # Class: IN (Internet)

        # Send the DNS query
        sock.sendto(query, (host, 53))
        response, _ = sock.recvfrom(512)
        sock.close()

        if response:
            return "DNS"
        return "Unknown"
    except socket.timeout:
        return "Timeout: No DNS response"
    except Exception as e:
        return f"Error: {e}"


def detect_protocol(host, port):
    """
    Detect protocols like POP3, IMAP, or Telnet.

    Args:
        host (str): The target host.
        port (int): The target port.

    Returns:
        str: The detected protocol name or "Unknown".
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))

        if port == 110:  # POP3
            sock.send(b"USER test\r\n")
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "+OK" in response:
                return "POP3"

        elif port == 143:  # IMAP
            sock.send(b"1 LOGIN test test\r\n")
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "OK" in response:
                return "IMAP"

        elif port == 23:  # Telnet
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if response:
                return "Telnet"

        return "Unknown Protocol"
    except socket.timeout:
        return "Timeout: No response"
    except Exception as e:
        return f"Error: {e}"
    finally:
        sock.close()
