# Laborator: functii, metode si importuri pe web
# Student: Malai Carolina

import sys
import time
import requests
import urllib.request

URL_BAZA = "https://example.com"
TIMP_MAXIM = 10 

print("1. Versiune modul requests:", requests.__version__)

raspuns_simplu = requests.get(URL_BAZA, timeout=TIMP_MAXIM)
print("2. Status cu requests.get:", raspuns_simplu.status_code)

from requests import get
raspuns_direct = get(URL_BAZA, timeout=TIMP_MAXIM)
print("2. Status folosind from requests import:", raspuns_direct.status_code)

import requests as req
raspuns_alias = req.get(URL_BAZA, timeout=TIMP_MAXIM)
print("3. Status cu alias req:", raspuns_alias.status_code)

cerere = urllib.request.Request(
    URL_BAZA, 
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)
with urllib.request.urlopen(cerere, timeout=TIMP_MAXIM) as rasp:
    cod_stare = rasp.status
    text_pagina = rasp.read().decode("utf-8")
    print("4. Status cu urllib:", cod_stare)
    print("4. Inceputul paginii:\n", text_pagina[:150])

r_timeout = requests.get(URL_BAZA, timeout=TIMP_MAXIM)
print("6. Cerere cu timeout setat:", r_timeout.status_code)

start = time.perf_counter()
r_timp = requests.get(URL_BAZA, timeout=TIMP_MAXIM)
final = time.perf_counter()

print("7. Timp executie script: {} secunde".format(round(final - start, 3)))
print("7. Timp raspuns server: {} secunde".format(round(r_timp.elapsed.total_seconds(), 3)))

try:
    import bs4
except ImportError:
    print("8. Eroare: modulul bs4 nu este instalat. Folositi pip install beautifulsoup4")