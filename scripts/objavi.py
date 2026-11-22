#!/usr/bin/env python3
"""Objavi ali skrij gradivo iz gradiva.json brez prijave na strani.

Uporablja isto skrivnost kot kvizi.py (~/.config/brihta-sola/kviz-skrivnost),
zato deluje samo na Ninovem Macu. V Supabase mora biti zagnan
supabase_gradiva_skrivnost.sql.

    python3 scripts/objavi.py fleksi-spelling "Week 2 soft g"     objavi
    python3 scripts/objavi.py fleksi-spelling "Week 2" --skrij    skrij (vse, kar se ujema)
    python3 scripts/objavi.py fleksi-reading                      izpiše gradiva predmeta
    python3 scripts/objavi.py fleksi-spelling "Week 2" --vse      objavi vse zadetke

Ime se išče brez razlike med velikimi in malimi črkami, kot del naslova.
Če se ujema več gradiv, skripta brez --vse ne naredi nič in jih izpiše.
"""
import json
import os
import sys
import urllib.error
import urllib.request

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kvizi import SUPABASE_URL, SUPABASE_KEY, SKRIVNOST  # noqa: E402


def preberi_skrivnost():
    s = os.environ.get("KVIZ_SKRIVNOST")
    if s:
        return s.strip()
    if not os.path.isfile(SKRIVNOST):
        raise SystemExit(f"Ni skrivnosti v {SKRIVNOST}. Ta skripta deluje samo na Ninovem Macu.")
    with open(SKRIVNOST) as f:
        return f.read().strip()


def rpc(kljuc, objavljeno):
    telo = json.dumps({"p_skrivnost": preberi_skrivnost(), "p_kljuc": kljuc,
                       "p_objavljeno": objavljeno}).encode()
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/rpc/sola_gradivo_objavi_skrivnost", data=telo, method="POST",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read() or "false")
    except urllib.error.HTTPError as e:
        b = e.read().decode(errors="replace")
        if "NAPACNA_SKRIVNOST" in b:
            raise SystemExit("Supabase ne pozna te skrivnosti.")
        if e.code == 404:
            raise SystemExit("V Supabase še ni funkcije. Zaženi supabase_gradiva_skrivnost.sql.")
        raise SystemExit(f"Napaka Supabase ({e.code}): {b}")


def main():
    arg = [a for a in sys.argv[1:] if not a.startswith("--")]
    zastavice = {a for a in sys.argv[1:] if a.startswith("--")}
    with open(os.path.join(KOREN, "gradiva.json"), encoding="utf-8") as f:
        predmeti = json.load(f)["predmeti"]
    if not arg or arg[0] not in predmeti:
        raise SystemExit("Predmet mora biti eden od: " + ", ".join(predmeti))
    gradiva = [g for g in predmeti[arg[0]] if g.get("pot") or g.get("url")]
    if len(arg) < 2:
        for g in gradiva:
            print(f"  {g['datum'][:10]}  {g['ime']}{'  (naloženo vnaprej)' if g.get('vnaprej') else ''}")
        return
    iskano = arg[1].lower()
    zadetki = [g for g in gradiva if iskano in g["ime"].lower()]
    if not zadetki:
        raise SystemExit(f"Ni gradiva »{arg[1]}« v {arg[0]}.")
    if len(zadetki) > 1 and "--vse" not in zastavice and "--skrij" not in zastavice:
        print("Ujema se več gradiv (dodaj --vse ali natančnejše ime):")
        for g in zadetki:
            print(f"  {g['ime']}")
        raise SystemExit(1)
    objavljeno = "--skrij" not in zastavice
    for g in zadetki:
        ok = rpc(g.get("pot") or g.get("url"), objavljeno)
        print(f"  {'✓' if ok else '✗'} {g['ime']}: {'objavljeno' if objavljeno else 'skrito'}" + ("" if ok else " (ni uspelo)"))


if __name__ == "__main__":
    main()
