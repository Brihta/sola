# Brihta — Šola

Spletna stran za učence: https://brihta.github.io/sola/

Učenec izbere predmet (pri Računalništvu še skupino) in na vrhu vidi zadnje
objavljeno gradivo, ki ga odpre z enim klikom. Starejša gradiva so spodaj,
razvrščena po tednih.

## Kako objavim gradivo

Vsak predmet ima svojo mapo v `gradiva/`:

| Mapa | Predmet |
|---|---|
| `gradiva/racunalnistvo-4` | Računalništvo 4 |
| `gradiva/racunalnistvo-5` | Računalništvo 5 |
| `gradiva/racunalnistvo-6` | Računalništvo 6 |
| `gradiva/racunalnistvo-6-9` | Računalništvo 6–9 |
| `gradiva/gasilci` | Gasilci |
| `gradiva/rokodelnica` | Rokodelnica |
| `gradiva/svetovni-popotniki` | Svetovni popotniki |
| `gradiva/matematika-3` | Matematika – 3. skupina |
| `gradiva/slovenscina-3` | Slovenščina – 3. skupina |
| `gradiva/anglescina-3` | Angleščina – 3. skupina |

**Na GitHubu (najhitreje):** odpri mapo predmeta → *Add file* → *Upload files*
→ povleci datoteko → *Commit changes*. Čez 1–2 minuti je gradivo na strani.

**Na računalniku:** kopiraj datoteko v mapo predmeta, nato commit in push.

### Pravila

- **Ime datoteke je naslov**, ki ga vidijo učenci. Podčrtaji postanejo
  presledki: `Navodila_Scratch_labirint.pdf` → »Navodila Scratch labirint«.
- **Najnovejše je na vrhu** (»Danes na uri«).
- Datum na začetku imena določi datum gradiva in se ne pokaže:
  `2026-10-20 Kviz.pptx`.
- **Povezava:** naredi besedilno datoteko s končnico `.url`, v kateri je samo
  spletni naslov, npr. `Scratch.url` z vsebino `https://scratch.mit.edu`.
- **HTML z več datotekami:** naloži celo mapo, v kateri je `index.html`.
- **Skrij gradivo:** ime naj se začne s podčrtajem (`_osnutek.pdf`), ali pa
  datoteko izbriši.

Podprto: PDF, slike (PNG, JPG …), Word, PowerPoint, Excel, HTML, video, zvok,
povezave. PDF, slike in HTML se odprejo kar na strani; Word in PowerPoint
prikaže Microsoftov pregledovalnik.

## Prijava in kvizi

Učenci se prijavijo z **istim računom kot v Brihta-MAT** (uporabniško ime +
4 živali). Kdor računa nima, ga ustvari na strani. Ker sta obe strani na
brihta.github.io, je prijava skupna: kdor je prijavljen v Brihta-MAT, je tudi tukaj.
Učitelj se prijavi z e-naslovom (»Prijava za učitelje«). Prijava velja 12 ur
(seja na strežniku), odjava jo takoj prekliče.

Gradiva so dostopna brez prijave. Prijava je potrebna samo za kvize.

### Prvič (enkrat)

V Supabase → SQL Editor zaženi:
1. `supabase_kvizi.sql` (tabele in funkcije),
2. `supabase_kvizi_ucitelj.sql` (učiteljske seje, objava s strani),
3. `~/.config/brihta-sola/NASTAVI_SKRIVNOST.sql` — samo ob novi skrivnosti za skripto.

### Kako objavim kviz (na strani)

1. Prijavi se kot učitelj in odpri predmet.
2. Klikni **＋ Nov kviz**, prilepi besedilo kviza (ali »Vstavi primer«).
   Desno vidiš predogled s pravilnimi odgovori; napake so naštete z vrsticami.
3. Klikni **Objavi**. Kviz je takoj pri učencih.

Na strani kviza (kot učitelj) vidiš rezultate in imaš gumba **Uredi kviz** in
**Skrij kviz**. Pravilni odgovori so samo v bazi, ocenjuje strežnik.

Prva vrstica `Predmet: racunalnistvo-6` (neobvezna) sama izbere predmet — tako
lahko asistent pripravi kviz, ki ga samo prilepiš.

### Objava z računalnika (tajnik v zavihku Code ali skripta)

Kvizi kot datoteke so v `~/Documents/Brihta-kvizi/<predmet>/*.txt` — ZUNAJ
repozitorija (ta je javen, v kvizih so odgovori), na stalnem mestu, da jih najde
vsaka seja na tem Macu. Skrivnost za objavo je v `~/.config/brihta-sola/`.
`python3 scripts/kvizi.py` kvize preveri in objavi; skrije samo svoje kvize,
ki jih ni več v mapi, kvizov s strani se ne dotika. Nove skrivnosti nikoli ne
ustvari sama (samo z `--nova-skrivnost`).

Asistent »tajnik« (zavihek Code, mapa `Nino - Služba/tajnik`) to naredi sam;
navodila so v njegovem `CLAUDE.md`, za seje v tem repozitoriju pa v `CLAUDE.md` tukaj.

### Oblika kviza

```
Predmet: racunalnistvo-5
Naslov: Scratch – ponovitev
Opis: Imaš en poskus.

? Koliko je 2 + 3?          izbira: + pravilen, - napačen
- 4
+ 5

? Kateri so sesalci?        več pravilnih: več vrstic s +
+ pes
+ mačka
- vrabec

? Glavno mesto Slovenije?   kratek odgovor: = (lahko več možnih)
= Ljubljana

? Poveži.                   povezovanje: levo = desno
Francija = Pariz
Italija = Rim

? Razvrsti od najmanjšega.  vrstni red: oštevilčeno v pravilnem vrstnem redu
1. miška
2. mačka
3. slon
```

- Odgovori se učencem pokažejo premešani.
- Kratki odgovori: velike/male črke, presledki in pika na koncu niso pomembni.
- Vsako vprašanje je 1 točka. Učenec ima **en poskus** in po oddaji vidi samo
  svoje točke. Na strani kviza lahko poskus izbrišeš (»Ponastavi«), da ga reši znova.
- Kviz skriješ tako, da datoteko izbrišeš ali preimenuješ v `_ime.txt` in
  znova poženeš skripto. Oddaje ostanejo.
- Če kviz popraviš po tem, ko so ga učenci že oddali, njihove točke ostanejo stare.

## Kako deluje

Ob vsakem pushu v `gradiva/` GitHub Action (`.github/workflows/gradiva.yml`)
zažene `scripts/gradiva.py`, ki iz map zgradi `gradiva.json`. Stran prebere ta
seznam. Lokalno: `python3 scripts/gradiva.py`.

Predmeti (imena, barve, ikone) so na vrhu skripte v `index.html`
(`const PREDMETI`). Nov predmet = nov vnos tam + nova mapa v `gradiva/`.
