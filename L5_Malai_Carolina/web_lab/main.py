# Laborator: functii, metode si importuri pe web
# Student: Malai Carolina

import argparse
import csv
from datetime import datetime
import unelte_web

def main():
    parser = argparse.ArgumentParser(description="Generator de raport web.")
    parser.add_argument("url", nargs="?", default="https://example.com", help="Adresa de analizat")
    argumente = parser.parse_args()
    adresa = argumente.url

    # Ex 49: Salvare CSV
    cai_verificare = ["/", "/robots.txt", "/sitemap.xml"]
    with open("raport.csv", "w", newline="", encoding="utf-8") as fisier:
        scriitor = csv.writer(fisier)
        scriitor.writerow(["cale", "stare_http", "data_verificarii"])
        
        for cale in cai_verificare:
            url_complet = adresa.rstrip("/") + "/" + cale.lstrip("/")
            stare = unelte_web.afla_status(url_complet)
            data_curenta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            scriitor.writerow([cale, stare, data_curenta])

    # Ex 50: Raport final
    unelte_web.genereaza_raport_site(adresa)

if __name__ == "__main__":
    main()