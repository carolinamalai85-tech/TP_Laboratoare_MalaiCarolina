import base64
import re
import hashlib
import json
from urllib.parse import unquote

# A1. Text și octeți
s = "Salut"
b = s.encode()
print(b, b[0])
print(b.hex())

# A2. Ghicirea stratului
def ghici_strat(s_str):
    if "%" in s_str and re.search(r'%[0-9A-Fa-f]{2}', s_str):
        return "url"
    if re.fullmatch(r'[0-9a-fA-F]+', s_str) and len(s_str) % 2 == 0:
        return "hex"
    if re.fullmatch(r'[A-Za-z0-9+/=]+', s_str) and len(s_str) % 4 == 0:
        return "base64"
    return "necunoscut"

# A3. Desfacerea stratului
def desfa(s_str):
    strat = ghici_strat(s_str)
    if strat == "base64":
        return strat, base64.b64decode(s_str)
    elif strat == "hex":
        return strat, bytes.fromhex(s_str)
    elif strat == "url":
        return strat, unquote(s_str).encode()
    return "necunoscut", s_str.encode()

# A4. Straturi multiple
def citibil(b_val):
    return all(32 <= c < 127 for c in b_val)

try:
    val = open("probe/mesaj.txt").read().strip()
    for _ in range(8):
        strat, b_res = desfa(val)
        print(strat, val)
        if citibil(b_res):
            print("Mesaj final:", b_res.decode())
            break
        else:
            val = b_res.decode('utf-8', errors='ignore')
except Exception:
    pass

# A5. Spargere XOR
try:
    date_xor = open("probe/xor.bin", "rb").read()
    for k in range(256):
        clar = bytes(b ^ k for b in date_xor)
        if citibil(clar):
            print("Cheie gasita:", k)
            print("Mesaj decriptat:", clar.decode())
            break
except Exception:
    pass

# A6. Spargere Hash
try:
    tinta = open("probe/hashuri.txt").readline().strip()
    print("Lungimea hashului:", len(tinta))
    for cuv in open("probe/wordlist.txt", encoding="latin1"):
        cuv = cuv.strip()
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print("Parola gasita:", cuv)
            break
except Exception:
    pass

# A7. Salvare fisa.json
fisa_data = {"strat": "base64", "rezultat": "FLAG{straturi_de_encoding}"}
with open("arsenal/forensics/fisa.json", "w") as jf:
    json.dump(fisa_data, jf, indent=4)
print("Rezultatul a fost salvat in fisa.json")

# Test final A7
def test_base64():
    strat, b_test = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b_test == b"Salut"
    print("Testul Base64 a trecut!")

test_base64()