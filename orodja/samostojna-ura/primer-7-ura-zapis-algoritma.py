# Primer opisa ure: Računalništvo 6. do 9. r., 7. ura »Zapis algoritma« (23. 10. 2026).
# Zgradi:  python3 zgradi.py primer-7-ura-zapis-algoritma.py "/tmp/poskus"
# Za novo uro kopiraj to datoteko, zamenjaj vsebino in jo shrani ob ostalih opisih.

# ---------------- 2 Kaj je algoritem ----------------
stran('2 Kaj je algoritem.html', 'Kaj je algoritem?', [
    info('Algoritem = natančna navodila', '''
<p class="big">Računalnik ne misli. Naredi <b>točno to</b>, kar mu napišeš, nič več in nič manj.</p>
<div class="box big">🧩 <b>Algoritem</b> je natančno zaporedje korakov, ki reši problem.</div>
<p>Dober algoritem ima tri lastnosti:</p>
<p>✅ <b>jasni koraki</b>: vsak ve, kaj mora narediti<br>🔢 <b>pravi vrstni red</b>: najprej to, potem ono<br>🏁 <b>konča se</b>: ne teče v nedogled</p>
<p class="small">Klikni zeleni gumb <b>Naslednja naloga</b>.</p>'''),
    {'type': 'order', 'title': 'Prijava v računalnik', 'intro': 'Uredi korake algoritma »Prijavim se v šolski računalnik«.',
     'items': ['Prižgem računalnik.', 'Vpišem uporabniško ime.', 'Vpišem geslo.', 'Kliknem »Prijava«.'],
     'hints': ['Brez prižganega računalnika ne moreš ničesar vpisati.', 'Najprej povem, KDO sem (ime), šele nato skrivnost (geslo).']},
    {'type': 'order', 'title': 'Oddam nalogo', 'intro': 'Uredi korake algoritma »Oddam nalogo v spletno učilnico«.',
     'items': ['Prijavim se s šolskim računom.', 'Odprem predmet in nalogo.', 'Izberem datoteko na računalniku.', 'Kliknem »Oddaj«.', 'Preverim, ali piše »Oddano«.', 'Odjavim se.'],
     'hints': ['Pred vsem drugim se moraš prijaviti.', 'Odjava je vedno zadnja.', 'Preden klikneš »Oddaj«, mora biti datoteka že izbrana.']},
    {'type': 'choose', 'title': 'Kateri ukaz je natančen?', 'intro': 'Robot mora priti do vrat. Kateri ukaz robot razume brez vprašanj?',
     'options': [ch('Pojdi naprej.', why='Koliko korakov? Robot bo hodil, dokler ne zadene stene.'),
                 ch('Pojdi tja, kjer so vrata.', why='Robot ne ve, kje je »tja«. To je preveč splošno.'),
                 ch('Pojdi 3 korake naprej.', True, 'Ukaz pove, kaj (pojdi), kam (naprej) in koliko (3).')],
     'hints': ['Natančen ukaz pove tudi KOLIKO.']},
    {'type': 'choose', 'title': 'Robot kuhar', 'intro': 'Robot dobi algoritem: <b>1. Vzemi kruh. 2. Namaži maslo.</b> Kaj bo šlo narobe?',
     'options': [ch('Nič, algoritem je popoln.', why='Robot ne ve, s čim naj maže in kam. Morda bo namazal mizo!'),
                 ch('Manjka, s čim naj maže in kam (z nožem, na kruh).', True, 'Tako je. Ljudje si manjkajoče dodamo sami, računalnik pa ne.'),
                 ch('Algoritem je predolg.', why='Ni predolg, prej prekratek: manjkajo podrobnosti.')],
     'hints': ['Pomisli: kje točno bo robot namazal maslo?']},
    info('Zapomni si', '''
<div class="box big">Če računalnik naredi nekaj narobe, je napaka (pravimo ji <b>hrošč</b> 🐞) skoraj vedno v <b>algoritmu</b>, ne v računalniku.</div>
<p>V naslednjem koraku boš sam/a pisal/a algoritem za robota.</p>'''),
], 'Veš, kaj je algoritem in kaj je dober algoritem.')

