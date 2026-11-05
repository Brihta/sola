# Samostojna ura: interaktivne strani za korake ure

Ure računalništva so zgrajene tako, da jih učenci (4. razred 9 do 10 let,
ostali 11 do 14 let, okoli 25 v skupini) prehodijo **sami, s svojo hitrostjo, brez učitelja**. Vsak korak ure
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
6. **Jezik za starost:** kratke povedi, »ti«, oblike »/a« (naredil/a). V 4. razredu
   (9 do 10 let) še krajše: ena misel na poved, veliko emojijev in slik, brez zank
   (zanka je v 4. r šele pri Scratchu), mreža 4 × 4.
7. **Osnovna pot za vse v okoli 25 minutah.** Dodatno označi s `stars: '★★'` in
   `optional: True` (gumb »Preskoči«), ali kot zadnji korak ure »Izziv«.
8. **Dejavnost pred teorijo:** pojem vpelji skozi igro ali izziv.
9. Brez osebnih podatkov, brez zunanjih knjižnic in povezav (vse je v eni datoteki).
10. Nikoli pomišljajev (— ali –); uporabi vejico, dvopičje, oklepaj.
11. **Naloga se reši samo iz tega, kar je na zaslonu.** Vsi podatki (slika, vrsta,
    pravilo) morajo biti vidni. Če učenec lahko le ugiba s klikanjem, je naloga
    pokvarjena. `preveri.py` javi »NEPOPOLNO NAVODILO«, če se del uvoda ne prikaže.
12. **Pred prvo nalogo izbire povej, kako se dela:** »Klikni odgovor. Če je narobe,
    ti stran pove zakaj. Če ne veš, kako začeti, klikni Namig.«
13. **Mlajšim (4. r) daj naloge, ki jih znajo prebrati v eni sapi.** Težko nalogo
    (npr. igrače na traku) označi ★★ in `optional`, da jo lahko preskočijo.

## Vrste zaslonov

```python
info(naslov, html)                       # razlaga; razredi: big, box, warn, small, sym o/r/d, tk, tk loop
{'type':'choose', 'title', 'intro', 'options':[ch('besedilo', ok=True, why='...'), ...], 'hints':[...]}
                  # intro sme vsebovati <p>, <div>, mrežo (je v <div class="intro">); preveri posnetke
                  # 'abcd': True = možnosti ostanejo v danem vrstnem redu z oznakami A, B, C, D (kot na Bobrčku)
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
{'type':'slogi',  'title', 'intro', 'paras':[['besedilo','Naslov 1'], ['besedilo','Navadno','zakaj?'], ...], 'win', 'hints'}
                  # mali urejevalnik: klikni odstavek, nato slog (Naslov, Naslov 1, Naslov 2, Navadno);
                  # desno se sproti riše podokno za krmarjenje; Preveri obarva napačne in pove zakaj
{'type':'zrcali', 'id':'n1', 'title', 'intro', 'os':'v'|'h', 'pol':['..RR', ...], 'obrni':False, 'demo':False, 'hints'}
                  # simetrija na mreži: pol = dana polovica (pri 'v' levi stolpci, pri 'h' zgornje vrstice), '.' prazno
                  # barve: R rdeča, Y rumena, G zelena, B modra, O oranžna, P vijolična, K rjava, C črna
                  # obrni = lik je desno/spodaj; demo = učenec klikne »Poglej, kako« in gleda zrcaljenje
                  # odziv loči: napačno mesto (✖), napačna barva (obroba), manjka, lik le prerisan (ne zrcaljen)
{'type':'zrcali', 'prosto':True, 'w':12, 'h':10, 'os':'v', 'barve':'RYGBOP'}   # prosto risanje, zrcalo riše samo
```

Vsak zaslon lahko ima še `stars` in `optional`.

