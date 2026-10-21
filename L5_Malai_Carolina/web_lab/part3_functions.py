# Laborator: functii, metode si importuri pe web
# Student: Malai Carolina

import time
import requests

URL_TEST = "https://example.com"
ASTEPTARE_MAX = 8

def preia_pagina(url, timp=ASTEPTARE_MAX):
    return requests.get(url, timeout=timp)

def status_cod(url):
    r = preia_pagina(url)
    return r.status_code

def extrage_titlul_html(cod_html):
    i_start = cod_html.find("<title>")
    i_end = cod_html.find("</title>")
    if i_start != -1 and i_end != -1:
        return cod_html[i_start + 7 : i_end].strip()
    return "Fara titlu"

def verifica_pagina_activa(url):
    try:
        r = preia_pagina(url)
        if r.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False

def analizeaza_rute(domeniu, lista_rute):
    rezultate = {}
    for ruta in lista_rute:
        link = domeniu.rstrip("/") + "/" + ruta.lstrip("/")
        try:
            r = preia_pagina(link)
            rezultate[ruta] = r.status_code
        except Exception:
            rezultate[ruta] = 0
        time.sleep(1)
    return rezultate

def gaseste_header(url, nume_header, valoare_standard="lipsa"):
    try:
        r = preia_pagina(url)
        if nume_header in r.headers:
            return r.headers[nume_header]
        else:
            return valoare_standard
    except:
        return valoare_standard

def protectie_headere(url):
    lista = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security"]
    try:
        r = preia_pagina(url)
        dict_protectie = {}
        for h in lista:
            dict_protectie[h] = h in r.headers
        return dict_protectie
    except:
        return {}

def calculeaza_nota(dict_rezultate):
    ok = 0
    for val in dict_rezultate.values():
        if val == True:
            ok += 1
    return str(ok) + " din " + str(len(dict_rezultate))

def obtine_robots(domeniu):
    adresa = domeniu.rstrip("/") + "/robots.txt"
    try:
        r = preia_pagina(adresa)
        if r.status_code == 200:
            return r.text
    except:
        pass
    return None

def rute_blocate(text_robots):
    if text_robots is None:
        return []
    rute = []
    linii = text_robots.split("\n")
    for linie in linii:
        linie = linie.strip()
        if linie.lower().startswith("disallow:"):
            segmente = linie.split(":")
            if len(segmente) >= 2 and segmente[1].strip() != "":
                rute.append(segmente[1].strip())
    return rute

def timp_raspuns_multiplu(*adrese):
    dict_timp = {}
    for a in adrese:
        t1 = time.perf_counter()
        try:
            preia_pagina(a)
            t2 = time.perf_counter()
            dict_timp[a] = round(t2 - t1, 3)
        except:
            dict_timp[a] = -1
        time.sleep(1)
    return dict_timp

def inregistrare_log(mesaj, **alte_date):
    info_extra = []
    for c, v in alte_date.items():
        info_extra.append(str(c) + "=" + str(v))
    detalii = " | ".join(info_extra)
    print("LOG:", mesaj, "-", detalii)

if __name__ == "__main__":
    print("Testari P3...")
    print("Status:", status_cod(URL_TEST))
    
    pg = preia_pagina(URL_TEST)
    print("Titlu:", extrage_titlul_html(pg.text))
    
    print("Exista site fals?", verifica_pagina_activa("https://domeniu-fals-12345.com"))
    
    dictionar_rute = analizeaza_rute(URL_TEST, ["/", "/login", "/admin"])
    print("Rute verificate:", dictionar_rute)
    
    h_server = gaseste_header(URL_TEST, "Server")
    print("Server folosit:", h_server)
    
    securitate = protectie_headere(URL_TEST)
    print("Scor securitate:", calculeaza_nota(securitate))
    
    txt_rob = obtine_robots(URL_TEST)
    print("Interzis din robots:", rute_blocate(txt_rob))
    
    timpi = timp_raspuns_multiplu(URL_TEST, "https://postman-echo.com")
    print("Timpi executie:", timpi)
    
    inregistrare_log("Test finalizat", stare="OK", erori=0)