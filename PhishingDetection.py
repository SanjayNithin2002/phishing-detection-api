import re
import urllib.request as urlreq
from urllib.parse import urlparse
import urllib
import requests
import favicon
import socket
from bs4 import BeautifulSoup
import whois
import datetime
import dns.resolver
import ssl



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
    try:
        link = urlreq.urlopen(url)
        full_url = link.url
        if full_url:
            return 1 if len(url) == len(full_url) else -1
        else:
            return 0
    except urllib.error.URLError: # type: ignore
        return -1


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

def check_https_certificate(url):
    url = url.replace("https://", "")
    url = url.replace("www.", "")
    try:
        # Create an SSL context
        context = ssl.create_default_context()

        with context.wrap_socket(socket.socket(), server_hostname=url) as sock:
            sock.connect((url, 443))
            cert = sock.getpeercert()
            issuer = cert["issuer"][1][0][1]
            expiration_date = cert["notAfter"]
            current_date = datetime.datetime.now()
            
            # Check if the certificate issuer is trusted
            trusted_issuers = ["GeoTrust", "GoDaddy", "Network Solutions", "Thawte", "Comodo", "Doster", "VeriSign", "DigiCert Inc"]
            if issuer in trusted_issuers:
                expiration_date = datetime.datetime.strptime(expiration_date, r'%b %d %H:%M:%S %Y %Z')
                certificate_age = expiration_date - current_date
                minimum_certificate_age = datetime.timedelta(days=365)
                if certificate_age >= minimum_certificate_age:
                    return 1
                else:
                    return -1
            else:
                return 0
                
    except ssl.SSLError:
        return -1
    except socket.error:
        return -1

def check_domain_expiration(domain):
    try:
        domain_info = whois.whois(domain)
        if domain_info.expiration_date is not None:
            current_date = datetime.datetime.now().date()
            if isinstance(domain_info.expiration_date, list):
                expiration_date = domain_info.expiration_date[0].date()
            else:
                expiration_date = domain_info.expiration_date.date()
            time_difference = (expiration_date - current_date).days
            if time_difference <= 365:
                return -1
            else:
                return 1
        else:
            return 0
    except whois.parser.PywhoisError:
        return -1


def is_favicon(url):
    try:
        icons = favicon.get(url)
        if icons:
            icon = icons[0]
            icon_url = icon.url
            parsed_url = urlparse(icon_url)
            website = parsed_url.netloc
            return 1 if website in url else -1
        else:
            return 0
    except Exception:
        return -1

def is_port(url):
    port = 80
    try:
        if url.startswith("https"):
            port = 443
        parsed_url = urlparse(url).netloc
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((parsed_url, port))
        sock.close()
        return 1 if result == 0 else -1
    except (socket.gaierror, socket.timeout):
        return -1


def is_https(url):
    return 1 if url.startswith("https") else -1

def calculate_request_url_percentage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            webpage_content = response.text
            total_urls = 0
            external_urls = 0
            base_domain = urlparse(url).hostname.replace("www.", "").split('.')[0]
            soup = BeautifulSoup(webpage_content, 'html.parser')

            image_tags = soup.find_all('img')
            video_tags = soup.find_all('video')
            audio_tags = soup.find_all('audio')
            for tag in image_tags:
                total_urls += 1
                url = tag.get('src')
                if url and base_domain not in url:
                    external_urls += 1
            for tag in video_tags:
                total_urls += 1
                url = tag.get('src')
                if url and base_domain not in url:
                    external_urls += 1
            for tag in audio_tags:
                total_urls += 1
                url = tag.get('src')
                if url and base_domain not in url:
                    external_urls += 1
            if total_urls > 0:
                percentage = (external_urls / total_urls) * 100
                if percentage < 22:
                    return 1
                elif 22 <= percentage <= 61:
                    return 0
                else:
                    return -1
            else:
                return 0
        else:
            return 0
    except (requests.exceptions.RequestException):
        return -1

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
                if link and link.startswith("#"): 
                    different_site_links.append(link)
                    continue
                if link:
                    parsed_link = urlparse(link)
                    link_domain = parsed_link.netloc
                    if not link_domain:
                        continue
                    if not link_domain.startswith("www."):
                        link_domain = "www." + link_domain
                    if link_domain != main_domain:
                        different_site_links.append(link_domain)
            if len(anchor_tags) > 0:
                a_percentage = len(different_site_links) / len(anchor_tags) * 100
                if a_percentage < 31:
                    return 1
                elif 31 <= a_percentage < 67:
                    return 0
                else:
                    return -1
            else:
                return 0
        else:
            return 0
    except (requests.exceptions.RequestException, ConnectionError):
        return -1
   
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
                if not link:
                    link = tag.get('content')
                if link:
                    parsed_link = urlparse(link)
                    link_domain = parsed_link.netloc
                    if not link_domain:
                        continue
                    if not link_domain.startswith("www."):
                        link_domain = "www." + link_domain
                    if link_domain != main_domain:
                        different_site_links.append(link_domain)
            if len(meta_tags) > 0:
                a_percentage = len(different_site_links) / len(meta_tags) * 100
                if a_percentage < 17:
                    return 1
                elif 17 <= a_percentage < 81:
                    return 0
                else:
                    return -1
            else:
                return 0
        else:
            return 0
    except (requests.exceptions.RequestException, ConnectionError):
        return -1

