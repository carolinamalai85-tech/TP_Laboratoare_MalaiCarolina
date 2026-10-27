import re
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS

def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"\x89PNG"): return "png"
    elif cap.startswith(b"\xff\xd8"): return "jpeg"
    elif cap.startswith(b"PK\x03\x04"): return "zip/docx"
    return cap.hex()

print("Tip real foto.jpg:", tip_real("probe/foto.jpg"))

date_bin = open("probe/ascuns.png", "rb").read()
print("\n--- Strings găsite în ascuns.png ---")
for m in re.findall(rb"[ -~]{4,}", date_bin):
    print(m.decode(errors='ignore'))

print("\n--- Metadate EXIF foto.jpg ---")
exif = Image.open("probe/foto.jpg").getexif() or {}
for tag_id, val in exif.items():
    print(f"{TAGS.get(tag_id, tag_id)} = {val}")

i = date_bin.find(b"PK\x03\x04")
if i != -1:
    open("gasit.zip", "wb").write(date_bin[i:])
    print("\n[+] Arhivă ZIP extrasă cu succes!")

def ascunde_lsb(cale_sursa, mesaj, cale_dest):
    img = Image.open(cale_sursa).convert("RGB")
    px = list(img.getdata())
    biti = "".join(f"{x:08b}" for x in (mesaj + b'\x00'))
    
    px_nou = []
    bit_idx = 0
    for pixel in px:
        r, g, b = pixel
        canal_nou = []
        for c in (r, g, b):
            if bit_idx < len(biti):
                c = (c & ~1) | int(biti[bit_idx])
                bit_idx += 1
            canal_nou.append(c)
        px_nou.append(tuple(canal_nou))
        
    img_noua = Image.new(img.mode, img.size)
    img_noua.putdata(px_nou)
    img_noua.save(cale_dest, "PNG")
    print(f"\n[+] Mesaj ascuns prin LSB în {cale_dest}")

ascunde_lsb("probe/foto.jpg", b"FLAG{ascuns_in_pixeli}", "stego.png")