# Samostojna ura: interaktivne strani za korake ure

Ure računalništva so zgrajene tako, da jih učenci (11 do 14 let, okoli 25 v
skupini) prehodijo **sami, s svojo hitrostjo, brez učitelja**. Vsak korak ure
je ena HTML stran, ki uči, preveri in odklene naslednji korak.

## Datoteke

| Datoteka | Kaj je |
|---|---|
| `engine.js`, `style.css` | pogon in videz strani (se vgradita v vsako stran) |
| `zgradi.py` | iz opisa ure (Python) naredi HTML strani |
| `preveri.py` | samodejno preklika vse zaslone in javi napake (Playwright) |
| `primer-7-ura-zapis-algoritma.py` | celoten primer ure, ki je v rabi; kopiraj ga za novo uro |

```
python3 zgradi.py "<opis-ure.py>" "<mapa ure v gradiva/...>"
python3 preveri.py "<mapa ure v gradiva/...>"
```

Opise ur shranjuj sem, kot `opisi/<predmet>/<YYYY-MM-DD> <N>. ura <Naslov>.py`,
da jih lahko kasneje popraviš in znova zgradiš.

## Pravila zasnove (obvezno)

1. **En zaslon, eno dejanje.** Največ dve kratki povedi, nato učenec nekaj naredi.
2. **Najprej primer, nato naloga.** Nov pojem pokaži na `info` zaslonu ali na
   nalogi, ki jo učenec samo zažene (npr. `grid` z `locked`).
3. **Vsaka naloga se preveri sama** in pove, *zakaj* je narobe (polje `why` pri
   vsaki napačni možnosti).
4. **Vsaka naloga ima 1 do 3 namige** (`hints`), od splošnega do skoraj rešitve.
   Po zadnjem se pokaže »Pokaži rešitev«, da nihče ne obtiči.
5. **Brez dela v paru in brez učiteljeve razlage** kot pogoja za napredek.
6. **Jezik za 11 let:** kratke povedi, »ti«, oblike »/a« (naredil/a).
7. **Osnovna pot za vse v okoli 25 minutah.** Dodatno označi s `stars: '★★'` in
   `optional: True` (gumb »Preskoči«), ali kot zadnji korak ure »Izziv«.
8. **Dejavnost pred teorijo:** pojem vpelji skozi igro ali izziv.
9. Brez osebnih podatkov, brez zunanjih knjižnic in povezav (vse je v eni datoteki).
10. Nikoli pomišljajev (— ali –); uporabi vejico, dvopičje, oklepaj.

## Vrste zaslonov

```python
info(naslov, html)                       # razlaga; razredi: big, box, warn, small, sym o/r/d, tk, tk loop
{'type':'choose', 'title', 'intro', 'options':[ch('besedilo', ok=True, why='...'), ...], 'hints':[...]}
{'type':'order',  'title', 'intro', 'items':[koraki v PRAVEM vrstnem redu], 'hints'}
{'type':'match',  'title', 'pairs':[['levo','desno'], ...], 'hints'}
{'type':'check',  'title', 'html', 'label':'Prepisal/a sem v zvezek.'}   # zapis v zvezek
{'type':'grid',   'title', 'intro', 'n':5, 'target':[[vrstica,stolpec],...], 'solution':[...],
                  'loops':[2,3,4,5], 'max':4, 'start':[...], 'locked':True, 'win':'...', 'hints'}
                  # žetoni: 'R','L','D','U','P' (pobarvaj), 'N3' (ponovi 3× ( ), ')'
                  # 'max' šteje VSAK gumb v programu, tudi ')' (kar učenec vidi, to se šteje)
{'type':'trace',  'title', 'intro', 'path':[{'n':'z'},{'n':'e','a':'ne','q':'Ali je 65 = 40?','why':'...'},...], 'win'}
                  # diagram »Ugani število«; vozlišča: z i v e l m1 m2 b k
{'type':'guess',  'title', 'intro', 'hints'}               # igra Ugani število 1 do 100
{'type':'cards',  'title', 'n':8, 'hints'}                 # najdi največje med obrnjenimi kartami
{'type':'keys',   'title', 'intro', 'keys':'asdfjklč', 'n':25, 'min':85, 'win', 'hints'}
                  # pritisni označeno tipko; zaslonska tipkovnica z barvo prsta; ';' šteje kot č
{'type':'times',  'title', 'intro', 'tables':[2,3,4,5], 'n':10, 'save':True|'compare':True, 'win', 'hints'}
                  # poštevanka: natipkaj rezultat (številke zgoraj), meri čas in napake
{'type':'type',   'title', 'intro', 'text':'...', 'min':90, 'save':True|'compare':True, 'win', 'hints'}
                  # natipkaj vrstico; natančnost (Levenshtein) in hitrost; save = izhodišče, compare = primerjava z njim
```

Vsak zaslon lahko ima še `stars` in `optional`. Na koncu vsake strani se sam doda
zaslon »🎉 Končano!«.

**Nova vrsta naloge** (npr. za Scratch, binarna števila, omrežja): dodaj
`TYPES.<ime> = (s, c) => { ...; done('✅ ...'); return { solve: () => {...} }; }`
v `engine.js`. Funkcija `done()` odklene naprej, `feedback(html, 'ok'|'bad'|'hint')`
pokaže odziv. Nato znova zgradi in preveri **tudi stare ure**.

## Zaklep gumba »Naprej« na Brihti

Stran ob nalaganju pošlje `postMessage({tip:'brihta-korak', stanje:'zacetek'})`,
ob koncu pa `stanje:'koncano'`. Brihta (`index.html`) do takrat zaklene oranžni
gumb »Naprej« pod okvirjem. Strani brez tega sporočila gumba ne zaklenejo.
Napredek je shranjen v brskalniku učenca (localStorage).

## Kviz ure

Korak `.kviz` se odklene šele, ko so rešeni **vsi interaktivni koraki pred
njim** (`gradiva.py` jih označi z `interaktivno: true`, ker vsebujejo
`brihta-korak`). Do takrat učenec vidi seznam nerešenih korakov s povezavami.
Ko je odklenjen, se kviz ob prvem obisku odpre sam. Neobvezne izzive zato
postavi ZA kviz.
