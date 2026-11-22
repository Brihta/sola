#!/usr/bin/env python3
"""Doda zahtevo za objavo ali skrivanje v objave/zahteve.jsonl (nato commit in push na main).
    python3 scripts/zahteva.py fleksi-spelling "Week 2"            objavi (vse, kar se ujema)
    python3 scripts/zahteva.py fleksi-spelling "Week 2" --skrij    skrij
Ime preveri v gradiva.json, da Mac ne dobi zahteve, ki se ne ujema z ničemer."""
import json, os, sys, time, secrets
KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
arg = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(arg) != 2: raise SystemExit(__doc__)
predmet, ime = arg
gr = json.load(open(os.path.join(KOREN, "gradiva.json"), encoding="utf-8"))["predmeti"]
if predmet not in gr: raise SystemExit("Predmet mora biti eden od: " + ", ".join(gr))
zad = [g["ime"] for g in gr[predmet] if (g.get("pot") or g.get("url")) and ime.lower() in g["ime"].lower()]
if not zad: raise SystemExit(f"Ni gradiva »{ime}« v {predmet}.")
z = {"id": time.strftime("%Y%m%d-%H%M%S-") + secrets.token_hex(3), "predmet": predmet, "ime": ime,
     "objavi": "--skrij" not in sys.argv, "vse": True}
with open(os.path.join(KOREN, "objave", "zahteve.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(z, ensure_ascii=False) + "\n")
print(("Objavi" if z["objavi"] else "Skrij") + ": " + ", ".join(zad))
