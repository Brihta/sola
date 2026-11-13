# Računalništvo 6. do 9. razred, 9. ura »Šolsko tekmovanje Bober« (13. 11. 2026, predura).
# LDN/PRIPRAVE: sklop 3 Mladi bober, 9. ura »Šolsko tekmovanje Mladi bober« (okno 9. do 20. 11. 2026).
# Tekmovanje samo zavzame skoraj vso uro, zato je tu le kratka priprava (okoli 3 minute) in povezava.
# Brez kviza: po tekmovanju ni časa, rezultate potrdi mentor na bober.acm.si.
# Namenoma brez trditev o točkovanju in trajanju (ne smemo zavesti učencev).

stran('2 Pred tekmovanjem.html', 'Pred tekmovanjem', [
    info('Danes je tekmovanje Bober 🦫', '''
<p class="big">Danes rešuješ <b>pravo</b> tekmovanje. Rešuješ <b>sam/a</b>.</p>
<div class="box">Najprej dve hitri vprašanji o pravilih. Klikni odgovor. Če je narobe, ti stran pove zakaj. Če ne veš, klikni Namig.</div>'''),
    {'type': 'choose', 'abcd': True, 'title': 'Zataknilo se je', 'intro': 'Pri eni nalogi razmišljaš že dolgo in ne veš, kako naprej. Kaj narediš?',
     'options': [ch('Vprašam soseda, kaj je izbral.', why='Na tekmovanju rešuješ sam/a. Tudi sosed rešuje svoje naloge.'),
                 ch('Nalogo preskočim, rešim druge in se vrnem, če ostane čas.', True, 'Tako je. Čas teče za vse naloge, zato ne obtiči pri eni.'),
                 ch('Čakam pri tej nalogi, dokler ne pride ideja.', why='Tako lahko porabiš čas, ki bi ga potreboval/a za naloge, ki jih znaš.'),
                 ch('Zaprem zavihek in začnem znova.', why='Zapiranje zavihka ti ne pomaga, lahko pa izgubiš odgovore.')],
     'hints': ['Čas je skupen za vse naloge.']},
    {'type': 'choose', 'abcd': True, 'title': 'Pomoč pri tekmovanju', 'intro': 'Kaj je pri tekmovanju dovoljeno?',
     'options': [ch('Odpreti drug zavihek in poiskati rešitev na spletu.', why='Na spletu ne iščeš. Rešuješ s svojo glavo.'),
                 ch('Pomagati sošolcu, ki ne ve.', why='Vsak rešuje sam. Pomagal/a mu boš po tekmovanju.'),
                 ch('Dvigniti roko, če se ti zatakne računalnik ali prijava.', True, 'Da. Pri tehnični težavi pokliči učitelja. Pri nalogah pa ne more pomagati.'),
                 ch('Klepetati s sosedom o nalogah.', why='S tem motiš druge in to ni dovoljeno.')],
     'hints': ['Učitelj ti pomaga samo, če nekaj ne deluje.']},
    {'type': 'check', 'title': 'Pripravljen/a?', 'label': 'Pripravljen/a sem. Grem na tekmovanje.', 'html': '''
<div class="box">1️⃣ Naslednji korak odpre stran <b>bober.acm.si</b>.<br>
2️⃣ Prijaviš se s podatki, ki ti jih da <b>učitelj</b>.<br>
3️⃣ Vsako nalogo preberi <b>do konca</b>, šele nato odgovori.<br>
4️⃣ Ko končaš, preveri odgovore in klikni <b>Zaključi</b>.</div>
<p class="small">Srečno! 🍀</p>'''},
], 'Pravila poznaš. Klikni Naprej in začni tekmovanje.')
