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

## Kako deluje

Ob vsakem pushu v `gradiva/` GitHub Action (`.github/workflows/gradiva.yml`)
zažene `scripts/gradiva.py`, ki iz map zgradi `gradiva.json`. Stran prebere ta
seznam. Lokalno: `python3 scripts/gradiva.py`.

Predmeti (imena, barve, ikone) so na vrhu skripte v `index.html`
(`const PREDMETI`). Nov predmet = nov vnos tam + nova mapa v `gradiva/`.
