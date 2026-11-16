#!/usr/bin/env python3
"""Zgradi podmnožico pisave Noto Color Emoji (COLRv1) z emojiji, ki jih stran uporablja.

Zakaj: Windows nima barvnih zastav (🇬🇧 se pokaže kot »GB«), Segoe UI Emoji pa
riše emojije v drugačnem slogu. Pisavo strežemo sami (brez Google Fonts).

Poženi, ko dodaš nov emoji (v index.html ali v gradivu, npr. emoji= v .url):
    pip3 install --user fonttools brotli
    python3 scripts/emoji_pisava.py

Skripta:
  1. pobere emojije iz index.html in iz gradiva/ (imena datotek in vsebina .url, .md, .txt),
  2. iz Noto-COLRv1.ttf naredi pisave/brihta-emoji.woff2,
  3. v index.html med oznakama emoji-pisava zapiše @font-face z unicode-range.

Izvorna pisava: --vir POT, sicer jo prenese (pripeta različica) v ~/.cache/brihta.
Emoji, ki ga v podmnožici ni, brskalnik nariše s sistemsko pisavo (nič se ne zlomi).
"""
import argparse
import hashlib
import io
import re
import sys
import urllib.request
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
CILJ = KOREN / "pisave" / "brihta-emoji.woff2"
INDEX = KOREN / "index.html"
NOTO_COMMIT = "99701e07d3d1fe1bdbcdb14964547f0fd592966f"
NOTO_URL = f"https://raw.githubusercontent.com/googlefonts/noto-emoji/{NOTO_COMMIT}/2D/fonts/Noto-COLRv1.ttf"
ZAC, KON = "/* emoji-pisava:zacetek */", "/* emoji-pisava:konec */"

# Znaki, ki so v pisavi emojijev, a jih v besedilu NE želimo barvnih
# (števke, #, *, ©, ®, ™, ◀ ▶ ✔ ✖ ⬆ ...). Znak pod U+1F000 vzamemo samo, če je
# privzeto emoji (Emoji_Presentation=Yes) ali če mu v viru sledi U+FE0F (npr. ✏️).
POMOZNI = {0x200D, 0xFE0F, 0x20E3}
_EP = [(0x231A, 0x231B), (0x23E9, 0x23EC), (0x23F0, 0x23F0), (0x23F3, 0x23F3), (0x25FD, 0x25FE),
       (0x2614, 0x2615), (0x2648, 0x2653), (0x267F, 0x267F), (0x2693, 0x2693), (0x26A1, 0x26A1),
       (0x26AA, 0x26AB), (0x26BD, 0x26BE), (0x26C4, 0x26C5), (0x26CE, 0x26CE), (0x26D4, 0x26D4),
       (0x26EA, 0x26EA), (0x26F2, 0x26F3), (0x26F5, 0x26F5), (0x26FA, 0x26FA), (0x26FD, 0x26FD),
       (0x2705, 0x2705), (0x270A, 0x270B), (0x2728, 0x2728), (0x274C, 0x274C), (0x274E, 0x274E),
       (0x2753, 0x2755), (0x2757, 0x2757), (0x2795, 0x2797), (0x27B0, 0x27B0), (0x27BF, 0x27BF),
       (0x2B1B, 0x2B1C), (0x2B50, 0x2B50), (0x2B55, 0x2B55)]


def emoji_v_besedilu(besedilo: str) -> set[int]:
    najdeni: set[int] = set()
    for i, c in enumerate(besedilo):
        cp = ord(c)
        if cp >= 0x1F000 or cp == 0x200D:
            najdeni.add(cp)
        elif 0x2000 <= cp < 0x1F000 and cp not in POMOZNI:
            fe0f = besedilo[i + 1:i + 2] == "\uFE0F"
            if fe0f or any(a <= cp <= b for a, b in _EP):
                najdeni.add(cp)
    return najdeni


