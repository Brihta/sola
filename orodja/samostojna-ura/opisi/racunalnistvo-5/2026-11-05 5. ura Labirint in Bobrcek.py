# Računalništvo 5. razred, 5. ura »Algoritem in zanka, vaja za Bobrček« (5. B, 5. 11. 2026).
# LDN: Blockly Games, programiranje labirinta (sklop 2 Algoritmi in Bobrček). Labirint na blockly.games je
# zunanja stran brez preverjanja, zato je osnovna pot na mreži z robotom (zaporedje, zanka, hrošč),
# Blockly Labirint pa je izziv za kvizom. Bobrčkove naloge so izvirne, v slogu tekmovanja (ne prepisane).

L = [2, 3, 4]


def mreza(vrstice):
    """Mreža iz emojijev; prazno polje je ''."""
    st = len(vrstice[0])
    celice = ''.join(f'<span style="display:flex;align-items:center;justify-content:center;width:52px;height:52px;border:2px solid #9aa;font-size:30px">{x}</span>'
                     for r in vrstice for x in r)
    return f'<br><span style="display:inline-grid;grid-template-columns:repeat({st},52px);gap:0;margin:10px 0">{celice}</span><br>'


# ---------------- 2 Robot v labirintu ----------------
stran('2 Robot na mrezi.html', 'Robot na mreži', [
    info('Robot dela točno to, kar mu rečeš', '''
<p class="big">Robot 🤖 ne razmišlja. Naredi <b>točno</b> tiste ukaze, ki mu jih daš, <b>po vrsti</b>.</p>
<div class="box big"><b>→</b> desno &nbsp; <b>←</b> levo &nbsp; <b>↓</b> dol &nbsp; <b>↑</b> gor<br><b>■</b> pobarvaj polje, na katerem stojiš</div>
<p>Robot začne na polju <b>S</b>. Črtasta polja mora pobarvati. Ti sestaviš program, nato klikneš <b>▶ Zaženi</b>.</p>'''),
    {'type': 'grid', 'title': 'Poskusi: samo zaženi', 'intro': 'Program je že napisan. Klikni <b>▶ Zaženi</b> in opazuj robota.',
     'n': 5, 'target': [[0, 0], [0, 1], [1, 1]], 'start': ['P', 'R', 'P', 'D', 'P'], 'locked': True, 'solution': ['P', 'R', 'P', 'D', 'P'],
     'win': '✅ Pobarvaj, desno, pobarvaj, dol, pobarvaj. Točno po vrsti! Ukazom po vrsti rečemo <b>algoritem</b>.'},
    {'type': 'grid', 'title': 'Stolpec', 'intro': 'Napiši program, ki pobarva 4 polja <b>navzdol</b>.',
     'n': 5, 'target': [[0, 0], [1, 0], [2, 0], [3, 0]], 'solution': ['P', 'D', 'P', 'D', 'P', 'D', 'P'],
     'hints': ['Robot že stoji na prvem polju. Začni z ■.', 'Vzorec: ■ ↓ ■ ↓ … Zadnji ukaz je ■.']},
    {'type': 'grid', 'title': 'Ovinek', 'intro': 'Pobarvaj obliko. Začni na S.',
     'n': 5, 'target': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]], 'solution': ['P', 'R', 'P', 'R', 'P', 'D', 'P', 'D', 'P'],
     'hints': ['Najprej desno, nato dol.', '■ → ■ → ■, nato še 2 × (↓ ■).']},
    info('Zanka: ponovi', '''
<p class="big">Pri stolpcu si pisal/a <b>■ ↓ ■ ↓ ■ ↓ ■</b>. Ukaza <b>■ ↓</b> se ponavljata!</p>
<div class="box big"><span class="tk loop">ponovi 3× (</span> <span class="tk">■</span> <span class="tk">↓</span> <span class="tk loop">)</span> <span class="tk">■</span></div>
<p>To pomeni: 3-krat naredi »■ ↓«, nato še ■. Ponavljanju rečemo <b>zanka</b>.</p>
<p class="warn">Zanko vedno zapri z gumbom <b>)</b>. Vse med »ponovi (« in »)« se ponavlja.</p>'''),
    {'type': 'grid', 'title': 'Poskusi zanko', 'intro': 'Ta program ima zanko. Klikni <b>▶ Zaženi</b> in štej, kolikokrat robot naredi »■ →«.',
     'n': 5, 'target': [[0, 0], [0, 1], [0, 2], [0, 3]], 'start': ['N3', 'P', 'R', ')', 'P'], 'locked': True, 'loops': L,
     'solution': ['N3', 'P', 'R', ')', 'P'],
     'win': '✅ Robot je 3-krat naredil »■ →« in na koncu še ■. Program ima samo 5 ukazov, pobarval pa je 4 polja.'},
    {'type': 'grid', 'title': 'Dolg stolpec, kratek program', 'intro': 'Pobarvaj 5 polj navzdol. Uporabi <b>največ 5 ukazov</b>, zato potrebuješ zanko.',
     'n': 5, 'target': [[k, 0] for k in range(5)], 'loops': L + [5], 'max': 5, 'solution': ['N4', 'P', 'D', ')', 'P'],
     'hints': ['Kaj se ponavlja? ■ ↓', 'Če ponoviš »■ ↓« 5-krat, robot pade z mreže. Ponovi 4-krat, na koncu dodaj še ■.', 'ponovi 4× ( ■ ↓ ) ■']},
    {'type': 'grid', 'title': 'Stopnice', 'intro': 'Pobarvaj stopnice. Uporabi <b>največ 6 ukazov</b>.',
     'n': 5, 'target': [[k, k] for k in range(4)], 'loops': L, 'max': 6, 'solution': ['N3', 'P', 'R', 'D', ')', 'P'],
     'hints': ['Na vsaki stopnici: pobarvaj, desno, dol.', 'ponovi 3× ( ■ → ↓ ) in na koncu še ■']},
    {'type': 'grid', 'title': '🐞 Najdi hrošča', 'intro': 'Napaki v programu rečemo <b>hrošč</b>. Ta program bi moral pobarvati 4 polja v vrsti. Zaženi ga, poglej, kaj gre narobe, in ga popravi.',
     'n': 5, 'target': [[0, 0], [0, 1], [0, 2], [0, 3]], 'start': ['N2', 'P', 'R', ')', 'P'], 'loops': L,
     'solution': ['N3', 'P', 'R', ')', 'P'],
     'hints': ['Preštej pobarvana polja. Koliko jih manjka?', 'Zanka se ponovi premalokrat. Klikni Pobriši vse in napiši: ponovi 3× ( ■ → ) ■']},
    {'type': 'grid', 'stars': '★★', 'optional': True, 'title': 'Okvir', 'intro': 'Pobarvaj rob kvadrata 3 × 3 (8 polj, sredina ostane prazna). Največ <b>16 ukazov</b>.',
     'n': 5, 'target': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0]], 'loops': L, 'max': 16,
     'solution': ['N2', 'P', 'R', ')', 'N2', 'P', 'D', ')', 'N2', 'P', 'L', ')', 'N2', 'P', 'U', ')'],
     'hints': ['Okvir ima 4 stranice. Vsaka je ena zanka.', 'Desno: ponovi 2× ( ■ → ). Nato enako navzdol, levo in gor.']},
], 'Znaš napisati algoritem, ga skrajšati z zanko in najti hrošča.')

