# Računalništvo 6. r., 6. ura »Naslovi, odstavki, slogi«.
# Prva različica 5. 11. 2026 (6. B). Predelano 27. 11. 2026: v 6. B je bilo preveč klikanja slogov na tujem besedilu.
# Zdaj po Rosenshineu: ponovitev, primer (prve vrstice že urejene), vodena vaja, nato učenec SAM napiše svoje
# poglavje (nova vrsta naloge 'pisi'), ga natipka v Word in uredi s slogi; zapis v zvezek z vrzelmi (priklic).
# 7. ura nadaljuje z dokumentom »Savinjska dolina« v mapi Dokumenti, zato ga učenci tu shranijo pod tem imenom.

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

def dok(vrstice, nav=None):
    """Mala slika Wordove strani: vrstice so [besedilo, razred], ¶ pokaže Enter."""
    p = ''.join(f'<div class="{r}" style="font-family:Calibri,Arial,sans-serif;margin:0 0 4px">{t}</div>' for t, r in vrstice)
    n = ''
    if nav is not None:
        n = ('<div class="nav"><div class="navh">Podokno za krmarjenje</div>' +
             (''.join(f'<div class="nv {r}">{t}</div>' for t, r in nav) or '<div class="small">(prazno)</div>') + '</div>')
    return f'<div class="sdoc" style="margin-top:10px"><div class="page" style="min-height:0">{p}</div>{n}</div>'

PIL = ' <b style="color:#c0392b">¶</b>'

# ---------------- 2 Ogrevanje in ponovitev ----------------
stran('2 Ogrevanje prstov.html', 'Ogrevanje in ponovitev', [
    info('Prsti domov', '''
<p class="big">Vsako uro začnemo s kratko tipkalno vajo.</p>
<div class="box big">👉 kazalca na <b>F</b> in <b>J</b><br>🖐️ levo <b>A S D F</b>, desno <b>J K L Č</b><br>👀 gledaš zaslon, ne tipk</div>'''),
    {'type': 'keys', 'title': 'Osnovna vrsta', 'intro': 'Pritiskaj označeno tipko. Glej <b>zaslon</b>.',
     'keys': 'asdfghjklč', 'n': 20, 'min': 85, 'win': 'Prsti so ogreti.',
     'hints': ['Po vsaki tipki se prst vrne domov.', 'G in H tipkata kazalca.']},
    {'type': 'type', 'title': 'Ena vrstica', 'intro': 'Natipkaj vrstico in pritisni <b>Enter</b>. Natančnost je pomembnejša od hitrosti.',
     'text': 'naslov je kratek, odstavek pove več', 'min': 85,
     'hints': ['Presledek tipka palec.', 'Vejico tipka sredinec desne roke.']},
    {'type': 'match', 'title': 'Ponovimo bližnjice',
     'intro': '<div>Danes jih boš rabil/a v Wordu. Poveži bližnjico in kaj naredi.</div>',
     'pairs': [
         ['Ctrl + C', 'kopiraj'],
         ['Ctrl + V', 'prilepi'],
         ['Ctrl + S', 'shrani'],
         ['Ctrl + Z', 'razveljavi zadnji korak']],
     'hints': ['C kot copy, V je takoj zraven.', 'Z je rešilna bilka: ko se zmotiš, greš korak nazaj.']},
], 'Prsti in bližnjice so pripravljeni.')

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
<p class="big">V Wordu naslova ne oblikuješ na roko. Izbereš mu <b>slog</b>.</p>
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
    {'type': 'choose', 'title': '🔍 Detektiv: znak ¶',
     'intro': f'''<div>Word zna pokazati, kje si pritisnil/a <b>Enter</b>: tam nariše znak <b style="color:#c0392b">¶</b>. Žan je natipkal tole. Kaj je naredil narobe?</div>
{dok([['Mačka prespi tudi do 16 ur' + PIL, 'st3'], ['na dan. Največ spi' + PIL, 'st3'], ['podnevi, ponoči pa lovi.' + PIL, 'st3']])}''',
     'options': [
         ch('Enter je pritisnil sredi odstavka, na koncu vrstic.', ok=True, why='Prav. To je en odstavek, zato je ¶ lahko samo na koncu. Vrstico prelomi Word sam.'),
         ch('Nič, tako mora biti.', why='Poglej, kje so ¶: sredi povedi. Word zdaj misli, da so to trije odstavki.'),
         ch('Za vsako piko bi moral pritisniti Enter.', why='Ne. En odstavek ima lahko več povedi. Enter pride šele, ko se začne nova misel.'),
     ],
     'hints': ['Koliko misli je v tem besedilu? Ena ali tri?', 'Poglej, kje stojijo znaki ¶. Ali stojijo na koncu povedi?']},
    {'type': 'choose', 'title': '🔍 Detektiv: kje je naslov?',
     'intro': f'''<div>Ana je naslov »Spanje« naredila <b>krepak in večji</b>. Odprla je podokno za krmarjenje. Zakaj je prazno?</div>
{dok([['<b style="font-size:20px">Spanje</b>', ''], ['Mačka prespi tudi do 16 ur na dan.', 'st3']], nav=[])}''',
     'options': [
         ch('Ker »Spanje« nima sloga Naslov 1. Za Word je to le krepko navadno besedilo.', ok=True, why='Tako je. Slog pove Wordu, KAJ je besedilo. Krepko pove le, kako je videti.'),
         ch('Ker je naslov premajhen.', why='Velikost ni bistvo. Tudi velik krepak naslov je za Word navadno besedilo, dokler nima sloga.'),
         ch('Ker podokno pokaže samo slike.', why='Ne. Podokno pokaže naslove, a samo tiste, ki imajo slog Naslov 1, Naslov 2 …'),
     ],
     'hints': ['Kako Word ve, da je nekaj naslov?']},
], 'Veš, kaj so naslov, odstavek in slog, in znaš najti napako.')

