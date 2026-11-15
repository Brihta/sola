# Dnevni planer

Ninova zasebna jutranja stran: ure dneva na časovnem traku, ob kliku na uro eVio
opis dejavnosti, predlagani vpis (z gumbom Kopiraj) in kratek pregled za učitelja.
Pod urami so Ksenijina nadomeščanja, obvestila, opozorila, osebni koledar, pogled
na teden in seznam virov z oznako, kaj je bilo prebrano in kaj ne.

Stran je artefakt v Claude (zasebna povezava), ne del javne strani Brihta, ker
vsebuje interne šolske podatke. `planer.html` tukaj je samo predloga s primerom
podatkov, brez pravih vsebin.

## Kako deluje

- Vsak delovni dan ob 4.47 teče načrtovana naloga »Dnevni planer« (Claude Code,
  oddaljena seja). Prebere Ksenijin mail »Nadomeščanje za <dan>« in PDF iz mape
  Drive `Nadomeščanja`, obvestila zadnjih dni, koledarje, Notion opis dejavnosti
  RAP, priprave `EVIO vpisi <dejavnost>.xlsx` na Ninovem Macu (če je povezan) in
  Brihto za ure računalništva.
- Nato zamenja samo JSON v `<script id="podatki" type="application/json">` in
  stran znova objavi na isti naslov. Vse ostalo v datoteki ostane enako.
- Pošlje še kratek mail s povezavo in povzetkom.

## Predloga

`planer.html` nima `<html>`, `<head>` in `<body>`: ogrodje doda Claude ob objavi.
Za lokalni ogled jo odpri v brskalniku; podatki se izrišejo iz JSON bloka.
Sprememba videza: uredi CSS ali JS, nato objavi novo različico na isti naslov
artefakta (Claude: »preberi artefakt, zamenjaj vse razen JSON, objavi na isti url«).

Polja v JSON so opisana v primeru. Pravila:

- `ure` so v časovnem vrstnem redu po uveljavljenih spremembah; proste ure nariše
  stran sama. `sprememba` ni `null` samo pri urah, ki jih je spremenila Ksenija.
- `zastavice` vsebuje `PREVERI`, kadar vpis ni iz priprave ali je položaj skupine
  negotov.
- `viri` povedo za vsak vir, ali je bil prebran (`da`, `delno`, `ne`) in zakaj ne.
- Brez pomišljajev in brez imen učencev.
