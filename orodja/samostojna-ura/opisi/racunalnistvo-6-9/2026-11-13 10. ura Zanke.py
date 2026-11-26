# Računalništvo 6. do 9. razred, 10. ura »Zanke« (13. 11. 2026). V razredu izvedena v Scratchu brez Brihte; ta stran je bila objavljena 26. 11. kot ponovitev, da je številčenje na Brihti polno.
# LDN/PRIPRAVE: sklop 4 Blokovno programiranje, 10. ura »Izzivi naraščajoče zahtevnosti: zanke«.
# Bloki so videti kot v Scratchu (pojdi, obrni se, ponovi), pisalo riše kot razširitev Pero.
# Nova vrsta naloge 'risar' (engine.js): primerja narisane črte s ciljno sliko.
# Pot: kvadrat brez zanke, kvadrat z zanko, pravilo 360 : n, hrošč, zanka v zanki. Izziv: prosto risanje + pravi Scratch.

L = [3, 4, 5, 6, 8]

# ---------------- 2 Pisalo in zanka ----------------
stran('2 Pisalo in zanka.html', 'Pisalo in zanka', [
    info('Programiraš pisalo ✏️', '''
<p class="big">Modra puščica je <b>pisalo</b>. Kamor gre, tam nariše zeleno črto.</p>
<div class="box"><span class="sb mot">pojdi <b>100</b> korakov</span> &nbsp;gre naprej in riše<br><br>
<span class="sb mot">obrni se ↻ <b>90</b>°</span> &nbsp;se obrne v smeri urinega kazalca, ne riše</div>
<p>Taki so bloki tudi v <b>Scratchu</b>. Siva črta pokaže, kaj mora pisalo narisati.</p>'''),
    {'type': 'risar', 'title': 'Poskusi: samo zaženi', 'intro': 'Program je že sestavljen. Klikni <b>▶ Zaženi</b> in opazuj pisalo.',
     'start': ['F100', 'T90', 'F100'], 'solution': ['F100', 'T90', 'F100'], 'locked': True,
     'win': '✅ Pisalo je šlo naprej, se obrnilo za 90° (pravi kot) in šlo spet naprej.'},
    {'type': 'risar', 'title': 'Kvadrat', 'intro': 'Sestavi program, ki nariše <b>kvadrat</b> s stranico 100. Klikaj bloke spodaj, nato ▶ Zaženi.',
     'tools': ['F100', 'T90'], 'solution': ['F100', 'T90', 'F100', 'T90', 'F100', 'T90', 'F100', 'T90'],
     'hints': ['Kvadrat ima 4 stranice. Po vsaki se pisalo obrne.', 'pojdi 100, obrni se 90, in to še trikrat.']},
    info('Zanka: ponovi', '''
<p class="big">Pri kvadratu si 4-krat sestavil/a isti par blokov. To je <b>vzorec</b>!</p>
<div class="box"><span class="sb ctl">ponovi <b>4</b>-krat</span><br>
<span style="margin-left:26px" class="sb mot">pojdi <b>100</b> korakov</span><br>
<span style="margin-left:26px" class="sb mot">obrni se ↻ <b>90</b>°</span><br>
<span class="sb ctl kon">konec ponovi</span></div>
<p>Vse med »ponovi« in »konec ponovi« se ponovi. Temu rečemo <b>zanka</b>. 8 blokov je postalo 4.</p>'''),
    {'type': 'risar', 'title': 'Kvadrat z zanko', 'intro': 'Nariši isti kvadrat, a uporabi <b>največ 4 bloke</b>.',
     'tools': ['F100', 'T90'], 'loops': L, 'max': 4, 'solution': ['N4', 'F100', 'T90', ')'],
     'hints': ['Najprej klikni »ponovi 4-krat«.', 'Nato pojdi 100, obrni se 90 in na koncu »konec ponovi«.']},
    {'type': 'choose', 'title': 'Kaj bo narisal?', 'intro': '''<div class="box"><span class="sb ctl">ponovi <b>3</b>-krat</span><br>
<span style="margin-left:26px" class="sb mot">pojdi <b>100</b> korakov</span><br>
<span style="margin-left:26px" class="sb mot">obrni se ↻ <b>120</b>°</span><br>
<span class="sb ctl kon">konec ponovi</span></div><p>Klikni odgovor. Če je narobe, ti stran pove zakaj. Če ne veš, kako začeti, klikni <b>Namig</b>.</p>''',
     'options': [ch('trikotnik', True, 'Tako je: 3 stranice, po vsaki obrat za 120°. Skupaj 3 × 120° = 360°, cel krog.'),
                 ch('kvadrat', why='Kvadrat ima 4 stranice. Zanka se tu ponovi samo 3-krat.'),
                 ch('3 črte v ravni vrsti', why='Po vsaki črti se pisalo obrne za 120°, zato črte niso v isti vrsti.')],
     'hints': ['Koliko črt nariše? Toliko, kolikorkrat se zanka ponovi.']},
    {'type': 'risar', 'title': 'Trikotnik', 'intro': 'Preveri: nariši enakostranični trikotnik z <b>največ 4 bloki</b>.',
     'tools': ['F100', 'T60', 'T90', 'T120'], 'loops': L, 'max': 4, 'solution': ['N3', 'F100', 'T120', ')'],
     'hints': ['Program je zelo podoben kvadratu.', 'ponovi 3-krat ( pojdi 100, obrni se 120 ).']},
], 'Znaš napisati zanko »ponovi« in z njo narisati lik.')

