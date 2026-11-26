# Računalništvo 6. do 9. razred, 11. ura »Pogoji in spremenljivke« (27. 11. 2026, predura).
# LDN/PRIPRAVE: sklop 4 Blokovno programiranje, 11. ura »Pogoji in spremenljivke« (v EVIO vpisal Claudio 23. 11.).
# Zanke so bile 13. 11. (v Scratchu), 20. 11. Bober. Bloki so videti kot v Scratchu (vrsta naloge 'risar').
# Pot: spremenljivka dolžina (kvadrat, spirala), pogoj če (barvna spirala, hrošč), ★★ sicer. Izziv: prosto risanje + pravi Scratch.

L = [4, 12]
K = ')'   # blok »konec« (za ponovi in za če)

# ---------------- 2 Spremenljivka ----------------
stran('2 Spremenljivka.html', 'Spremenljivka', [
    info('Ogrevanje: pisalo ✏️', '''
<p class="big">Modra puščica je <b>pisalo</b>. Kamor gre, tam nariše črto. Bloki so taki kot v <b>Scratchu</b>.</p>
<div class="box"><span class="sb mot">pojdi <b>100</b> korakov</span> &nbsp;gre naprej in riše<br><br>
<span class="sb mot">obrni se ↻ <b>90</b>°</span> &nbsp;se obrne v smeri urinega kazalca<br><br>
<span class="sb ctl">ponovi <b>4</b>-krat</span> &nbsp;ponavlja vse do bloka <span class="sb ctl kon">konec ponovi</span></div>
<p>Siva črta pokaže, kaj mora pisalo narisati.</p>'''),
    {'type': 'risar', 'title': 'Ogrevanje: kvadrat', 'intro': 'Z zanko nariši kvadrat. Največ <b>4 bloki</b>. To že znaš iz Scratcha.',
     'tools': ['F100', 'T90'], 'loops': L, 'max': 4, 'solution': ['N4', 'F100', 'T90', K],
     'hints': ['Kvadrat ima 4 enake stranice. Kaj pisalo naredi pri vsaki stranici?', 'Pri vsaki stranici gre naprej in se obrne. Kateri blok to ponovi 4-krat?', 'Ne pozabi zapreti zanke. Vse, kar se ponavlja, mora biti med ponovi in konec.']},
    info('Spremenljivka = škatla 📦', '''
<p class="big"><b>Spremenljivka</b> je škatla z imenom. V njej je ena vrednost, ki se lahko spreminja.</p>
<div class="box"><span class="sb var">nastavi <span class="vpill">dolžina</span> na <b>100</b></span> &nbsp;v škatlo »dolžina« da 100<br><br>
<span class="sb mot">pojdi <span class="vpill">dolžina</span> korakov</span> &nbsp;pogleda v škatlo in gre toliko korakov</div>
<p>Vrednost vidiš v okencu <b>dolžina</b> levo zgoraj na platnu, tako kot v Scratchu.</p>'''),
    {'type': 'risar', 'title': 'Poglej: kvadrat s spremenljivko', 'intro': 'Program je že sestavljen. Klikni <b>▶ Zaženi</b> in poglej okence <b>dolžina</b>.',
     'start': ['S100', 'N4', 'FV', 'T90', K], 'solution': ['S100', 'N4', 'FV', 'T90', K], 'locked': True,
     'win': '✅ Pisalo je 4-krat pogledalo v škatlo »dolžina« in vsakič šlo 100 korakov.'},
    {'type': 'choose', 'title': 'Manjši kvadrat', 'intro': '''<div>Hočeš enak program, a kvadrat s stranico <b>50</b>. Kaj spremeniš?</div>
<p>Klikni odgovor. Če je narobe, ti stran pove zakaj. Če ne veš, kako začeti, klikni <b>Namig</b>.</p>''',
     'options': [ch('samo en blok: nastavi dolžina na 50', True, 'Tako je. Vrednost je na enem mestu, zato jo spremeniš enkrat. To je moč spremenljivke.'),
                 ch('vse bloke pojdi', why='Bloki pojdi ne vsebujejo števila, ampak pogledajo v škatlo. Spremeniš samo, kar je v škatli.'),
                 ch('blok ponovi 4-krat', why='Ponovi določa število stranic, ne dolžine. Kvadrat ima še vedno 4 stranice.')],
     'hints': ['Kje v programu piše 100?']},
    {'type': 'risar', 'title': 'Kvadrat s stranico 50', 'intro': 'Nariši kvadrat s stranico 50. Uporabi spremenljivko <b>dolžina</b>. Največ <b>5 blokov</b>.',
     'tools': ['S50', 'S100', 'FV', 'T90'], 'loops': L, 'max': 5, 'solution': ['S50', 'N4', 'FV', 'T90', K],
     'hints': ['Pisalo mora vedeti, koliko je v škatli, PREDEN začne risati. Kateri blok je zato prvi?', 'Nato je program tak kot pri ogrevanju, le namesto števila pri pojdi uporabi škatlo.']},
    info('Spremenljivka se lahko spreminja 🌀', '''
<div class="box"><span class="sb var">spremeni <span class="vpill">dolžina</span> za <b>10</b></span> &nbsp;vrednosti v škatli prišteje 10</div>
<p class="big">Če je ta blok v zanki, je vsaka naslednja črta za 10 daljša. Tako nastane <b>spirala</b>.</p>'''),
    {'type': 'choose', 'title': 'Kako dolga je tretja črta?', 'intro': '''<div class="box"><span class="sb var">nastavi <span class="vpill">dolžina</span> na <b>10</b></span><br>
<span class="sb ctl">ponovi <b>3</b>-krat</span><br>
<span style="margin-left:26px" class="sb mot">pojdi <span class="vpill">dolžina</span> korakov</span><br>
<span style="margin-left:26px" class="sb var">spremeni <span class="vpill">dolžina</span> za <b>10</b></span><br>
<span class="sb ctl kon">konec ponovi</span></div>''',
     'options': [ch('10', why='10 je dolga samo prva črta. Po njej se dolžina poveča.'),
                 ch('30', True, 'Da: 10, nato 20, nato 30. Po tretji črti je v škatli 40, a črta je že narisana.'),
                 ch('40', why='40 je v škatli PO tretji črti. Tretja črta se nariše, ko je v škatli še 30.')],
     'hints': ['Zapiši si: 1. črta 10, nato prištej 10 …']},
    {'type': 'risar', 'title': 'Spirala', 'intro': 'Nariši spiralo: 12 črt, prva dolga 10, vsaka naslednja za 10 daljša. Največ <b>6 blokov</b>.',
     'tools': ['S10', 'FV', 'T90', 'A10'], 'loops': L, 'max': 6, 'solution': ['S10', 'N12', 'FV', 'T90', 'A10', K],
     'hints': ['Kakšna je prva črta? Kaj mora biti v škatli na začetku?', 'Po vsaki črti se pisalo obrne. Kaj se mora še zgoditi, da je naslednja črta daljša?', 'Koliko črt ima spirala? Toliko-krat se zanka ponovi. Preštej bloke: največ 6.']},
], 'Znaš uporabiti spremenljivko in jo spreminjati v zanki.')

