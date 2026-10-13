import requests

SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if path.startswith("/"):
        path = path[1:]
    return "https://" + host + "/" + path


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url)
    print("Status:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type", "unknown"))


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        r = requests.get(url, timeout=5)
        return {
            "status": r.status_code,
            "content_type": r.headers.get("Content-Type", "unknown"),
            "length": len(r.content),
            "server": r.headers.get("Server", "unknown"),
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)[:100]}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    rezultate = []
    for url in SITES:
        rez = check_site(url)
        rez["url"] = url
        rezultate.append(rez)

    reusite = [r for r in rezultate if r.get("status") == 200]
    reusite.sort(key=lambda r: r["length"], reverse=True)

    for r in reusite:
        print(f"{r['url']} -> {r['status']}, {r['length']} octeti")

    total = len(rezultate)
    ok = len(reusite)
    print(f"Reușite: {ok} | Eșuate: {total - ok}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
    except requests.RequestException as e:
        return {"status": None, "error": str(e)[:100]}

    present = []
    missing = []

    for header in SECURITY_HEADERS:
        if header in r.headers:
            present.append(header)
        else:
            missing.append(header)

    score = int(len(present) / len(SECURITY_HEADERS) * 100)

    return {
        "present": present,
        "missing": missing,
        "score": score,
    }


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    ultimul_status = None
    ultima_eroare = None
    incercari_facute = 0

    for i in range(attempts):
        incercari_facute += 1
        try:
            r = requests.get(url, timeout=5)
            ultimul_status = r.status_code
            ultima_eroare = None
            if r.status_code < 500:
                break
        except requests.RequestException as e:
            ultimul_status = None
            ultima_eroare = str(e)[:100]

    rezultat = {
        "status": ultimul_status,
        "attempts": incercari_facute,
    }
    if ultimul_status is None and ultima_eroare is not None:
        rezultat["error"] = ultima_eroare
    return rezultat