# ---------------- 3 Program za mrežo ----------------
L = [2, 3, 4, 5]
stran('3 Program za mrežo.html', 'Program za robota', [
    info('Robot riše po mreži', '''
<p class="big">Robot 🤖 stoji na polju <b>S</b> (levo zgoraj). Razume samo te ukaze:</p>
<div class="box big"><b>→ ← ↓ ↑</b> &nbsp;premakni se za 1 polje<br><b>■</b> &nbsp;pobarvaj polje, na katerem stojiš</div>
<p>Črtasta polja so tista, ki jih mora robot pobarvati. Ti sestaviš program, klikneš <b>▶ Zaženi</b> in pogledaš, kaj naredi.</p>'''),
    {'type': 'grid', 'title': 'Poskusi: samo zaženi', 'intro': 'Program je že napisan. Klikni <b>▶ Zaženi</b> in opazuj robota.',
     'n': 5, 'target': [[0, 0], [0, 1], [0, 2]], 'start': ['P', 'R', 'P', 'R', 'P'], 'locked': True, 'solution': ['P', 'R', 'P', 'R', 'P'],
     'win': '✅ Robot je pobarval, premaknil, pobarval, premaknil, pobarval. Točno po vrsti!'},
    {'type': 'grid', 'title': 'Stolpec', 'intro': 'Napiši program, ki pobarva 4 polja <b>navzdol</b>.',
     'n': 5, 'target': [[0, 0], [1, 0], [2, 0], [3, 0]], 'solution': ['P', 'D', 'P', 'D', 'P', 'D', 'P'],
     'hints': ['Začni z ■, ker robot že stoji na prvem polju.', 'Vzorec: ■ ↓ ■ ↓ … Zadnji ukaz je ■.']},
    {'type': 'grid', 'title': 'Črka L', 'intro': 'Pobarvaj obliko. Začni na S.',
     'n': 5, 'target': [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]], 'solution': ['P', 'D', 'P', 'D', 'P', 'R', 'P', 'R', 'P'],
     'hints': ['Najprej pojdi navzdol, nato desno.', '■ ↓ ■ ↓ ■ in potem še 2 × (→ ■).']},
    info('Zanka: ponovi', '''
<p class="big">Pri stolpcu si pisal/a <b>■ ↓ ■ ↓ ■ ↓ ■</b>. Ukaza <b>■ ↓</b> se ponavljata!</p>
<div class="box big"><span class="tk loop">ponovi 3× (</span> <span class="tk">■</span> <span class="tk">↓</span> <span class="tk loop">)</span> <span class="tk">■</span></div>
<p>To pomeni: 3-krat naredi »■ ↓«, nato še ■. Ponavljanju rečemo <b>zanka</b>.</p>
<p class="warn">Zanko vedno zapri z gumbom <b>)</b>. Vse med »ponovi (« in »)« se ponavlja.</p>'''),
    {'type': 'grid', 'title': 'Dolga vrsta, kratek program', 'intro': 'Pobarvaj 5 polj v vrsti. Uporabi <b>največ 5 ukazov</b>, zato potrebuješ zanko.',
     'n': 5, 'target': [[0, k] for k in range(5)], 'loops': L, 'max': 5, 'solution': ['N4', 'P', 'R', ')', 'P'],
     'hints': ['Kaj se ponavlja? ■ →', 'Če ponoviš »■ →« 5-krat, robot pade z mreže. Ponovi 4-krat, na koncu dodaj še ■.', 'Rešitev ima obliko: ponovi 4× ( ■ → ) ■']},
    {'type': 'grid', 'title': 'Stopnice', 'intro': 'Pobarvaj diagonalo. Uporabi <b>največ 6 ukazov</b>.',
     'n': 5, 'target': [[k, k] for k in range(4)], 'loops': L, 'max': 6, 'solution': ['N3', 'P', 'R', 'D', ')', 'P'],
     'hints': ['Na vsaki stopnici: pobarvaj, desno, dol.', 'ponovi 3× ( ■ → ↓ ) in na koncu še ■']},
    {'type': 'grid', 'title': '🐞 Najdi hrošča', 'intro': 'Ta program bi moral narisati diagonalo s 3 polji. Zaženi ga, poglej, kaj gre narobe, in ga popravi.',
     'n': 5, 'target': [[0, 0], [1, 1], [2, 2]], 'start': ['P', 'R', 'D', 'P', 'D', 'P'], 'solution': ['P', 'R', 'D', 'P', 'R', 'D', 'P'],
     'hints': ['Po prvem ■ gre robot → in ↓. Kaj naredi po drugem ■?', 'Po drugem ■ manjka →. Briši zadnja dva ukaza in napiši → ↓ ■.']},
    {'type': 'grid', 'stars': '★★', 'optional': True, 'title': 'Okvir', 'intro': 'Pobarvaj rob kvadrata 3 × 3 (8 polj, sredina ostane prazna). Največ <b>16 ukazov</b>.',
     'n': 5, 'target': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0]], 'loops': L, 'max': 16,
     'solution': ['N2', 'P', 'R', ')', 'N2', 'P', 'D', ')', 'N2', 'P', 'L', ')', 'N2', 'P', 'U', ')'],
     'hints': ['Okvir ima 4 stranice. Vsaka je ena zanka.', 'Desno: ponovi 2× ( ■ → ). Nato enako navzdol, levo in gor.']},
], 'Znaš napisati algoritem za robota, ga skrajšati z zanko in najti hrošča.')

