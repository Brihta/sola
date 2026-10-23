# Brihta — Šola (brihta.github.io/sola)

Stran za učence: predmeti, gradiva za uro in spletni kvizi. Nino je učitelj;
piši mu v slovenščini.

## Kvizi — naredi IN objavi jih sam

Ko Nino prosi za kviz (ali ko pri pripravi ure nastane kviz), ga ne daj Ninu
v kopiranje: zapiši datoteko in jo objavi.

1. Zapiši `~/Documents/Brihta-kvizi/<predmet>/<Kratko ime>.txt`
   (mapa je ZUNAJ repozitorija; datoteke kvizov nikoli ne daj v repozitorij,
   ker je javen, v kvizih pa so pravilni odgovori).
2. Preveri: `python3 /Users/ninokokalj/Documents/Shared_documents/GitHub/sola/scripts/kvizi.py --preveri`
3. Objavi:  `python3 /Users/ninokokalj/Documents/Shared_documents/GitHub/sola/scripts/kvizi.py`
   Skripta objavi vse kvize iz mape; na strani so takoj (brez commita, brez čakanja).
4. Ninu povej naslov, predmet in da je kviz objavljen. Rezultate vidi na strani,
   ko se prijavi kot učitelj in odpre kviz.

Pravila za skripto:
- Če skripta javi napake, jih popravi v datoteki in poženi znova.
- Če javi, da ni skrivnosti: NE uporabi `--nova-skrivnost` in ne ustvarjaj
  nove. Pomeni, da ne tečeš na Ninovem Macu — daj Ninu besedilo kviza, da ga
  prilepi na strani (»＋ Nov kviz«).
- Kviz popraviš tako, da urediš datoteko in znova objaviš. Skriješ ga tako, da
  datoteko preimenuješ v `_Ime.txt` in znova objaviš. Oddaje ostanejo.
- Ime datoteke določa kviz: preimenovanje (brez `_`) naredi NOV kviz.

`<predmet>` je eden od: racunalnistvo-4, racunalnistvo-5, racunalnistvo-6,
racunalnistvo-6-9, gasilci, rokodelnica, svetovni-popotniki, matematika-3,
slovenscina-3, anglescina-3.

### Oblika

```
Predmet: racunalnistvo-6
Naslov: Razgradnja problema
Opis: Reši sam. Imaš en poskus.

? Vprašanje z eno pravilno izbiro
- napačen odgovor
+ pravilen odgovor

? Vprašanje z več pravilnimi
+ pravilen
+ pravilen
- napačen

? Vprašanje s kratkim odgovorom
= odgovor
= druga sprejemljiva oblika

? Poveži pojme.
pojem A = razlaga A
pojem B = razlaga B

? Razvrsti v pravilni vrstni red.
1. prvi
2. drugi
3. tretji
```

- `Predmet:` se mora ujemati z mapo. Vprašanje se začne z `?`; `#` je komentar.
- Vsako vprašanje je 1 točka. Pri enem vprašanju ne mešaj vrst odgovorov.
- Izbira: vsaj 2 odgovora, vsaj en `+`, nobena dva enaka.
- Kratek odgovor samo, kadar je nedvoumen; naštej vse sprejemljive oblike.
  Velike/male črke, presledki, pika na koncu in decimalna vejica/pika niso pomembni.
- Povezovanje: `levo = desno` s presledkoma okoli `=`, vsaj 2 para.
- Razvrščanje: oštevilčeno v PRAVILNEM vrstnem redu, vsaj 2 elementa.
- Nadaljevalna vrstica vprašanja se ne sme začeti s `+`, `-`, `=`, številko s
  piko in ne sme vsebovati ` = `.
- Odgovori se učencem premešajo: ne piši »vse zgoraj navedeno«.

### Vsebina

- 5–8 vprašanj, vezanih na cilje ure, v slovenščini, primerno starosti razreda.
- Brez osebnih podatkov (prava gesla, naslovi, imena sošolcev).
- Učenec ima en poskus in po oddaji vidi samo svoje točke. Pod 50 % se oddaja
  ne shrani: dobi »Poskusi znova« in reši ponovno.

## Ure računalništva: samostojne interaktivne strani (obvezno od 23. 10. 2026)

Pri VSEH urah računalništva (racunalnistvo-4, -5, -6, -6-9) so koraki ure
samostojne HTML strani, ki jih učenci prehodijo sami, brez učitelja (do 25
učencev, 11 do 14 let; učiteljeva razlaga in delo v paru za to ne delujeta).
Ne delaj več Word zapisov, PDF prosojnic in delovnih listov za te ure.
Orodje, pravila zasnove in primer so v `orodja/samostojna-ura/README.md`:
preberi ga, preden začneš. Zgradi z `zgradi.py`, preveri s `preveri.py`.

## Gradiva za uro

Vsaka ura je MAPA `gradiva/<predmet>/<YYYY-MM-DD> <N>. ura <Naslov ure>/` s koraki, ki
jih učenci prehodijo po vrsti:

- `1 Navodila.md`: cilj ure (## 🎯 Cilj ure), kriteriji uspešnosti, kaj bomo delali (oštevilčeno);
- `2 Zapis.docx`: zapis za zvezek;
- `3 Razlaga.pdf`: razlaga učitelja (PDF prosojnic 1280×720, npr. iz HTML s headless Chrome `--print-to-pdf`);
- `4 Delovni list.docx` (če je);
- `5 Kviz.kviz`: ena vrstica, slug ali naslov kviza (slug = ime datoteke kviza, npr. `razgradnja-in-vzorci`).

Številka določa vrstni red in se ne pokaže. Nato commit in push na `main`;
GitHub Action posodobi `gradiva.json` (v 1–2 minutah). Posamezne datoteke
neposredno v mapi predmeta še delujejo, a uro vedno objavi kot mapo.

Več v README.md.
