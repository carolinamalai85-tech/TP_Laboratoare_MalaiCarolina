# Laborator: functii, metode si importuri pe web - Modul unelte_web
# Student: Malai Carolina

import time
import ssl
import json
import socket
import urllib.parse
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

HEADER_STUDENT = {"User-Agent": "Bot-Malai-Carolina"}

def ia_continut(url):
    return requests.get(url, headers=HEADER_STUDENT, timeout=10)

def afla_status(url):
    try:
        return ia_continut(url).status_code
    except:
        return 0

def extrage_titlu(html):
    bs = BeautifulSoup(html, "html.parser")
    if bs.title and bs.title.string:
        return bs.title.string.strip()
    return "Fara Titlu"

def analizor_linkuri(html, domeniu):
    bs = BeautifulSoup(html, "html.parser")
    interne, externe = [], []
    for tag in bs.find_all("a", href=True):
        link_abs = urllib.parse.urljoin("https://" + domeniu, tag["href"])
        host = urllib.parse.urlparse(link_abs).netloc
        if host == domeniu or host == "":
            if link_abs not in interne: interne.append(link_abs)
        else:
            if link_abs not in externe: externe.append(link_abs)
    return interne, externe

def genereaza_raport_site(url):
    r = ia_continut(url)
    host = urllib.parse.urlparse(r.url).netloc
    
    ip = "Necunoscut"
    try:
        ip = socket.gethostbyname(host)
    except:
        pass
        
    int, ext = analizor_linkuri(r.text, host)
    
    date_raport = {
        "adresa_cautata": url,
        "status": r.status_code,
        "titlu_gasit": extrage_titlu(r.text),
        "ip_server": ip,
        "nr_link_interne": len(int),
        "nr_link_externe": len(ext)
    }
    
    print("\n=== Raport Generat pentru", url, "===")
    print("Status HTTP:", date_raport["status"])
    print("Titlu:", date_raport["titlu_gasit"])
    print("IP:", date_raport["ip_server"])
    print("Linkuri:", date_raport["nr_link_interne"], "interne si", date_raport["nr_link_externe"], "externe.")
    
    with open("raport.json", "w", encoding="utf-8") as fis:
        json.dump(date_raport, fis, indent=4)
    print("Raportul a fost salvat in raport.json")
    
    return date_raport