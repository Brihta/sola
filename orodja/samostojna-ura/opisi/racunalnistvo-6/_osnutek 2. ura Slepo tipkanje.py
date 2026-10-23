# Računalništvo 6. r. (6. A), 2. ura »Uvodna ura slepega tipkanja« (23. 10. 2026).
LEG = '<p class="legend"><span class="f-lm">mezinec</span><span class="f-lp">prstanec</span><span class="f-ls">sredinec</span><span class="f-lk">kazalec</span><span class="f-pa">palec</span></p>'

# ---------------- 2 Izziv: koliko znaš ----------------
stran('2 Izziv koliko znas.html', 'Izziv: koliko znaš?', [
    info('Preden začnemo', '''
<p class="big">Najprej izmerimo, kako tipkaš <b>zdaj</b>, čisto po svoje.</p>
<div class="box big">Natipkaj vrstico, ki jo vidiš. Računalnik bo izmeril <b>natančnost</b> (koliko je pravilnih znakov) in <b>hitrost</b>.</div>
<p>Rezultat si zapomni. Na koncu ure ga boš primerjal/a s svojim novim.</p>'''),
    {'type': 'type', 'title': 'Tvoje izhodišče', 'intro': 'Natipkaj vrstico in pritisni <b>Enter</b>.',
     'text': 'mama in ata sta danes kuhala dober golaž', 'min': 0, 'save': True,
     'win': 'To je tvoje <b>izhodišče</b>. Zapiši si ga v zvezek, ko pride na vrsto zapis.',
     'hints': ['Tipkaj kakor znaš. Tu ni napačnega rezultata.']},
    {'type': 'choose', 'title': 'Kam si gledal/a?', 'intro': 'Bodi iskren/a: kam si največkrat gledal/a med tipkanjem?',
     'options': [ch('Na tipke.', True, 'Tako tipka večina. Danes se začneš učiti tipkati, ne da bi gledal/a tipke.'),
                 ch('Na zaslon.', True, 'Odlično. Ko gledaš zaslon, takoj opaziš napako.'),
                 ch('Malo tja, malo sem.', True, 'Ko oči skačejo med tipkami in zaslonom, se izgubiš in delaš napake. To bomo danes popravili.')]},
    {'type': 'choose', 'title': 'Zakaj slepo tipkanje?', 'intro': 'Slepo tipkanje pomeni: tipkam z <b>vsemi desetimi prsti</b> in <b>ne gledam tipk</b>. Kaj s tem pridobiš?',
     'options': [ch('Gledam zaslon, zato takoj vidim napako, in sčasoma tipkam hitreje.', True, 'Tako je. Hitrost pride sama, ko prsti vedo, kje so tipke.'),
                 ch('Tipkovnica se manj obrabi.', why='To ni razlog. Razlog si ti: manj napak in več hitrosti.'),
                 ch('Nič, z dvema prstoma je vedno hitreje.', why='Na začetku morda. Po nekaj tednih vaje so deset prstov veliko hitrejši od dveh.')],
     'hints': ['Pomisli, kam gledajo oči, ko ne gledajo tipk.']},
], 'Izmeril/a si svoje izhodišče.')

