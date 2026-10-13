"""Dovada că fiecare parte funcționează. Rulează: python main.py"""
from checker import (
    build_url, is_https, show_response,
    check_site, scan_sites, check_headers, retry_check,
    SITES,
)

print("=" * 60)
print("PARTEA 1: Funcții ajutătoare")
print("=" * 60)
print(build_url("example.com", "login"))
print(build_url("example.com", "/login"))
print(is_https("https://example.com"))
print(is_https("http://example.com"))

print()
print("=" * 60)
print("PARTEA 2: show_response")
print("=" * 60)
show_response("https://example.com")

print()
print("=" * 60)
print("PARTEA 3: check_site pe fiecare site")
print("=" * 60)
for url in SITES:
    print(url)
    print("  ", check_site(url))

print()
print("=" * 60)
print("PARTEA 4: scan_sites")
print("=" * 60)
scan_sites()

print()
print("=" * 60)
print("PARTEA 5: check_headers")
print("=" * 60)
for url in SITES:
    if "response-headers" in url:
        print(url)
        print("  ", check_headers(url))

print()
print("=" * 60)
print("PARTEA 6: retry_check")
print("=" * 60)
print(retry_check("https://httpbin.org/status/200"))
print(retry_check("https://httpbin.org/status/404"))
print(retry_check("https://httpbin.org/status/500"))
print(retry_check("https://httpbin.org/status/500", attempts=2))
print(retry_check("http://this-site-does-not-exist.invalid"))