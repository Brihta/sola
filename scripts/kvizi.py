#!/usr/bin/env python3
"""Objavi kvize iz kvizi/<predmet>/*.txt v Supabase.

Mapa kvizi/ NI na GitHubu (.gitignore), ker so v datotekah pravilni odgovori.

    python3 scripts/kvizi.py            preveri in objavi vse kvize
    python3 scripts/kvizi.py --preveri  samo preveri, nič ne pošlje

Oblika datoteke (podrobneje v README.md):

    Naslov: Scratch – ponovitev
    Opis: Reši sam. Imaš en poskus.

    ? Koliko je 2 + 3?
    - 4
    + 5

    ? Kateri so sesalci?
    + pes
    + mačka
    - vrabec

    ? Glavno mesto Slovenije je …
    = Ljubljana

    ? Poveži državo in glavno mesto.
    Francija = Pariz
    Italija = Rim

    ? Razvrsti od najmanjšega do največjega.
    1. miška
    2. mačka
    3. slon
"""
import json
import os
import random
import re
import secrets
import sys
import unicodedata
import urllib.error
import urllib.request

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KVIZI = os.path.join(KOREN, "kvizi")
GRADIVA = os.path.join(KOREN, "gradiva")
SKRIVNOST = os.path.join(KOREN, ".kviz-skrivnost")
NASTAVI_SQL = os.path.join(KVIZI, "NASTAVI_SKRIVNOST.sql")

SUPABASE_URL = "https://ldczgbajbarlgwqzcggh.supabase.co"
SUPABASE_KEY = "sb_publishable_888IYcEb-nSmGO0d67hEwA_rBFuXnv8"

R_ODG = re.compile(r"^([+\-=])\s*(.+)$")
R_VRSTNI = re.compile(r"^(\d+)[.)]\s*(.+)$")
R_POVEZI = re.compile(r"^(.+?)\s+=\s+(.+)$")


class Napaka(Exception):
    pass


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") or "kviz"


def preberi(pot):
    """Vrne (naslov, opis, vprasanja[]); vprasanje = dict(besedilo, vrstice[(st, vrsta, ...)])."""
    with open(pot, encoding="utf-8-sig") as f:
        vrstice = f.read().splitlines()
    naslov = opis = None
    vprasanja = []
    trenutno = None
    for st, surovo in enumerate(vrstice, 1):
        v = surovo.strip()
        if not v or v.startswith("#"):
            continue
        if trenutno is None and not vprasanja:
            m = re.match(r"^(naslov|opis)\s*:\s*(.*)$", v, re.I)
            if m:
                if m.group(1).lower() == "naslov":
                    naslov = m.group(2).strip()
                else:
                    opis = m.group(2).strip()
                continue
        if v.startswith("?"):
            trenutno = {"st": st, "besedilo": v[1:].strip(), "odg": []}
            vprasanja.append(trenutno)
            continue
        if trenutno is None:
            raise Napaka(f"vrstica {st}: pred prvim vprašanjem (vprašanje se začne z »?«)")
        m = R_ODG.match(v)
        if m:
            trenutno["odg"].append((st, m.group(1), m.group(2).strip()))
            continue
        m = R_VRSTNI.match(v)
        if m:
            trenutno["odg"].append((st, "#", int(m.group(1)), m.group(2).strip()))
            continue
        m = R_POVEZI.match(v)
        if m:
            trenutno["odg"].append((st, "<>", m.group(1).strip(), m.group(2).strip()))
            continue
        if trenutno["odg"]:
            raise Napaka(f"vrstica {st}: ne razumem »{v}« (odgovor se začne z +, -, =, številko ali ima »levo = desno«)")
        trenutno["besedilo"] += "\n" + v  # vprašanje v več vrsticah
    return naslov, opis, vprasanja


def zgradi(id_kviza, vprasanja):
    """Vrne (javna vprašanja, ključ)."""
    rnd = random.Random(id_kviza)  # vedno enako premešano za isti kviz
    javno, kljuc = [], []
    for q in vprasanja:
        st, besedilo, odg = q["st"], q["besedilo"], q["odg"]
        if not besedilo:
            raise Napaka(f"vrstica {st}: vprašanje brez besedila")
        vrste = {o[1] for o in odg}
        if not odg:
            raise Napaka(f"vrstica {st}: vprašanje nima odgovorov")
        if vrste <= {"+", "-"}:
            pravilni = [o[2] for o in odg if o[1] == "+"]
            vsi = [o[2] for o in odg]
            if not pravilni:
                raise Napaka(f"vrstica {st}: ni pravilnega odgovora (označi ga s +)")
            if len(vsi) < 2:
                raise Napaka(f"vrstica {st}: izbira potrebuje vsaj dva odgovora")
            if len(set(vsi)) != len(vsi):
                raise Napaka(f"vrstica {st}: dva enaka odgovora")
            moznosti = vsi[:]
            rnd.shuffle(moznosti)
            t = "izbira" if len(pravilni) == 1 else "vec"
            javno.append({"t": t, "b": besedilo, "m": moznosti})
            kljuc.append({"t": t, "p": pravilni})
        elif vrste == {"="}:
            javno.append({"t": "kratek", "b": besedilo})
            kljuc.append({"t": "kratek", "p": [o[2] for o in odg]})
        elif vrste == {"<>"}:
            pari = [[o[2], o[3]] for o in odg]
            levo = [p[0] for p in pari]
            desno = [p[1] for p in pari]
            if len(pari) < 2:
                raise Napaka(f"vrstica {st}: povezovanje potrebuje vsaj dva para")
            if len(set(levo)) != len(levo):
                raise Napaka(f"vrstica {st}: leva stran se ponovi")
            desno_m = sorted(set(desno))
            rnd.shuffle(desno_m)
            javno.append({"t": "povezi", "b": besedilo, "l": levo, "d": desno_m})
            kljuc.append({"t": "povezi", "p": pari})
        elif vrste == {"#"}:
            urejeno = [o[3] for o in sorted(odg, key=lambda o: o[2])]
            if len(urejeno) < 2:
                raise Napaka(f"vrstica {st}: razvrščanje potrebuje vsaj dva elementa")
            if len(set(urejeno)) != len(urejeno):
                raise Napaka(f"vrstica {st}: dva enaka elementa")
            premesano = urejeno[:]
            for _ in range(10):
                rnd.shuffle(premesano)
                if premesano != urejeno:
                    break
            javno.append({"t": "vrstni", "b": besedilo, "m": premesano})
            kljuc.append({"t": "vrstni", "p": urejeno})
        else:
            raise Napaka(f"vrstica {st}: pri enem vprašanju so pomešane različne vrste odgovorov")
    return javno, kljuc


