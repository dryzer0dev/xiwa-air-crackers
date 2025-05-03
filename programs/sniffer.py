import socket
import struct
import argparse
import time
from datetime import datetime
from colorama import init, Fore, Style
import sys

init()

def print_animated(text, color=Fore.RED, delay=0.01):
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

print_animated("""
██╗  ██╗██╗██╗    ██╗ █████╗     ███████╗███╗   ██╗██╗███████╗███████╗███████╗██████╗ 
╚██╗██╔╝██║██║    ██║██╔══██╗    ██╔════╝████╗  ██║██║██╔════╝██╔════╝██╔════╝██╔══██╗
 ╚███╔╝ ██║██║ █╗ ██║███████║    ███████╗██╔██╗ ██║██║█████╗  █████╗  █████╗  ██████╔╝
 ██╔██╗ ██║██║███╗██║██╔══██║    ╚════██║██║╚██╗██║██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██╗
██╔╝ ██╗██║╚███╔███╔╝██║  ██║    ███████║██║ ╚████║██║██║     ███████╗███████╗██║  ██║
╚═╝  ╚═╝╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝
""", Fore.RED, 0.001)

def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

def sniff_packets(output_file):
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    
    with open(output_file, 'w') as f:
        f.write("Timestamp,Source MAC,Destination MAC,Protocol,Source IP,Destination IP,Source Port,Destination Port\n")
        
        while True:
            try:
                raw_data, addr = conn.recvfrom(65536)
                dest_mac, src_mac, eth_proto = struct.unpack('! 6s 6s H', raw_data[:14])
                
                dest_mac = get_mac_addr(dest_mac)
                src_mac = get_mac_addr(src_mac)
                
                if eth_proto == 8:
                    version_header_len = raw_data[14]
                    version = version_header_len >> 4
                    header_len = (version_header_len & 15) * 4
                    
                    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[14:34])
                    src_ip = socket.inet_ntoa(src)
                    dest_ip = socket.inet_ntoa(target)
                    
                    if proto == 6:
                        offset = 14 + header_len
                        src_port, dest_port = struct.unpack('! H H', raw_data[offset:offset+4])
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"{timestamp},{src_mac},{dest_mac},TCP,{src_ip},{dest_ip},{src_port},{dest_port}\n")
                        f.flush()
                        print_animated(f"[>] TCP Packet captured: {src_ip}:{src_port} -> {dest_ip}:{dest_port}", Fore.GREEN, 0.001)
                        
                    elif proto == 17:
                        offset = 14 + header_len
                        src_port, dest_port = struct.unpack('! H H', raw_data[offset:offset+4])
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"{timestamp},{src_mac},{dest_mac},UDP,{src_ip},{dest_ip},{src_port},{dest_port}\n")
                        f.flush()
                        print_animated(f"[>] UDP Packet captured: {src_ip}:{src_port} -> {dest_ip}:{dest_port}", Fore.YELLOW, 0.001)
                        
            except KeyboardInterrupt:
                print_animated("\n[!] Sniffing stopped by user", Fore.RED)
                break
            except Exception as e:
                print_animated(f"[x] Error: {e}", Fore.RED)
                continue

def main():
    parser = argparse.ArgumentParser(description='Network Packet Sniffer')
    parser.add_argument('-o', '--output', required=True, help='Output file to save captured packets')
    
    args = parser.parse_args()
    
    print_animated("[>] Starting packet sniffing... Press Ctrl+C to stop", Fore.RED)
    print_animated(f"[>] Captured packets will be saved to: {args.output}", Fore.YELLOW)
    
    sniff_packets(args.output)

if __name__ == "__main__":
    main()