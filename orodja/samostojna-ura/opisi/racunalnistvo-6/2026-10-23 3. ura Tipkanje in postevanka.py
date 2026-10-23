# Računalništvo 6. r. (6. A), 3. ura »Slepo tipkanje; utrjevanje poštevanke« (23. 10. 2026).
LEG = '<p class="legend"><span class="f-lm">mezinec</span><span class="f-lp">prstanec</span><span class="f-ls">sredinec</span><span class="f-lk">kazalec</span><span class="f-pa">palec</span></p>'

# ---------------- 2 Ogrevanje: osnovna vrsta ----------------
stran('2 Ogrevanje osnovna vrsta.html', 'Ogrevanje: osnovna vrsta', [
    info('Se spomniš?', '''
<p class="big">Pri prejšnji uri si spoznal/a <b>osnovno vrsto</b>.</p>
<div class="box big">🪑 pravilno se usedi<br>👉 kazalca potipata izboklini na <b>F</b> in <b>J</b><br>🖐️ levo <b>A S D F</b>, desno <b>J K L Č</b>, palca na presledku<br>👀 gledaš zaslon, ne tipk</div>
<p>Postavi prste domov. Ko si pripravljen/a, klikni Naslednja naloga.</p>'''),
    {'type': 'type', 'title': 'Tvoje današnje izhodišče', 'intro': 'Natipkaj vrstico in pritisni <b>Enter</b>. Ne hiti.',
     'text': 'sad las lak kad dal glas hlad skala', 'min': 0, 'save': True,
     'win': 'To je tvoje izhodišče za danes. Na koncu ure ga primerjaš.',
     'hints': ['Tipkaj kakor znaš. Tu ni napačnega rezultata.']},
    {'type': 'keys', 'title': 'Hitri trening osnovne vrste', 'intro': 'Pritiskaj označeno tipko. Glej <b>zaslon</b>.',
     'keys': 'asdfghjklč', 'n': 20, 'min': 85, 'win': 'Prsti so ogreti.',
     'hints': ['Po vsaki tipki se prst vrne domov.', 'G in H tipkata kazalca: premakneta se in se vrneta.']},
], 'Prsti so ogreti in veš, kje je osnovna vrsta.')

# ---------------- 3 Številke ----------------
stran('3 Stevilke na tipkovnici.html', 'Številke na tipkovnici', [
    info('Številke so v zgornji vrsti', f'''
<p class="big">Za poštevanko rabiš številke. So v <b>najvišji vrsti</b> tipkovnice.</p>
<div class="box big">Prst iz osnovne vrste <b>se iztegne gor</b>, pritisne številko in <b>se vrne domov</b>.</div>
<p>levi mezinec <b>1</b>, levi prstanec <b>2</b>, levi sredinec <b>3</b>, levi kazalec <b>4 5</b><br>desni kazalec <b>6 7</b>, desni sredinec <b>8</b>, desni prstanec <b>9</b>, desni mezinec <b>0</b></p>
{LEG}'''),
    {'type': 'match', 'title': 'Kateri prst?', 'pairs': [['levi mezinec', '1'], ['levi kazalec', '4 in 5'], ['desni kazalec', '6 in 7'], ['desni sredinec', '8'], ['desni mezinec', '0']],
     'hints': ['Vsak prst gre naravnost gor od svoje domače tipke.', 'Kazalca imata po dve številki, ker imata tudi v osnovni vrsti po dve tipki.']},
    {'type': 'keys', 'title': 'Vaja: levica', 'intro': 'Številke 1 do 5 tipka <b>leva</b> roka.', 'keys': '12345', 'n': 15, 'min': 80, 'win': 'Levica zna številke.',
     'hints': ['1 je nad A, 2 nad S, 3 nad D, 4 in 5 nad F in G.']},
    {'type': 'keys', 'title': 'Vaja: desnica', 'intro': 'Številke 6 do 0 tipka <b>desna</b> roka.', 'keys': '67890', 'n': 15, 'min': 80, 'win': 'Desnica zna številke.',
     'hints': ['6 in 7 sta nad H in J, 8 nad K, 9 nad L, 0 nad Č.']},
    {'type': 'keys', 'title': 'Vaja: vse številke', 'intro': 'Zdaj vse premešane. Glej zaslon!', 'keys': '1234567890', 'n': 20, 'min': 85, 'win': 'Vseh deset številk brez gledanja!',
     'hints': ['Ne hiti. 85 % pomeni, da smeš kakšno zgrešiti.']},
], 'Znaš tipkati številke z ustreznimi prsti.')