def pobrani_znaki() -> set[int]:
    # Samo to, kar izriše index.html. Samostojne HTML strani v gradiva/ ne nalagajo te pisave.
    viri = [INDEX]
    g = KOREN / "gradiva"
    if g.is_dir():
        viri += [p for p in g.rglob("*") if p.is_file()]
    znaki: set[int] = set()
    for p in viri:
        besedilo = p.name
        if p == INDEX or p.suffix.lower() in {".url", ".md", ".txt", ".kviz"}:
            besedilo += "\n" + p.read_text(encoding="utf-8", errors="ignore")
        znaki |= emoji_v_besedilu(besedilo)
    return znaki


def izvorna_pisava(vir: str | None) -> Path:
    if vir:
        return Path(vir)
    pot = Path.home() / ".cache" / "brihta" / f"Noto-COLRv1-{NOTO_COMMIT[:8]}.ttf"
    if not pot.exists():
        pot.parent.mkdir(parents=True, exist_ok=True)
        print(f"Prenašam {NOTO_URL}")
        with urllib.request.urlopen(NOTO_URL) as r:
            pot.write_bytes(r.read())
    return pot


def obsegi(cps: list[int]) -> str:
    deli, i = [], 0
    while i < len(cps):
        j = i
        while j + 1 < len(cps) and cps[j + 1] == cps[j] + 1:
            j += 1
        deli.append(f"U+{cps[i]:X}" if i == j else f"U+{cps[i]:X}-{cps[j]:X}")
        i = j + 1
    return ", ".join(deli)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vir", help="pot do Noto-COLRv1.ttf")
    a = ap.parse_args()
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except ImportError:
        print("Manjka fonttools: pip3 install --user fonttools brotli")
        return 1

    vir = izvorna_pisava(a.vir)
    v_pisavi = set(TTFont(vir, lazy=True)["cmap"].getBestCmap())
    zeleni = pobrani_znaki()
    manjka = sorted(cp for cp in zeleni if cp not in v_pisavi and cp not in POMOZNI)
    znaki = sorted(cp for cp in zeleni if cp in v_pisavi)

    opt = subset.Options()
    opt.flavor = "woff2"
    opt.layout_features = ["*"]
    opt.name_IDs = ["*"]
    opt.notdef_outline = False
    opt.drop_tables += ["vhea", "vmtx"]
    pisava = TTFont(vir)
    s = subset.Subsetter(opt)
    s.populate(unicodes=znaki)
    s.subset(pisava)
    buf = io.BytesIO()
    pisava.save(buf)
    podatki = buf.getvalue()
    CILJ.parent.mkdir(exist_ok=True)
    CILJ.write_bytes(podatki)

    cmap = sorted(pisava["cmap"].getBestCmap())
    razlicica = hashlib.sha1(podatki).hexdigest()[:8]
    blok = (
        f"{ZAC}\n"
        "    /* Barvni emojiji (Noto Color Emoji COLRv1, podmnožica; scripts/emoji_pisava.py).\n"
        "       tech() poskrbi, da jo naložijo samo brskalniki s COLRv1 (Chrome, Edge, Firefox);\n"
        "       Safari na iPadih obdrži svoje emojije. */\n"
        "    @font-face {\n"
        "      font-family: 'Brihta Emoji';\n"
        f"      src: url('pisave/brihta-emoji.woff2?v={razlicica}') format('woff2') tech(color-COLRv1);\n"
        "      font-display: swap;\n"
        f"      unicode-range: {obsegi(cmap)};\n"
        "    }\n"
        f"    {KON}"
    )
    html = INDEX.read_text(encoding="utf-8")
    vzorec = re.compile(re.escape(ZAC) + r".*?" + re.escape(KON), re.S)
    if not vzorec.search(html):
        print(f"V index.html ni oznak {ZAC} ... {KON}")
        return 1
    INDEX.write_text(vzorec.sub(lambda _: blok, html, count=1), encoding="utf-8")

    print(f"Znakov: {len(znaki)}, glif: {len(pisava.getGlyphOrder())}, "
          f"velikost: {len(podatki) / 1024:.1f} KB -> {CILJ.relative_to(KOREN)}")
    if manjka:
        print("Ni v pisavi (ostanejo sistemski):", " ".join(chr(c) for c in manjka))
    return 0


if __name__ == "__main__":
    sys.exit(main())
