# Računalništvo (racunalnistvo-6): vaje za Bober doma (objavljeno 13. 11. 2026, petek z izleti 6. in 7. r, vaje za vikend).
# Izvirne naloge v slogu Bobra in prave naloge prejšnjih let v vadnici za goste (ID-ji kot pri 8. uri 6-9).
# Skupne izvirne vaje za Bober (6. in 7. r), vstavljene v opisa za racunalnistvo-6 in racunalnistvo-6-9.
NALOGE = [
    info('Vadimo za Bober 🦫', '''
<p class="big">To so <b>nove</b> naloge v slogu Bobra. Rešuješ jih lahko tudi doma.</p>
<div class="box">Klikni odgovor. Če je narobe, ti stran pove zakaj. Če ne veš, kako začeti, klikni Namig.</div>
<p class="small">Pomagaš si lahko s papirjem in svinčnikom.</p>'''),
    {'type': 'choose', 'abcd': True, 'title': '1. Bobrova pisava', 'intro': 'Bober vsako črko zamenja z <b>naslednjo</b> v abecedi (A postane B, B postane C …). Tako iz BOBER nastane CPCFS.<p class="big">Kaj pomeni <b>SFLB</b>?</p><p class="small">Abeceda brez šumnikov: A B C D E F G H I J K L M N O P R S T U V Z</p>',
     'options': [ch('REKA', True, 'S → R, F → E, L → K, B → A.'),
                 ch('TGMC', why='Tu si vsako črko še enkrat premaknil/a naprej. Pri odkodiranju greš nazaj.'),
                 ch('RAKE', why='Črke so prave, a v napačnem vrstnem redu.'),
                 ch('SEKA', why='Prva črka S ni odkodirana. Črka pred S je R.')],
     'hints': ['Za odkodiranje vzemi črko, ki je v abecedi <b>pred</b> dano.', 'Pred S je R, pred F je E.']},
    {'type': 'choose', 'abcd': True, 'title': '2. Kup krožnikov', 'intro': 'Bober zloži krožnike enega na drugega: najprej A, nato B, C in D (D je na vrhu). Nato:<br>1. z vrha vzame <b>2</b> krožnika,<br>2. na vrh položi krožnik <b>E</b>,<br>3. z vrha vzame <b>1</b> krožnik.<br>Kateri krožnik je zdaj na vrhu?',
     'options': [ch('B', True, 'A B C D → vzame D in C → A B → doda E → A B E → vzame E → A B. Na vrhu je B.'),
                 ch('E', why='E je na vrh položil, a ga je v 3. koraku spet vzel.'),
                 ch('C', why='C je vzel že v 1. koraku.'),
                 ch('A', why='A je na dnu, nad njim je še B.')],
     'hints': ['Jemlje se vedno z vrha. Napiši kup: A B C D in prečrtuj.']},
    {'type': 'choose', 'abcd': True, 'title': '3. Lučke', 'intro': 'Bober ima 4 lučke. Vsaka prižgana lučka šteje svojo vrednost:<p class="big">8 &nbsp; 4 &nbsp; 2 &nbsp; 1<br>💡 ⚫ 💡 💡</p>(💡 prižgana, ⚫ ugasnjena) Katero število kažejo lučke?',
     'options': [ch('11', True, '8 + 2 + 1 = 11. Lučka s 4 je ugasnjena.'),
                 ch('13', why='13 = 8 + 4 + 1. Lučka s 4 pa je ugasnjena.'),
                 ch('1011', why='Tako se lučke zapišejo (1 prižgana, 0 ugasnjena), vprašanje pa je, katero število pomenijo.'),
                 ch('3', why='Sešteti moraš vrednosti prižganih lučk, ne prešteti lučk.')],
     'hints': ['Seštej vrednosti nad prižganimi lučkami.']},
    {'type': 'choose', 'abcd': True, 'title': '4. Najkrajša pot', 'intro': 'Med jezovi so poti. Številka pove, koliko minut traja pot:<div class="box">A do B: 2 &nbsp;|&nbsp; A do C: 4 &nbsp;|&nbsp; B do C: 1<br>B do D: 5 &nbsp;|&nbsp; C do D: 1</div>Najmanj koliko minut potrebuje bober od A do D?',
     'options': [ch('4', True, 'A → B → C → D: 2 + 1 + 1 = 4.'),
                 ch('5', why='A → C → D traja 5. Obstaja hitrejša pot čez B.'),
                 ch('7', why='A → B → D traja 7. Poskusi še čez C.'),
                 ch('3', why='Ni poti, ki bi trajala 3. Preveri vse poti od A do D.')],
     'hints': ['Napiši vse poti od A do D in vsaki seštej minute.', 'Poskusi tudi pot A → B → C → D.']},
    {'type': 'choose', 'abcd': True, 'title': '5. Stroj za števila', 'intro': 'Stroj vsako število spremeni po pravilu:<div class="box">Če je število <b>sodo</b>, ga deli z 2.<br>Če je <b>liho</b>, mu prištej 1.</div>Vanj vstavimo <b>7</b> in ga poženemo <b>3-krat</b>. Kaj dobimo?',
     'options': [ch('2', True, '7 je liho → 8. 8 je sodo → 4. 4 je sodo → 2.'),
                 ch('4', why='To je po 2 korakih. Je še en korak.'),
                 ch('1', why='To bi bilo po 4 korakih.'),
                 ch('3', why='7 je liho, zato mu prišteješ 1 (dobiš 8), ne deliš ga.')],
     'hints': ['Pojdi korak za korakom in vsakič preveri, ali je število sodo ali liho.']},
    {'type': 'choose', 'abcd': True, 'title': '6. Menjave', 'intro': 'Trije bobri stojijo v vrsti po številkah:<p class="big">3 &nbsp; 1 &nbsp; 2</p>V enem koraku se lahko zamenjata samo <b>soseda</b>. Najmanj koliko korakov je potrebnih, da stojijo <b>1 2 3</b>?',
     'options': [ch('1', why='Z eno menjavo dobiš 1 3 2 ali 3 2 1. Nobeno ni urejeno.'),
                 ch('2', True, '3 1 2 → 1 3 2 → 1 2 3.'),
                 ch('3', why='Gre tudi z dvema: najprej zamenjaj 3 in 1, nato 3 in 2.'),
                 ch('0', why='Vrsta ni urejena, 3 stoji spredaj.')],
     'hints': ['Trojka mora priti na konec. Vsak korak jo premakne za eno mesto.']},
]

