"""Samodejno preklika vse zaslone vseh strani v mapi in javi napake.
Uporaba: python3 preveri.py "<mapa ure>"   (potrebuje: pip install playwright && playwright install chromium)
Posnetki zaslonov gredo v <mapa ure>/../_posnetki-<ime ure>/ (ta mapa NI za objavo, izbriši jo)."""
import sys, pathlib
from playwright.sync_api import sync_playwright
out = pathlib.Path(sys.argv[1]); shots = pathlib.Path('/tmp') / ('posnetki-' + out.name.replace(' ', '_')); shots.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sorted(out.glob('*.html')):
        pg = b.new_page(viewport={'width': 1100, 'height': 600})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.goto(f.resolve().as_uri()); pg.wait_for_timeout(300)
        n = 0
        while n < 20:
            n += 1
            pg.screenshot(path=str(shots / f'{f.stem[:6]}_{n:02d}.png'), full_page=True)
            if pg.locator('.end').count(): break
            nxt = pg.locator('#next')
            if nxt.is_disabled():
                # grid: test real run of solution
                for _ in range(5):
                    if pg.locator('#hint').is_visible(): pg.click('#hint')
                if pg.locator('#solve').is_visible(): pg.click('#solve')
                elif pg.locator('.chk input').count(): pg.check('.chk input')
                elif pg.locator('#skip').is_visible(): pg.click('#skip'); continue
                elif pg.locator('.opt:not(:disabled)').count():
                    for k in range(pg.locator('.opt').count()):
                        if not nxt.is_disabled(): break
                        o = pg.locator('.opt').nth(k)
                        if o.is_enabled(): o.click()
                if pg.locator('.gridtask').count():
                    pg.click('.run'); pg.wait_for_timeout(5500)
                    print('  grid run:', pg.locator('.fb').inner_text()[:90])
            if nxt.is_disabled(): print('OBTIČAL na zaslonu', n, 'v', f.name); break
            pg.click('#next'); pg.wait_for_timeout(150)
        print(f.name, 'zaslonov', n, 'NAPAKE: ' + str(errs) if errs else 'brez napak')
    print('posnetki:', shots)
    b.close()
