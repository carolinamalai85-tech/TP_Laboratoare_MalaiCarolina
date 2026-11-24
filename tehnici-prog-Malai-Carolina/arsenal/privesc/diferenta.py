import os
from arsenal.privesc.colectii_enum import GTFO, citeste_linii, nume


def cai(fisier):
    return set(citeste_linii(fisier))


def main():
    baza_dir = os.path.dirname(__file__)
    baza = cai(os.path.join(baza_dir, "start", "baza_suid.txt"))
    acum = cai(os.path.join(baza_dir, "start", "suid.txt"))
    print("baza:", len(baza), " acum:", len(acum))

    noi = acum - baza
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)

    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()