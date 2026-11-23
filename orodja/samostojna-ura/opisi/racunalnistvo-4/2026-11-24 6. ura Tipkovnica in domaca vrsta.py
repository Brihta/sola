# Računalništvo 4. razred, 6. ura »Razporeditev tipk, položaj rok, domača vrsta« (4. B, 24. 11. 2026).
# Učenci so stari 9 do 10 let: zelo kratke povedi, veliko emojijev, mala števila nalog.
# Tipkovnica: slovenska razporeditev (Č desno od L).

TIPKE = '''<div class="box" style="font:20px/1.9 monospace;text-align:center">
<span style="opacity:.55">Q W E R T Z U I O P Š</span><br>
<b>A S D <u>F</u> G H <u>J</u> K L Č</b><br>
<span style="opacity:.55">Y X C V B N M</span><br>
<span style="display:inline-block;border:2px solid #9aa;border-radius:8px;padding:0 70px">presledek</span></div>'''

# ---------------- 2 Spoznaj tipkovnico ----------------
stran('2 Spoznaj tipkovnico.html', 'Spoznaj tipkovnico', [
    info('Poglej svojo tipkovnico', '''
<p class="big">Na tipkovnici so <b>črke</b>, <b>številke</b> in <b>posebne tipke</b>. ⌨️</p>
<div class="box big">Črke niso po abecedi. 🤔<br>Pomembne so, kje so <b>prsti</b>.</div>
<p>Poišči na svoji tipkovnici tipko <b>A</b>. Nato poišči <b>L</b>.</p>'''),
    {'type': 'choose', 'title': 'Velika tipka spodaj', 'intro': '''<div>Najdaljša tipka je spodaj na sredini. Kaj naredi?</div>
<p class="small">Klikni odgovor. Če je narobe, ti stran pove zakaj. Če ne veš, kako začeti, klikni Namig.</p>''',
     'options': [ch('Naredi presledek med besedama.', True, 'Tako je. To je presledek. Tipkaš ga s palcem. 👍'),
                 ch('Izbriše črko.', why='Za brisanje je tipka zgoraj desno, s puščico ←.'),
                 ch('Ugasne računalnik.', why='Ne. S tipkovnico ne ugašamo računalnika.')],
     'hints': ['Pritisni jo v mislih med besedama »dober dan«.']},
    {'type': 'match', 'title': 'Kaj naredi tipka?', 'pairs': [
        ['presledek', 'prazen prostor med besedama'],
        ['Enter ↵', 'nova vrstica'],
        ['Backspace ←', 'izbriše črko levo'],
        ['Shift ⇧', 'velika črka']],
     'hints': ['Enter je velika tipka desno, v obliki puščice ↵.', 'Shift držiš in hkrati pritisneš črko.']},
    {'type': 'choose', 'title': 'Kje je Č?', 'intro': '<div>Poišči na svoji tipkovnici črko <b>L</b>. Kaj je desno od nje?</div>',
     'options': [ch('Č', True, 'Na slovenski tipkovnici je Č desno od L.'),
                 ch('K', why='K je levo od L. Poglej na drugo stran.'),
                 ch('M', why='M je v spodnji vrsti.')],
     'hints': ['Prst položi na L in se premakni za eno tipko desno.']},
], 'Poznaš tipkovnico in posebne tipke.')