# ---------------- 4 Slogi na poskus ----------------
stran('4 Slogi na poskus.html', 'Slogi na poskus', [
    {'type': 'slogi', 'title': 'Mačka',
     'intro': '<div>To je mali urejevalnik. <b>Prve tri vrstice sem uredil jaz</b>: poglej jih. Ostale uredi ti: klikni vrstico, nato zgoraj pravi slog. Na koncu klikni <b>Preveri</b>.</div>',
     'paras': [
         ['Mačka', 'Naslov', '', 'Naslov'],
         ['Mačka je domača žival. Ljudje jo imajo radi že tisoče let.', 'Navadno', '', 'Navadno'],
         ['Hrana', 'Naslov 1', '', 'Naslov 1'],
         ['Kaj jedo mačke', 'Naslov 2'],
         ['Mačke jedo meso in ribe.', 'Navadno'],
         ['Kaj pijejo mačke', 'Naslov 2'],
         ['Mačke pijejo vodo. Mleko jim ne dela dobro.', 'Navadno'],
         ['Spanje', 'Naslov 1'],
         ['Mačka prespi tudi do 16 ur na dan.', 'Navadno']],
     'win': 'Vsi slogi so pravi. Poglej podokno za krmarjenje: Hrana ima dva manjša dela, Spanje nobenega.',
     'hints': ['Hrana je veliko poglavje. Kaj jedo in kaj pijejo mačke sta dela poglavja Hrana.',
               'Spanje je novo veliko poglavje, kot Hrana.']},
], 'Znaš izbrati pravi slog za naslov in odstavek.')

# ---------------- 5 Moje poglavje ----------------
NAV_SAV = [[t, s] for t, s in SAVINJSKA if s != 'Navadno']
stran('5 Moje poglavje.html', 'Moje poglavje', [
    info('Ti si avtor/ica', '''
<p class="big">V Wordu boš uredil/a besedilo <b>Savinjska dolina</b>. Ima tri poglavja: Narava, Kmetijstvo, Zgodovina.</p>
<div class="box big">Dodal/a mu boš <b>četrto poglavje</b>, ki ga napišeš <b>sam/a</b>: o kraju, hrani, športu ali kotičku v dolini, ki ga imaš rad/a.</div>
<p>Najprej ga napiši tukaj. Stran ti pove, ali so naslovi in odstavek pravi.</p>'''),
    {'type': 'pisi', 'id': 'moje-poglavje', 'shrani': 'r6-moje-poglavje', 'title': 'Napiši svoje poglavje',
     'intro': '<div>Izpolni tri polja. Desno vidiš, kam se tvoji naslovi uvrstijo v podoknu za krmarjenje (rumeno). Na koncu klikni <b>Preveri</b>.</div>',
     'pred': NAV_SAV,
     'polja': [
         {'slog': 'Naslov 1', 'oznaka': 'naslov poglavja (kratko, brez pike)', 'zgled': 'Prosti čas'},
         {'slog': 'Naslov 2', 'oznaka': 'manjši del tega poglavja', 'zgled': 'Kopanje v Savinji'},
         {'slog': 'Navadno', 'oznaka': 'odstavek: vsaj 2 povedi, ne pritiskaj Enter', 'zgled': 'Poleti se s prijatelji kopamo v Savinji. Voda je hladna, a čista.', 'povedi': 2, 'besed': 10},
     ],
     'win': 'Tvoje poglavje je pripravljeno. Zdaj ga boš natipkal/a v Word.',
     'hints': ['Naslov 1 je tema, npr. Šport ali Hrana. Naslov 2 je nekaj ožjega znotraj teme.',
               'Odstavek odgovori na naslov 2: kaj, kje, zakaj ti je všeč.',
               'Naslov je kratek kot kažipot. Odstavek je iz celih povedi s piko.']},
], 'Svoje poglavje si napisal/a.')

