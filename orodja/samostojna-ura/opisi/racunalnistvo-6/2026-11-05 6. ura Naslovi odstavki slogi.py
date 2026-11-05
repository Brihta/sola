# Računalništvo 6. r. (6. B), 6. ura »Naslovi, odstavki, slogi« (5. 11. 2026).

SAVINJSKA = [
    ['Savinjska dolina', 'Naslov'],
    ['Savinjska dolina leži ob reki Savinji, med Celjem in Logarsko dolino.', 'Navadno'],
    ['Narava', 'Naslov 1'],
    ['Reka Savinja', 'Naslov 2'],
    ['Savinja izvira nad Logarsko dolino in se pri Zidanem Mostu izlije v Savo.', 'Navadno'],
    ['Kmetijstvo', 'Naslov 1'],
    ['Hmelj', 'Naslov 2'],
    ['Hmelju pravijo zeleno zlato. Raste ob visokih žicah.', 'Navadno'],
    ['Zgodovina', 'Naslov 1'],
    ['Rimska nekropola', 'Naslov 2'],
    ['V Šempetru so ohranjeni rimski nagrobniki, stari skoraj 2000 let.', 'Navadno'],
]
BESEDILO = '\n'.join(p[0] for p in SAVINJSKA)
KOPIRAJ = f'''<textarea id="besedilo" rows="11" readonly style="width:100%;font:16px/1.4 Calibri,Arial,sans-serif;padding:8px;border:2px solid #b9c6d3;border-radius:10px">{BESEDILO}</textarea>
<p><button class="btn go2" onclick="var t=document.getElementById('besedilo');t.focus();t.select();var ok=false;try{{ok=document.execCommand('copy')}}catch(e){{}}this.textContent=ok?'✅ Kopirano':'Besedilo je označeno: pritisni Ctrl + C'">📋 Kopiraj besedilo</button></p>'''

# ---------------- 2 Ogrevanje ----------------
stran('2 Ogrevanje prstov.html', 'Ogrevanje prstov', [
    info('Prsti domov', '''
<p class="big">Vsako uro začnemo s kratko tipkalno vajo.</p>
<div class="box big">👉 kazalca na <b>F</b> in <b>J</b><br>🖐️ levo <b>A S D F</b>, desno <b>J K L Č</b><br>👀 gledaš zaslon, ne tipk</div>'''),
    {'type': 'keys', 'title': 'Osnovna vrsta', 'intro': 'Pritiskaj označeno tipko. Glej <b>zaslon</b>.',
     'keys': 'asdfghjklč', 'n': 20, 'min': 85, 'win': 'Prsti so ogreti.',
     'hints': ['Po vsaki tipki se prst vrne domov.', 'G in H tipkata kazalca.']},
    {'type': 'type', 'title': 'Ena vrstica', 'intro': 'Natipkaj vrstico in pritisni <b>Enter</b>. Natančnost je pomembnejša od hitrosti.',
     'text': 'naslov in odstavek sta dela besedila', 'min': 85,
     'hints': ['Presledek tipka palec.', 'Če se zmotiš, tipkaj naprej. Šteje, koliko je skupaj prav.']},
], 'Prsti so pripravljeni za delo z besedilom.')

