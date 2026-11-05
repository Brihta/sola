# Računalništvo 6. do 9. razred, 8. ura »Vaja za Bober« (6. 11. 2026, predura).
# LDN/PRIPRAVE: sklop 3 Mladi bober, 8. ura »Naloge Mladega bobra prejšnjih let, razlaga rešitev«.
# Povezave so z uradne strani https://tekmovanja.acm.si/?q=bober%2Fnaloge-re%C5%A1itve (vadnica za goste).
# Po Ninovi želji (5. 11.) samo korak z vajami: brez uvoda, kviza in knjižic z rešitvami.
# Vadnica med reševanjem ne pove, ali je odgovor pravilen; po »Zaključi« pokaže stran Rezultati
# (za vsako odgovorjeno nalogo Pravilen ali Napačen odgovor in točke). Preverjeno 5. 11. 2026 (2025/26, 6. in 7. r).
# Učenec rezultat vpiše v kviz »Samoocena Bober <leto> <skupina>« (vsaka naloga: Pravilen, Napačen, Nisem odgovoril/a);
# ti kvizi nimajo pravila 50 % (supabase_kvizi_samoocena.sql). Učitelj vidi točke in uspešnost po nalogah.
# Vrstni red odgovorov se v vadnici premeša za vsak poskus, zato list za odgovore s črkami ne bi deloval.

VADNICA = 'https://bober.acm.si/simple/guest/compete/'
LETA = [
    ('2025/26', '532', '533'),
    ('2024/25', '492', '493'),
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
    return ('<table style="border-collapse:collapse;margin:8px 0">'
            '<tr><th style="padding:6px;text-align:left">Šolsko tekmovanje</th><th style="padding:6px;text-align:left">Vaja</th>'
            '<th style="padding:6px;text-align:left">Vaja</th></tr>'
            + vrstice + '</table>')


# ---------------- 2 Naloge prejšnjih let ----------------
stran('2 Naloge prejsnjih let.html', 'Naloge prejšnjih let', [
    {'type': 'check', 'title': 'Reši prave Bobrove naloge', 'label': 'Vajo sem končal/a in vidim stran Rezultati.', 'html': f'''
<div class="box">1️⃣ Izberi leto in <b>svojo skupino</b> (6. in 7. r ali 8. in 9. r). Odpre se nov zavihek.<br>
2️⃣ Če se pokaže obrazec: vpiši samo ime, priimek <b>Vaja</b>, datum 1. 1., kodo pusti <b>prazno</b>.<br>
3️⃣ Čas teče zgoraj desno. Med reševanjem ne izveš, ali je odgovor pravilen, tako kot na tekmovanju.<br>
4️⃣ Ko končaš, klikni <b>Zaključi</b>. Pokažejo se <b>rezultati</b>: pri vsaki nalogi piše, ali je pravilno.<br>
5️⃣ Zavihka z rezultati <b>ne zapri</b>. Na Brihti odpri korak z <b>istim letom in skupino</b> (npr. 2025-26, 6. in 7. r) in prepiši, kaj piše pri vsaki nalogi.</div>
{tabela()}
<p class="small">Če ti ostane čas, reši še drugo leto in vpiši tudi ta rezultat.</p>'''},
], 'Treniral/a si na pravih nalogah. Srečno na tekmovanju! 🦫')
