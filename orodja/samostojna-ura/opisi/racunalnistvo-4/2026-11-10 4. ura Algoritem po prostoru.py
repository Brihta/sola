# Računalništvo 4. razred, 4. ura »Algoritem po prostoru, naloge Bobrčka« (4. A, 10. 11. 2026).
# Učenci so stari 9 do 10 let: zelo kratke povedi, veliko slik, brez zank (zanka je pri Scratchu, 14. ura).
# Bobrčkove naloge so izvirne, v slogu tekmovanja (ne prepisane naloge ACM Bober).

def mreza(vrstice):
    """Mreža iz emojijev (spani, ker je uvod v odstavku <p>); prazno polje je ''."""
    st = len(vrstice[0])
    celice = ''.join(f'<span style="display:flex;align-items:center;justify-content:center;width:52px;height:52px;border:2px solid #9aa;font-size:30px">{x}</span>'
                     for r in vrstice for x in r)
    return f'<br><span style="display:inline-grid;grid-template-columns:repeat({st},52px);gap:0;margin:10px 0">{celice}</span><br>'


# ---------------- 2 Robot na mreži ----------------
stran('2 Robot na mrezi.html', 'Robot na mreži', [
    info('Ti si robot', '''
<p class="big">Robot dela <b>točno to</b>, kar mu rečeš. Nič več.</p>
<div class="box big">Sedi na stolu in naredi po vrsti:<br>
1. Dvigni desno roko. ✋<br>2. Ploskni 2-krat. 👏👏<br>3. Obrni glavo v levo. 👈<br>4. Spusti roko.</div>
<p>Bravo! Bil/a si robot. Ukazom po vrsti rečemo <b>algoritem</b>.</p>'''),
    info('Ukazi za robota', '''
<p class="big">Robot 🤖 stoji na polju <b>S</b> (levo zgoraj). Razume samo te ukaze:</p>
<div class="box big"><b>→</b> desno &nbsp; <b>←</b> levo &nbsp; <b>↓</b> dol &nbsp; <b>↑</b> gor<br><b>■</b> pobarvaj polje, na katerem stojiš</div>
<p>Črtasta polja mora robot pobarvati. Ti klikaš ukaze, nato <b>▶ Zaženi</b>.</p>'''),
    {'type': 'grid', 'title': 'Poglej robota', 'intro': 'Program je že napisan. Klikni <b>▶ Zaženi</b> in glej robota.',
     'n': 4, 'target': [[0, 2]], 'start': ['R', 'R', 'P'], 'solution': ['R', 'R', 'P'], 'locked': True,
     'win': '✅ Robot je šel 2-krat desno in pobarval polje.'},
    {'type': 'grid', 'title': 'Navzdol', 'intro': 'Pobarvaj črtasto polje. Robot mora iti <b>dol</b>.',
     'n': 4, 'target': [[2, 0]], 'solution': ['D', 'D', 'P'],
     'hints': ['Preštej, za koliko polj mora robot dol.', 'Klikni ↓ ↓ in nato ■.']},
    {'type': 'grid', 'title': 'Dol in desno', 'intro': 'Pobarvaj črtasto polje.',
     'n': 4, 'target': [[2, 1]], 'solution': ['D', 'D', 'R', 'P'],
     'hints': ['Robot gre najprej dol, nato desno.', '↓ ↓ → ■']},
    {'type': 'grid', 'title': 'Tri polja v vrsti', 'intro': 'Pobarvaj vsa 3 črtasta polja.',
     'n': 4, 'target': [[0, 0], [0, 1], [0, 2]], 'solution': ['P', 'R', 'P', 'R', 'P'],
     'hints': ['Robot že stoji na prvem polju. Začni z ■.', '■ → ■ → ■']},
    {'type': 'grid', 'title': 'Črka L', 'intro': 'Pobarvaj obliko črke L.',
     'n': 4, 'target': [[0, 0], [1, 0], [2, 0], [2, 1]], 'solution': ['P', 'D', 'P', 'D', 'P', 'R', 'P'],
     'hints': ['Najprej barvaj navzdol, nato še eno polje desno.', '■ ↓ ■ ↓ ■ → ■']},
    {'type': 'grid', 'title': '🐞 Najdi hrošča', 'intro': 'Napaki v programu rečemo <b>hrošč</b>. Ta program bi moral pobarvati 3 polja navzdol. Zaženi ga in ga popravi.',
     'n': 4, 'target': [[0, 0], [1, 0], [2, 0]], 'start': ['P', 'D', 'P', 'R', 'P'], 'solution': ['P', 'D', 'P', 'D', 'P'],
     'hints': ['Glej robota: kam gre po drugem ■?', 'Namesto → mora biti ↓. Briši zadnja dva ukaza in dodaj ↓ ■.']},
    {'type': 'grid', 'stars': '★★', 'optional': True, 'title': 'Kvadrat', 'intro': 'Pobarvaj kvadrat iz 4 polj. Potrebuješ tudi ←.',
     'n': 4, 'target': [[0, 0], [0, 1], [1, 1], [1, 0]], 'solution': ['P', 'R', 'P', 'D', 'P', 'L', 'P'],
     'hints': ['Pojdi okoli: desno, dol, levo.', '■ → ■ ↓ ■ ← ■']},
], 'Znaš napisati algoritem za robota in najti hrošča.')

