# Računalništvo 6. do 9. razred, 20. 11. 2026 (predura): ura za učence, ki NE tekmujejo na Bobru
# (Bober je danes za 6. in 7. razred, mentor je zaseden s tekmovalci).
# LDN: vsebina VARNOST IN DIGITALNA IDENTITETA (gesla, dvostopenjska prijava, prepoznavanje prevar).
# Samostojna ura, okoli 25 minut osnovne poti + izziv za kvizom.
# Vsa gesla in sporočila v primerih so izmišljena.

# ---------------- 2 Močno geslo ----------------
stran('2 Mocno geslo.html', 'Močno geslo', [
    info('Geslo je ključ', '''
<p class="big">Tvoj račun je kot stanovanje, geslo pa je <b>ključ</b> 🔑. Kdor ima ključ, pride noter.</p>
<div class="box">Klikni odgovor. Če je narobe, ti stran pove zakaj. Če ne veš, kako začeti, klikni <b>Namig</b>.</div>'''),
    {'type': 'choose', 'title': 'Katero geslo je najmočnejše?', 'intro': 'Vsa gesla so izmišljena. Katero bi računalnik najtežje uganil?',
     'options': [ch('123456', why='To je eno najpogostejših gesel na svetu. Programi ga uganejo v trenutku.'),
                 ch('Luka2013', why='Ime in letnica rojstva. Kdor te pozna (ali tvoj profil), ga hitro ugane.'),
                 ch('geslo', why='Beseda iz slovarja. Programi najprej preizkusijo prav take besede.'),
                 ch('ModriSlon!plešeTango7', True, 'Tako je. Dolgo je, ima več besed, veliko črko, znak in številko.')],
     'hints': ['Računalnik ugiba zelo hitro. Kaj mu vzame največ časa?', 'Daljše geslo je veliko težje uganiti kot kratko.']},
    info('Recept za močno geslo', '''
<div class="box big">🧩 Sestavi <b>3 ali 4 naključne besede</b>, ki nimajo zveze s teboj.<br>➕ Dodaj številko in znak.</div>
<p>Primer recepta (ne uporabi ga!): <b>kava + oblak + kolo</b> → <b>KavaOblak!kolo42</b></p>
<p class="warn">Brez imen, rojstnih dni, imena psa ali kluba. To ljudje o tebi vedo ali najdejo na spletu.</p>'''),
    {'type': 'choose', 'title': 'Kaj je narobe?', 'intro': 'Maja ima geslo <b>Maja2013</b>. Pravi: »Saj ima veliko črko in številke!« Kaj je narobe?',
     'options': [ch('Nič, geslo je dobro.', why='Velika črka in številke same ne pomagajo, če je vsebina lahko uganljiva.'),
                 ch('Vsebuje njeno ime in letnico, ki ju drugi poznajo.', True, 'Da. Kdor jo pozna, najprej preizkusi prav ime in letnico.'),
                 ch('Je predolgo.', why='Ni predolgo, prej prekratko. Daljše je boljše.')],
     'hints': ['Pomisli, kaj o Maji vedo sošolci.']},
    {'type': 'choose', 'title': 'Isto geslo povsod?', 'intro': 'Jan ima zelo močno geslo in ga uporablja za šolo, igrice in e-pošto. Je to v redu?',
     'options': [ch('Da, saj je geslo močno.', why='Če ena igrica izgubi gesla (to se dogaja), ima napadalec ključ do vseh Janovih računov.'),
                 ch('Ne. Če kdo ukrade geslo z ene strani, odpre vse račune.', True, 'Tako je. Za vsak pomemben račun drugo geslo.'),
                 ch('Ne, ker se geslo obrabi.', why='Geslo se ne obrabi. Težava je, da en ukraden ključ odpre vsa vrata.')],
     'hints': ['Kaj se zgodi, če spletno stran z igrico nekdo vdre?']},
    {'type': 'match', 'title': 'Poveži', 'intro': 'Poveži pojem z razlago.', 'pairs': [
        ['Geslo', 'skrivnost, ki jo veš samo ti'],
        ['Dvostopenjska prijava', 'poleg gesla še koda na telefonu'],
        ['Upravitelj gesel', 'program, ki varno hrani vsa tvoja gesla'],
        ['Deljenje gesla', 'tega ne narediš niti s prijateljem']],
     'hints': ['Dvostopenjska = dva koraka: najprej geslo, nato še nekaj.']},
], 'Znaš sestaviti močno geslo in veš, zakaj ne isto geslo povsod.')