# ---------------- 4 Diagram poteka ----------------
stran('4 Diagram poteka.html', 'Diagram poteka', [
    info('Algoritem kot slika', '''
<p class="big">Algoritem lahko narišemo. Taki sliki rečemo <b>diagram poteka</b>. Uporablja 4 znake:</p>
<p><span class="sym o">oval</span> začetek ali konec</p>
<p><span class="sym r">pravokotnik</span> ukaz: naredi nekaj</p>
<p><span class="sym d">romb</span> vprašanje z odgovorom <b>da</b> ali <b>ne</b></p>
<p><span class="sym" style="border:none;font-size:30px">➜</span> puščica: kam gremo naprej</p>'''),
    {'type': 'match', 'title': 'Poveži znak in pomen', 'pairs': [['oval', 'začetek ali konec'], ['pravokotnik', 'ukaz: naredi nekaj'], ['romb', 'vprašanje: da ali ne?'], ['puščica', 'kam gremo naprej']],
     'hints': ['Romb je edini, ki ima dva izhoda: da in ne.']},
    {'type': 'trace', 'title': 'Igra »Ugani število«: sledi s prstom', 'intro': 'Računalnik si je izmislil <b>40</b>. Ti ugibaš <b>65</b>. Klikaj like po vrsti, kot teče algoritem.',
     'path': [{'n': 'z'}, {'n': 'i'}, {'n': 'v'}, {'n': 'e', 'a': 'ne', 'q': 'Ali je 65 = 40?', 'why': '65 ni enako 40.'},
              {'n': 'l', 'a': 'ne', 'q': 'Ali je 65 < 40 (65 manjše od 40)?', 'why': '65 je večje od 40, zato odgovor ne.'}, {'n': 'm2'}],
     'win': 'Računalnik izpiše »Manj!«. Puščica te nato vrne na »Vprašaj«: to je zanka.',
     'hints': ['Sledi puščici, ki gre iz zelenega lika.', 'Pri rombu najprej odgovori da ali ne, potem klikni lik na koncu te puščice.']},
    {'type': 'trace', 'title': 'Še enkrat: zadetek!', 'intro': 'Skrito število je še vedno <b>40</b>. Zdaj ugibaš <b>40</b>. Začnemo pri »Vprašaj«.',
     'path': [{'n': 'v'}, {'n': 'e', 'a': 'da', 'q': 'Ali je 40 = 40?', 'why': '40 je enako 40.'}, {'n': 'b'}, {'n': 'k'}],
     'win': 'Bravo! Algoritem se konča. Dober algoritem se vedno konča.',
     'hints': ['Pri »da« gre puščica desno.']},
    {'type': 'choose', 'title': 'Kaj izpiše računalnik?', 'intro': 'Skrito število je <b>40</b>. Ugibaš <b>12</b>. Kaj izpiše računalnik?',
     'options': [ch('Več!', True, '12 je manjše od 40, zato mora biti naslednji ugib večji.'), ch('Manj!', why='12 je MANJŠE od 40. Ali mora biti naslednji ugib manjši ali večji?'), ch('Bravo!', why='12 ni enako 40.')],
     'hints': ['Ali je 12 < 40?']},
    {'type': 'guess', 'title': 'Zdaj igraj ti', 'intro': 'Računalnik izvaja ta algoritem. Ugani njegovo število.', 'hints': ['Začni s 50. Če reče »Več!«, poskusi 75, če »Manj!«, poskusi 25.']},
], 'Znaš brati diagram poteka in razumeš, kako deluje igra Ugani število.')

