# Računalništvo 6. do 9. razred, 8. ura »Vaja za Bober« (6. 11. 2026, predura).
# LDN/PRIPRAVE: sklop 3 Mladi bober, 8. ura »Naloge Mladega bobra prejšnjih let, razlaga rešitev«.
# Vse povezave so z uradne strani https://tekmovanja.acm.si/?q=bober%2Fnaloge-re%C5%A1itve (vadnica za goste
# in knjižice z rešitvami). Pravih nalog ne prepisujemo v repozitorij; vaje na strani 2 so izvirne.
# Vrstni red: kratek uvod, kviz (pravila in strategija), nato do konca ure prave naloge prejšnjih let.

VADNICA = 'https://bober.acm.si/simple/guest/compete/'
LETA = [
    ('2025/26', '532', '533', 'https://ucilnica.acm.si/mod/resource/view.php?id=3016'),
    ('2024/25', '492', '493', 'https://ucilnica.acm.si/mod/resource/view.php?id=2864'),
    ('2023/24', '392', '393', 'https://ucilnica.acm.si/mod/resource/view.php?id=2726'),
    ('2022/23', '410', '411', 'https://dajmi.fri.uni-lj.si/bober/Bober-2022-23-solsko.pdf'),
]


def gumb(url, besedilo):
    return (f'<a href="{url}" target="_blank" rel="noopener" style="display:inline-block;padding:6px 12px;'
            f'border-radius:8px;background:#e8f1ff;border:2px solid #4a7bd0;color:#1d3f7a;font-weight:700;'
            f'text-decoration:none;margin:2px">{besedilo} ↗</a>')


def tabela():
    vrstice = ''.join(
        f'<tr><td style="padding:6px"><b>{leto}</b></td>'
        f'<td style="padding:6px">{gumb(VADNICA + a + "/", "6. in 7. r")}</td>'
        f'<td style="padding:6px">{gumb(VADNICA + b + "/", "8. in 9. r")}</td>'
        f'<td style="padding:6px">{gumb(pdf, "📖 Rešitve")}</td></tr>'
        for leto, a, b, pdf in LETA)
    zvezdice = (
        '<tr><td style="padding:6px"><b>★★ državno 2024/25</b></td>'
        f'<td style="padding:6px" colspan="2">{gumb("https://bober.acm.si/simple/guest/competition/drzavno2024gostje/", "Izberi kategorijo")}</td>'
        f'<td style="padding:6px">{gumb("https://ucilnica.acm.si/mod/resource/view.php?id=2911", "📖 Rešitve")}</td></tr>')
    return ('<table style="border-collapse:collapse;margin:8px 0">'
            '<tr><th style="padding:6px;text-align:left">Šolsko tekmovanje</th><th style="padding:6px;text-align:left">Vaja</th>'
            '<th style="padding:6px;text-align:left">Vaja</th><th style="padding:6px;text-align:left">Naloge z razlago</th></tr>'
            + vrstice + zvezdice + '</table>')