def predmeti():
    return {d for d in os.listdir(GRADIVA) if os.path.isdir(os.path.join(GRADIVA, d)) and not d.startswith((".", "_"))}


def nalozi_vse():
    kvizi, napake = [], []
    if not os.path.isdir(KVIZI):
        return kvizi, napake
    znani = predmeti()
    for predmet in sorted(os.listdir(KVIZI)):
        mapa = os.path.join(KVIZI, predmet)
        if not os.path.isdir(mapa) or predmet.startswith((".", "_")):
            continue
        if predmet not in znani:
            napake.append(f"kvizi/{predmet}: ni tak predmet (možni: {', '.join(sorted(znani))})")
            continue
        for ime in sorted(os.listdir(mapa)):
            if not ime.lower().endswith(".txt") or ime.startswith((".", "_")):
                continue
            pot = os.path.join(mapa, ime)
            osnova = os.path.splitext(ime)[0]
            id_kviza = f"{predmet}/{slug(osnova)}"
            try:
                naslov, opis, vpr = preberi(pot)
                if not vpr:
                    raise Napaka("ni nobenega vprašanja (vprašanje se začne z »?«)")
                javno, kljuc = zgradi(id_kviza, vpr)
            except Napaka as e:
                napake.append(f"kvizi/{predmet}/{ime}: {e}")
                continue
            kvizi.append({
                "id": id_kviza, "predmet": predmet,
                "naslov": naslov or osnova.replace("_", " "), "opis": opis or "",
                "vprasanja": javno, "kljuc": kljuc,
            })
    ids = [k["id"] for k in kvizi]
    for d in {i for i in ids if ids.count(i) > 1}:
        napake.append(f"{d}: dva kviza z enakim imenom")
    return kvizi, napake


def skrivnost():
    s = os.environ.get("KVIZ_SKRIVNOST")
    if s:
        return s.strip()
    if os.path.isfile(SKRIVNOST):
        with open(SKRIVNOST) as f:
            return f.read().strip()
    s = secrets.token_urlsafe(32)
    with open(SKRIVNOST, "w") as f:
        f.write(s + "\n")
    os.makedirs(KVIZI, exist_ok=True)
    with open(NASTAVI_SQL, "w", encoding="utf-8") as f:
        f.write("-- Zaženi enkrat v Supabase → SQL Editor (po supabase_kvizi.sql).\n"
                "-- Ta datoteka NI na GitHubu. Ne pošiljaj je nikomur.\n"
                "insert into app_config (key, value) values ('sola_kviz_skrivnost', '"
                + s + "')\n  on conflict (key) do update set value = excluded.value;\n")
    print("Ustvaril sem novo skrivnost. Zaženi kvizi/NASTAVI_SKRIVNOST.sql v Supabase → SQL Editor.")
    return s


def objavi(kvizi):
    telo = json.dumps({"p_skrivnost": skrivnost(), "p_kvizi": kvizi}).encode()
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/rpc/sola_kviz_objavi", data=telo, method="POST",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read() or "0")
    except urllib.error.HTTPError as e:
        besedilo = e.read().decode(errors="replace")
        if "NAPACNA_SKRIVNOST" in besedilo:
            raise SystemExit("Supabase ne pozna te skrivnosti. Zaženi kvizi/NASTAVI_SKRIVNOST.sql v SQL Editorju.")
        if "sola_kviz_objavi" in besedilo and e.code == 404:
            raise SystemExit("V Supabase še ni kvizov. Najprej zaženi supabase_kvizi.sql v SQL Editorju.")
        raise SystemExit(f"Napaka Supabase ({e.code}): {besedilo}")


def main():
    kvizi, napake = nalozi_vse()
    for k in kvizi:
        vrste = {}
        for q in k["vprasanja"]:
            vrste[q["t"]] = vrste.get(q["t"], 0) + 1
        opis = ", ".join(f"{n}× {t}" for t, n in vrste.items())
        print(f"  ✓ {k['id']}  »{k['naslov']}«  ({len(k['vprasanja'])} vprašanj: {opis})")
    for n in napake:
        print(f"  ✗ {n}")
    if napake:
        raise SystemExit("\nPopravi napake, nato poženi znova. Nič ni bilo objavljeno.")
    if "--preveri" in sys.argv:
        print(f"\n{len(kvizi)} kvizov je v redu (nič ni bilo poslano).")
        return
    n = objavi(kvizi)
    print(f"\nObjavljeno: {n} kvizov. Na strani so takoj.")


if __name__ == "__main__":
    main()