# ---------------- 5 Zapis v zvezek ----------------
stran('5 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek.', 'html': f'''
<div class="zapis"><h3>ZAPIS ALGORITMA</h3>
<p><b>Algoritem</b> je natančno zaporedje korakov, ki reši problem.</p>
<p>Dober algoritem: jasni koraki, pravi vrstni red, se konča.</p>
<p><b>Zanka</b>: ponovi 3 × ( ■ → ) je isto kot ■ → ■ → ■ →</p>
<p><b>Diagram poteka</b>: oval = začetek/konec, pravokotnik = ukaz, romb = vprašanje (da/ne).</p>
<p><b>Hrošč</b> 🐞 je napaka v algoritmu. Najdem ga tako, da program zaženem in pogledam, kje gre narobe.</p>
<p class="small">Nariši tudi diagram (lahko manjši):</p>
<img src="{slika('primer-diagram.png')}" alt="Diagram poteka Ugani število" style="width:340px;max-width:100%"></div>'''},
], 'Zapis je v zvezku.')

# ---------------- 7 Izziv: Najdi največje ----------------
stran('7 Izziv Najdi največje.html', '★★ Izziv: Najdi največje število', [
    info('Pravila igre', '''
<p class="big">Na mizi je kup kart s števili, obrnjenih navzdol.</p>
<div class="box big">Naenkrat smeš obrniti <b>samo eno karto</b>.<br>V glavi si smeš zapomniti <b>samo eno število</b>.</div>
<p>Kako najdeš največje število? Poskusi!</p>'''),
    {'type': 'cards', 'title': 'Igraj', 'n': 8, 'hints': ['Prvo karto si zapomni. Vsako naslednjo primerjaj s tisto v glavi.']},
    {'type': 'choose', 'title': 'Kateri algoritem je pravi?', 'intro': 'Kateri zapis natančno opiše, kar si delal/a?',
     'options': [ch('Poišči največjo karto.', why='To pove, KAJ hočemo, ne pa KAKO. To ni algoritem.'),
                 ch('Zapomni si prvo karto. Za vsako naslednjo: če je večja od tiste v glavi, si zapomni njo. Ko ni več kart, je v glavi največje.', True, 'To je algoritem: jasni koraki, zanka in pogoj.'),
                 ch('Obrni vse karte in poglej, katera je največja.', why='Pravila dovolijo obrniti samo eno karto naenkrat in si zapomniti eno število.')]},
    {'type': 'choose', 'stars': '★★★', 'title': 'Koliko primerjav?', 'intro': 'Koliko primerjav naredi ta algoritem pri <b>10</b> kartah?',
     'options': [ch('10', why='Prve karte ne primerjaš z ničemer, samo zapomniš si jo.'), ch('9', True, 'Pri n kartah naredi n - 1 primerjav.'), ch('20', why='Vsako karto primerjaš samo enkrat.')],
     'hints': ['Pri 8 kartah si naredil/a 7 primerjav.']},
], 'Rešil/a si izziv. Algoritem za iskanje največjega uporablja zanko in pogoj.')