# ---------------- 3 Pogoj ----------------
stran('3 Pogoj.html', 'Pogoj: če … potem', [
    info('Pogoj = vprašanje da ali ne', '''
<div class="box"><span class="sb ctl">če <span class="opill"><span class="vpill">dolžina</span> &gt; <b>60</b></span> potem</span><br>
<span style="margin-left:26px" class="sb pen">nastavi barvo pisala na <span class="cpill" style="background:#E6443C"></span> rdeča</span><br>
<span class="sb ctl kon">konec če</span></div>
<p class="big">Računalnik vpraša: »Ali je dolžina večja od 60?« Če je odgovor <b>da</b>, izvede bloke v »če«. Če je <b>ne</b>, jih preskoči.</p>
<p>To je romb iz diagrama poteka. <b>&gt;</b> pomeni večje, <b>&lt;</b> pomeni manjše.</p>'''),
    {'type': 'choose', 'title': 'Kakšna bo črta?', 'intro': '''<div class="box"><span class="sb var">nastavi <span class="vpill">dolžina</span> na <b>30</b></span><br>
<span class="sb ctl">če <span class="opill"><span class="vpill">dolžina</span> &gt; <b>60</b></span> potem</span><br>
<span style="margin-left:26px" class="sb pen">nastavi barvo pisala na <span class="cpill" style="background:#E6443C"></span> rdeča</span><br>
<span class="sb ctl kon">konec če</span><br>
<span class="sb mot">pojdi <span class="vpill">dolžina</span> korakov</span></div><p>Pisalo na začetku riše zeleno. Kakšno črto nariše?</p>''',
     'options': [ch('zeleno, dolgo 30', True, 'Tako je. 30 ni večje od 60, zato »če« preskoči in barva ostane zelena.'),
                 ch('rdečo, dolgo 30', why='Ali je 30 večje od 60? Ne. Zato se barva ne spremeni.'),
                 ch('rdečo, dolgo 60', why='60 je le meja v pogoju. Pisalo gre toliko, kolikor je v škatli: 30.')],
     'hints': ['Ali je 30 > 60?']},
    {'type': 'risar', 'title': 'Barvna spirala', 'intro': 'Nariši spiralo kot prej, a črte, ki so <b>daljše od 60</b>, naj bodo <b>rdeče</b>. Pogoj daj na začetek zanke. Največ <b>9 blokov</b>.',
     'tools': ['S10', 'FV', 'T90', 'A10', 'I>60', 'I<60', 'Cr', K], 'loops': L, 'max': 9,
     'solution': ['S10', 'N12', 'I>60', 'Cr', K, 'FV', 'T90', 'A10', K],
     'hints': ['Začni s programom spirale z prejšnjega koraka. Kaj mu manjka?', 'Pisalo mora pred vsako črto vprašati: ali je dolžina večja od 60? Kateri znak pomeni večje?', 'Pogoj ima svoj konec. V »če« je samo menjava barve, risanje je za »konec če«.']},
    {'type': 'risar', 'title': '🐞 Najdi hrošča', 'intro': 'Ta program bi moral narisati isto barvno spiralo, a je vsa rdeča. Zaženi ga, poišči hrošča in ga popravi.',
     'tools': ['S10', 'FV', 'T90', 'A10', 'I>60', 'I<60', 'Cr', K], 'loops': L, 'max': 9,
     'start': ['S10', 'N12', 'I<60', 'Cr', K, 'FV', 'T90', 'A10', K], 'solution': ['S10', 'N12', 'I>60', 'Cr', K, 'FV', 'T90', 'A10', K],
     'hints': ['Preberi pogoj na glas. Ali je prva črta (10) že rdeča? Zakaj?', 'Poglej znak v pogoju. &lt; pomeni manjše, &gt; pomeni večje. Katere črte naj bodo rdeče?', 'Ko je barva enkrat rdeča, ostane rdeča. Zato je hrošč samo v enem bloku.']},
    {'type': 'risar', 'stars': '★★', 'optional': True, 'title': 'Če … sicer', 'intro': 'Kratke črte (60 ali manj) naj bodo <b>vijolične</b>, daljše <b>rdeče</b>. Uporabi blok <b>sicer</b>: kar je za njim, se zgodi, ko je odgovor <b>ne</b>. Največ <b>11 blokov</b>.',
     'tools': ['S10', 'FV', 'T90', 'A10', 'I>60', 'Cr', 'Cv', 'E', K], 'loops': L, 'max': 11,
     'solution': ['S10', 'N12', 'I>60', 'Cr', 'E', 'Cv', K, 'FV', 'T90', 'A10', K],
     'hints': ['Pogoj vpraša: ali je dolžina večja od 60? Kaj naredi pisalo pri da in kaj pri ne?', 'Kar je pred »sicer«, se zgodi pri da. Kar je za njim, pri ne.']},
], 'Znaš uporabiti pogoj »če« in najti hrošča v pogoju.')