# ---------------- 3 Prepoznaj prevaro ----------------
stran('3 Prepoznaj prevaro.html', 'Prepoznaj prevaro', [
    info('Ribarjenje 🎣', '''
<p class="big">Prevarant ti pošlje sporočilo, ki je videti pravo. Želi, da klikneš povezavo in vpišeš geslo.</p>
<div class="box">Znaki prevare:<br>⏰ <b>mudi se</b> (»v 24 urah!«)<br>🎁 <b>prevelika nagrada</b> (»zastonj telefon«)<br>🔗 <b>čuden naslov</b> povezave<br>🔑 prosi za <b>geslo ali kodo</b></div>'''),
    {'type': 'choose', 'title': 'Sporočilo 1', 'intro': '''<div class="box">📩 <b>Od: podpora-skola@mail-varnost.xyz</b><br>Tvoj šolski račun bo IZBRISAN v 24 urah! Klikni tukaj in vpiši geslo, da ga rešiš.</div><p>Kaj narediš?</p>''',
     'options': [ch('Hitro kliknem, da ne izgubim računa.', why='Prav to prevarant želi: da se prestrašiš in ne razmisliš.'),
                 ch('Ne kliknem in povem učitelju ali staršem.', True, 'Odlično. Mudi se, čuden naslov, prosi za geslo: trije znaki prevare.'),
                 ch('Odgovorim in vprašam, ali je res.', why='Z odgovorom prevarantu poveš, da naslov deluje. Ne odgovarjaj.')],
     'hints': ['Poglej naslov pošiljatelja. Je to šola?', 'Prava šola te nikoli ne prosi za geslo po e-pošti.']},
    {'type': 'choose', 'title': 'Sporočilo 2', 'intro': '''<div class="box">💬 <b>Neznana številka:</b><br>Čestitamo! Izbran si za NAGRADO: nove slušalke. Pošlji nam kodo, ki ti jo bomo zdaj poslali po SMS.</div><p>Kaj je najbolj sumljivo?</p>''',
     'options': [ch('Da je sporočilo kratko.', why='Tudi prava sporočila so kratka. Dolžina ni znak.'),
                 ch('Prosijo za kodo iz SMS in obljubljajo nagrado, za katero se nisi prijavil/a.', True, 'Da. Koda iz SMS je ključ do tvojega računa. Nikoli je ne pošlji naprej.'),
                 ch('Da je napisano v slovenščini.', why='Prevaranti pišejo tudi v slovenščini. Jezik ni dober znak.')],
     'hints': ['Si se kam prijavil/a za slušalke?', 'Čemu služi koda, ki jo dobiš po SMS?']},
    {'type': 'choose', 'title': 'Sporočilo 3', 'intro': '''<div class="box">💬 <b>Prijatelj Tim (na igrici):</b><br>Hej, rabim tvoje geslo samo za 5 minut, da ti dam en skin zastonj 😉</div><p>Kaj narediš?</p>''',
     'options': [ch('Dam mu geslo, saj je prijatelj.', why='Morda Timov račun ni več v Timovih rokah. Prevaranti pogosto pišejo z ukradenih računov prijateljev.'),
                 ch('Ne dam gesla. Tima vprašam v živo, ali je res on.', True, 'Tako je. Geslo ne deliš z nikomer, in sumljivo prošnjo preveriš drugje.'),
                 ch('Dam mu geslo in ga potem spremenim.', why='V 5 minutah lahko spremeni geslo on in ti izgubiš račun.')],
     'hints': ['Kaj, če je nekdo vdrl v Timov račun?']},
    {'type': 'order', 'title': 'Kliknil/a sem povezavo. Kaj zdaj?', 'intro': 'Zgodi se. Uredi korake v pravi vrstni red.',
     'items': ['Takoj povem učitelju ali staršem.', 'Z njihovo pomočjo spremenim geslo za ta račun.', 'Na koncu vklopim še dvostopenjsko prijavo.'],
     'hints': ['Najprej poišči pomoč odraslega.', 'Dvostopenjsko prijavo vklopiš, ko je geslo že novo.']},
], 'Prepoznaš sporočilo, ki je prevara, in veš, kaj narediti.')

