# Laborator: functii, metode si importuri pe web
# Student: Malai Carolina

import re
import json
import ssl
import socket
import hashlib
import urllib.parse
import requests
from datetime import datetime, timezone
from html.parser import HTMLParser

DOMENIU = "https://example.com"
MAX_WAIT = 10

def descompune_link(link):
    date = urllib.parse.urlparse(link)
    return {
        "protocol": date.scheme,
        "domeniu": date.netloc,
        "ruta": date.path
    }

def rezolva_relative(baza, lista_relative):
    lista_finala = []
    for rel in lista_relative:
        lista_finala.append(urllib.parse.urljoin(baza, rel))
    return lista_finala

def gaseste_toate_linkurile(html):
    rezultate = re.findall(r'href="(.*?)"', html)
    return list(set(rezultate))

def imparte_linkuri(lista_linkuri, nume_domeniu):
    interne = []
    externe = []
    for lk in lista_linkuri:
        url_abs = urllib.parse.urljoin("https://" + nume_domeniu, lk)
        host = urllib.parse.urlparse(url_abs).netloc
        if host == nume_domeniu or host == "":
            if url_abs not in interne:
                interne.append(url_abs)
        else:
            if url_abs not in externe:
                externe.append(url_abs)
    return interne, externe

class CautatorImagini(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lista_imagini = []

    def handle_starttag(self, eticheta, atribute):
        if eticheta.lower() == "img":
            dict_atribute = dict(atribute)
            if "src" in dict_atribute:
                self.lista_imagini.append(dict_atribute["src"])

def genereaza_hash(url):
    r = requests.get(url, timeout=MAX_WAIT)
    return hashlib.sha256(r.content).hexdigest()

def procesare_json_headere(url, nume_fis="headere.json"):
    r = requests.get(url, timeout=MAX_WAIT)
    date_headere = dict(r.headers)

    with open(nume_fis, "w", encoding="utf-8") as f_out:
        json.dump(date_headere, f_out, indent=4)

    with open(nume_fis, "r", encoding="utf-8") as f_in:
        date_citite = json.load(f_in)

    return date_citite

def afla_ip(nume_host):
    try:
        return socket.gethostbyname(nume_host)
    except:
        return "Necunoscut"

def zile_certificat(nume_host):
    setari = ssl.create_default_context()
    try:
        conexiune = socket.create_connection((nume_host, 443), timeout=MAX_WAIT)
        with setari.wrap_socket(conexiune, server_hostname=nume_host) as sock_sigur:
            cert = sock_sigur.getpeercert()
            data_exp = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
            data_exp = data_exp.replace(tzinfo=timezone.utc)
            zile_ramase = (data_exp - datetime.now(timezone.utc)).days
            return zile_ramase
    except:
        return -1

if __name__ == "__main__":
    print("Teste P4...")
    print("URL Descompus:", descompune_link("https://example.com/contact?id=5"))
    print("Relative -> Absolute:", rezolva_relative(DOMENIU, ["/test", "poza.jpg"]))
    
    pagina = requests.get(DOMENIU).text
    toate = gaseste_toate_linkurile(pagina)
    netloc = urllib.parse.urlparse(DOMENIU).netloc
    int, ext = imparte_linkuri(toate, netloc)
    print("Linkuri totale:", len(toate), "Interne:", len(int), "Externe:", len(ext))

    html_test = '<html><img src="img1.png"><IMG SRC="img2.jpg"><a href="/">link</a></html>'
    parser_img = CautatorImagini()
    parser_img.feed(html_test)
    print("Imagini gasite:", parser_img.lista_imagini)

    print("Hash SHA256:", genereaza_hash(DOMENIU))
    
    headere_salvate = procesare_json_headere(DOMENIU)
    print("Tip content din JSON:", headere_salvate.get("Content-Type"))
    
    print("Adresa IP:", afla_ip(netloc))
    print("Zile SSL:", zile_certificat(netloc))