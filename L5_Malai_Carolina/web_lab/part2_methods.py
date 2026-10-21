# Laborator: functii, metode si importuri pe web
# Student: Malai Carolina

import time
import requests

ADRESA = "https://example.com"
ADRESA_TEST = "https://postman-echo.com"
ASTEPTARE = 10

raspuns = requests.get(ADRESA, timeout=ASTEPTARE)

print("9. Atribut status_code:", raspuns.status_code)
print("9. Atribut ok:", raspuns.ok)
print("9. Atribut url:", raspuns.url)

raspuns.raise_for_status()

try:
    r_eroare = requests.get(ADRESA + "/pagina-inexistenta-123", timeout=ASTEPTARE)
    r_eroare.raise_for_status()
except requests.HTTPError as eroare:
    print("10. Am prins o eroare HTTP:", eroare)

time.sleep(1)

print("\n--- 11. Lista de headere ---")
for cheie, valoare in raspuns.headers.items():
    print(cheie, "->", valoare)

header_server = raspuns.headers.get("Server", "Nu a fost gasit")
print("\n12. Tip server:", header_server)
print("12. Testare case-insensitive:", raspuns.headers.get("CONTENT-TYPE", "lipsa"))

nr_aparitii = raspuns.text.lower().count("domain")
print("\n13. Cuvantul 'domain' apare de:", nr_aparitii, "ori")

text_html = raspuns.text
idx_start = text_html.find("<title>")
idx_stop = text_html.find("</title>")
if idx_start > 0 and idx_stop > 0:
    titlu_pagina = text_html[idx_start + 7 : idx_stop].strip()
else:
    titlu_pagina = "Titlu negasit"
print("14. Titlul este:", titlu_pagina)

randuri = text_html.split("\n")
print("15. Pagina are", len(randuri), "randuri in total.")

if raspuns.url.startswith("https"):
    print("16. Site-ul foloseste conexiune sigura HTTPS.")

test_http = requests.get("http://example.com", timeout=ASTEPTARE)
print("\n17. Redirectionari:")
for pas in test_http.history:
    print("Status:", pas.status_code, "la", pas.url)
print("Adresa finala:", test_http.url)

time.sleep(1)

r_head = requests.head(ADRESA, timeout=ASTEPTARE)
r_get = requests.get(ADRESA, timeout=ASTEPTARE)
print("\n18. Marime HEAD:", len(r_head.content), "vs Marime GET:", len(r_get.content))

if len(raspuns.cookies) > 0:
    for c in raspuns.cookies:
        print("19. Cookie gasit:", c.name)
else:
    print("\n19. Nu exista cookie-uri returnate.")

sesiune = requests.Session()
sesiune.headers.update({"User-Agent": "Student-MalaiCarolina"})
r_sesiune = sesiune.get(ADRESA_TEST + "/headers", timeout=ASTEPTARE)
print("\n20. Headere trimise cu Session:")
print(r_sesiune.json())