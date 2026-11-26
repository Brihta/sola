# Predloga za kviz (Excel)

Učitelj odpre svojo kopijo `Brihta predloga za kviz.xlsx` (deljena na OneDrivu), vpiše vprašanja
in datoteko naloži na Brihto Šola v izbrani modul. Stran iz nje naredi kviz.

Predlogo zgradiš znova s `python3 predloga.py "Brihta predloga za kviz.xlsx"` (potrebuje openpyxl).
Spremembe vrst ali stolpcev morajo iti hkrati v `predloga.py`, ta opis in bralnik na strani.

## Oblika, ki jo bere stran

- Bere se SAMO list z imenom **`Kviz`**. Listi `Navodila` in `Primer` ter skriti list `Seznami` (vrste za spustni seznam) se ne berejo
  (za poskusno nalaganje primera ga učitelj skopira na list Kviz).
- `C1` = naslov kviza (obvezen), `C2` = opis (neobvezen).
- Vrstica 5 = glava, vprašanja so od vrstice **6** naprej (60 pripravljenih vrstic; bralnik naj bere,
  dokler je kaj vpisano, ne samo do 65).
- Stolpci: `A` št. (prezri), `B` vrsta, `C` vprašanje, `D`–`I` odgovor 1 do 6,
  `J` in `K` sta formuli za pomoč (prezri).
- Popolnoma prazna vrstica (B, C, D–I prazni) se preskoči.

| Vrsta (`B`) | Odgovori (`D`–`I`) |
|---|---|
| `Izbira` | D = pravilni; E–H = napačni (1 do 4); I prazen |
| `Več pravilnih` | 2 do 6 odgovorov; pravilni imajo spredaj `*` (zvezdica se odreže); vsaj 1 pravilen in 1 napačen; učenec mora označiti vse pravilne (`vec`) |
| `Drži / Ne drži` | D = `Drži` ali `Ne drži` |
| `Poveži` | vsak neprazen odgovor je `levo = desno` (presledek, enačaj, presledek); 2 do 6 parov |
| `Razvrsti` | 2 do 6 odgovorov v PRAVILNEM vrstnem redu |
| `Število` | D = število (v Excelu številska celica; besedilo z decimalno vejico sprejmi kot število) |

Bralnik na strani mora ponoviti vsa preverjanja iz stolpca K (učitelj lahko formule izbriše)
in učitelju napake pokazati z besedami in številko vrstice, npr. »Vprašanje 7: manjka pravilni odgovor«.

Pravilni odgovori gredo samo v skrito polje `kljuc` (kot pri obstoječih kvizih, `supabase_kvizi.sql`),
nikoli v brskalnik učenca. Odgovori se učencem premešajo. Vsako vprašanje je 1 točka.

Slik v predlogi ni: učitelj jih doda na strani k posameznemu vprašanju, ko je kviz narejen.
