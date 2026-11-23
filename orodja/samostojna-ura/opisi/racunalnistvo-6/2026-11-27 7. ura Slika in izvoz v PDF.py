# Računalništvo 6. r. (6. A), 7. ura »Vstavljanje slike, izvoz v PDF« (27. 11. 2026).
# Nadaljuje 6. uro (dokument Savinjska dolina s slogi). Kdor dokumenta nima, ga na koraku 4 hitro naredi znova.
# Fotografija: Magdalena Šajinovićová, CC BY-SA 3.0, Wikimedia Commons (File:Humulus_lupulus_cones.jpg), pomanjšana.

HMELJ = slika('slike/hmelj.jpg')
VIR = 'Vir: Magdalena Šajinovićová, Wikimedia Commons, CC BY-SA 3.0'
VIR_HTML = ('Magdalena Šajinovićová, <a href="https://commons.wikimedia.org/wiki/File:Humulus_lupulus_cones.jpg" '
            'target="_blank" rel="noopener">Wikimedia Commons</a>, licenca CC BY-SA 3.0')

BESEDILO = '\n'.join([
    'Savinjska dolina',
    'Savinjska dolina leži ob reki Savinji, med Celjem in Logarsko dolino.',
    'Narava', 'Reka Savinja',
    'Savinja izvira nad Logarsko dolino in se pri Zidanem Mostu izlije v Savo.',
    'Kmetijstvo', 'Hmelj',
    'Hmelju pravijo zeleno zlato. Raste ob visokih žicah.',
    'Zgodovina', 'Rimska nekropola',
    'V Šempetru so ohranjeni rimski nagrobniki, stari skoraj 2000 let.'])
KOPIRAJ = f'''<textarea id="besedilo" rows="6" readonly style="width:100%;font:15px/1.4 Calibri,Arial,sans-serif;padding:8px;border:2px solid #b9c6d3;border-radius:10px">{BESEDILO}</textarea>
<p><button class="btn go2" onclick="var t=document.getElementById('besedilo');t.focus();t.select();var ok=false;try{{ok=document.execCommand('copy')}}catch(e){{}}this.textContent=ok?'✅ Kopirano':'Besedilo je označeno: pritisni Ctrl + C'">📋 Kopiraj besedilo</button></p>'''


def stran_a4(vsebina):
    return f'<div style="flex:1 1 230px;border:1px solid #bbb;background:#fff;padding:10px 12px;font-size:13px;line-height:1.35;min-height:150px">{vsebina}</div>'


# ---------------- 2 Ogrevanje ----------------
stran('2 Ogrevanje prstov.html', 'Ogrevanje prstov', [
    info('Prsti domov', '''
<p class="big">Vsako uro začnemo s kratko tipkalno vajo.</p>
<div class="box big">👉 kazalca na <b>F</b> in <b>J</b><br>🖐️ levo <b>A S D F</b>, desno <b>J K L Č</b><br>👀 gledaš zaslon, ne tipk</div>'''),
    {'type': 'keys', 'title': 'Osnovna vrsta', 'intro': 'Pritiskaj označeno tipko. Glej <b>zaslon</b>.',
     'keys': 'asdfghjklč', 'n': 20, 'min': 85, 'win': 'Prsti so ogreti.',
     'hints': ['Po vsaki tipki se prst vrne domov.', 'G in H tipkata kazalca.']},
    {'type': 'type', 'title': 'Ena vrstica', 'intro': 'Natipkaj vrstico in pritisni <b>Enter</b>. Natančnost je pomembnejša od hitrosti.',
     'text': 'slika ima vedno svoj vir', 'min': 85,
     'hints': ['Presledek tipka palec.', 'Če se zmotiš, tipkaj naprej. Šteje, koliko je skupaj prav.']},
], 'Prsti so pripravljeni.')