# ---------------- 3 Kaj je slog ----------------
stran('3 Kaj je slog.html', 'Kaj je slog?', [
    {'type': 'choose', 'title': 'Kje hitreje najdeš?',
     'intro': '''<div>Isto besedilo je zapisano na dva načina. V katerem hitreje najdeš, <b>koliko ur na dan spi mačka</b>?</div>
<div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:10px">
<div style="flex:1 1 260px;border:1px solid #ccc;padding:10px 14px;font-size:15px"><b>A</b><br>Mačka. Mačka je domača žival. Ljudje jo imajo radi že tisoče let. Kaj jedo mačke. Mačke jedo meso in ribe. Rade imajo tudi briketke. Spanje. Mačka prespi tudi do 16 ur na dan. Največ spi podnevi.</div>
<div style="flex:1 1 260px;border:1px solid #ccc;padding:10px 14px;font-size:15px"><b>B</b><div class="st0" style="font-size:24px">Mačka</div><div>Mačka je domača žival. Ljudje jo imajo radi že tisoče let.</div><div class="st1" style="font-size:19px">Kaj jedo mačke</div><div>Mačke jedo meso in ribe. Rade imajo tudi briketke.</div><div class="st1" style="font-size:19px">Spanje</div><div>Mačka prespi tudi do 16 ur na dan. Največ spi podnevi.</div></div>
</div>
<p class="small">Klikni odgovor. Če je narobe, ti stran pove zakaj. Če ne veš, kako začeti, klikni Namig.</p>''',
     'options': [
         ch('V besedilu B', ok=True, why='Naslov »Spanje« te takoj pripelje do odgovora. Naslovi so kot kažipoti.'),
         ch('V besedilu A', why='V A so vse besede enake velikosti. Prebrati moraš skoraj vse, da najdeš spanje.'),
         ch('Enako hitro', why='Besedilo je enako, a v B naslov »Spanje« izstopa in ga opaziš takoj.'),
     ],
     'hints': ['Poišči besedo »spanje«. Kje jo opaziš brez branja vsega?']},
    info('Slog je oblika z imenom', '''
<p class="big">V Wordu naslov ne oblikuješ na roko. Izbereš mu <b>slog</b>.</p>
<div class="box">
<div class="st0" style="font-size:26px">Naslov</div><div class="small">ime celega besedila, samo enkrat na vrhu</div>
<div class="st1" style="font-size:21px">Naslov 1</div><div class="small">naslov poglavja</div>
<div class="st2" style="font-size:18px">Naslov 2</div><div class="small">manjši del znotraj poglavja</div>
<div class="st3">Navadno</div><div class="small">odstavek: povedi z razlago</div></div>'''),
    {'type': 'match', 'title': 'Kateri slog?', 'pairs': [
        ['Naslov', 'ime celega besedila na vrhu'],
        ['Naslov 1', 'naslov poglavja, npr. »Spanje«'],
        ['Naslov 2', 'manjši del znotraj poglavja'],
        ['Navadno', 'povedi z razlago (odstavek)']],
     'hints': ['Večja številka pomeni manjši, bolj podrejen naslov.', 'Navadno ni naslov: to je besedilo, ki nekaj razloži.']},
    {'type': 'choose', 'title': 'Kdaj pritisneš Enter?', 'intro': '<div>Tipkaš daljše besedilo. Kdaj pritisneš <b>Enter</b>?</div>',
     'options': [
         ch('Ko se začne nov odstavek ali nov naslov.', ok=True, why='Enter konča odstavek. Vrstico prelomi Word sam.'),
         ch('Na koncu vsake vrstice.', why='Ne. Word sam prelomi vrstico, ko je polna. Če pritisneš Enter, nastane nov odstavek sredi povedi.'),
         ch('Za vsako piko.', why='Ne. En odstavek ima lahko več povedi. Enter pritisneš šele, ko se začne nova misel.'),
     ],
     'hints': ['Odstavek je skupina povedi o eni stvari.']},
    {'type': 'choose', 'title': 'Zakaj slog, ne kar krepko?',
     'intro': '<div>Ana je naslov naredila krepak in večji. Miha mu je izbral slog <b>Naslov 1</b>. Kaj ima Miha več?</div>',
     'options': [
         ch('Word ve, da je to naslov: pokaže ga v podoknu za krmarjenje in iz njega naredi kazalo.', ok=True, why='Slog pove, KAJ je besedilo. Zato Word naslove najde sam.'),
         ch('Nič, oba naslova sta videti enako.', why='Videti sta lahko enaka, a Anin naslov je za Word le navadno besedilo. V podoknu za krmarjenje ga ne bo.'),
         ch('Mihov naslov je lepše pobarvan.', why='Barva ni bistvo. Bistvo je, da Word iz sloga ve, da je to naslov.'),
     ],
     'hints': ['Pomisli: kako Word ve, kaj je naslov?']},
], 'Veš, kaj so naslov, odstavek in slog.')