# ---------------- 4 Postevanka ----------------
stran('4 Postevanka s tipkanjem.html', 'Poštevanka s tipkanjem', [
    info('Dve nalogi hkrati', '''
<p class="big">Zdaj boš računal/a in tipkal/a hkrati.</p>
<div class="box big">Na zaslonu je račun. Rezultat <b>natipkaj</b> s številkami zgoraj in pritisni <b>Enter</b>.</div>
<p class="warn">Številke tipkaj z zgornjo vrsto, <b>ne</b> s številčnico desno. Tako vadiš slepo tipkanje.</p>'''),
    {'type': 'times', 'title': 'Krog 1: poštevanka 2, 3, 4, 5', 'tables': [2, 3, 4, 5], 'n': 10, 'save': True,
     'win': 'Čas si zapomni. V krogu 3 ga boš poskusil/a premagati.',
     'hints': ['Če ne veš rezultata, ga izračunaj s seštevanjem: 4 · 3 = 4 + 4 + 4.']},
    {'type': 'times', 'title': 'Krog 2: poštevanka 6, 7, 8, 9', 'tables': [6, 7, 8, 9], 'n': 10,
     'hints': ['7 · 8 = 56 (5, 6, 7, 8 po vrsti!).', '9 · 6: 10 · 6 = 60, odštej 6, dobiš 54.']},
    {'type': 'times', 'title': 'Krog 3: premagaj svoj čas', 'intro': 'Spet poštevanka 2 do 5. Si hitrejši/a kot v krogu 1?', 'tables': [2, 3, 4, 5], 'n': 10, 'compare': True,
     'hints': ['Gledaj zaslon, ne tipk. Prsti že vedo, kje so številke.']},
    {'type': 'type', 'title': 'Primerjaj z izhodiščem', 'intro': 'Ista vrstica kot na začetku ure.', 'text': 'sad las lak kad dal glas hlad skala', 'min': 80, 'compare': True,
     'hints': ['Prsti domov, oči na zaslon.']},
], 'Računal/a si poštevanko in tipkal/a številke brez gledanja.')

# ---------------- 5 Zapis v zvezek ----------------
stran('5 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek in dodal/a svoje rezultate.', 'html': '''
<div class="zapis"><h3>ŠTEVILKE NA TIPKOVNICI</h3>
<p>Številke so v <b>zgornji vrsti</b>. Prst iz osnovne vrste se iztegne gor in se vrne domov.</p>
<p>Leva roka: <b>1 2 3 4 5</b> &nbsp; Desna roka: <b>6 7 8 9 0</b></p>
<p>Kazalca imata po dve številki: levi <b>4 5</b>, desni <b>6 7</b>.</p>
<p>Moj čas pri poštevanki: krog 1 ____ s, krog 3 ____ s.</p>
<p>Natančnost danes: na začetku ____ %, na koncu ____ %.</p></div>'''},
], 'Zapis je v zvezku.')

# ---------------- 7 Izziv ----------------
stran('7 Izziv vsa postevanka.html', '★★ Izziv: vsa poštevanka', [
    {'type': 'times', 'stars': '★★', 'title': '20 računov, vse poštevanke', 'tables': [2, 3, 4, 5, 6, 7, 8, 9, 10], 'n': 20,
     'win': 'Prava računska in tipkarska moč! 💪', 'hints': ['Ne hiti. Napaka vzame več časa kot počasen pravilen odgovor.']},
    {'type': 'type', 'stars': '★★★', 'title': 'Številke in besede', 'text': 'ana ima 12 jabolk, saša pa 34 sliv', 'min': 90,
     'hints': ['Vejico tipka desni sredinec.', 'Š je desno od P, tipka jo desni mezinec.']},
], 'Rešil/a si izziv.')