stran('2 Bobrove vaje.html', 'Vaje za Bober: A, B, C ali D?', NALOGE, 'Rešil/a si nove vaje za Bober! 🦫')

VADNICA = 'https://bober.acm.si/simple/guest/compete/'
def gumb(url, besedilo):
    return (f'<a href="{url}" target="_blank" rel="noopener" style="display:inline-block;padding:6px 12px;'
            f'border-radius:8px;background:#e8f1ff;border:2px solid #4a7bd0;color:#1d3f7a;font-weight:700;'
            f'text-decoration:none;margin:2px">{besedilo} ↗</a>')

stran('3 Naloge prejsnjih let.html', 'Prave naloge prejšnjih let', [
    {'type': 'check', 'title': 'Reši prave Bobrove naloge', 'label': 'Rešil/a sem vsaj eno leto in kliknil/a Zaključi.', 'html': '''
<div class="box">1️⃣ Klikni leto. Odpre se nov zavihek.<br>
2️⃣ Če se pokaže obrazec: vpiši samo ime, priimek <b>Vaja</b>, datum 1. 1., kodo pusti <b>prazno</b>.<br>
3️⃣ Imaš 40 minut, tako kot na tekmovanju. Med reševanjem ne izveš, ali je odgovor pravilen.<br>
4️⃣ Na koncu klikni <b>Zaključi</b> in poglej, katere naloge so bile pravilne.</div>
<p><b>6. in 7. razred:</b><br>''' + gumb(VADNICA + '532/', '2025/26') + gumb(VADNICA + '492/', '2024/25') + '''</p>
<p class="small">Si že rešil/a obe leti? Reši ju še enkrat: naloge pridejo v drugem vrstnem redu.</p>'''},
], 'Treniral/a si na pravih nalogah. Srečno na tekmovanju! 🦫')