# ---------------- 3 Bobrckove naloge ----------------
stran('3 Bobrckove naloge.html', 'Vaja za Bobrček: A, B, C ali D?', [
    info('Kaj je Bobrček?', '''
<p class="big"><b>Bobrček</b> je tekmovanje z ugankami za pametne glave. 🦫</p>
<div class="box big">Pri vsaki nalogi: <b>preberi počasi</b>, poglej sliko, nato izberi <b>A, B, C ali D</b>.</div>
<p>Naloge so take, kot so na tekmovanju. Pomagaj si s prstom na zaslonu.</p>'''),
    {'type': 'choose', 'abcd': True, 'title': '1. Kam pride bober?', 'intro': 'Bober 🦫 gre po ukazih: <b>→ → ↓</b>. Kje se ustavi?' + mreza([
        ['🦫', '', '🍎'], ['', '🌳', '🪵'], ['🌸', '', '']]),
     'options': [ch('pri 🍎', why='Pri 🍎 je po dveh ukazih. Zadnji ukaz ↓ ga premakne še dol.'),
                 ch('pri 🌳', why='Do 🌳 bi prišel z → ↓. Ukazov je več.'),
                 ch('pri 🪵', True, '→ → pride do 🍎, nato ↓ pride na 🪵.'),
                 ch('pri 🌸', why='🌸 je levo spodaj. Bober pa gre najprej desno.')],
     'hints': ['Pokaži s prstom na bobra in premikaj prst po vsakem ukazu.']},
    {'type': 'choose', 'abcd': True, 'title': '2. Pot okoli drevesa', 'intro': 'Bober 🦫 hoče do 🪵. Skozi drevo 🌳 ne more. Kateri program je pravi?' + mreza([
        ['🦫', '🌳', '🪵'], ['', '', '']]),
     'options': [ch('→ →', why='Prvi → ga pelje naravnost v drevo.'),
                 ch('↓ → →', why='Bober pride pod 🪵, manjka še ↑.'),
                 ch('↓ → → ↑', True, 'Bober gre dol, mimo drevesa in nazaj gor do debla.'),
                 ch('→ ↓ → ↑', why='Prvi → ga pelje v drevo.')],
     'hints': ['Drevo je desno od bobra. Najprej se mu umakni.', 'Pri vsakem programu sledi s prstom.']},
    {'type': 'choose', 'abcd': True, 'title': '3. Robot pobira sladoled', 'intro': 'Robot 🤖 mora pobrati 🍓 in 🍫. Vsaka puščica je en pritisk na gumb. Najmanj koliko pritiskov potrebuje?' + mreza([
        ['🤖', '', '🍓'], ['', '', ''], ['', '', '🍫']]),
     'options': [ch('3', why='Samo do 🍓 potrebuje že 2 pritiska, do 🍫 pa še 2.'),
                 ch('4', True, '→ → do 🍓, nato ↓ ↓ do 🍫. Skupaj 4.'),
                 ch('5', why='Gre tudi s 4: → → ↓ ↓.'),
                 ch('6', why='To je ovinek. Najkrajša pot je → → ↓ ↓.')],
     'hints': ['Najprej pojdi do 🍓. Koliko puščic?', 'Od 🍓 do 🍫 gre robot samo dol.']},
    {'type': 'choose', 'abcd': True, 'title': '4. Čarobna roža', 'intro': 'Vsako noč se roža spremeni:<p class="big">🌷 → 🌻 → 🌹 → 🌷 → …</p>Danes je 🌷. Kakšna bo čez <b>4 noči</b>?',
     'options': [ch('🌷', why='Čez 3 noči je spet 🌷. Preštej še eno noč.'),
                 ch('🌻', True, '1. noč 🌻, 2. noč 🌹, 3. noč 🌷, 4. noč 🌻.'),
                 ch('🌹', why='🌹 je čez 2 noči.'),
                 ch('🌼', why='Te rože v vrsti sploh ni.')],
     'hints': ['Štej s prsti: 1. noč, 2. noč, 3. noč, 4. noč.']},
    {'type': 'choose', 'abcd': True, 'title': '5. Darilo za bobra', 'intro': 'Bober želi žogo, ki je <b>velika</b>, ima <b>črte</b> in <b>ni rdeča</b>. Katero mu kupimo?',
     'options': [ch('velika, rdeča, s črtami', why='Ta je rdeča, bober pa ne mara rdeče.'),
                 ch('majhna, modra, s črtami', why='Ta je majhna, bober želi veliko.'),
                 ch('velika, modra, s pikami', why='Ta ima pike, ne črt.'),
                 ch('velika, modra, s črtami', True, 'Velika, s črtami in ni rdeča. Vsi trije pogoji držijo.')],
     'hints': ['Preveri vse tri pogoje pri vsaki žogi. Če en ne drži, žoga odpade.']},
    {'type': 'choose', 'abcd': True, 'title': '6. Ana briše risbo', 'intro': 'Ana riše po vrsti: 1. glavo ⚪, 2. oči 👀, 3. usta 👄, 4. lase. Nato <b>2-krat</b> klikne <b>Razveljavi</b> (vsak klik izbriše zadnjo potezo). Kaj ostane?',
     'options': [ch('samo glava', why='To bi ostalo po 3 klikih.'),
                 ch('glava in oči', True, 'Prvi klik izbriše lase, drugi usta. Ostaneta glava in oči.'),
                 ch('glava, oči in usta', why='To bi ostalo po samo 1 kliku.'),
                 ch('nič', why='Za to bi morala klikniti 4-krat.')],
     'hints': ['Razveljavi briše od zadaj: najprej tisto, kar je narisala zadnje.']},
    {'type': 'choose', 'abcd': True, 'stars': '★★', 'optional': True, 'title': '7. Igrače na traku', 'intro': 'Na traku so igrače:<p class="big">🧸 🚗 ⚽ 🎈</p>Mia <b>prvo vzame</b>, <b>naslednjo preskoči</b> (ta gre na konec traku), naslednjo vzame, naslednjo preskoči … Katera igrača ostane zadnja?',
     'options': [ch('🧸', why='🧸 Mia vzame takoj na začetku.'),
                 ch('🚗', why='🚗 gre najprej na konec, a Mia jo vzame v tretjem krogu.'),
                 ch('⚽', why='⚽ vzame v drugem krogu.'),
                 ch('🎈', True, 'Vzame 🧸, 🚗 na konec. Vzame ⚽, 🎈 na konec. Vzame 🚗. Ostane 🎈.')],
     'hints': ['Nariši si igrače na list in jih prečrtuj.', 'Po prvem koraku je trak: ⚽ 🎈 🚗.']},
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
<div class="zapis"><h3>ALGORITEM</h3>
<p><b>Algoritem</b> so natančni ukazi, ki si sledijo po vrsti.</p>
<p>Ukazi za robota: → desno, ← levo, ↓ dol, ↑ gor, ■ pobarvaj</p>
<p><b>Hrošč</b> 🐞 je napaka v programu.</p>
<p class="small">Nariši mrežo 3 × 3 in na njej pot robota: ■ → ■ ↓ ■</p></div>'''},
], 'Zapis je v zvezku.')

# ---------------- 6 Izziv ----------------
stran('6 Izziv Kaca.html', '★★ Izziv: Kača', [
    {'type': 'grid', 'title': 'Kača', 'intro': 'Pobarvaj kačo. Robot ne sme pobarvati nobenega drugega polja.',
     'n': 4, 'target': [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [2, 2], [2, 1], [2, 0]],
     'solution': ['P', 'R', 'P', 'R', 'P', 'R', 'P', 'D', 'P', 'D', 'P', 'L', 'P', 'L', 'P', 'L', 'P'],
     'hints': ['Kača gre desno, dol in nazaj levo.', 'Po vsakem premiku pobarvaj: ■ → ■ → ■ → ■, nato ↓ ■ ↓ ■, nato ← ■ ← ■ ← ■.']},
    {'type': 'grid', 'stars': '★★★', 'title': 'Črka U', 'intro': 'Pobarvaj črko U.',
     'n': 4, 'target': [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [1, 2], [0, 2]],
     'solution': ['P', 'D', 'P', 'D', 'P', 'R', 'P', 'R', 'P', 'U', 'P', 'U', 'P'],
     'hints': ['Dol, desno, gor.', '■ ↓ ■ ↓ ■ → ■ → ■ ↑ ■ ↑ ■']},
], 'Rešil/a si izziv!')