# ---------------- 4 Slogi na poskus ----------------
stran('4 Slogi na poskus.html', 'Slogi na poskus', [
    {'type': 'slogi', 'title': 'Mačka', 'intro': '<div>To je mali urejevalnik. Klikni odstavek, nato zgoraj klikni pravi slog. Na koncu klikni <b>Preveri</b>.</div>',
     'paras': [
         ['Mačka', 'Naslov'],
         ['Mačka je domača žival. Ljudje jo imajo radi že tisoče let.', 'Navadno'],
         ['Kaj jedo mačke', 'Naslov 1'],
         ['Mačke jedo meso in ribe. Rade imajo tudi briketke.', 'Navadno'],
         ['Spanje', 'Naslov 1'],
         ['Mačka prespi tudi do 16 ur na dan.', 'Navadno']],
     'hints': ['Na vrhu je ime celega besedila: Naslov.', 'Kratki vrstici brez pike sta naslova poglavij: Naslov 1. Vse s piko je Navadno.']},
    {'type': 'slogi', 'title': 'Savinjska dolina',
     'intro': '<div>Zdaj imajo poglavja še manjše dele. Za te uporabi <b>Naslov 2</b>. Opazuj podokno za krmarjenje desno.</div>',
     'paras': SAVINJSKA,
     'hints': ['Narava, Kmetijstvo in Zgodovina so velika poglavja.', 'Reka Savinja je del poglavja Narava, Hmelj je del Kmetijstva. To sta Naslov 2.',
               'Vrstni red: Naslov, Navadno, potem trikrat: Naslov 1, Naslov 2, Navadno.']},
], 'Znaš izbrati pravi slog za naslov in odstavek.')

# ---------------- 5 V Wordu ----------------
stran('5 Slogi v Wordu.html', 'Zdaj zares: Word', [
    info('Odpri Word', '''
<p class="big">Isto besedilo boš uredil/a v pravem Wordu.</p>
<div class="box big">1. Odpri nov zavihek in pojdi na <b>office.com</b>.<br>2. Prijavi se s šolskim <b>Arnes</b> računom.<br>3. Klikni <b>Word</b> in nato <b>Prazen dokument</b>.</div>
<p>Ko je prazen dokument odprt, se vrni v ta zavihek in klikni Naslednja naloga.</p>'''),
    info('Prenesi besedilo', f'''
<p class="big">Besedila ti ni treba tipkati. Kopiraj ga in ga prilepi v Word s <b>Ctrl + V</b>.</p>
{KOPIRAJ}
<p class="small">Vsaka vrstica je svoj odstavek, ker je na koncu Enter.</p>'''),
    {'type': 'order', 'title': 'Kako v Wordu izbereš slog?', 'intro': '<div>Uredi korake v pravi vrstni red.</div>',
     'items': ['Klikni v vrstico, ki jo želiš oblikovati.', 'Zgoraj odpri zavihek <b>Osnovno</b>.', 'V skupini <b>Slogi</b> poišči pravi slog.', 'Klikni slog, na primer <b>Naslov 1</b>.'],
     'hints': ['Najprej Word potrebuje vedeti, KATERO vrstico urejaš.']},
    {'type': 'check', 'title': 'Uredi svoj dokument', 'label': 'Moj dokument ima vse sloge in naslove vidim v podoknu za krmarjenje.', 'html': '''
<div class="box">V Wordu izberi sloge <b>čisto enako kot v nalogi Savinjska dolina</b>:<br>
☐ Savinjska dolina: <b>Naslov</b><br>
☐ Narava, Kmetijstvo, Zgodovina: <b>Naslov 1</b><br>
☐ Reka Savinja, Hmelj, Rimska nekropola: <b>Naslov 2</b><br>
☐ stavki s piko: <b>Navadno</b><br>
☐ Zavihek <b>Pogled</b>, vklopi <b>Podokno za krmarjenje</b>. Ali vidiš vse naslove?<br>
☐ Zgoraj klikni na ime dokumenta in ga preimenuj v <b>Savinjska dolina</b>.</div>
<p class="small">Word za splet shranjuje sam. Če slogov ne najdeš, poglej na zavihek Osnovno, desni del.</p>'''},
], 'Uredil/a si pravi dokument s slogi.')