# ---------------- 3 Slika v besedilu ----------------
stran('3 Slika v besedilu.html', 'Slika v besedilu', [
    {'type': 'choose', 'title': 'Kam spada slika?',
     'intro': f'''<div>Ista stran je oblikovana na dva načina. Kje je slika hmelja na <b>pravem mestu</b>?</div>
<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:10px">
{stran_a4('<b>A</b><div style="font-size:17px;font-weight:bold">Kmetijstvo</div><b>Hmelj</b><div>Hmelju pravijo zeleno zlato.</div><img src="' + HMELJ + '" style="width:90px;display:block;margin:6px 0"><div style="font-size:10px;font-style:italic">' + VIR + '</div><div style="font-size:17px;font-weight:bold;margin-top:6px">Zgodovina</div>')}
{stran_a4('<b>B</b><img src="' + HMELJ + '" style="width:90px;display:block;margin:0 0 6px"><div style="font-size:17px;font-weight:bold">Kmetijstvo</div><b>Hmelj</b><div>Hmelju pravijo zeleno zlato.</div><div style="font-size:17px;font-weight:bold;margin-top:6px">Zgodovina</div><div>V Šempetru so rimski nagrobniki.</div>')}
</div>
<p class="small">Klikni odgovor. Če je narobe, ti stran pove zakaj. Če ne veš, kako začeti, klikni Namig.</p>''',
     'options': [
         ch('A', ok=True, why='Slika je pri odstavku o hmelju in pod njo piše vir.'),
         ch('B', why='Slika je na vrhu, nad poglavjem, ki z njo nima zveze. Bralec ne ve, kaj kaže. Tudi vira ni.'),
         ch('Vseeno je.', why='Ni vseeno. Slika mora biti ob besedilu, ki ga pojasni.'),
     ],
     'hints': ['O čem govori slika? Poišči odstavek o isti stvari.']},
    info('Vsaka slika ima avtorja', f'''
<p class="big">Fotografijo je nekdo posnel. To je njegovo <b>delo</b>. 📸</p>
<div class="box">Če tujo sliko uporabiš, pod njo napišeš <b>vir</b>: kdo jo je naredil in od kod je.<br>
<img src="{HMELJ}" style="width:150px;display:block;margin:8px 0">
<i style="font-size:13px">{VIR}</i></div>
<p class="small"><b>CC BY-SA</b> je licenca: avtor dovoli uporabo, če ga navedeš.</p>'''),
    {'type': 'choose', 'title': 'Kateri zapis vira je dober?',
     'intro': f'''<div>Luka je sliko hmelja našel na strani <b>Wikimedia Commons</b>. Ob sliki je pisalo:</div>
<div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;border:1px solid #bbb;background:#fff;padding:10px 12px;margin:8px 0;max-width:520px">
<img src="{HMELJ}" style="width:80px">
<div style="font-size:14px;line-height:1.5"><b>Avtor:</b> Magdalena Šajinovićová<br><b>Licenca:</b> CC BY-SA 3.0<br><b>Stran:</b> Wikimedia Commons</div></div>
<div>Luka je sliko dal v svoj dokument. Kaj naj napiše pod njo?</div>''',
     'options': [
         ch('Vir: Magdalena Šajinovićová, Wikimedia Commons, CC BY-SA 3.0', ok=True, why='Pove avtorja, stran in licenco, točno kot piše ob sliki. Vsak lahko sliko poišče.'),
         ch('Vir: internet', why='Internet je ogromen. Iz tega nihče ne najde slike in ne ve, kdo jo je posnel.'),
         ch('Vir: Google', why='Google je iskalnik, ne avtor. Slika je na neki drugi strani in ima svojega avtorja.'),
         ch('Nič, saj je bila na internetu.', why='Tudi slike na internetu imajo avtorje. Brez vira se delaš, da je slika tvoja.'),
     ],
     'hints': ['Dober vir pove, KDO je sliko naredil in KJE si jo našel.']},
    {'type': 'match', 'title': 'Kaj je kaj?', 'pairs': [
        ['avtor', 'oseba, ki je posnela fotografijo'],
        ['vir', 'zapis pod sliko: kdo in od kod'],
        ['licenca', 'pove, kako smeš sliko uporabiti'],
        ['PDF', 'oblika datoteke, ki je povsod videti enako']],
     'hints': ['Licenca je kot dovoljenje.', 'PDF boš spoznal/a na koncu ure.']},
], 'Veš, kam spada slika in zakaj potrebuje vir.')