# ---------------- 2 Kako poteka Bober ----------------
stran('2 Kako poteka Bober.html', 'Kako poteka Bober?', [
    info('Kaj je Bober?', '''
<p class="big"><b>Bober</b> 🦫 je mednarodno tekmovanje iz <b>računalniškega mišljenja</b>. Ne programiraš, rešuješ uganke.</p>
<div class="box big">Šolsko tekmovanje bo ta mesec, na računalniku. Danes treniraš na <b>pravih nalogah prejšnjih let</b>.</div>
<p class="small">Klikni zeleni gumb <b>Naslednja naloga</b>.</p>'''),
    info('Dve kategoriji', '''
<p class="big">V osnovni šoli tekmujeta dve skupini:</p>
<div class="box big">🟢 <b>6. in 7. razred</b><br>🔵 <b>8. in 9. razred</b></div>
<p>Vsaka skupina ima svoje naloge. Vedno izberi skupino <b>svojega razreda</b>.</p>'''),
    {'type': 'choose', 'title': 'Katero skupino izbereš?',
     'intro': '<div>Klikni odgovor. Če je narobe, ti stran pove zakaj. Če ne veš, kako začeti, klikni Namig.</div><div class="big">Luka hodi v <b>8. razred</b>. Katero skupino izbere v vadnici?</div>',
     'options': [ch('6. in 7. razred', why='Te naloge so za mlajše. Luka je v 8. razredu.'),
                 ch('8. in 9. razred', True, 'Tako je. 8. razred spada v skupino 8. in 9. razred.'),
                 ch('Srednja šola', why='Te naloge so za dijake. Luka je še v osnovni šoli.'),
                 ch('6. in 7. razred HU', why='HU pomeni naloge v madžarščini.')],
     'hints': ['Poišči skupino, v kateri je številka 8.']},
    info('Kako rešiš Bobrovo nalogo', '''
<div class="box big">1️⃣ Preberi <b>celo</b> nalogo, tudi zadnjo poved.<br>
2️⃣ Poglej, kaj vprašanje <b>točno</b> sprašuje.<br>
3️⃣ Preizkusi odgovore in <b>izloči</b> napačne.<br>
4️⃣ Če obtičiš, nalogo <b>preskoči</b> in se vrni na koncu.</div>
<p>Zdaj poskusi dve vaji v slogu Bobra.</p>'''),
    {'type': 'choose', 'abcd': True, 'title': 'Vaja 1: Kup krožnikov',
     'intro': '<div>Ana zlaga krožnike na kup, enega na drugega: najprej 🔴, nato 🔵, nato 🟢.</div>'
              '<div>Nato <b>vzame 1 krožnik z vrha</b>, položi 🟡 in spet <b>vzame 2 krožnika z vrha</b>.</div>'
              '<div class="big">Kateri krožnik ostane na kupu?</div>',
     'options': [ch('🔴', True, '🟢 vzame. Na kupu je 🔴 🔵, doda 🟡. Vzame 🟡 in 🔵. Ostane 🔴.'),
                 ch('🔵', why='🔵 je bil pod 🟡. Ko Ana vzame 2 krožnika, vzame 🟡 in nato 🔵.'),
                 ch('🟢', why='🟢 je bil na vrhu, zato ga je Ana vzela prvega.'),
                 ch('🟡', why='🟡 je bil zadnji položen, zato je na vrhu in ga Ana vzame.')],
     'hints': ['Z vrha vedno vzameš tistega, ki si ga položil/a zadnjega.',
               'Zapiši kup od spodaj navzgor: 🔴 🔵 🟢. Nato sledi korakom enega za drugim.']},
    {'type': 'choose', 'abcd': True, 'title': 'Vaja 2: Lučke',
     'intro': '<div>Bobri pišejo števila z lučkami. Vsaka lučka ima svojo vrednost:</div>'
              '<div class="big">8 &nbsp; 4 &nbsp; 2 &nbsp; 1</div>'
              '<div>Število dobiš tako, da sešteješ vrednosti <b>prižganih</b> lučk. Na primer 💡⚫⚫💡 je 8 + 1 = 9.</div>'
              '<div class="big">Koliko je 💡⚫💡💡 ?</div>',
     'options': [ch('7', why='Prva lučka je prižgana in je vredna 8. Že sama je več kot 7.'),
                 ch('11', True, '8 + 2 + 1 = 11. Druga lučka (4) je ugasnjena.'),
                 ch('13', why='Druga lučka (4) je ugasnjena, zato je ne prišteješ.'),
                 ch('15', why='15 bi bilo, če bi gorele vse štiri lučke.')],
     'hints': ['Pod vsako lučko si zapiši njeno vrednost: 8, 4, 2, 1.', 'Seštej samo vrednosti pod 💡.']},
    {'type': 'choose', 'title': 'Ko obtičiš', 'intro': '<div class="big">Pri eni nalogi ne najdeš odgovora že nekaj minut. Kaj narediš?</div>',
     'options': [ch('Vprašam soseda.', why='Na tekmovanju vsak rešuje sam.'),
                 ch('Nalogo preskočim in se k njej vrnem, ko rešim ostale.', True, 'Tako je. Najprej poberi točke pri nalogah, ki jih znaš.'),
                 ch('Ostanem pri njej, dokler je ne rešim.', why='Tako ti zmanjka časa za lažje naloge.'),
                 ch('Kliknem kateri koli odgovor in grem naprej.', why='Slepo ugibanje redko pomaga. Raje se vrni, ko imaš čas za razmislek.')],
     'hints': ['Pomisli, kako v omejenem času rešiš čim več nalog.']},
    info('Vadnica: prijava kot gost', '''
<p class="big">Prave naloge rešuješ v <b>vadnici</b> na strani bober.acm.si. Odpre se obrazec <b>Registracija</b>:</p>
<div class="box">👤 <b>Ime:</b> samo tvoje ime<br>👤 <b>Priimek:</b> napiši <b>Vaja</b><br>📅 <b>Datum rojstva:</b> izberi 1. 1.<br>🔑 <b>Koda:</b> pusti <b>prazno</b></div>
<p class="warn">Na tujih straneh ne vpisuj celega imena in rojstnega dne, kadar to ni potrebno.</p>'''),
    {'type': 'choose', 'title': 'Kaj vpišeš pri Koda?', 'intro': '<div class="big">V vadnici za goste vidiš polje <b>Koda</b>. Kaj narediš?</div>',
     'options': [ch('Polje pustim prazno.', True, 'Tako je. Za vajo koda ni potrebna.'),
                 ch('Vpišem svoje geslo za Arnes.', why='Gesla nikoli ne vpisuj na tuje strani. Polje pusti prazno.'),
                 ch('Vpišem svojo rojstno letnico.', why='Za vajo koda ni potrebna. Polje pusti prazno.')],
     'hints': ['Gost ne potrebuje kode.']},
    {'type': 'choose', 'title': 'Kdaj pogledaš rešitve?', 'intro': '<div>Pri vsakem letu je tudi gumb <b>📖 Rešitve</b>: knjižica z nalogami, rešitvami in razlago.</div><div class="big">Kdaj jo odpreš?</div>',
     'options': [ch('Takoj, da hitro vidim pravilne odgovore.', why='Na tekmovanju bodo nove naloge. Naučiš se samo, če najprej misliš sam/a.'),
                 ch('Ko vajo oddam: preberem razlago nalog, ki sem jih zgrešil/a.', True, 'Tako je. Iz razlage napake se naučiš največ.'),
                 ch('Nikoli, rešitve so za učitelja.', why='Knjižica je za vse. Razlaga ti pove, kako razmišljati naslednjič.')],
     'hints': ['Kdaj se iz rešitve res kaj naučiš: preden ali potem ko si poskusil/a sam/a?']},
], 'Veš, kako poteka Bober in kako boš vadil/a.')