def get_form_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            form = soup.find('form')
            form_url = form.get('action') if form else None
            if form_url and str(form_url).startswith("/"):
                return 1
            parsed_url = urlparse(url).netloc
            parsed_form_url = urlparse(str(form_url)).netloc if form_url else None
            if not form_url:
                return -1
            elif parsed_form_url and parsed_form_url != parsed_url:
                return 0
            else:
                return 1
        else:
            return 0
    except (requests.exceptions.RequestException, ConnectionError):
        return -1

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

            if mailto_links:
                return -1
            else:
                return 1
        else:
            return 0
    except (requests.exceptions.RequestException, ConnectionError):
        return -1

def get_redirect_urls(url):
    try:
        redirect_urls = []
        response = requests.get(url, allow_redirects=True)
        for redirect in response.history:
            redirect_urls.append(redirect.url)
        no_of_redirects = len(redirect_urls)
        
        if no_of_redirects <= 1:
            return 1
        elif 2 <= no_of_redirects < 4:
            return 0
        else:
            return -1

    except (requests.exceptions.RequestException, ConnectionError):
        return -1

def check_status_bar(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for element in soup.find_all():
            if element.has_attr('onmouseover'):
                onmouseover = element['onmouseover']
                if 'window.status' in onmouseover:
                    return -1

        return 1

    except (requests.exceptions.RequestException, ConnectionError):
        return -1

def check_right_click_disabled(url):
    try:
        response = requests.get(url)
        source_code = response.text

        if "event.button==2" in source_code:
            return -1

        return 1

    except (requests.exceptions.RequestException, ConnectionError):
        return -1

def check_popup_windows(url):
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        popups = soup.find_all(attrs={"data-popup": True})
        for popup in popups:
            text_fields = popup.select('input[type="text"]')
            if len(text_fields) > 0:
                return -1

        return 1

    except (requests.exceptions.RequestException, ConnectionError):
        return -1

def check_iframe_usage(url):
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        iframes = soup.find_all('iframe')

        if len(iframes) > 0:
            return -1

        return 1

    except (requests.exceptions.RequestException, ConnectionError):
        return -1

def check_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if not creation_date:
            return -1

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        current_date = datetime.datetime.now()
        age = (current_date - creation_date).days

        if age >= 180:
            return 1

    except (whois.parser.PywhoisError):
        return -1

    return -1

def check_dns_records(domain):
    parsed_url = urlparse(domain).netloc
    if not parsed_url: return -1
    try:
        answers = dns.resolver.resolve(parsed_url)
        if answers:
            return 1

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return -1

    return -1



def check_google_index(url):
    try:
        google_url = "https://www.google.com/search?q=site:" + url + "&hl=en"
        response = requests.get(google_url, cookies={"CONSENT": "YES+1"})
        soup = BeautifulSoup(response.content, "html.parser")
        not_indexed = re.compile("did not match any documents")

        if soup(text=not_indexed):
            return -1
        else:
            return 1

    except requests.exceptions.RequestException:
        return -1

def url_domain_matches(url1, url2):
    return get_domain(url1) == get_domain(url2)

def get_domain(url):
    return url.split("//")[-1].split("/")[0]

def count_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")
        
        external_links = 0
        for link in links:
            href = link.get("href")
            if href and href.startswith("http") and not url_domain_matches(href, url):
                external_links += 1
        
        if external_links == 0:
            return -1
        elif external_links > 0 and external_links <= 2:
            return 0
        else:
            return 1

    except requests.exceptions.RequestException:
        return -1

def detect_phishing(url):
    results = {}

    # Apply the functions and store the results in the dictionary
    results['having_IPhaving_IP_Address'] = find_ip_address(url)
    results['URLURL_Length'] = url_length(url)
    results['Shortining_Service'] = is_shortened(url)
    results['having_At_Symbol'] = at_symbol(url)
    results['double_slash_redirecting'] = has_double_slashes(url)
    results['Prefix_Suffix'] = prefix_suffix(url)
    results['having_Sub_Domain'] = having_subdomain(url)
    results['SSLfinal_State'] = check_https_certificate(url)
    results['Domain_registeration_length'] = check_domain_expiration(get_domain(url))
    results['Favicon'] = is_favicon(url)
    results['port'] = is_port(url)
    results['HTTPS_token'] = is_https(url)
    results['Request_URL'] = calculate_request_url_percentage(url)
    results['URL_of_Anchor'] = anchor_links(url)
    results['Links_in_tags'] = meta_links(url)
    results['SFH'] = get_form_url(url)
    results['Submitting_to_email'] = check_mailto_links(url)
    results['Abnormal_URL'] = get_redirect_urls(url)
    results['Redirect'] = check_status_bar(url)
    results['on_mouseover'] = check_right_click_disabled(url)
    results['RightClick'] = check_popup_windows(url)
    results['popUpWidnow'] = check_iframe_usage(url)
    results['Iframe'] = check_iframe_usage(url)
    results['age_of_domain'] = check_domain_age(get_domain(url))
    results['DNSRecord'] = check_dns_records(get_domain(url))
    results['Google_Index'] = check_google_index(url)
    results['Domain_registeration_length'] = check_domain_expiration(get_domain(url))
    results['Links_pointing_to_page'] = count_links(url)
    return results