# ---------------- 6 Zapis v zvezek ----------------
stran('6 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek.', 'html': '''
<div class="zapis"><h3>NASLOVI, ODSTAVKI, SLOGI</h3>
<p><b>Slog</b> je shranjena oblika z imenom. Word iz sloga ve, kaj je naslov.</p>
<p><b>Naslov</b>: ime besedila &nbsp; <b>Naslov 1</b>: poglavje &nbsp; <b>Naslov 2</b>: del poglavja &nbsp; <b>Navadno</b>: odstavek</p>
<p><b>Enter</b> pritisnem samo, ko se začne nov odstavek. Vrstico prelomi Word sam.</p>
<p>Naslove vidim v <b>podoknu za krmarjenje</b> (zavihek Pogled).</p></div>'''},
], 'Zapis je v zvezku.')

# ---------------- 8 Izziv ----------------
stran('8 Izziv kazalo z enim klikom.html', '★★ Izziv: kazalo z enim klikom', [
    {'type': 'choose', 'stars': '★★', 'title': 'Od kod Word ve?',
     'intro': '<div>Word zna sam narediti <b>kazalo</b> (seznam poglavij na začetku). Od kod ve, kaj spada v kazalo?</div>',
     'options': [
         ch('Iz naslovov, ki imajo slog Naslov 1 ali Naslov 2.', ok=True, why='Zato so slogi tako pomembni: brez njih Word naslovov ne najde.'),
         ch('Iz besed, ki so krepke.', why='Krepka beseda je lahko kjerkoli v odstavku. Word v kazalo vzame samo naslove s slogi.'),
         ch('Iz prvih besed vsake vrstice.', why='Potem bi bili v kazalu tudi odstavki. Word vzame samo naslove s slogi.'),
     ],
     'hints': ['Kaj je pokazalo podokno za krmarjenje?']},
    {'type': 'check', 'stars': '★★', 'title': 'Vstavi kazalo v Wordu', 'label': 'V dokumentu imam kazalo z vsemi poglavji.', 'html': '''
<div class="box">1. Klikni na konec prvega odstavka (za »Logarsko dolino.«) in pritisni <b>Enter</b>.<br>2. Odpri zavihek <b>Sklici</b>.<br>3. Klikni <b>Kazalo vsebine</b> in izberi prvo možnost.<br>4. Ali so v kazalu Narava, Kmetijstvo in Zgodovina?</div>
<p class="small">Če kakšnega naslova ni v kazalu, nima pravega sloga. Popravi slog in kazalo posodobi.</p>'''},
    {'type': 'slogi', 'stars': '★★★', 'title': 'Računalnik',
     'intro': '<div>Daljše besedilo brez namigov v naslovih. Dobro preberi vsako vrstico.</div>',
     'paras': [
         ['Računalnik', 'Naslov'],
         ['Strojna oprema', 'Naslov 1'],
         ['Strojna oprema so deli računalnika, ki se jih lahko dotakneš.', 'Navadno'],
         ['Vhodne naprave', 'Naslov 2'],
         ['Tipkovnica in miška pošiljata podatke v računalnik.', 'Navadno'],
         ['Izhodne naprave', 'Naslov 2'],
         ['Zaslon in tiskalnik nam pokažeta rezultat.', 'Navadno'],
         ['Programska oprema', 'Naslov 1'],
         ['Programi so navodila, ki povedo računalniku, kaj naj dela.', 'Navadno']],
     'hints': ['Strojna oprema in Programska oprema sta veliki poglavji.', 'Vhodne in izhodne naprave so del strojne opreme.']},
], 'Spoznal/a si, zakaj so slogi močno orodje.')
