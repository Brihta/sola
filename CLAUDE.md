# Brihta — Šola (brihta.github.io/sola)

Stran za učence: predmeti, gradiva za uro in spletni kvizi. Kazalo vseh projektov: `matematika/KAZALO.md`
(repozitorij Brihta/matematika). Nino je učitelj;
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

`<predmet>` je eden od: racunalnistvo-3, racunalnistvo-4, racunalnistvo-5, racunalnistvo-6,
racunalnistvo-6-9, fleksi-matematika, fleksi-spelling, fleksi-reading, fleksi-teaching, fleksi-lessons.

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

Pri VSEH urah računalništva (racunalnistvo-3, -4, -5, -6, -6-9) so koraki ure
samostojne HTML strani, ki jih učenci prehodijo sami, brez učitelja (do 25
učencev; 3. r 8 do 9 let, 4. r 9 do 10 let, ostali 11 do 14 let; učiteljeva razlaga in delo v paru za to ne delujeta).
Ne delaj več Word zapisov, PDF prosojnic in delovnih listov za te ure.
Orodje, pravila zasnove in primer so v `orodja/samostojna-ura/README.md`:
preberi ga, preden začneš (tudi razdelek »Naučeno iz prakse«). Zgradi z
`zgradi.py`, preveri s `preveri.py` in poglej posnetke vseh nalog: naloga mora
biti rešljiva samo iz tega, kar je na zaslonu.

## Gradiva za uro

Vsaka ura je MAPA `gradiva/<predmet>/<YYYY-MM-DD> <N>. ura <Naslov ure>/` s koraki, ki
jih učenci prehodijo po vrsti:

