# Računalništvo 3. razred, tehniški dan 6. 11. 2026: »Simetrija na mreži«.
# Nadomesti ure simetrije pri matematiki (3. r): navpična in vodoravna os, barve.
# Učenci so stari 8 do 9 let: ena misel na poved, veliko slik.
# Vsaka rešena naloga se shrani za učiteljevo poročilo (izdelki, supabase_izdelki.sql).
#
# Zgradi: python3 zgradi.py "opisi/racunalnistvo-3/2026-11-06 Tehniski dan Simetrija.py" "../../gradiva/racunalnistvo-3/2026-11-06 Tehniški dan"

BARVA = {'R': '#ef4444', 'Y': '#facc15', 'G': '#22c55e', 'B': '#3b82f6', 'C': '#1f2937', 'O': '#fb923c'}


def mini(vrstice, os=None):
    """Majhna slika na mreži (cela slika); os = 'v', 'h' ali None. Iz <span>, ker je lahko v odstavku."""
    st = len(vrstice[0])
    cel = ''.join(f'<span style="background:{BARVA.get(x, "#fff")}"></span>' for r in vrstice for x in r)
    crta = '<span class="os"></span>' if os else ''
    return f'<span class="mini {os or ""}" style="grid-template-columns:repeat({st},22px)">{cel}{crta}</span>'


def cela_v(pol):
    return [v + v[::-1] for v in pol]


def cela_h(pol):
    return pol + pol[::-1]


METULJ = ['...C..', '....C.', '.RR..C', 'RYYR.C', 'RYBYRC', 'RYYRRC', '.RRR.C', '.RYR.C', '..RR.C']

