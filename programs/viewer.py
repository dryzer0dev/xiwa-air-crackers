import requests
import socket
import re
import os
import argparse
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import time
import sys
import ssl
from urllib.parse import urljoin

init()

def print_animated(text, color=Fore.RED, delay=0.01):
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def get_server_info(url):
    try:
        domain = url.split('//')[-1].split('/')[0]
        ip = socket.gethostbyname(domain)
        
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
        
        response = requests.head(url)
        headers = response.headers
        
        print_animated("\n[>] Server Information:", Fore.RED)
        print_animated(f"[>] Domain: {domain}", Fore.YELLOW)
        print_animated(f"[>] IP Address: {ip}", Fore.YELLOW)
        print_animated(f"[>] Server: {headers.get('Server', 'Unknown')}", Fore.YELLOW)
        print_animated(f"[>] SSL Issuer: {dict(cert['issuer'][0]).get('organizationName')}", Fore.YELLOW)
        print_animated(f"[>] SSL Expiry: {cert['notAfter']}", Fore.YELLOW)
        print_animated(f"[>] Content Type: {headers.get('Content-Type', 'Unknown')}", Fore.YELLOW)
        print_animated(f"[>] Powered By: {headers.get('X-Powered-By', 'Unknown')}", Fore.YELLOW)
        print_animated(f"[>] HTTP Version: {response.raw.version}", Fore.YELLOW)
        print_animated(f"[>] Connection: {headers.get('Connection', 'Unknown')}", Fore.YELLOW)
        print_animated(f"[>] Cache Control: {headers.get('Cache-Control', 'Unknown')}", Fore.YELLOW)
        
    except Exception as e:
        print_animated(f"[x] Error getting server info: {e}", Fore.RED)

def save_source_code(url, output_dir):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        os.makedirs(output_dir, exist_ok=True)
        
        html_file = os.path.join(output_dir, 'source.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        css_links = soup.find_all('link', rel='stylesheet')
        for i, css in enumerate(css_links):
            if css.get('href'):
                css_url = css['href']
                if not css_url.startswith(('http://', 'https://')):
                    css_url = urljoin(url, css_url)
                
                try:
                    css_response = requests.get(css_url)
                    css_file = os.path.join(output_dir, f'style_{i}.css')
                    with open(css_file, 'w', encoding='utf-8') as f:
                        f.write(css_response.text)
                except:
                    continue

        script_tags = soup.find_all('script', src=True)
        for i, script in enumerate(script_tags):
            script_url = script['src']
            if not script_url.startswith(('http://', 'https://')):
                script_url = urljoin(url, script_url)
            
            try:
                script_response = requests.get(script_url)
                ext = script_url.split('.')[-1] if '.' in script_url else 'js'
                if ext not in ['js', 'jsx', 'tsx']:
                    ext = 'js'
                script_file = os.path.join(output_dir, f'script_{i}.{ext}')
                with open(script_file, 'w', encoding='utf-8') as f:
                    f.write(script_response.text)
            except:
                continue

        php_links = soup.find_all('a', href=re.compile(r'\.php$'))
        for i, php in enumerate(php_links):
            php_url = php['href']
            if not php_url.startswith(('http://', 'https://')):
                php_url = urljoin(url, php_url)
            
            try:
                php_response = requests.get(php_url)
                php_file = os.path.join(output_dir, f'page_{i}.php')
                with open(php_file, 'w', encoding='utf-8') as f:
                    f.write(php_response.text)
            except:
                continue
        
        print_animated(f"\n[!] Source code saved to: {output_dir}", Fore.GREEN)
        
    except Exception as e:
        print_animated(f"[x] Error saving source code: {e}", Fore.RED)

def main():
    print_animated("""
    ██╗  ██╗██╗██╗    ██╗ █████╗     ██╗   ██╗██╗███████╗██╗    ██╗███████╗██████╗ 
    ╚██╗██╔╝██║██║    ██║██╔══██╗    ██║   ██║██║██╔════╝██║    ██║██╔════╝██╔══██╗
     ╚███╔╝ ██║██║ █╗ ██║███████║    ██║   ██║██║█████╗  ██║ █╗ ██║█████╗  ██████╔╝
     ██╔██╗ ██║██║███╗██║██╔══██║    ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║██╔══╝  ██╔══██╗
    ██╔╝ ██╗██║╚███╔███╔╝██║  ██║     ╚████╔╝ ██║███████╗╚███╔███╔╝███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝      ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝
    """, Fore.RED, 0.001)

    parser = argparse.ArgumentParser(description='Website Source Code Viewer')
    parser.add_argument('url', help='URL of the website to view')
    parser.add_argument('--save', help='Directory to save source code')
    parser.add_argument('--info', action='store_true', help='Show server information')
    
    args = parser.parse_args()
    
    if args.info:
        get_server_info(args.url)
    
    if args.save:
        save_source_code(args.url, args.save)
    else:
        try:
            response = requests.get(args.url)
            response.raise_for_status()
            default_dir = os.path.join('output', 'source')
            save_source_code(args.url, default_dir)
        except Exception as e:
            print_animated(f"[x] Error accessing website: {e}", Fore.RED)

if __name__ == "__main__":
    main()