# ---------------- 6 V Wordu ----------------
stran('6 Slogi v Wordu.html', 'Zdaj zares: Word', [
    info('Odpri Word', '''
<p class="big">Besedilo boš uredil/a v pravem Wordu, ki je na tem računalniku.</p>
<div class="box big">1. Klikni gumb <b>Start</b> spodaj levo.<br>2. Natipkaj <b>Word</b> in pritisni <b>Enter</b>.<br>3. Klikni <b>Prazen dokument</b>.</div>
<p>Ko je prazen dokument odprt, se vrni v brskalnik in klikni Naslednja naloga.</p>'''),
    info('Prenesi besedilo', f'''
<p class="big">Tega besedila ti ni treba tipkati. Kopiraj ga in ga prilepi v Word s <b>Ctrl + V</b>.</p>
{KOPIRAJ}'''),
    {'type': 'check', 'title': 'Uredi Savinjsko dolino', 'label': 'Vsi slogi so izbrani in naslove vidim v podoknu za krmarjenje.', 'html': '''
<div class="box">1. Klikni v vrstico. 2. Na zavihku <b>Osnovno</b> v skupini <b>Slogi</b> klikni slog.<br><br>
☐ Savinjska dolina: <b>Naslov</b><br>
☐ Narava, Kmetijstvo, Zgodovina: <b>Naslov 1</b><br>
☐ Reka Savinja, Hmelj, Rimska nekropola: <b>Naslov 2</b><br>
☐ stavki s piko ostanejo <b>Navadno</b><br>
☐ Zavihek <b>Pogled</b>, vklopi <b>Podokno za krmarjenje</b>.</div>
<p class="small">Se zmotiš? <b>Ctrl + Z</b>. Slogov ne najdeš? Zavihek Osnovno, desni del.</p>'''},
    {'type': 'check', 'title': 'Natipkaj svoje poglavje', 'label': 'Moje poglavje je v Wordu, s pravimi slogi.', 'html': '''
<div>To je tvoje besedilo s prejšnjega koraka:</div>
<div data-pisi="r6-moje-poglavje" data-slogi="Naslov 1,Naslov 2,Navadno"></div>
<div class="box">☐ Pritisni <b>Ctrl + End</b> (skok na konec dokumenta) in nato <b>Enter</b>.<br>
☐ Svoje poglavje <b>natipkaj</b> z vsemi prsti. Enter samo na koncu naslova in na koncu odstavka.<br>
☐ Izberi sloge: <b>Naslov 1</b>, <b>Naslov 2</b>, <b>Navadno</b>.<br>
☐ Na zavihku Osnovno klikni gumb <b>¶</b> (Pokaži vse). Je ¶ samo na koncu vrstic, kjer si res pritisnil/a Enter?</div>'''},
    {'type': 'choose', 'title': 'Poglej v podokno',
     'intro': '<div>Poglej podokno za krmarjenje v <b>svojem</b> Wordu. Koliko naslovov poglavij (Naslov 1) vidiš?</div>',
     'options': [
         ch('4', ok=True, why='Narava, Kmetijstvo, Zgodovina in tvoje poglavje. Klikni v podoknu na svoje poglavje: Word te pelje tja.'),
         ch('3', why='Manjka tvoje poglavje. Klikni na njegov naslov in izberi slog Naslov 1.'),
         ch('7', why='Šteješ tudi Naslove 2. V podoknu so zamaknjeni malo v desno. Štej samo tiste ob levem robu.'),
         ch('Podokno je prazno.', why='Vklopi ga: zavihek Pogled, Podokno za krmarjenje. Če je še vedno prazno, naslovi nimajo slogov.'),
     ],
     'hints': ['Naslovi 1 so v podoknu ob levem robu, Naslovi 2 so zamaknjeni.']},
    {'type': 'check', 'title': 'Shrani', 'label': 'Dokument Savinjska dolina je shranjen v mapi Dokumenti.', 'html': '''
<div class="box big">Pritisni <b>Ctrl + S</b>, izberi mapo <b>Dokumenti</b> in ime <b>Savinjska dolina</b>.</div>
<p class="warn">Dokument potrebuješ pri naslednji uri: vanj boš vstavil/a sliko.</p>'''},
], 'Dokument s tvojim poglavjem je urejen in shranjen.')