- `1 Navodila.md`: cilj ure (## 🎯 Cilj ure), kriteriji uspešnosti, kaj bomo delali (oštevilčeno);
- `2 Zapis.docx`: zapis za zvezek;
- `3 Razlaga.pdf`: razlaga učitelja (PDF prosojnic 1280×720, npr. iz HTML s headless Chrome `--print-to-pdf`);
- `4 Delovni list.docx` (če je);
- `5 Kviz.kviz`: ena vrstica, slug ali naslov kviza (slug = ime datoteke kviza, npr. `razgradnja-in-vzorci`).

Povezava je korak `N Ime.url`: prva vrstica je spletni naslov, neobvezno še
`opis=…` (ena kratka poved), `emoji=…` ali `slika=…` (pot od korena strani, npr.
`brihta.png`). Učenec dobi kartico s sliko in gumbom »Gremo!«.

Številka določa vrstni red in se ne pokaže. Nato commit in push na `main`;
GitHub Action posodobi `gradiva.json` (v 1–2 minutah). Posamezne datoteke
neposredno v mapi predmeta še delujejo, a uro vedno objavi kot mapo.

Več v README.md.

## Fleksi Spelling: tedenski postopek

Nino reče npr. »Spelling, teden 2«. Takrat:

1. Vir: `/Users/ninokokalj/Library/CloudStorage/OneDrive-OŠŠempetervSavinjskidolini/1. Šolsko leto 26-27/Dejavnosti/Fleksi Angleščina/English/Spelling/Stopnja 2 (Year 2)/<1. ali 2.> ocenjevalno obdobje/Teden NN <vzorec>.pdf`
   (tedni 1 do 16 so v 1., 17 do 30 v 2. ocenjevalnem obdobju). Trenutna stopnja je **2**, skupina **Tree**.
   Če Nino reče drugo stopnjo ali skupino, uporabi tisto.
2. Vsak PDF ima 3 strani: 1 Kite, 2 Boat, 3 Tree. Vzemi SAMO stran Tree (3. stran) in preveri,
   da je na njej »Tree« in »My test«. Uporabi pypdf ali pymupdf (če ga ni: `pip3 install --user pypdf`).
   Originala na OneDrivu ne spreminjaj.
3. Shrani v `gradiva/fleksi-spelling/<YYYY-MM-DD> Week <N> <vzorec>.pdf`: datum je ponedeljek, ko je ura
   (če Nino ne reče drugače, najbližji ponedeljek), N brez vodilne ničle, vzorec iz imena vira
   (npr. `Teden 02 soft g.pdf` → `2026-11-23 Week 2 soft g.pdf`).
   Poleg lista objavi še narek: stavek za ta teden je v `00 Seznam besed in narek Stopnja <N>.pdf`
   (v mapi stopnje, stolpec »Narek«). Zapiši ga v `gradiva/fleksi-spelling/<isti datum> Week <N> Dictation.html`
   po vzoru `2026-11-16 Week 1 Dictation.html` (stavek velik, besede tedna obarvane). Viden je vsem, tudi učencem
   (Nino se je tako odločil).
   Tedni 2 do 11 (do 1. 2. 2027) so že naloženi vnaprej. Vnaprej naloženo gradivo se NIKOLI ne objavi
   samo: ostane skrito, dokler ga Nino ne objavi s stikalom 👁/🙈 (prijavljen kot učitelj). Tako se je odločil.
   Ko Nino reče »Spelling, teden N« za že naložen teden, preveri, da sta list in narek tam, in ju objavi
   sam (glej »Objava gradiva brez prijave« spodaj). Če skripta ne teče, mu povej, da ju objavi s stikalom.
4. `python3 scripts/gradiva.py`, nato commit in push na `main`.
5. Ninu povej naslov in da je čez 1 do 2 minuti na strani (Fleksi › Angleščina › Spelling).

Pravilo točkovanja na listih: vse natisnjene besede (tudi zvezdica) se točkujejo, okvir je »My test ___ / N«
(Kite 6, Boat 9, Tree 12). Če kdaj popravljaš liste, ostane tako v vseh stopnjah.

## Objava gradiva brez prijave

Ko Nino reče »objavi …« ali »skrij …« (tudi s telefona, v katerem koli klepetu), to narediš sam:

1. `python3 scripts/zahteva.py <predmet> "<del imena>"` (dodaj `--skrij` za skrivanje). Skripta preveri ime
   v gradiva.json in doda vrstico v `objave/zahteve.jsonl`. Vse, kar se ujema, se objavi ali skrije
   (»Week 2« = list in narek).
2. Commit in push na `main`.
3. Ninov Mac (launchd `si.brihta.objave`) vsaki 2 minuti pogleda datoteko na GitHubu, izvede nove
   zahteve in mu pokaže obvestilo. Ninu povej, kaj si zahteval, in da bo na strani v največ 2 do 3 minutah,
   če je Mac prižgan. Potrditve ne vidiš: ne trdi, da je že objavljeno.

Če je klepet povezan z Macom in je dodana mapa `~/.config/brihta-sola`, lahko namesto tega zahtevo
odložiš v `$HOME/mnt/brihta-sola/vrsta/<ime>.zahteva` (JSON kot zgoraj) in po ~20 s prebereš
`<ime>.rezultat` (to je potrditev). Skrivnosti NIKOLI ne beri. Supabase iz Claudovih okolij ni dosegljiv.
V Supabase je zagnan `supabase_gradiva_skrivnost.sql`; namestitev na Macu: `~/.config/brihta-sola/namesti_vrsto.sh`.

## Fleksi Angleščina: Teaching in Our lessons (dve različici vsake ure)

Nino ure gradi po Rosenshineovih načelih. Vsaka ura ima DVE različici z istim datumom in naslovom:
- `gradiva/fleksi-teaching/<ponedeljek> <Naslov>/` (ploščica **Teaching**, vidi jo SAMO učitelj, `samoUcitelj`):
  koraki `.md` za učitelja, en zaslon na korak: `## ⏱ N minutes`, vrstica `📐 *Rosenshine: …*`,
  `## 🧒 Pupils` (kratka navodila za tablo) in `## 🧑‍🏫 Teacher` (kaj reče in naredi, rešitve). Seznam
  `ol` se ne sme prekiniti z `ul` (številčenje se začne znova). Prvi korak je »Lesson plan« (cilji, časi, kaj pripraviti).
- `gradiva/fleksi-lessons/<ponedeljek> <Naslov>/index.html` (ploščica **Our lessons**, za učence, starše, odsotne):
  ena prijazna stran, sklopi 🔁 Look back, 🧩 Something new, 🤝 Practise together, ✍️ On your own,
  🏠 Missed the lesson? (s povezavami `target="_top"` na Spelling/Reading). Risbe v SVG in emojiji, brez fotografij,
  brez imen učencev, BREZ rešitev in testnih besed. Vzor: `2026-11-23 Badgers and soft g`.
- Besede za test spellinga s povedmi (naključni vrstni red) so posebno gradivo v Spelling:
  `<ponedeljek> Week <N> Test.html` (skrito, dokler ga Nino ne objavi za vajo). Učenci pišejo v zvezek 1 do 12,
  nato si zamenjajo zvezke in popravljajo po listu tedna; narek na tablo (Week N Dictation).
Obe različici sta naloženi vnaprej (skriti). Our lessons se objavi PO uri (povzetek), Teaching se ne objavlja.

## Fleksi Reading: tedensko besedilo

Reading PDF-ji na OneDrivu (`.../English/Reading`) so od 16. 11. 2026 že očiščeni (brez Twinkl noge; Nino
je tako želel). Enaka kopija je v `~/Documents/Brihta-reading/`, originali s Twinkl nogo pa v
`~/Documents/Brihta-reading-originali-twinkl/`. Skripta za čiščenje novih datotek:
`~/Documents/Brihta-reading/_odstrani_twinkl_nogo.py` (nad nogo se ne sme spremeniti noben piksel).
Objavljamo SAMO raven **Tree** (`... 3 Tree.pdf`) iz `KS1 (Year 1 in 2)/<mesec>/`, BREZ strani z rešitvami
(stran z naslovom »Answers«), kot `gradiva/fleksi-reading/<ponedeljek> <Naslov>.pdf`. Ena na teden, isti
ponedeljki kot Spelling. Tedni do 1. 2. 2027 so naloženi vnaprej (skriti, dokler jih Nino ne objavi s stikalom):
Road Safety Week, Planting Trees, Hanukkah, Winter, New Year Celebrations Around the World, Epiphany,
The Snowball Fight Poem, All About Penguins, British Garden Birds, Rumpelstiltskin.
Pred objavo preveri: ni besede »twinkl« in ni »Answers« v besedilu, in poglej vse strani.

## Moja besedila (pisanje-besedil/)

Vse znanje o programu Moja besedila (baza, načini popravljanja, objava, odločitve)
je v `pisanje-besedil/CLAUDE.md`. Preberi ga, preden kaj spreminjaš.

## Video navodila za učence

Ko Nino prosi za video (»pripravi video: …«, »sestavi«), uporabi skill `video-navodila` in orodje v
`~/Documents/Brihta-video/` (zunaj repozitorija; README tam). Ne začenjaj znova. Nino posname samo glas.

## Emojiji (pisava Brihta Emoji)

Pisave strežemo sami iz `pisave/` (brez Google Fonts, GDPR): Nunito (`pisave/nunito.css`) in emojije. `index.html` nalaga lastno podmnožico Noto Color Emoji (COLRv1) iz `pisave/brihta-emoji.woff2`,
da so emojiji (tudi zastave) na Windows enaki kot drugod. Ko dodaš nov emoji v `index.html` ali v
gradivo (npr. `emoji=` v `.url`), poženi `python3 scripts/emoji_pisava.py` (potrebuje
`pip3 install --user fonttools brotli`) in commitaj `pisave/` in `index.html`. Emoji, ki ga v
podmnožici ni, se pokaže s sistemsko pisavo.

## Ikona in logotip

Rdeča sova (`brihta.png`, `apple-touch-icon.png`, `ikona-*.png`, `favicon-32.png`, `manifest.webmanifest`).
Izvor je `ikona-1024.png`: logotip iz `matematika/Brihta.svg`, zeleni deli prebarvani v rdečo (odtenek ~359°),
da se Šola loči od Matematike. Nove velikosti delaj iz `ikona-1024.png`.