# ---------------- 4 Naloge prejšnjih let ----------------
stran('4 Naloge prejsnjih let.html', 'Naloge prejšnjih let', [
    {'type': 'check', 'title': 'Reši prave Bobrove naloge', 'label': 'Rešil/a sem vsaj eno leto in v zvezek zapisal/a razlago ene naloge.', 'html': f'''
<div class="box">1️⃣ Izberi leto in <b>svojo skupino</b> (6. in 7. r ali 8. in 9. r). Odpre se nov zavihek.<br>
2️⃣ Prijavi se kot gost: ime, priimek <b>Vaja</b>, datum 1. 1., koda prazna.<br>
3️⃣ Reši vse naloge, nato vajo končaj.<br>
4️⃣ Šele zdaj odpri <b>📖 Rešitve</b> istega leta. Poišči nalogo, ki jo nisi znal/a (Ctrl + F in ime naloge).</div>
{tabela()}
<div class="zapis"><h3>BOBER: VAJA</h3>
<p>Leto: ______ &nbsp; Skupina: ______</p>
<p>Naloga, ki sem jo zgrešil/a: ______________</p>
<p>Pravilni odgovor in <b>zakaj</b> (s svojimi besedami): ______________</p></div>
<p class="small">Ko končaš eno leto, vzemi naslednje. ★★ Državno tekmovanje je težje, za tiste, ki želijo več.</p>'''},
], 'Treniral/a si na pravih nalogah. Srečno na tekmovanju! 🦫')