# ---------------- 7 Zapis v zvezek ----------------
L = lambda r: f'<span class="luk" data-r="{r}">{r}</span>'
stran('7 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši in dopolni', 'label': 'Zapis sem prepisal/a, dopolnil/a in preveril/a.', 'html': f'''
<p>Prepiši v zvezek. <b>Prazna mesta dopolni sam/a</b>, iz glave. Nato klikni Preveri in popravi z rdečo.</p>
<div class="zapis"><h3>NASLOVI, ODSTAVKI, SLOGI</h3>
<p><b>Slog</b> je shranjena oblika z {L('imenom')}. Word iz sloga ve, kaj je naslov.</p>
<p>Naslov: ime besedila &nbsp; {L('Naslov 1')}: poglavje &nbsp; Naslov 2: del poglavja &nbsp; {L('Navadno')}: odstavek</p>
<p><b>Enter</b> pritisnem samo, ko se začne nov {L('odstavek')}. Znak {L('¶')} pokaže, kje sem pritisnil/a Enter.</p>
<p>Naslove vidim v {L('podoknu za krmarjenje')} (zavihek Pogled).</p></div>
<p><button class="btn go2" onclick="document.querySelectorAll('.luk').forEach(function(e){{e.classList.add('vidi')}});this.textContent='✅ Popravi, kar je drugače.'">👀 Preveri svoje besede</button></p>'''},
], 'Zapis je v zvezku.')

# ---------------- 9 Izziv ----------------
stran('9 Izziv kazalo z enim klikom.html', '★★ Izziv: kazalo z enim klikom', [
    {'type': 'choose', 'stars': '★★', 'title': 'Od kod Word ve?',
     'intro': '<div>Word zna sam narediti <b>kazalo</b> (seznam poglavij na začetku). Od kod ve, kaj spada v kazalo?</div>',
     'options': [
         ch('Iz naslovov, ki imajo slog Naslov 1 ali Naslov 2.', ok=True, why='Zato so slogi tako pomembni: brez njih Word naslovov ne najde.'),
         ch('Iz besed, ki so krepke.', why='Krepka beseda je lahko kjerkoli v odstavku. Word v kazalo vzame samo naslove s slogi.'),
         ch('Iz prvih besed vsake vrstice.', why='Potem bi bili v kazalu tudi odstavki. Word vzame samo naslove s slogi.'),
     ],
     'hints': ['Kaj je pokazalo podokno za krmarjenje?']},
    {'type': 'check', 'stars': '★★', 'title': 'Vstavi kazalo v Wordu', 'label': 'V dokumentu imam kazalo z vsemi poglavji, tudi s svojim.', 'html': '''
<div class="box">1. Klikni na konec prvega odstavka (za »Logarsko dolino.«) in pritisni <b>Enter</b>.<br>2. Odpri zavihek <b>Sklici</b>.<br>3. Klikni <b>Kazalo vsebine</b> in izberi prvo možnost.<br>4. Je v kazalu tudi tvoje poglavje?</div>
<p class="small">Če kakšnega naslova ni v kazalu, nima pravega sloga. Popravi slog in kazalo posodobi.</p>'''},
    {'type': 'check', 'stars': '★★', 'title': 'Še en del poglavja', 'label': 'Moje poglavje ima dva dela z Naslovom 2.', 'html': '''
<div class="box">Svojemu poglavju dodaj še en <b>Naslov 2</b> in pod njim odstavek z vsaj dvema povedma. Posodobi kazalo: desni klik na kazalo, <b>Posodobi polje</b>.</div>'''},
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