# ---------------- 4 Slika v Wordu ----------------
stran('4 Slika v Wordu.html', 'Slika v Wordu', [
    info('Odpri svoj dokument', f'''
<p class="big">Odpri dokument <b>Savinjska dolina</b>, ki si ga naredil/a pri prejšnji uri.</p>
<div class="box">1. Odpri <b>Word</b>.<br>2. Klikni <b>Odpri</b> in v mapi <b>Dokumenti</b> poišči <b>Savinjska dolina</b>.</div>
<p class="small"><b>Dokumenta ne najdeš?</b> Odpri prazen dokument, prilepi besedilo (Ctrl + V) in izberi sloge: prva vrstica Naslov, Narava, Kmetijstvo, Zgodovina Naslov 1, ostali kratki naslovi Naslov 2.</p>
{KOPIRAJ}'''),
    {'type': 'order', 'title': 'Kako prideš do slike?', 'intro': '<div>Sliko boš kopiral/a s te strani. Uredi korake v pravi vrstni red.</div>',
     'items': ['Na tej strani z desnim klikom klikni sliko in izberi <b>Kopiraj sliko</b>.',
               'V Wordu klikni na konec odstavka o hmelju (za »visokih žicah.«).',
               'Pritisni <b>Enter</b>, da dobiš novo vrstico.',
               'Pritisni <b>Ctrl + V</b>, da prilepiš sliko.'],
     'hints': ['Najprej moraš sliko imeti v odložišču, šele nato jo lahko prilepiš.', 'Preden prilepiš, mora biti kazalka v Wordu na pravem mestu.']},
    {'type': 'check', 'title': 'Vstavi sliko', 'label': 'Slika hmelja je v mojem dokumentu, pod njo je vir.', 'html': f'''
<div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start">
<div><img src="{HMELJ}" alt="Hmelj" style="width:220px;border:1px solid #ccc"><br><span class="small">⬆ desni klik, <b>Kopiraj sliko</b></span></div>
<div class="box" style="flex:1 1 260px">
☐ V Wordu klikni za »visokih žicah.«, pritisni <b>Enter</b> in <b>Ctrl + V</b>.<br>
☐ Slika je prevelika? Klikni jo in <b>povleci kotni krogec</b> proti sredini. Kot, ne stranica, da se slika ne raztegne.<br>
☐ Pod sliko pritisni Enter in natipkaj vir:<br><i>{VIR}</i><br>
☐ Vrstico z virom naredi <b>manjšo</b> (10) in <b>poševno</b> (Ctrl + I).<br>
☐ Pritisni <b>Ctrl + S</b>.</div></div>
<p class="small">Fotografija: {VIR_HTML}.</p>'''},
    {'type': 'choose', 'title': 'Slika se je raztegnila', 'intro': '<div>Maja je sliko povlekla za <b>desno stranico</b>. Hmelj je zdaj širok in sploščen. Kaj je naredila narobe?</div>',
     'options': [
         ch('Vleči bi morala za kotni krogec.', ok=True, why='Kot spremeni širino in višino skupaj, zato slika ostane prave oblike.'),
         ch('Sliko bi morala izbrisati.', why='Ni treba. Dovolj je razveljaviti (Ctrl + Z) in vleči za kot.'),
         ch('Nič, tako mora biti.', why='Raztegnjena slika ne kaže resnice. Hmelj ni sploščen.'),
     ],
     'hints': ['Krogci so na kotih in na sredinah stranic. Kateri spremeni obe smeri hkrati?']},
], 'Slika je v dokumentu, z virom.')

# ---------------- 5 Izvoz v PDF ----------------
stran('5 Izvoz v PDF.html', 'Izvoz v PDF', [
    {'type': 'choose', 'title': 'Zakaj PDF?',
     'intro': '<div>Dokument boš poslal/a učitelju. Ta ga odpre na drugem računalniku, kjer ni enakih pisav. Kaj je bolje poslati?</div>',
     'options': [
         ch('PDF', ok=True, why='PDF je povsod videti enako: na računalniku, tablici in telefonu. In nihče ga po nesreči ne spremeni.'),
         ch('Wordov dokument (.docx)', why='Na drugem računalniku se lahko pisave in slike premaknejo. Docx pošlješ, kadar naj ga kdo ureja naprej.'),
         ch('Posnetek zaslona', why='Na posnetku je samo del strani in besedila ni mogoče označiti ali iskati.'),
     ],
     'hints': ['Kaj želiš: da ga učitelj ureja ali da ga vidi točno tako, kot si ga naredil/a?']},
    {'type': 'order', 'title': 'Kako shraniš v PDF?', 'intro': '<div>Uredi korake v pravi vrstni red.</div>',
     'items': ['Klikni zavihek <b>Datoteka</b>.',
               'Klikni <b>Shrani kot</b>.',
               'Pri vrsti datoteke izberi <b>PDF (*.pdf)</b>.',
               'Klikni <b>Shrani</b>.'],
     'hints': ['Vse se začne na zavihku levo zgoraj.']},
    {'type': 'check', 'title': 'Shrani svoj PDF', 'label': 'Moj dokument je shranjen kot PDF in sem ga odprl/a.', 'html': '''
<div class="box">
☐ <b>Datoteka</b>, <b>Shrani kot</b>, mapa <b>Dokumenti</b>.<br>
☐ Ime: <b>Savinjska dolina</b>, vrsta: <b>PDF (*.pdf)</b>, <b>Shrani</b>.<br>
☐ Odpri mapo Dokumenti. Zdaj imaš <b>dve</b> datoteki z istim imenom: ena je Word, druga PDF.<br>
☐ Odpri PDF. So naslovi, slika in vir na mestu?</div>
<p class="small">Word dokument obdrži: v njem lahko še popravljaš. PDF je za pošiljanje in tiskanje.</p>'''},
], 'Dokument je shranjen kot PDF.')

