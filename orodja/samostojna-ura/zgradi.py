#!/usr/bin/env python3
"""Zgradi samostojne HTML strani za korake učne ure.

Uporaba:  python3 zgradi.py <opis-ure.py> "<mapa ure v gradiva/...>"

<opis-ure.py> je navaden Python, ki kliče stran(...). Na voljo so:
  stran(ime_datoteke, naslov, zasloni, besedilo_konca)
  info(naslov, html)              zaslon z razlago (Naprej je takoj odklenjen)
  ch(besedilo, ok=False, why='')  možnost za zaslon 'choose'
  slika(pot)                      PNG/JPG kot data: URI (pot relativno na opis ure)
Vrste zaslonov in pravila so v README.md. Primer: primer-7-ura-zapis-algoritma.py
"""
import base64, json, os, runpy, sys

TU = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(TU, 'style.css'), encoding='utf-8').read()
JS = open(os.path.join(TU, 'engine.js'), encoding='utf-8').read()


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    opis, izhod = os.path.abspath(sys.argv[1]), sys.argv[2]
    os.makedirs(izhod, exist_ok=True)
    mapa_opisa = os.path.dirname(opis)
    narejeno = []

    def stran(ime, naslov, zasloni, konec='Ta korak je opravljen.'):
        if not ime.endswith('.html'):
            ime += '.html'
        data = json.dumps({'title': naslov, 'screens': zasloni, 'endText': konec}, ensure_ascii=False)
        html = (f'<!doctype html><html lang="sl"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{naslov}</title>'
                f'<style>{CSS}</style></head><body><div id="app"></div>'
                f'<script>window.PAGE={data};</script><script>{JS}</script></body></html>')
        with open(os.path.join(izhod, ime), 'w', encoding='utf-8') as f:
            f.write(html)
        narejeno.append(ime)

    def slika(pot):
        pot = os.path.join(mapa_opisa, pot)
        vrsta = 'png' if pot.lower().endswith('.png') else 'jpeg'
        return f'data:image/{vrsta};base64,' + base64.b64encode(open(pot, 'rb').read()).decode()

    runpy.run_path(opis, init_globals={
        'stran': stran, 'slika': slika,
        'info': lambda naslov, html: {'type': 'info', 'title': naslov, 'html': html},
        'ch': lambda t, ok=False, why='': {'t': t, 'ok': ok, 'why': why},
    })
    for n in narejeno:
        print('narejeno:', os.path.join(izhod, n))


if __name__ == '__main__':
    main()