stran('4 Simetrija.html', 'Simetrija', [
    info('Kaj je simetrija?', f'''
<p class="big">Poglej metulja. 🦋 Rdeča črta ga razdeli na dva dela.</p>
<p>{mini(cela_v(METULJ), 'v')}</p>
<div class="box big">Levi del je <b>enak</b> desnemu, le obrnjen. Kot v ogledalu. 🪞<br>
Taki sliki rečemo <b>simetrična</b>. Črta je <b>os simetrije</b>.</div>'''),

    {'type': 'zrcali', 'demo': True, 'title': 'Poglej, kako dela zrcalo',
     'intro': '<div>Klikni <b>▶ Poglej, kako</b>. Glej, kam gre vsak kvadratek.</div>',
     'os': 'v', 'pol': ['....', '..RR', '.RRR', '..RR', '....']},

    {'type': 'choose', 'title': 'Katera slika je simetrična?',
     'intro': '<div>Klikni sliko, kjer sta oba dela pri rdeči črti <b>enaka</b>. Če je narobe, ti stran pove zakaj.</div>',
     'options': [ch(mini(cela_v(['..GG', '.GGG', 'GG.G', '...G']), 'v'), True, 'Levi del je kot v ogledalu desni.'),
                 ch(mini(['..GG..G.', '.GGG.GG.', 'GG.G.G..', '...G....'], 'v'), why='Desni del je drugačen od levega. Poglej spodnjo vrsto.'),
                 ch(mini(['GGG.....', 'GGG.....', '........', '........'], 'v'), why='Na desni strani ni ničesar. Desni del bi moral biti enak levemu.')],
     'hints': ['Primerjaj kvadratke tik ob rdeči črti: levo in desno morata biti enaka.']},

    {'type': 'choose', 'title': 'Kje je os simetrije?',
     'intro': f'<div>Poglej hišico. Na kateri sliki je rdeča črta <b>os simetrije</b>?</div>',
     'options': [ch(mini(cela_v(['...R', '..RR', '.RRR', '.YYY', '.YGY', '.YYG']), 'v'), True, 'Levi del hiše je enak desnemu.'),
                 ch(mini(cela_v(['...R', '..RR', '.RRR', '.YYY', '.YGY', '.YYG']), 'h'), why='Zgoraj je streha, spodaj zid. Zgornji del ni enak spodnjemu.')],
     'hints': ['Prepogni hišico v mislih. Kje se oba dela pokrijeta?']},

    info('Zdaj rišeš ti', '''
<p class="big">Na eni strani črte je lik. Ti ga narišeš na <b>drugi strani</b>, kot v ogledalu.</p>
<div class="box big">👆 Klikni kvadratek: pobarva se.<br>👆 Še en klik: pobriše se.<br>✔ Ko končaš, klikni <b>Preveri</b>.</div>
<p>Naloge so vedno malo težje. Zadnja je pravi izziv! 💪</p>'''),

    # 1. stopnja: navpična os, ena barva, lik se dotika osi
    {'type': 'zrcali', 'id': 'n1', 'title': '1. Zastavica', 'intro': '<div>Nariši drugo polovico na desni strani črte.</div>',
     'os': 'v', 'pol': ['....', '..RR', '.RRR', '..RR', '...R', '....'],
     'win': 'Bravo! Kvadratki ob črti imajo par tudi ob črti.'},
    {'type': 'zrcali', 'id': 'n2', 'title': '2. Smrekica', 'intro': '<div>Nariši drugo polovico smrekice.</div>',
     'os': 'v', 'pol': ['...G', '..GG', '...G', '.GGG', 'GGGG', '...G']},

    # 2. stopnja: lik ni ob osi, šteti je treba kvadratke
    {'type': 'zrcali', 'id': 'n3', 'title': '3. Daleč od črte', 'intro': '<div>Lik se <b>ne dotika</b> črte. Preštej, koliko praznih kvadratkov je vmes.</div>',
     'os': 'v', 'pol': ['.....', '.BB..', '.B...', '.BBB.', '.B...', '.....'],
     'win': 'Super! Med likom in črto sta na obeh straneh 2 prazna kvadratka.'},

    # 3. stopnja: vodoravna os
    info('Črta je lahko tudi ležeča', f'''
<p class="big">Os simetrije je lahko tudi <b>vodoravna</b>. Takrat je zrcalo kot gladina jezera. 🏞️</p>
<p>{mini(cela_h(['...BB...', '..BBBB..', '.BB..BB.', 'BB....BB']), 'h')}</p>
<p class="big">Kar je zgoraj, je tudi spodaj. Rišeš <b>pod</b> črto.</p>'''),
    {'type': 'zrcali', 'id': 'h1', 'title': '4. Gladina jezera', 'intro': '<div>Nariši spodnjo polovico, pod črto.</div>',
     'os': 'h', 'pol': ['...GG...', '..GGGG..', '.GG..GG.', 'GG....GG']},
    {'type': 'zrcali', 'id': 'h2', 'title': '5. Gore', 'intro': '<div>Lik se ne dotika črte. Preštej kvadratke do črte.</div>',
     'os': 'h', 'pol': ['...B....', '..BBB..B', '.BBBBBBB', '........'],
     'win': 'Odlično! Gore se zrcalijo v jezeru.'},

    # 4. stopnja: dve barvi, lik na desni (risanje na levo)
    {'type': 'zrcali', 'id': 'b2', 'title': '6. Dve barvi', 'intro': '<div>Zdaj je lik na <b>desni</b>. Riši na levi. Pazi na <b>barve</b>: najprej izberi barvo, nato klikaj.</div>',
     'os': 'v', 'obrni': True, 'pol': ['..R.', '.RYR', '..R.', '...G', '..GG', '...G'],
     'hints': ['Desno od črte je rožica. Na levi mora biti enaka, kot v ogledalu.',
               'Rumeni kvadratek je obdan z rdečimi. Tako mora biti tudi na levi.',
               'Steblo (zeleno) se dotika črte. Njegov par se je tudi dotika.']},

    # 5. stopnja: tri barve
    {'type': 'zrcali', 'id': 'b3', 'title': '7. Hiša v treh barvah', 'intro': '<div>Uporabi <b>rdečo, rumeno in zeleno</b>. Vsak par ima isto barvo.</div>',
     'os': 'v', 'pol': ['....R', '...RR', '..RRR', '.RRRR', '.YYYY', '.YGYY', '.YYYG']},
    {'type': 'zrcali', 'id': 'b3h', 'title': '8. Barvni vzorec', 'intro': '<div>Os je vodoravna. Nariši vzorec pod črto, z enakimi barvami.</div>',
     'os': 'h', 'pol': ['Y......Y', '.R....R.', '..G..G..', '...RR...']},

    # 6. stopnja: podrobna slika
    {'type': 'zrcali', 'id': 'metulj', 'title': '9. Veliki metulj 🦋', 'stars': '★',
     'intro': '<div>Zadnja naloga: cel metulj v štirih barvah. Delaj vrsto za vrsto, od zgoraj navzdol.</div>',
     'os': 'v', 'pol': METULJ,
     'hints': ['Začni pri zgornji vrsti in pojdi navzdol.', 'Črno telo je ob črti. Pri vsaki vrsti najprej naredi telo.',
               'Preštej kvadratke od telesa navzven, barvo za barvo.']},

    {'type': 'check', 'title': 'V zvezek',
     'html': f'''<p class="big">V zvezek (karo) nariši ta lik in njegovo zrcalno sliko.</p>
<p>{mini(['..R.....', '.RR.....', 'RRR.....', '.YY.....', '..Y.....'], 'v')}</p>
<div class="box big">1. S svinčnikom in ravnilom nariši rdečo črto, to je os.<br>2. Na levi nariši lik.<br>3. Na desni ga nariši kot v ogledalu, z barvicami.</div>''',
     'label': 'Narisal/a sem v zvezek.'},

    {'type': 'zrcali', 'id': 'moj', 'prosto': True, 'stars': '★★', 'optional': True, 'title': 'Ustvari svojo simetrično sliko',
     'intro': '<div>Riši, kar želiš: metulja, robota, rožo. Zrcalo nariše drugo polovico samo! Ko končaš, klikni <b>Končal/a sem</b>.</div>',
     'w': 12, 'h': 10, 'os': 'v', 'barve': 'RYGBOP'},
], 'Znaš narisati simetrično sliko z navpično in vodoravno osjo.', izdelki='racunalnistvo-3/2026-11-06-simetrija')
