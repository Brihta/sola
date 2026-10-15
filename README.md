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
Učitelj se prijavi z e-naslovom (»Prijava za učitelje«), odpre kviz in vidi rezultate.

Gradiva so dostopna brez prijave. Prijava je potrebna samo za kvize.

### Prvič (enkrat)

V Supabase → SQL Editor zaženi:
1. `supabase_kvizi.sql` (tabele in funkcije),
2. `kvizi/NASTAVI_SKRIVNOST.sql` (samo na tem računalniku; ne pošiljaj ga nikomur).

### Kako objavim kviz

Kvizi so v mapi `kvizi/<predmet>/` **samo na tem računalniku** (niso na
GitHubu, ker so v njih pravilni odgovori, repozitorij pa je javen).

1. Naredi besedilno datoteko `kvizi/racunalnistvo-5/Scratch ponovitev.txt`
   (primer z vsemi vrstami vprašanj: `kvizi/racunalnistvo-5/_Primer kviza.txt`).
2. Poženi `python3 scripts/kvizi.py` — preveri vse kvize in jih objavi.
   Na strani so takoj (brez čakanja na GitHub).

Ali pa Claudu reci: »naredi kviz za Računalništvo 5 s temi vprašanji …«.

```
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