# ---------------- 6 Zapis v zvezek ----------------
stran('6 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek.', 'html': '''
<div class="zapis"><h3>SLIKA IN PDF</h3>
<p>Slika stoji ob besedilu, ki ga pojasni.</p>
<p>Velikost spreminjam s <b>kotnim krogcem</b>, da se slika ne raztegne.</p>
<p>Pod tujo sliko napišem <b>vir</b>: avtor, stran, licenca.</p>
<p><b>PDF</b> je povsod videti enako. Pošljem ga, kadar naj dokument kdo samo bere ali natisne.</p>
<p><b>Datoteka, Shrani kot, PDF</b></p></div>'''},
], 'Zapis je v zvezku.')

# ---------------- 8 Izziv ----------------
stran('8 Izziv besedilo ob sliki.html', '★★ Izziv: besedilo ob sliki', [
    {'type': 'choose', 'stars': '★★', 'title': 'Prelom besedila',
     'intro': '<div>Slika stoji sama v svoji vrstici in desno od nje je prazno. Želiš, da besedilo teče <b>ob sliki</b>. Kaj nastaviš?</div>',
     'options': [
         ch('Ob kliku na sliko ikono Možnosti postavitve in izbiro Kvadrat.', ok=True, why='Kvadrat pomeni, da besedilo obteka sliko okoli in okoli.'),
         ch('Sliko pomanjšam, dokler besedilo ne skoči zraven.', why='V vrstici z besedilom slika ostane kot velika črka. Brez preloma besedilo ne steče ob njej.'),
         ch('Pred besedilo dodam veliko presledkov.', why='Presledki se ob vsaki spremembi premaknejo. Za to ima Word prelom besedila.'),
     ],
     'hints': ['Ko klikneš sliko, se desno zgoraj pokaže majhna ikona.']},
    {'type': 'check', 'stars': '★★', 'title': 'Poskusi v Wordu', 'label': 'Besedilo teče ob sliki in dokument sem znova shranil/a kot PDF.', 'html': '''
<div class="box">1. Klikni sliko hmelja.<br>2. Klikni ikono <b>Možnosti postavitve</b> desno zgoraj ob sliki.<br>3. Izberi <b>Kvadrat</b>.<br>4. Sliko povleci desno ob odstavek o hmelju. Vir naj ostane tik pod njo.<br>5. Znova shrani kot <b>PDF</b> in preveri, ali se je spremenil.</div>'''},
    {'type': 'choose', 'stars': '★★★', 'title': 'Kdo sme kaj?',
     'intro': '<div>Slika ima licenco <b>CC BY-SA</b>. Ana je iz nje naredila plakat. Kaj mora storiti?</div>',
     'options': [
         ch('Navesti avtorja in plakat deliti pod enako licenco.', ok=True, why='BY pomeni »navedi avtorja«, SA pomeni »deli naprej pod enakimi pogoji«.'),
         ch('Plačati avtorju.', why='Licence CC so brezplačne. Pogoj je, da navedeš avtorja.'),
         ch('Nič, slika je zdaj njena.', why='Slika ostane avtorjeva. Ana mora navesti avtorja.'),
     ],
     'hints': ['BY: kdo je avtor. SA: share alike, deli enako.']},
], 'Rešil/a si izziv!')