**Izdelki za učiteljevo poročilo:** `stran(..., izdelki='racunalnistvo-3/2026-11-06-simetrija')`.
Stran potem zahteva prijavo (ali »Nadaljuj brez shranjevanja«), v glavi pokaže, za koga shranjuje,
in po vsaki rešeni nalogi zapiše v Supabase (`supabase_izdelki.sql`): stanje (sam, namig, rešitev),
poskuse, namige in pri `zrcali` še mrežo. Daj nalogam stalen `id`, da se ob popravku ure poročilo ne pomeša. Na koncu vsake strani se sam doda
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

**Učitelj** (prijavljen kot učitelj) kviza nima nikoli zaklenjenega: na koraku
Kviz vidi naslov, število vprašanj in gumb »📊 Oddaje učencev in vprašanja«
(rezultati po učencih, povprečje, pravilnost po vprašanjih, Ponastavi, predogled
vprašanj). Zaklep velja samo za učence. Zelena kljukica pri interaktivnem koraku
pomeni, da je korak REŠEN (🎉 Končano!), ne le odprt, zato se kljukice in
zaklep vedno ujemajo. Pri spremembah `index.html` tega ne pokvari.

## Naučeno iz prakse

**4. razred, 4. ura Algoritem po prostoru (3. 11. 2026), ura je uspela:** učenci so
uživali in delali vsak s svojo hitrostjo. Kar je šlo narobe in je popravljeno:

- Uvod naloge je bil v `<p>`; brskalnik je odvrgel vse od notranjega `<p>` naprej
  (učenka ni videla igrač in pravila, zato je ugibala). Zdaj je uvod v `<div>`, in
  `preveri.py` to preverja. Pri vsaki novi uri vseeno poglej posnetke VSEH nalog.
- Gumbi so bili pripeti na dno okvirja (velik prazen pas pod kratkimi zasloni).
  Zdaj so tik pod vsebino in pri dolgih nalogah prilepljeni na dno okna.
- Mrežo s sliko v uvodu naredi iz `<span>` z `display:inline-grid` (glej funkcijo
  `mreza()` v `opisi/racunalnistvo-4/2026-11-10 4. ura Algoritem po prostoru.py`).

**Bobrček (ACM Bober, 2. do 5. r):**

- Za 4. razred NI spletne vadnice; na bober.acm.si so vaje za goste šele od 6. r.
  Tekmovanje za 2. do 5. r je na papirnatih polah (PDF), naloge niso vse ABCD.
- Arhiv: https://tekmovanja.acm.si/?q=bober%2Fnaloge-re%C5%A1itve , pole po
  razredih: https://ucilnica.acm.si/course/view.php?id=103 (4. r 2024/25: id=2855).
- Pravih nalog NE prepisuj v repozitorij (je javen, licenca ni navedena). Napiši
  izvirne naloge v istem slogu in dodaj povezavo na pravo polo kot `.url` korak.
- Vaja za Bobrček je `choose` z `'abcd': True` (možnosti po vrsti z A, B, C, D, kot
  na tekmovanju; učitelj jih lahko uporabi tudi za glasovanje v razredu).
- Šolsko tekmovanje je novembra (2026: 9. do 20. 11.). Preveri, ali ima oddelek v
  tem oknu sploh uro, in to Ninu povej takoj.

**Bober (ACM, 6. do 9. r), vadnica za goste (preverjeno 5. 11. 2026):**

- Povezave `https://bober.acm.si/simple/guest/compete/<id>/` odprejo test brez obrazca (v vgrajenem brskalniku).
- Med reševanjem vadnica ne pove, ali je odgovor pravilen. Po »Zaključi« pokaže stran Rezultati
  (za vsako ODGOVORJENO nalogo Pravilen ali Napačen odgovor in točke); vsote ne pokaže.
- Vrstni red nalog in odgovorov se za vsak poskus premeša, zato list za odgovore s črkami ne deluje.
- Rezultat učenec vpiše v kviz `Samoocena …` (vsaka naloga: Pravilen, Napačen, Nisem odgovoril/a).
  Kvizi z id `…/samoocena-…` nimajo pravila 50 % (`supabase_kvizi_samoocena.sql`).