# ---------------- 3 Drza in osnovna vrsta ----------------
stran('3 Drza in osnovna vrsta.html', 'Drža in osnovna vrsta', [
    info('Pravilna drža', '''
<p class="big">Preden tipkaš, se pravilno usedi:</p>
<div class="box big">🪑 hrbet naslonjen, stopala na tleh<br>💪 komolca ob telesu, podlakti vodoravno<br>🖐️ zapestja ne ležijo na mizi, prsti so rahlo upognjeni<br>👀 zaslon je za iztegnjeno roko stran</div>
<p>Zdaj se tako usedi. Res, zdaj. 🙂</p>'''),
    {'type': 'choose', 'title': 'Kdo sedi prav?', 'intro': 'Kateri učenec sedi pravilno?',
     'options': [ch('Nika: sklonjena naprej, nos skoraj na zaslonu.', why='Tako hitro bolijo vrat in oči. Zaslon naj bo za iztegnjeno roko stran.'),
                 ch('Tim: zapestja ležijo na robu mize, prsti iztegnjeni.', why='Zapestja naj ne ležijo, prsti naj bodo rahlo upognjeni, kot bi držal žogico.'),
                 ch('Ana: hrbet naslonjen, stopala na tleh, prsti rahlo upognjeni.', True, 'Ana sedi pravilno. Tako lahko tipkaš dolgo in brez bolečin.')],
     'hints': ['Išči hrbet, stopala in prste.']},
    info('Osnovna vrsta', f'''
<p class="big">Vsak prst ima svojo <b>domačo tipko</b>. Tem tipkam rečemo <b>osnovna vrsta</b>:</p>
<div class="box big">levo: <b>A S D F</b> &nbsp;&nbsp; desno: <b>J K L Č</b> &nbsp;&nbsp; palca: <b>presledek</b></div>
<p>Na tipkah <b>F</b> in <b>J</b> je majhna <b>izboklina</b>. Tja položiš kazalca, ne da bi pogledal/a. Potipaj jo zdaj!</p>
{LEG}<p class="small">Barva tipke pove, kateri prst jo pritisne. Kazalca imata največ dela: vsak tudi tipko poleg (G in H).</p>'''),
    {'type': 'match', 'title': 'Kateri prst?', 'pairs': [['levi kazalec', 'F'], ['desni kazalec', 'J'], ['levi mezinec', 'A'], ['desni mezinec', 'Č'], ['palec', 'presledek']],
     'hints': ['Kazalca ležita na tipkah z izboklino.', 'Mezinca sta na koncu vrste: levo A, desno Č.']},
    {'type': 'choose', 'title': 'Brez gledanja', 'intro': 'Kako najdeš osnovno vrsto, ne da bi pogledal/a tipkovnico?',
     'options': [ch('S kazalcema potipam izboklini na F in J, ostali prsti se postavijo zraven.', True, 'Tako je. Izboklini sta tvoja kompasa.'),
                 ch('Hitro pogledam in nato ne gledam več.', why='Gre, ampak bolje je, da prste najdeš s tipom. Tako jih najdeš tudi sredi tipkanja.'),
                 ch('Dlani položim na sredino tipkovnice.', why='Sredina ni natančna. Domači tipki kazalcev sta F in J.')]},
    {'type': 'keys', 'title': 'Vaja: levi kazalec in desni kazalec', 'intro': 'Prste postavi na osnovno vrsto. Pritiskaj tipko, ki jo vidiš.',
     'keys': 'fj', 'n': 12, 'min': 80, 'win': 'Kazalca vesta, kje sta doma.',
     'hints': ['F pritisne levi kazalec, J desni.', 'Če se izgubiš, potipaj izboklini.']},
    {'type': 'keys', 'title': 'Vaja: cela osnovna vrsta', 'intro': 'Zdaj vseh 8 tipk. Glej <b>zaslon</b>, ne tipkovnice. Barva pove, kateri prst.',
     'keys': 'asdfjklč', 'n': 25, 'min': 85, 'win': 'Vseh osem prstov zna domov.',
     'hints': ['Prsti ostanejo na osnovni vrsti. Premakne se samo tisti, ki tipka, in se takoj vrne.', 'Ne hiti. Pri 85 % natančnosti lahko tudi kakšno zgrešiš.']},
], 'Znaš pravilno sedeti in najdeš osnovno vrsto brez gledanja.')