# ---------------- 3 Bobrckove naloge ----------------
stran('3 Bobrckove naloge.html', 'Vaja za Bobrček: A, B, C ali D?', [
    info('Kaj je Bobrček?', '''
<p class="big"><b>Bobrček</b> je tekmovanje z ugankami za računalniško razmišljanje. 🦫 Šolsko tekmovanje je ta mesec.</p>
<div class="box big">Pri vsaki nalogi: <b>preberi počasi</b>, poglej sliko, nato izberi <b>A, B, C ali D</b>.</div>
<div class="box">👆 Klikni odgovor. Če je narobe, ti stran pove, <b>zakaj</b>. Preberi in poskusi znova.<br>💡 Če ne veš, kako začeti, klikni <b>Namig</b>.</div>'''),
    {'type': 'choose', 'abcd': True, 'title': '1. Kam pride bober?', 'intro': 'Bober 🦫 gre po ukazih: <b>→ ↓ ↓ ←</b>. Kje se ustavi?' + mreza([
        ['🦫', '🍎', ''], ['🌳', '', '🪵'], ['🌸', '🍄', '']]),
     'options': [ch('pri 🌳', why='Do 🌳 bi prišel samo z ↓. Bober gre najprej desno.'),
                 ch('pri 🍄', why='Pri 🍄 je po ukazih → ↓ ↓. Zadnji ukaz ← ga premakne še levo.'),
                 ch('pri 🌸', True, '→ do 🍎, ↓ ↓ do 🍄, ← do 🌸.'),
                 ch('pri 🪵', why='Bober nikoli ne gre 2-krat desno, do 🪵 ne pride.')],
     'hints': ['Pokaži s prstom na bobra in premikaj prst po vsakem ukazu.']},
    {'type': 'choose', 'abcd': True, 'title': '2. Kratek program', 'intro': 'Kateri program nariše <b>enako</b> kot ■ → ■ → ■ → ■ ?',
     'options': [ch('ponovi 4× ( ■ → )', why='Na koncu robot naredi še en →, ki ga v prvotnem programu ni.'),
                 ch('ponovi 3× ( ■ → ) ■', True, '3-krat »■ →« in nato še ■. Točno enako kot dolgi program.'),
                 ch('ponovi 3× ( → ■ )', why='Ta začne s premikom, zato prvo polje ostane nepobarvano.'),
                 ch('ponovi 4× ( ■ )', why='Robot se nikamor ne premakne, 4-krat pobarva isto polje.')],
     'hints': ['Zapiši vsak program na dolgo, brez zanke, in ga primerjaj.']},
    {'type': 'choose', 'abcd': True, 'title': '3. Čarobni kamenčki', 'intro': 'Vsako jutro se kamenček spremeni:<p class="big">🔴 → 🟡 → 🟢 → 🔵 → 🔴 → …</p>Danes je 🔴. Kakšen bo čez <b>10 jutr</b>?',
     'options': [ch('🔴', why='🔴 je čez 4 in čez 8 jutr. Štej naprej od 8.'),
                 ch('🟡', why='🟡 je čez 1, 5 in 9 jutr.'),
                 ch('🟢', True, 'Vsaka 4 jutra je spet 🔴 (4, 8). Čez 9 je 🟡, čez 10 🟢.'),
                 ch('🔵', why='🔵 je čez 3, 7 in 11 jutr.')],
     'hints': ['Kdaj je kamenček spet 🔴? Čez 4 jutra.', 'Čez 8 jutr je 🔴. Štej še 2.']},
    {'type': 'choose', 'abcd': True, 'title': '4. Darilo za bobra', 'intro': 'Bober želi nahrbtnik, ki je <b>moder</b>, ima <b>2 žepa</b> in <b>ni težak</b>. Katerega mu kupimo?',
     'options': [ch('moder, 3 žepi, lahek', why='Ta ima 3 žepe, bober želi 2.'),
                 ch('zelen, 2 žepa, lahek', why='Ta je zelen, bober želi modrega.'),
                 ch('moder, 2 žepa, lahek', True, 'Moder, 2 žepa in ni težak. Vsi trije pogoji držijo.'),
                 ch('moder, 2 žepa, težak', why='Ta je težak, bober pa želi lahkega.')],
     'hints': ['Pri vsakem nahrbtniku preveri vse tri pogoje. Če en ne drži, odpade.']},
    {'type': 'choose', 'abcd': True, 'title': '5. Skladovnica knjig', 'intro': 'Maja na mizo zlaga knjige eno na drugo: najprej 📕, nato 📗, nato 📘. Nato <b>vzame 2 knjigi z vrha</b> in položi še 📙. Katera knjiga je zdaj <b>spodaj</b> in katera <b>na vrhu</b>?',
     'options': [ch('spodaj 📕, na vrhu 📙', True, 'Vzame 📘 in 📗. Ostane 📕, nanjo položi 📙.'),
                 ch('spodaj 📕, na vrhu 📘', why='📘 je bila na vrhu, zato jo Maja vzame prvo.'),
                 ch('spodaj 📙, na vrhu 📕', why='Novo knjigo položi na vrh, ne spodaj.'),
                 ch('spodaj 📗, na vrhu 📙', why='📗 je bila nad 📕, zato jo Maja vzame.')],
     'hints': ['Z vrha jemlješ tisto, kar si položil/a zadnje.', 'Nariši si knjige eno na drugo in jih prečrtuj.']},
    {'type': 'choose', 'abcd': True, 'title': '6. Najkrajša pot', 'intro': 'Robot 🤖 mora do 🔋. Skozi kamen 🪨 ne more. Najmanj koliko korakov (puščic) potrebuje?' + mreza([
        ['🤖', '🪨', ''], ['', '🪨', ''], ['', '', '🔋']]),
     'options': [ch('2', why='Z 2 koraki ne pride niti mimo kamnov.'),
                 ch('3', why='Do 🔋 sta 2 polji dol in 2 polji desno. To so vsaj 4 koraki.'),
                 ch('4', True, '↓ ↓ → → . Robot gre okoli kamnov spodaj.'),
                 ch('6', why='Gre krajše: ↓ ↓ → →.')],
     'hints': ['Kamni so desno od robota. Pojdi najprej dol.', 'Preštej: koliko dol, koliko desno?']},
    {'type': 'choose', 'abcd': True, 'stars': '★★', 'optional': True, 'title': '7. Skrivna koda', 'intro': 'Bobri pišejo skrivna sporočila tako, da vsako črko zamenjajo z <b>naslednjo</b> v abecedi (A → B, B → C …). Sporočilo <b>MJT</b> je zakodirano. Kaj pomeni?',
     'options': [ch('NKU', why='To je MJT, zakodiran še enkrat. Ti moraš iti nazaj.'),
                 ch('LIS', True, 'Vsako črko premakni eno nazaj: M → L, J → I, T → S.'),
                 ch('MJT', why='Sporočilo je zakodirano, zato ni enako.'),
                 ch('LIT', why='T premakni še eno nazaj: T → S.')],
     'hints': ['Za odkodiranje vsako črko premakni eno <b>nazaj</b> v abecedi.', 'Pred M je L.']},
    {'type': 'choose', 'abcd': True, 'title': '8. Na tekmovanju', 'intro': 'Na tekmovanju naloge ne znaš rešiti. Kaj narediš?',
     'options': [ch('Vprašam soseda.', why='Na tekmovanju vsak rešuje sam.'),
                 ch('Jo preskočim in se k njej vrnem na koncu.', True, 'Tako je. Najprej reši tiste, ki jih znaš.'),
                 ch('Neham reševati.', why='Potem ne dobiš točk pri nalogah, ki jih znaš.'),
                 ch('Obkrožim vse odgovore.', why='Tako je odgovor zagotovo napačen.')],
     'hints': ['Pomisli, kako dobiš največ točk.']},
], 'Rešil/a si vajo za Bobrček.')

# ---------------- 4 Zapis v zvezek ----------------
stran('4 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek.', 'html': '''
<div class="zapis"><h3>ALGORITEM IN ZANKA</h3>
<p><b>Algoritem</b> so natančni ukazi, ki si sledijo po vrsti.</p>
<p><b>Zanka</b> ukaze ponavlja: ponovi 3× ( ■ → ) ■ je enako kot ■ → ■ → ■ → ■</p>
<p><b>Hrošč</b> 🐞 je napaka v programu. Najdemo ga tako, da program zaženemo in opazujemo.</p>
<p class="small">Nariši mrežo 4 × 4 in na njej pot programa: ponovi 3× ( ■ ↓ ) ■</p></div>'''},
], 'Zapis je v zvezku.')