# ---------------- 3 Skrivnost 360 ----------------
stran('3 Skrivnost 360.html', 'Skrivnost števila 360', [
    {'type': 'risar', 'title': 'Šestkotnik', 'intro': 'Nariši pravilni <b>šestkotnik</b> (6 enakih stranic). Največ <b>4 bloki</b>. Kateri obrat je pravi? Preizkusi!',
     'tools': ['F70', 'T45', 'T60', 'T72', 'T90', 'T120'], 'loops': L, 'max': 4, 'solution': ['N6', 'F70', 'T60', ')'],
     'hints': ['Zanka se ponovi 6-krat, ker ima lik 6 stranic.', 'Pisalo se mora v 6 obratih obrniti za cel krog, 360°.', '360 : 6 = 60. ponovi 6-krat ( pojdi 70, obrni se 60 ).']},
    {'type': 'match', 'title': 'Poišči vzorec', 'intro': 'Poveži lik z obratom, ki ga nariše.',
     'pairs': [['trikotnik (3 stranice)', 'obrni se 120°'], ['kvadrat (4 stranice)', 'obrni se 90°'],
               ['petkotnik (5 stranic)', 'obrni se 72°'], ['šestkotnik (6 stranic)', 'obrni se 60°']],
     'hints': ['Pomnoži število stranic z obratom. Kaj dobiš vsakič?', 'Vedno dobiš 360. Npr. 5 × 72 = 360.']},
    info('Pravilo 360', '''
<div class="box big">🔄 Ko pisalo obide lik, se obrne za <b>cel krog: 360°</b>.<br>
Zato: <b>obrat = 360 : število stranic</b></div>
<p>Odkril/a si vzorec, ki velja za <b>vsak</b> pravilni lik. To je bistvo programiranja: najdeš pravilo, računalnik ga ponavlja.</p>'''),
    {'type': 'choose', 'title': 'Osemkotnik', 'intro': 'Za koliko stopinj se mora pisalo obrniti pri pravilnem <b>osemkotniku</b>?',
     'options': [ch('45°', True, 'Da: 360 : 8 = 45.'), ch('80°', why='Ne deliš 8 v 80. Deliš 360 z 8.'),
                 ch('135°', why='135° je notranji kot osemkotnika, pisalo pa se obrne za zunanji kot: 360 : 8.')],
     'hints': ['obrat = 360 : število stranic']},
    {'type': 'risar', 'title': 'Petkotnik', 'intro': 'Nariši pravilni <b>petkotnik</b>. Največ <b>4 bloki</b>. Pazi na past med obrati!',
     'tools': ['F80', 'T60', 'T72', 'T90', 'T108'], 'loops': L, 'max': 4, 'solution': ['N5', 'F80', 'T72', ')'],
     'hints': ['Uporabi pravilo 360 : število stranic.', '360 : 5 = 72. Obrat 108° je notranji kot, ta ni pravi.']},
    {'type': 'risar', 'title': '🐞 Najdi hrošča', 'intro': 'Ta program bi moral narisati kvadrat, a nariše le ravno črto. Zaženi ga, poišči hrošča in ga popravi.',
     'tools': ['F100', 'T90'], 'loops': L, 'max': 4, 'start': ['N4', 'F100', ')', 'T90'], 'solution': ['N4', 'F100', 'T90', ')'],
     'hints': ['Kateri bloki so znotraj zanke in kateri zunaj?', 'Obrat je ZUNAJ zanke, zato se pisalo obrne šele na koncu. Briši zadnja dva bloka in dodaj obrni se 90, nato konec ponovi.']},
], 'Poznaš pravilo 360 in znaš najti hrošča v zanki.')

