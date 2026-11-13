# Računalništvo 4. razred: vaje za Bobrček doma (objavljeno 13. 11. 2026, za vikend pred šolskim tekmovanjem).
# Izvirne naloge v slogu Bobrčka (pravih nalog ne prepisujemo); prava pola je povezava (.url).

def mreza(vrstice):
    st = len(vrstice[0])
    celice = ''.join(f'<span style="display:flex;align-items:center;justify-content:center;width:52px;height:52px;border:2px solid #9aa;font-size:30px">{x}</span>'
                     for r in vrstice for x in r)
    return f'<br><span style="display:inline-grid;grid-template-columns:repeat({st},52px);gap:0;margin:10px 0">{celice}</span><br>'


stran('2 Bobrckove vaje.html', 'Vaje za Bobrček: A, B, C ali D?', [
    info('Vadimo za Bobrček 🦫', '''
<p class="big">Bobrček je tekmovanje z ugankami. To so <b>nove</b> vaje.</p>
<div class="box big">Pri vsaki nalogi <b>preberi počasi</b>, poglej sliko, nato izberi <b>A, B, C ali D</b>.</div>
<div class="box">👆 Klikni odgovor.<br>❌ Če je narobe, ti stran pove, <b>zakaj</b>.<br>💡 Če ne veš, kako začeti, klikni <b>Namig</b>.</div>'''),
    {'type': 'choose', 'abcd': True, 'title': '1. Kam pride bober?', 'intro': 'Bober 🦫 gre po ukazih: <b>↓ → →</b>. Kje se ustavi?' + mreza([
        ['🦫', '', '🍓'], ['🌸', '🍄', '🪵'], ['', '', '🍎']]),
     'options': [ch('pri 🍓', why='Do 🍓 bi prišel z → →. Prvi ukaz pa je ↓.'),
                 ch('pri 🍄', why='Pri 🍄 je po dveh ukazih. Je še en →.'),
                 ch('pri 🪵', True, '↓ pride do 🌸, → do 🍄, → do 🪵.'),
                 ch('pri 🍎', why='Do 🍎 bi potreboval še en ↓.')],
     'hints': ['Pokaži s prstom na bobra in ga premikaj po vsakem ukazu.']},
    {'type': 'choose', 'abcd': True, 'title': '2. Mimo kamna', 'intro': 'Bober 🦫 hoče do 🪵. Na kamen 🪨 ne sme stopiti. Kateri program je pravi?' + mreza([
        ['🦫', '', ''], ['', '🪨', ''], ['', '', '🪵']]),
     'options': [ch('→ ↓ ↓ →', why='Po → ↓ bober stoji na kamnu.'),
                 ch('↓ → → ↓', why='Po ↓ → bober stoji na kamnu.'),
                 ch('→ → ↓ ↓', True, 'Bober gre po zgornji vrsti do konca, nato dol do 🪵. Kamna se ne dotakne.'),
                 ch('↓ ↓ →', why='Bober pride do polja levo od 🪵. Manjka še en →.')],
     'hints': ['Kamen je na sredini. Bober mora iti okoli roba.', 'Sledi s prstom vsakemu programu.']},
    {'type': 'choose', 'abcd': True, 'title': '3. Vzorec', 'intro': 'Bober niza kroglice po vzorcu:<p class="big">🔴 🔵 🔵 🔴 🔵 🔵 🔴 ❓</p>Katera kroglica pride na mesto ❓?',
     'options': [ch('🔴', why='Po vsaki 🔴 prideta <b>dve</b> 🔵.'),
                 ch('🔵', True, 'Vzorec je 🔴 🔵 🔵. Po 🔴 pride 🔵.'),
                 ch('🟢', why='Zelene kroglice v vzorcu sploh ni.'),
                 ch('⚪', why='Bele kroglice v vzorcu sploh ni.')],
     'hints': ['Kateri del se ponavlja? Obkroži ga s prstom.']},
    {'type': 'choose', 'abcd': True, 'title': '4. Tehtnica', 'intro': '⚖️ 🍎 je <b>težje</b> od 🍐.<br>⚖️ 🍐 je <b>težja</b> od 🍋.<br>Kaj je <b>najlažje</b>?',
     'options': [ch('🍎', why='🍎 je težje od 🍐, zato ni najlažje.'),
                 ch('🍐', why='🍐 je težja od 🍋.'),
                 ch('🍋', True, '🍎 je težje od 🍐, 🍐 je težja od 🍋. Najlažja je 🍋.'),
                 ch('Tega ne moremo vedeti.', why='Lahko: postavi jih v vrsto od najtežjega do najlažjega.')],
     'hints': ['Postavi sadje v vrsto: najtežje, srednje, najlažje.']},
    {'type': 'choose', 'abcd': True, 'title': '5. Skrivna koda', 'intro': 'Bober ima skrivno kodo:<p class="big">🔺 = 1 &nbsp; 🟦 = 2 &nbsp; ⭐ = 3</p>Kaj pomeni <b>🟦 ⭐ 🔺</b>?',
     'options': [ch('123', why='To je 🔺 🟦 ⭐. Poglej vrstni red znakov.'),
                 ch('231', True, '🟦 = 2, ⭐ = 3, 🔺 = 1. Skupaj 231.'),
                 ch('321', why='To bi bilo ⭐ 🟦 🔺.'),
                 ch('213', why='To bi bilo 🟦 🔺 ⭐.')],
     'hints': ['Pojdi od leve proti desni in vsak znak zamenjaj s številko.']},
    {'type': 'choose', 'abcd': True, 'title': '6. V vrsti', 'intro': 'Trije bobri stojijo v vrsti.<br>Ana stoji <b>pred</b> Bojanom.<br>Cene stoji <b>za</b> Bojanom.<br>Kdo je <b>prvi</b>?',
     'options': [ch('Ana', True, 'Vrsta je: Ana, Bojan, Cene.'),
                 ch('Bojan', why='Pred Bojanom stoji Ana.'),
                 ch('Cene', why='Cene je za Bojanom, torej zadnji.'),
                 ch('Tega ne moremo vedeti.', why='Lahko: nariši tri kroge in vpiši imena.')],
     'hints': ['Nariši tri kroge v vrsto in vanje vpisuj imena.']},
    {'type': 'choose', 'abcd': True, 'stars': '★★', 'optional': True, 'title': '7. Tri jabolka', 'intro': 'Robot 🤖 mora pobrati vsa tri jabolka 🍎. Vsaka puščica je en pritisk. Najmanj koliko pritiskov potrebuje?' + mreza([
        ['🤖', '', '🍎'], ['', '', ''], ['🍎', '', '🍎']]),
     'options': [ch('4', why='Samo do prvega jabolka potrebuje 2 pritiska.'),
                 ch('5', why='Poskusi: → → do prvega, ↓ ↓ do drugega, ← ← do tretjega. Preštej.'),
                 ch('6', True, '→ → ↓ ↓ ← ←. Skupaj 6.'),
                 ch('8', why='Gre krajše: → → ↓ ↓ ← ←.')],
     'hints': ['Jabolka so v treh kotih. Pojdi od enega kota do drugega.', 'Od kota do kota sta vedno 2 pritiska.']},
], 'Rešil/a si vaje za Bobrček! 🦫')