# ---------------- 4 Vaja osnovne vrste ----------------
stran('4 Vaja osnovne vrste.html', 'Vaja: osnovna vrsta', [
    info('Pokrij roke', '''
<p class="big">Zdaj boš tipkal/a cele vrstice.</p>
<div class="box big">🙈 Trik: čez roke položi <b>zvezek</b> (kot strešico), da tipk ne vidiš.</div>
<p class="warn">Natančnost je pomembnejša od hitrosti. Za vsako vrstico potrebuješ vsaj <b>90 %</b>. Hitrost pride kasneje sama.</p>'''),
    {'type': 'type', 'title': 'Vrstica 1', 'intro': 'Med skupinami je <b>presledek</b> (palec).', 'text': 'fff jjj fff jjj fjf jfj', 'min': 90,
     'hints': ['Levi kazalec F, desni J, palec presledek.']},
    {'type': 'type', 'title': 'Vrstica 2', 'text': 'asdf jklč asdf jklč fdsa čklj', 'min': 90,
     'hints': ['Vsak prst pritisne svojo tipko na osnovni vrsti.', 'Č je pod desnim mezincem.']},
    {'type': 'type', 'title': 'Vrstica 3: prave besede', 'intro': 'Te besede so samo iz osnovne vrste.', 'text': 'sad las lak kad dal', 'min': 90,
     'hints': ['Po vsaki besedi palec pritisne presledek.']},
    {'type': 'type', 'title': 'Vrstica 4: še G in H', 'intro': '<b>G</b> pritisne levi kazalec, <b>H</b> desni kazalec. Kazalec se premakne in se takoj vrne domov.',
     'text': 'glas hlad skala klada halja', 'min': 90,
     'hints': ['Po G se levi kazalec vrne na F, po H se desni vrne na J.']},
    {'type': 'type', 'title': 'Primerjaj z izhodiščem', 'intro': 'Isto vrstico kot na začetku ure. Tokrat z desetimi prsti in brez gledanja.',
     'text': 'mama in ata sta danes kuhala dober golaž', 'min': 70, 'compare': True,
     'win': 'Če si zdaj počasnejši/a kot na začetku, je to <b>normalno</b>: nov način je na začetku počasnejši. Po nekaj tednih bo hitrejši.',
     'hints': ['Ta vrstica ima tudi tipke izven osnovne vrste. Prst gre do tipke in se vrne domov.', 'Tu dovolj 70 %.']},
], 'Natipkal/a si cele vrstice z osnovne vrste.')

# ---------------- 5 Zapis v zvezek ----------------
stran('5 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek in dodal/a svoje izhodišče in cilj.', 'html': '''
<div class="zapis"><h3>SLEPO TIPKANJE</h3>
<p><b>Slepo tipkanje</b>: tipkam z desetimi prsti in gledam zaslon, ne tipk.</p>
<p><b>Drža</b>: hrbet naslonjen, stopala na tleh, zapestja ne ležijo, prsti rahlo upognjeni.</p>
<p><b>Osnovna vrsta</b>: levo A S D F, desno J K L Č, palca na presledku.</p>
<p>Na <b>F</b> in <b>J</b> je izboklina. Tam sta kazalca.</p>
<p>Prst pritisne tipko in se <b>vrne domov</b>.</p>
<p><b>Natančnost</b> je pomembnejša od hitrosti.</p>
<p>Moje izhodišče: ____ % natančnosti, ____ besed na minuto.<br>Moj cilj do konca leta: ____ % natančnosti.</p></div>
<p class="small">Izhodišče je rezultat iz 1. naloge (Izziv). Cilj si izberi sam/a, npr. 95 %.</p>'''},
], 'Zapis je v zvezku.')

# ---------------- 7 Izziv: velike črke ----------------
stran('7 Izziv velike crke.html', '★★ Izziv: velike črke in ločila', [
    info('Tipka Shift', '''
<p class="big">Veliko črko dobiš s tipko <b>Shift ⇧</b>.</p>
<div class="box big">Pravilo: Shift pritisne mezinec <b>druge roke</b>.<br>Veliki <b>J</b>: levi mezinec drži Shift, desni kazalec J.<br>Veliki <b>F</b>: desni mezinec drži Shift, levi kazalec F.</div>'''),
    {'type': 'choose', 'title': 'Kateri mezinec?', 'intro': 'Tipkaš veliki <b>A</b>. S katerim mezincem pritisneš Shift?',
     'options': [ch('Z desnim.', True, 'A tipka levi mezinec, zato Shift drži desni.'), ch('Z levim.', why='Levi mezinec že pritiska A. Shift drži mezinec druge roke.')]},
    {'type': 'type', 'title': 'Stavek 1', 'text': 'Ana ima lak. Saša ima sladko kašo.', 'min': 90,
     'hints': ['Piko tipka desni prstanec.', 'Š je desno od P, tipka jo desni mezinec.']},
    {'type': 'type', 'title': 'Stavek 2', 'stars': '★★★', 'text': 'Danes, ko je jasno, gremo na Kras.', 'min': 90,
     'hints': ['Vejico tipka desni sredinec.']},
], 'Znaš tipkati velike črke s Shiftom druge roke.')