# ---------------- 3 Prsti domov ----------------
stran('3 Prsti domov.html', 'Prsti gredo domov', [
    info('Domača vrsta', f'''
<p class="big">Prsti imajo svoj <b>dom</b>. 🏠</p>
{TIPKE}
<div class="box big">👆 Na <b>F</b> in <b>J</b> sta izboklini. Potipaj ju!<br>👉 Tam sta kazalca.</div>'''),
    info('Vseh osem prstov', '''
<div class="box big">🖐️ Leva roka: <b>A S D F</b><br>🖐️ Desna roka: <b>J K L Č</b><br>👍 Palca: na presledku</div>
<p class="big">Pravilno sedi:</p>
<div class="box big">🪑 hrbet naravnost<br>🦶 stopala na tleh<br>👀 gledaš <b>zaslon</b>, ne tipk</div>
<p>Postavi prste domov. Nato klikni Naslednja naloga.</p>'''),
    {'type': 'keys', 'title': 'Kazalca', 'intro': 'Pritisni tipko, ki je označena. Kazalca: <b>F</b> in <b>J</b>.',
     'keys': 'fj', 'n': 10, 'min': 80, 'win': 'Kazalca znata! 👏',
     'hints': ['Levi kazalec pritisne F, desni kazalec J.', 'Potipaj izboklini, ne glej dol.']},
    {'type': 'keys', 'title': 'Sredinca', 'intro': 'Zdaj sredinca: <b>D</b> in <b>K</b>.',
     'keys': 'dk', 'n': 10, 'min': 80, 'win': 'Sredinca znata! 👏',
     'hints': ['D je levo od F, K je desno od J.']},
    {'type': 'keys', 'title': 'Prstanca in mezinca', 'intro': 'Zdaj <b>S L</b> (prstanca) in <b>A Č</b> (mezinca).',
     'keys': 'slač', 'n': 12, 'min': 80, 'win': 'Vsi prsti so doma! 🏠',
     'hints': ['Mezinca sta na robu: A levo, Č desno.', 'Po vsaki tipki se prst vrne domov.']},
    {'type': 'keys', 'title': 'Vsa domača vrsta', 'intro': 'Vse tipke domače vrste, premešane. Glej <b>zaslon</b>.',
     'keys': 'asdfjklč', 'n': 16, 'min': 80, 'win': 'Bravo! Poznaš domačo vrsto. ⭐',
     'hints': ['Ne hiti. 80 % pomeni, da smeš kakšno zgrešiti.', 'Če se izgubiš, potipaj F in J.']},
], 'Prsti poznajo svoj dom.')

# ---------------- 4 Prve besede ----------------
stran('4 Prve besede.html', 'Prve besede', [
    info('Besede iz domače vrste', '''
<p class="big">Iz črk domače vrste lahko sestaviš <b>besede</b>! 🎉</p>
<div class="box big">las &nbsp; sad &nbsp; dal &nbsp; laj</div>
<p>Presledek pritisneš s palcem. Na koncu pritisni <b>Enter</b>.</p>'''),
    {'type': 'type', 'title': 'Dve besedi', 'intro': 'Natipkaj in pritisni <b>Enter</b>.',
     'text': 'las sad', 'min': 80,
     'hints': ['Med besedama je presledek. Pritisni ga s palcem.']},
    {'type': 'type', 'title': 'Tri besede', 'intro': 'Malo daljše. Ne hiti.',
     'text': 'laj dal kad', 'min': 80,
     'hints': ['J je desni kazalec, K desni sredinec.']},
    {'type': 'type', 'stars': '★★', 'optional': True, 'title': 'Cela vrstica', 'intro': 'Za tiste, ki želijo več.',
     'text': 'sad las kal dal laj skala', 'min': 80,
     'hints': ['Oči na zaslon. Prsti vedo, kje so tipke.']},
], 'Natipkal/a si prve besede.')

# ---------------- 5 Zapis v zvezek ----------------
stran('5 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek.', 'html': '''
<div class="zapis"><h3>TIPKOVNICA</h3>
<p><b>Domača vrsta</b>: A S D F &nbsp; J K L Č</p>
<p>Na <b>F</b> in <b>J</b> sta izboklini. Tam sta kazalca.</p>
<p>Palca sta na <b>presledku</b>.</p>
<p>Gledam <b>zaslon</b>, ne tipk.</p>
<p class="small">Nariši svoji roki in pod vsak prst napiši njegovo tipko.</p></div>'''},
], 'Zapis je v zvezku.')

# ---------------- 7 Izziv ----------------
stran('7 Izziv G in H.html', '★★ Izziv: G in H', [
    info('Kazalca se iztegneta', '''
<p class="big"><b>G</b> in <b>H</b> sta na sredini.</p>
<div class="box big">Levi kazalec skoči z F na <b>G</b> in nazaj.<br>Desni kazalec skoči z J na <b>H</b> in nazaj.</div>'''),
    {'type': 'keys', 'title': 'G in H', 'intro': 'Pritiskaj označeno tipko.', 'keys': 'fgjh', 'n': 16, 'min': 80,
     'win': 'Kazalca sta skočila in se vrnila. 🦘',
     'hints': ['Po G se kazalec vrne na F, po H na J.']},
    {'type': 'type', 'stars': '★★★', 'title': 'Besede z G in H', 'intro': 'Natipkaj in pritisni <b>Enter</b>.',
     'text': 'glas hlad gad hala', 'min': 80,
     'hints': ['G je levi kazalec, H desni kazalec.']},
], 'Rešil/a si izziv!')