# ---------------- 4 Zapis v zvezek ----------------
stran('4 Zapis v zvezek.html', 'Zapis v zvezek', [
    {'type': 'check', 'title': 'Prepiši v zvezek', 'label': 'Zapis sem prepisal/a v zvezek.', 'html': '''
<div class="zapis"><h3>GESLA IN PREVARE</h3>
<p><b>Močno geslo</b>: 3 ali 4 naključne besede + številka + znak. Brez imen in rojstnih dni.</p>
<p>Za vsak pomemben račun <b>drugo geslo</b>. Gesla ne povem nikomur.</p>
<p><b>Dvostopenjska prijava</b>: geslo + koda na telefonu.</p>
<p><b>Ribarjenje</b> je prevara, ki hoče moje geslo. Znaki: mudi se, nagrada, čuden naslov, prosi za geslo ali kodo.</p>
<p>Če sem kliknil/a: povem odraslemu, spremenim geslo.</p></div>'''},
], 'Zapis je v zvezku.')

# ---------------- 6 Izziv ----------------
stran('6 Izziv Prevara ali ne.html', '★★ Izziv: Prevara ali ne?', [
    info('Detektiv 🕵️', '''
<p class="big">Ni vsako sporočilo prevara. Dober detektiv loči pravo od lažnega.</p>
<div class="box">Klikni odgovor. Če je narobe, ti stran pove zakaj.</div>'''),
    {'type': 'choose', 'title': 'Naslov povezave', 'intro': 'Katera povezava najverjetneje vodi na pravo stran banke <b>banka.si</b>?',
     'options': [ch('banka.si.prijava-varno.com', why='Pravi lastnik je tisto pred zadnjo piko in končnico: prijava-varno.com. To ni banka.si.'),
                 ch('banka.si/prijava', True, 'Da. Naslov se začne z banka.si, vse za poševnico je le stran znotraj nje.'),
                 ch('banka-si.net', why='To je čisto druga stran (banka-si.net), le ime je podobno.')],
     'hints': ['Poglej, kaj je tik pred prvo poševnico /.', 'Pri banka.si.prijava-varno.com se naslov konča s prijava-varno.com.']},
    {'type': 'choose', 'title': 'Pravo ali ne?', 'intro': '''<div class="box">📩 Učiteljica ti v spletni učilnici napiše: »Naloga za petek je v mapi Računalništvo.«</div><p>Je to prevara?</p>''',
     'options': [ch('Da, vsako sporočilo je sumljivo.', why='Ne vsako. Ni nujnosti, ni nagrade, ne prosi za geslo, pride po znani poti.'),
                 ch('Najverjetneje ne: ne prosi za geslo, ni nujnosti in pride iz spletne učilnice.', True, 'Tako je. Detektiv išče znake, ne panike.')],
     'hints': ['Preveri štiri znake prevare. Ali je kateri tu?']},
    {'type': 'choose', 'title': 'Lažno spletno mesto', 'intro': 'Stran je videti kot prava, ima pa logotip malo razmazan in naslov <b>gmaiI.com</b> (z veliko črko I namesto l). Kaj to pomeni?',
     'options': [ch('Nič, logotip se je slabo naložil.', why='Razmazan logotip in podoben naslov skupaj sta resen znak.'),
                 ch('Prevarant je naredil kopijo prave strani s skoraj enakim naslovom.', True, 'Da. Črko l zamenjajo z I ali 0 z O, da tega ne opaziš.')],
     'hints': ['Preberi naslov črko za črko.']},
], 'Pravi detektiv! 🕵️', )