# ---------------- 4 Zanka v zanki ----------------
stran('4 Zanka v zanki.html', 'Zanka v zanki', [
    info('Zanka v zanki 🌀', '''
<p class="big">V zanko lahko daš <b>še eno zanko</b>. Notranja nariše lik, zunanja ga ponavlja in vmes obrne pisalo.</p>
<div class="box"><span class="sb ctl">ponovi <b>4</b>-krat</span><br>
<span style="margin-left:26px" class="sb ctl">ponovi <b>4</b>-krat</span><br>
<span style="margin-left:52px" class="sb mot">pojdi <b>80</b> korakov</span><br>
<span style="margin-left:52px" class="sb mot">obrni se ↻ <b>90</b>°</span><br>
<span style="margin-left:26px" class="sb ctl kon">konec ponovi</span><br>
<span style="margin-left:26px" class="sb mot">obrni se ↻ <b>90</b>°</span><br>
<span class="sb ctl kon">konec ponovi</span></div>'''),
    {'type': 'risar', 'title': 'Poglej: 4 kvadrati', 'intro': 'To je program z zgornje slike. Zaženi ga in opazuj, kako nastaja vzorec.',
     'start': ['N4', 'N4', 'F80', 'T90', ')', 'T90', ')'], 'solution': ['N4', 'N4', 'F80', 'T90', ')', 'T90', ')'], 'locked': True,
     'win': '✅ Notranja zanka nariše kvadrat. Zunanja to naredi 4-krat in med kvadrati obrne pisalo.'},
    {'type': 'risar', 'title': 'Satovje', 'intro': 'Nariši vzorec iz <b>6 šestkotnikov</b>, med vsakim se pisalo obrne za 60°. Največ <b>7 blokov</b>.',
     'tools': ['F50', 'T60', 'T90'], 'loops': L, 'max': 7, 'solution': ['N6', 'N6', 'F50', 'T60', ')', 'T60', ')'],
     'hints': ['Notranja zanka: šestkotnik (ponovi 6-krat, pojdi 50, obrni se 60).', 'Zunanja zanka ponovi šestkotnik 6-krat, po vsakem še obrni se 60.',
               'ponovi 6 ( ponovi 6 ( pojdi 50, obrni se 60 ) obrni se 60 )']},
    {'type': 'risar', 'stars': '★★', 'optional': True, 'title': 'Zvezda', 'intro': 'Nariši zvezdo s 5 kraki (5 črt, vsaka dolga 150). Največ <b>4 bloki</b>. Namig: pisalo obkroži sredino <b>dvakrat</b>.',
     'tools': ['F150', 'T72', 'T108', 'T144'], 'loops': L, 'max': 4, 'solution': ['N5', 'F150', 'T144', ')'],
     'hints': ['Pri zvezdi se pisalo obrne za 2 cela kroga: 2 × 360 = 720.', '720 : 5 = 144.']},
], 'Znaš zanko v zanki. Tako nastanejo zapleteni vzorci iz kratkih programov.')

# ---------------- 5 Zapis v zvezek ----------------
stran('5 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek.', 'html': '''
<div class="zapis"><h3>RISANJE Z ZANKAMI</h3>
<p><b>Zanka</b> ponavlja bloke, ki so v njej. Program je krajši in brez napak pri prepisovanju.</p>
<p>Kvadrat: ponovi 4-krat ( pojdi 100, obrni se 90° )</p>
<p><b>Pravilo 360</b>: za pravilni lik je obrat = 360 : število stranic.<br>trikotnik 120°, kvadrat 90°, petkotnik 72°, šestkotnik 60°</p>
<p><b>Hrošč v zanki</b>: preveri, kateri bloki so znotraj zanke in kateri zunaj.</p>
<p><b>Zanka v zanki</b>: notranja nariše lik, zunanja ga ponavlja.</p></div>'''},
], 'Zapis je v zvezku.')

# ---------------- 7 Izziv: Moj vzorec ----------------
stran('7 Izziv Moj vzorec.html', '★★ Izziv: Moj vzorec', [
    info('Ustvari svoj vzorec 🎨', '''
<p class="big">Zdaj ni pravilnih rešitev. Sestavi svoj vzorec z zanko v zanki.</p>
<div class="box">Ideje: ponovi 12-krat (kvadrat, obrni se 30°) · ponovi 8-krat (šestkotnik, obrni se 45°) · zvezda v zvezdi</div>
<p class="small">Ko ti je vzorec všeč, ga pokaži sosedu ali učitelju.</p>'''),
    {'type': 'risar', 'prosto': True, 'optional': True, 'title': 'Moj vzorec', 'intro': 'Sestavi program in klikni <b>▶ Zaženi</b>. Spreminjaj števila in opazuj, kaj se zgodi.',
     'tools': ['F30', 'F60', 'F100', 'T30', 'T45', 'T60', 'T72', 'T90', 'T120', 'T144'], 'loops': [2, 3, 4, 5, 6, 8, 10, 12, 18, 36],
     'win': '✅ Tvoj vzorec! Poskusi še drugačna števila.'},
], 'Ustvaril/a si svoj vzorec. Bravo, umetnik/umetnica kode! 🎨')
