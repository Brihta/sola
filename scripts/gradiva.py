#!/usr/bin/env python3
"""Zgradi gradiva.json iz map v gradiva/<predmet>/.

Vsaka datoteka v mapi predmeta postane eno gradivo. Ime gradiva je ime
datoteke brez končnice (podčrtaji postanejo presledki). Če se ime začne z
datumom (2026-10-15 ...), se ta datum uporabi; sicer datum zadnjega commita
datoteke, za še neshranjene datoteke pa čas spremembe.

Posebni primeri:
  *.url / *.link  vsebina je spletni naslov -> gradivo je povezava
  mapa/index.html cela mapa je eno HTML gradivo (z vsemi slikami ipd.)
  .ime, _ime      skrito (ni objavljeno)
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRADIVA = os.path.join(KOREN, "gradiva")
IZHOD = os.path.join(KOREN, "gradiva.json")

VRSTE = {
    "pdf": "pdf",
    "png": "slika", "jpg": "slika", "jpeg": "slika", "gif": "slika", "webp": "slika", "svg": "slika",
    "doc": "word", "docx": "word", "odt": "word", "rtf": "word",
    "ppt": "powerpoint", "pptx": "powerpoint", "pps": "powerpoint", "ppsx": "powerpoint", "odp": "powerpoint",
    "xls": "excel", "xlsx": "excel", "ods": "excel",
    "html": "html", "htm": "html",
    "mp4": "video", "webm": "video", "mov": "video",
    "mp3": "zvok", "m4a": "zvok", "wav": "zvok",
    "txt": "besedilo", "md": "besedilo",
    "url": "povezava", "link": "povezava",
}
DATUM_V_IMENU = re.compile(r"^(\d{4}-\d{2}-\d{2})[ _-]*")


def git_datum(pot):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", pot],
            cwd=KOREN, capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out or None
    except (OSError, subprocess.CalledProcessError):
        return None


def datum_mape(pot):
    """Najnovejši commit kjerkoli v mapi (za HTML mape)."""
    return git_datum(pot)


def mtime(pot):
    return dt.datetime.fromtimestamp(os.path.getmtime(pot)).astimezone().isoformat(timespec="seconds")


def preberi_url(pot):
    with open(pot, encoding="utf-8", errors="replace") as f:
        besedilo = f.read()
    m = re.search(r"^URL=(\S+)", besedilo, re.M)  # Windows .url bližnjica
    if m:
        return m.group(1)
    m = re.search(r"https?://\S+", besedilo)
    return m.group(0) if m else None


def lepo_ime(osnova):
    ime = DATUM_V_IMENU.sub("", osnova)
    ime = ime.replace("_", " ").strip()
    return ime or osnova


def gradivo(predmet, vnos):
    pot = os.path.join(GRADIVA, predmet, vnos)
    rel = f"gradiva/{predmet}/{vnos}"
    if os.path.isdir(pot):
        if not os.path.isfile(os.path.join(pot, "index.html")):
            return None
        osnova, vrsta, velikost = vnos, "html", None
        rel_odpri = rel + "/index.html"
        datum = datum_mape(rel)
    else:
        osnova, konc = os.path.splitext(vnos)
        vrsta = VRSTE.get(konc.lower().lstrip("."), "datoteka")
        velikost = os.path.getsize(pot)
        rel_odpri = rel
        datum = git_datum(rel)
    if not datum:
        datum = mtime(pot)
    m = DATUM_V_IMENU.match(osnova)
    if m:
        datum = m.group(1) + "T08:00:00+02:00"

    zapis = {"ime": lepo_ime(osnova), "vrsta": vrsta, "datum": datum}
    if vrsta == "povezava":
        url = preberi_url(pot)
        if not url:
            return None
        zapis["url"] = url
    else:
        zapis["pot"] = rel_odpri
        if velikost is not None:
            zapis["velikost"] = velikost
    return zapis


def main():
    predmeti = {}
    for predmet in sorted(os.listdir(GRADIVA)):
        mapa = os.path.join(GRADIVA, predmet)
        if not os.path.isdir(mapa) or predmet.startswith((".", "_")):
            continue
        seznam = []
        for vnos in sorted(os.listdir(mapa)):
            if vnos.startswith((".", "_")):
                continue
            z = gradivo(predmet, vnos)
            if z:
                seznam.append(z)
        seznam.sort(key=lambda z: z["datum"], reverse=True)
        predmeti[predmet] = seznam

    novo = {"predmeti": predmeti}
    try:
        with open(IZHOD, encoding="utf-8") as f:
            staro = json.load(f)
        if staro.get("predmeti") == predmeti:
            print("gradiva.json je že posodobljen.")
            return
    except (OSError, ValueError):
        pass
    novo["posodobljeno"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    with open(IZHOD, "w", encoding="utf-8") as f:
        json.dump(novo, f, ensure_ascii=False, indent=1)
        f.write("\n")
    skupaj = sum(len(s) for s in predmeti.values())
    print(f"gradiva.json: {skupaj} gradiv v {len(predmeti)} predmetih.")


if __name__ == "__main__":
    sys.exit(main())
