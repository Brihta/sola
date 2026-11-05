# Računalništvo 6. do 9. razred, 8. ura »Vaja za Bober« (6. 11. 2026, predura).
# LDN/PRIPRAVE: sklop 3 Mladi bober, 8. ura »Naloge Mladega bobra prejšnjih let, razlaga rešitev«.
# Povezave so z uradne strani https://tekmovanja.acm.si/?q=bober%2Fnaloge-re%C5%A1itve (vadnica za goste).
# Po Ninovi želji (5. 11.) samo korak z vajami: brez uvoda, kviza in knjižic z rešitvami.
# Vadnica med reševanjem ne pove, ali je odgovor pravilen; po »Zaključi« pokaže stran Rezultati
# (za vsako odgovorjeno nalogo Pravilen ali Napačen odgovor in točke). Preverjeno 5. 11. 2026 (2025/26, 6. in 7. r).
# Vrstni red odgovorov se v vadnici premeša za vsak poskus, zato list za odgovore s črkami ne bi deloval.

VADNICA = 'https://bober.acm.si/simple/guest/compete/'
LETA = [
    ('2025/26', '532', '533'),
    ('2024/25', '492', '493'),
    ('2023/24', '392', '393'),
    ('2022/23', '410', '411'),
]


def gumb(url, besedilo):
    return (f'<a href="{url}" target="_blank" rel="noopener" style="display:inline-block;padding:6px 12px;'
            f'border-radius:8px;background:#e8f1ff;border:2px solid #4a7bd0;color:#1d3f7a;font-weight:700;'
            f'text-decoration:none;margin:2px">{besedilo} ↗</a>')


def tabela():
    vrstice = ''.join(
        f'<tr><td style="padding:6px"><b>{leto}</b></td>'
        f'<td style="padding:6px">{gumb(VADNICA + a + "/", "6. in 7. r")}</td>'
        f'<td style="padding:6px">{gumb(VADNICA + b + "/", "8. in 9. r")}</td></tr>'
        for leto, a, b in LETA)
    zvezdice = (
        '<tr><td style="padding:6px"><b>★★ državno 2024/25</b></td>'
        f'<td style="padding:6px" colspan="2">{gumb("https://bober.acm.si/simple/guest/competition/drzavno2024gostje/", "Izberi skupino")}</td></tr>')
    return ('<table style="border-collapse:collapse;margin:8px 0">'
            '<tr><th style="padding:6px;text-align:left">Šolsko tekmovanje</th><th style="padding:6px;text-align:left">Vaja</th>'
            '<th style="padding:6px;text-align:left">Vaja</th></tr>'
            + vrstice + zvezdice + '</table>')


# ---------------- 2 Naloge prejšnjih let ----------------
stran('2 Naloge prejsnjih let.html', 'Naloge prejšnjih let', [
    {'type': 'check', 'title': 'Reši prave Bobrove naloge', 'label': 'Rešil/a sem vsaj eno leto in točke zapisal/a v zvezek.', 'html': f'''
<div class="box">1️⃣ Izberi leto in <b>svojo skupino</b> (6. in 7. r ali 8. in 9. r). Odpre se nov zavihek.<br>
2️⃣ Če se pokaže obrazec: vpiši samo ime, priimek <b>Vaja</b>, datum 1. 1., kodo pusti <b>prazno</b>.<br>
3️⃣ Čas teče zgoraj desno. Med reševanjem ne izveš, ali je odgovor pravilen, tako kot na tekmovanju.<br>
4️⃣ Ko končaš, klikni <b>Zaključi</b>. Pokažejo se <b>rezultati</b>: pri vsaki nalogi piše, ali je pravilno.</div>
{tabela()}
<div class="zapis"><h3>BOBER: VAJA</h3>
<p>Leto: ______ &nbsp; Skupina: ______</p>
<p>Pravilnih nalog: ______ od ______</p>
<p>Naloga, ki sem jo zgrešil/a: ______________</p></div>
<p class="small">Če ti ostane čas, vzemi naslednje leto. ★★ Državno tekmovanje je težje, za tiste, ki želijo več.</p>'''},
], 'Treniral/a si na pravih nalogah. Srečno na tekmovanju! 🦫')
