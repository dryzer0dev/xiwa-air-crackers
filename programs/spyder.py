import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import os
from datetime import datetime
import socket
import whois
from colorama import init, Fore, Style
import sys
import time

init()

def print_animated(text, color=Fore.RED, delay=0.01):
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

print_animated("""
██╗  ██╗██╗██╗    ██╗ █████╗     ███████╗██████╗ ██╗   ██╗██████╗ ███████╗██████╗ 
╚██╗██╔╝██║██║    ██║██╔══██╗    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
 ╚███╔╝ ██║██║ █╗ ██║███████║    ███████╗██████╔╝ ╚████╔╝ ██║  ██║█████╗  ██████╔╝
 ██╔██╗ ██║██║███╗██║██╔══██║    ╚════██║██╔═══╝   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
██╔╝ ██╗██║╚███╔███╔╝██║  ██║    ███████║██║        ██║   ██████╔╝███████╗██║  ██║
╚═╝  ╚═╝╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚══════╝╚═╝        ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
""", Fore.RED, 0.001)

class WebSpyder:
    def __init__(self, url):
        self.url = url
        self.visited_urls = set()
        self.emails = set()
        self.phone_numbers = set()
        self.social_media = set()
        self.output_dir = f"output/spyder/{urllib.parse.urlparse(url).netloc}"
        os.makedirs(self.output_dir, exist_ok=True)

    def is_valid_url(self, url):
        try:
            parsed = urllib.parse.urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)
        except:
            return False

    def normalize_url(self, url):
        if url.startswith('//'):
            return 'https:' + url
        elif url.startswith('/'):
            return urllib.parse.urljoin(self.url, url)
        return url

    def extract_emails(self, text):
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return set(re.findall(email_pattern, text))

    def extract_phone_numbers(self, text):
        phone_pattern = r'\+?[\d\s-]{10,}'
        return set(re.findall(phone_pattern, text))

    def extract_social_media(self, soup):
        social_media = set()
        social_platforms = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube']
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            for platform in social_platforms:
                if platform in href:
                    social_media.add(link['href'])
        return social_media

    def get_server_info(self, domain):
        try:
            ip = socket.gethostbyname(domain)
            whois_info = whois.whois(domain)
            info = {
                'IP': ip,
                'Registrar': whois_info.registrar,
                'Creation Date': whois_info.creation_date,
                'Expiration Date': whois_info.expiration_date,
                'Name Servers': whois_info.name_servers
            }
            return info
        except Exception as e:
            print_animated(f"[x] Error getting server info: {e}", Fore.RED)
            return None

    def crawl(self, url, depth=2):
        if depth == 0 or url in self.visited_urls:
            return
        self.visited_urls.add(url)
        print_animated(f"[>] Crawling: {url}", Fore.CYAN)
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.emails.update(self.extract_emails(response.text))
            self.phone_numbers.update(self.extract_phone_numbers(response.text))
            self.social_media.update(self.extract_social_media(soup))
            for link in soup.find_all('a', href=True):
                next_url = self.normalize_url(link['href'])
                if self.is_valid_url(next_url) and urllib.parse.urlparse(next_url).netloc == urllib.parse.urlparse(self.url).netloc:
                    self.crawl(next_url, depth-1)
        except Exception as e:
            print_animated(f"[x] Error crawling {url}: {e}", Fore.RED)

    def save_results(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(os.path.join(self.output_dir, f'emails_{timestamp}.txt'), 'w') as f:
            for email in self.emails:
                f.write(f"{email}\n")
        with open(os.path.join(self.output_dir, f'phone_numbers_{timestamp}.txt'), 'w') as f:
            for phone in self.phone_numbers:
                f.write(f"{phone}\n")
        with open(os.path.join(self.output_dir, f'social_media_{timestamp}.txt'), 'w') as f:
            for link in self.social_media:
                f.write(f"{link}\n")
        server_info = self.get_server_info(urllib.parse.urlparse(self.url).netloc)
        if server_info:
            with open(os.path.join(self.output_dir, f'server_info_{timestamp}.txt'), 'w') as f:
                for key, value in server_info.items():
                    f.write(f"{key}: {value}\n")

def main():
    url = input("[>] Enter the target URL (e.g., https://example.com): ")
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    spyder = WebSpyder(url)
    print_animated("\n[>] Starting web crawling and information gathering...", Fore.YELLOW)
    spyder.crawl(url)
    spyder.save_results()
    
    print_animated("\n[!] Crawling completed!", Fore.GREEN)
    print_animated(f"[>] Found {len(spyder.emails)} email addresses", Fore.CYAN)
    print_animated(f"[>] Found {len(spyder.phone_numbers)} phone numbers", Fore.CYAN)
    print_animated(f"[>] Found {len(spyder.social_media)} social media links", Fore.CYAN)
    print_animated(f"\n[>] Results saved in: {spyder.output_dir}", Fore.YELLOW)

if __name__ == "__main__":
    main()