# ---------------- 4 Zapis v zvezek ----------------
stran('4 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek.', 'html': '''
<div class="zapis"><h3>POGOJI IN SPREMENLJIVKE</h3>
<p><b>Spremenljivka</b> je škatla z imenom, v kateri je ena vrednost. Primer: dolžina = 100.</p>
<p>nastavi dolžina na 10 (v škatlo da 10) · spremeni dolžina za 10 (prišteje 10)</p>
<p>Prednost: vrednost spremenim na enem mestu.</p>
<p><b>Pogoj</b> je vprašanje z odgovorom da ali ne. <b>če … potem</b> izvede bloke samo, če je odgovor da.<br><b>sicer</b>: bloki, ki se izvedejo, če je odgovor ne.</p>
<p>&gt; večje, &lt; manjše</p></div>'''},
], 'Zapis je v zvezku.')

# ---------------- 6 Izziv: Moj vzorec ----------------
stran('6 Izziv Moj vzorec.html', '★★ Izziv: Moj vzorec', [
    info('Ustvari svoj vzorec 🎨', '''
<p class="big">Zdaj ni pravilnih rešitev. Sestavi svoj vzorec s spremenljivko in pogojem.</p>
<div class="box">Ideje: spirala z obratom 120° ali 144° · spirala, ki spreminja dolžino za 3 in se ponovi 50-krat · tri barve s pogoji</div>
<p class="small">Ko ti je vzorec všeč, ga pokaži sosedu ali učitelju.</p>'''),
    {'type': 'risar', 'prosto': True, 'optional': True, 'title': 'Moj vzorec', 'intro': 'Sestavi program in klikni <b>▶ Zaženi</b>. Spreminjaj števila in opazuj, kaj se zgodi.',
     'tools': ['S5', 'S10', 'FV', 'F50', 'T45', 'T60', 'T90', 'T120', 'T144', 'A3', 'A5', 'A10', 'I>60', 'I<60', 'Cg', 'Cr', 'Cv', 'E', K],
     'loops': [4, 6, 12, 20, 36, 50], 'win': '✅ Tvoj vzorec! Poskusi še drugačna števila.'},
], 'Ustvaril/a si svoj vzorec. Bravo! 🎨')
