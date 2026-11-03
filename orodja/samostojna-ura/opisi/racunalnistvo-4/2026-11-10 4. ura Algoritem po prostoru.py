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
stran('3 Bobrckove naloge.html', 'Bobrčkove naloge', [
    info('Kaj je Bobrček?', '''
<p class="big"><b>Bobrček</b> je tekmovanje z ugankami za pametne glave. 🦫</p>
<div class="box big">Pri vsaki nalogi: <b>preberi počasi</b>, poglej sliko, šele nato klikni.</div>
<p>Zdaj boš rešil/a nekaj nalog, kakršne so na tekmovanju.</p>'''),
    {'type': 'choose', 'title': 'Kam pride bober?', 'intro': 'Bober 🦫 gre po ukazih: <b>→ → ↓</b>. Kje se ustavi?' + mreza([
        ['🦫', '', '🍎'], ['', '🌳', '🪵'], ['🌸', '', '']]),
     'options': [ch('pri 🪵', True, '→ → pride do 🍎, nato ↓ pride na 🪵.'),
                 ch('pri 🍎', why='Pri 🍎 je po dveh ukazih. Zadnji ukaz ↓ ga premakne še dol.'),
                 ch('pri 🌳', why='Do 🌳 bi prišel z → ↓. Ukazov je več.')],
     'hints': ['Pokaži s prstom na bobra in premikaj prst po vsakem ukazu.']},
    {'type': 'choose', 'title': 'Pot okoli drevesa', 'intro': 'Bober 🦫 hoče do 🪵. Skozi drevo 🌳 ne more. Kateri program je pravi?' + mreza([
        ['🦫', '🌳', '🪵'], ['', '', '']]),
     'options': [ch('↓ → → ↑', True, 'Bober gre dol, mimo drevesa in nazaj gor do debla.'),
                 ch('→ →', why='Prvi → ga pelje naravnost v drevo.'),
                 ch('↓ → →', why='Bober pride pod 🪵, manjka še ↑.')],
     'hints': ['Drevo je desno od bobra. Najprej se mu umakni.', 'Pri vsakem programu sledi s prstom.']},
    {'type': 'choose', 'title': 'Vzorec perlic', 'intro': 'Bobrica niza perlice po vzorcu:<p class="big">🔴 🟡 🟡 🔴 🟡 🟡 🔴 ❓</p>Katera perlica pride na mesto ❓?',
     'options': [ch('🟡', True, 'Vzorec je 🔴 🟡 🟡 in se ponavlja. Za 🔴 pride 🟡.'),
                 ch('🔴', why='Za vsako 🔴 prideta dve 🟡.'),
                 ch('🔵', why='Modre perlice v vzorcu sploh ni.')],
     'hints': ['Poišči del, ki se ponavlja.']},
    {'type': 'order', 'title': 'Prečkam cesto', 'intro': 'Tudi to je algoritem. Uredi korake po vrsti.',
     'items': ['Ustavim se ob robu ceste.', 'Pogledam levo.', 'Pogledam desno.', 'Še enkrat pogledam levo.', 'Ko je cesta prosta, grem čez.'],
     'hints': ['Najprej se ustaviš.', 'Čez cesto greš šele na koncu.']},
    {'type': 'choose', 'title': 'Na tekmovanju', 'intro': 'Na tekmovanju naloge ne znaš rešiti. Kaj narediš?',
     'options': [ch('Jo preskočim in se k njej vrnem na koncu.', True, 'Tako je. Najprej reši tiste, ki jih znaš.'),
                 ch('Vprašam soseda.', why='Na tekmovanju vsak rešuje sam.'),
                 ch('Ugasnem računalnik.', why='Potem ne moreš rešiti nobene naloge več.')],
     'hints': ['Pomisli, kako dobiš največ točk.']},
], 'Rešil/a si naloge v slogu Bobrčka.')

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
