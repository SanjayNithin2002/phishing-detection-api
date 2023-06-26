import re
import urllib.request as urlreq
from urllib.parse import urlparse
import requests
import favicon
import socket
from bs4 import BeautifulSoup


def find_ip_address(url):
    ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    match = re.search(ip_regex, url)
    return -1 if match else 1

def url_length(url):
    x = len(url)
    if x < 54 : return 1
    elif x>=54 and x <=75 : return 0  
    else: return -1

def is_shortened(url):
    link = urlreq.urlopen(url)
    fullURL = link.url
    return 1 if len(url) == len(fullURL) else -1

def at_symbol(url):
    return -1 if ('@' in url) else 1

def has_double_slashes(url):
    pattern = r'https?://.*//' 
    match = re.search(pattern, url)
    return -1 if match else 1

def prefix_suffix(url):
    pattern = r'-'  
    match = re.search(pattern, url)
    return -1 if match else 1

def having_subdomain(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if hostname.startswith('www.'):
        hostname = hostname[4:]
    if '.' in hostname:
        subdomain = hostname.split('.')
    else:
        subdomain = ""
    no_of_subdomains= len(subdomain) - 2
    if(no_of_subdomains == 0): return 1
    elif(no_of_subdomains == 1): return 0
    else: return -1

def is_favicon(url):
    icons = favicon.get(url)
    icon = icons[0]
    icon_url = icon.url
    parsed_url = urlparse(icon_url)
    website = parsed_url.netloc
    return 1 if website in url else -1

def is_port(url):
    port = 80
    if url.startswith("https"): port = 443
    parsed_url = urlparse(url).netloc
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1) 
    result = sock.connect_ex((parsed_url, port))
    sock.close()
    return 1 if result == 0 else -1

def is_https(url):
    return 1 if url.startswith("https") else -1

def anchor_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            anchor_tags = soup.find_all('a')
            parsed_url = urlparse(url)
            main_domain = parsed_url.netloc
            different_site_links = []

            for tag in anchor_tags:
                link = tag.get('href')
                if link:
                    parsed_link = urlparse(link)
                    link_domain = parsed_link.netloc
                    if not link_domain: continue
                    if not link_domain.startswith("www.") : link_domain = "www." + link_domain
                    if link_domain != main_domain :
                        different_site_links.append(link_domain)
            a_percentage = len(different_site_links) / len(anchor_tags) * 100
            print(a_percentage)
            if a_percentage < 31 : return 1
            elif a_percentage >= 31 and a_percentage < 67: return 0 
            else : return -1
        
    except requests.exceptions.RequestException:
        pass
    return []

def meta_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_tags = list(set(soup.find_all('meta') + soup.find_all("script") + soup.find_all("link")))
            parsed_url = urlparse(url)
            main_domain = parsed_url.netloc
            different_site_links = []

            for tag in meta_tags:
                link = tag.get('href')
                if not link: link = tag.get('content')
                if link:
                    parsed_link = urlparse(link)
                    link_domain = parsed_link.netloc
                    if not link_domain: continue
                    if not link_domain.startswith("www.") : link_domain = "www." + link_domain
                    if link_domain != main_domain :
                        different_site_links.append(link_domain)
            a_percentage = len(different_site_links) / len(meta_tags) * 100
            if a_percentage < 17 : return 1
            elif a_percentage >= 17 and a_percentage < 81: return 0 
            else : return -1
        
    except requests.exceptions.RequestException:
        pass
    return []

def get_form_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            form = soup.find('form')
            form_url = form.get('action') if form else None
            parsed_url = urlparse(url).netloc
            parsed_form_url = urlparse(form_url).netloc
            if not form_url: return -1
            elif not parsed_form_url: return 1
            elif parsed_form_url != parsed_url: return 0
            else: return 1
    except requests.exceptions.RequestException:
        pass

    return None

def check_mailto_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            anchor_tags = soup.find_all('a')
            mailto_links = []

            for tag in anchor_tags:
                link = tag.get('href')
                if link and link.startswith('mailto:'):
                    mailto_links.append(link)

            return -1 if mailto_links else 1
    except requests.exceptions.RequestException:
        pass

    return []

import pythonwhois

def perform_whois_lookup(domain):
    try:
        w = pythonwhois.get_whois(domain)
        return w
    except pythonwhois.shared.WhoisException as e:
        print("Error occurred during WHOIS lookup:", str(e))
        return None

# Example usage
domain = "example.com"
result = perform_whois_lookup(domain)

if result is not None:
    print("Domain Name:", result['domain_name'])
    print("Registrar:", result['registrar'])
    print("Registrant's Name:", result['contacts']['registrant']['name'])
    # ... and other relevant WHOIS information























