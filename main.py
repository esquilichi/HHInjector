#
#
#   Host Header Injection Tool
#   made by Ismael Gómez Esquilichi
#
import sys
from colorama import Fore, init
import requests
import argparse


def check_chars(i1, i2):
    diferencia = i1 - i2
    if diferencia < 0:
        diferencia = diferencia * -1
    return diferencia


def web_cache_attack(url_web_cache, i):
    r = requests.get(url_web_cache, headers={"Host": "vulnerable.es", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                                                                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                                    "Chrome/51.0.2704.103 Safari/537.36"},
                     allow_redirects=False, verify=False)

    i2 = 0
    for c in r.text:
        i2 += 1
    diferencia = check_chars(i, i2)

    if diferencia < 400:
        if "vulnerable.es" in r.text:
            print(url_web_cache + " VULNERABLE changing Host Header :)")
            print("Host changes reflects on victim HTML\n")


# Este ataque debe hacerse con HTTP
def redirected_attack(url):
    burp0_url = url
    burp0_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/88.0.4324.150 Safari/537.36",
        "Host": "vulnerable.es"
    }

    try:
        r = requests.get(burp0_url, headers=burp0_headers, allow_redirects=False, verify=False)
        if r.headers['Location'] == "https://vulnerable.es/":
            print(url.strip() + " VULNERABLE to open redirection via changing Host Header\n")
    except KeyError:
        pass

    try:
        header2.update(user_agent)
        r = requests.get(burp0_url, headers=header2, allow_redirects=False, verify=False)
        if r.headers['Location'] == "https://vulnerable.es/":
            print(url.strip() + "VULNERABLE to open redirection changing X-Forwarded-Host header")
    except KeyError:
        pass

    try:
        header3.update(user_agent)
        r = requests.get(burp0_url, headers=header3, allow_redirects=False, verify=False)
        if r.headers['Location'] == "https://vulnerable.es/":
            print(url.strip() + "VULNERABLE to open redirection changing Origin header")
    except KeyError:
        pass


def attack_lista(lista):
    for u in lista:
        try:
            r = requests.get(u.strip(), verify=False)
            initial_text = r.text
            i = 0
            for c in initial_text:
                i += 1
            web_cache_attack(u.strip(), i)
            redirected_attack(u.strip())
        except Exception:
            pass


def attack_url(url):
    print("Testing: " + url)
    r = requests.get(url, verify=False)
    initial_text = r.text
    i = 0
    for c in initial_text:
        i += 1
    web_cache_attack(url.encode('ascii', errors='ignore'), i)
    redirected_attack(url.encode('ascii', errors='ignore'))


banner = """
 _   _ _   _ _____ _       _           _             
| | | | | | |_   _(_)     (_)         | |            
| |_| | |_| | | |  _ _ __  _  ___  ___| |_ ___  _ __ 
|  _  |  _  | | | | | '_ \| |/ _ \/ __| __/ _ \| '__|
| | | | | | |_| |_| | | | | |  __/ (__| || (_) | |   
\_| |_|_| |_/\___/|_|_| |_| |\___|\___|\__\___/|_|   
                         _/ |                        
                        |__/                         
"""

requests.packages.urllib3.disable_warnings()
# Cosas de Colorama
init()
print(Fore.GREEN + banner + Fore.RED)
print(Fore.RED + "made by Ismael Gómez Esquilichi\n" + Fore.LIGHTGREEN_EX)

# Burpsuite Confighttps://www.uam.es/uam/inicio
proxies = {
    'https': 'http://127.0.0.1:8080',
}

header1 = {
    "Host": "vulnerable.es"
}
header2 = {
    "X-Forwarded-Host": "vulnerable.es"
}
header3 = {
    "Origin": "vulnerable.es"
}
user_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/88.0.4324.150 Safari/537.36"
}

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=False, help="URL a comprobar")
ap.add_argument("-l", "--list", required=False, help="Lista de URLs separadas por comas")

url = str((vars(ap.parse_args()))['url'])
lista = str((vars(ap.parse_args()))['list'])

if url.lower() != 'none':
    if '//' not in url:
        print("Introduce the URL with the protocol you want to use (HTTP/HTTPS)")
        sys.exit(1)
    else:
        attack_url(url)
        sys.exit(0)
else:
    if lista != 'None':
        lista = open(lista, 'r').read().split(",")
        if lista is not None:
            attack_lista(lista)
            sys.exit(0)
