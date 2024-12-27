import sys
sys.path.append('../lib')

import scanner
import pingsweep
import portscan
import servicedetect
import results

def print_banner():
    print("""
    =============================
              Pico Nmap
    =============================
    Commands:
      ping_sweep <network> <start> <end>         - Perform a ping sweep
      port_scan <host> <ports> [save]            - Scan ports on a host
      detect_service <host> <port>               - Detect service on a port
      detect_dns <host>                          - Check if DNS service is running
      detect_protocol <host> <port>              - Detect specific protocols
      save_results <filename> <data>             - Save scan results to file
      exit                                       - Exit the tool
    """)

def main():
    print_banner()
    while True:
        try:
            command = input("PicoNmap> ").strip().split()
            if not command:
                continue

            cmd = command[0]
            args = command[1:]

            if cmd == "ping_sweep":
                if len(args) < 2:
                    print("Usage: ping_sweep <network> <start> <end>")
                    continue
                network = args[0]
                start = int(args[1])
                end = int(args[2]) if len(args) > 2 else 254
                live_hosts = pingsweep.ping_sweep(network, start, end)
                print(f"Live hosts: {live_hosts}")

            elif cmd == "port_scan":
                if len(args) < 2:
                    print("Usage: port_scan <host> <ports> [save]")
                    continue
                host = args[0]
                ports = list(map(int, args[1].split(",")))
                open_ports = portscan.scan_ports(host, ports)
                print(f"Open ports: {open_ports}")
                if len(args) > 2 and args[2] == "save":
                    results.save_results("port_scan_results.txt", str(open_ports))

            elif cmd == "detect_service":
                if len(args) < 2:
                    print("Usage: detect_service <host> <port>")
                    continue
                host = args[0]
                port = int(args[1])
                service = servicedetect.detect_service_low_level(host, port)
                print(f"Service on port {port}: {service}")

            elif cmd == "detect_dns":
                if len(args) < 1:
                    print("Usage: detect_dns <host>")
                    continue
                host = args[0]
                dns_service = servicedetect.detect_dns_service(host)
                print(f"DNS Service on {host}: {dns_service}")

            elif cmd == "detect_protocol":
                if len(args) < 2:
                    print("Usage: detect_protocol <host> <port>")
                    continue
                host = args[0]
                port = int(args[1])
                protocol = servicedetect.detect_protocol(host, port)
                print(f"Protocol on port {port}: {protocol}")

            elif cmd == "save_results":
                if len(args) < 2:
                    print("Usage: save_results <filename> <data>")
                    continue
                filename = args[0]
                data = " ".join(args[1:])
                results.save_results(filename, data)

            elif cmd == "exit":
                print("Exiting PicoNmap. Goodbye!")
                break

            else:
                print(f"Unknown command: {cmd}")

        except KeyboardInterrupt:
            print("\nExiting PicoNmap. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
