/* Brihta samostojna ura: zasloni z nalogami, ki se preverijo sami. */
(function () {
  const $ = (h) => { const d = document.createElement('div'); d.innerHTML = h.trim(); return d.firstElementChild; };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const KEY = 'brihta_ura7:' + location.pathname.split('/').pop();
  const load = () => { try { return parseInt(localStorage.getItem(KEY) || '0', 10) || 0; } catch (e) { return 0; } };
  const save = (v) => { try { localStorage.setItem(KEY, String(v)); } catch (e) {} };

  const tell = (stanje) => { try { if (window.parent !== window) window.parent.postMessage({ tip: 'brihta-korak', stanje }, '*'); } catch (e) {} };
  const P = window.PAGE;
  const screens = P.screens.concat([{ type: 'end' }]);
  let cur = Math.min(load(), screens.length - 1);
  let best = cur;

  const app = document.getElementById('app');
  app.innerHTML = `
    <header><h1>${esc(P.title)}</h1><div class="dots" id="dots"></div></header>
    <main id="card"></main>
    <footer>
      <button class="btn ghost" id="back">◀ Nazaj</button>
      <span class="sp"></span>
      <button class="btn hint" id="hint">💡 Namig</button>
      <button class="btn ghost" id="solve" hidden>Pokaži rešitev</button>
      <button class="btn ghost" id="skip" hidden>Preskoči</button>
      <button class="btn go" id="next" disabled>Naslednja naloga ▶</button>
    </footer>`;
  const card = document.getElementById('card');
  const bNext = document.getElementById('next'), bBack = document.getElementById('back');
  const bHint = document.getElementById('hint'), bSolve = document.getElementById('solve'), bSkip = document.getElementById('skip');

  function dots() {
    const d = document.getElementById('dots');
    d.innerHTML = screens.slice(0, -1).map((s, i) => `<span class="dot${i < best || i < cur ? ' ok' : ''}${i === cur ? ' now' : ''}"></span>`).join('') +
      `<span class="cnt">${Math.min(cur + 1, screens.length - 1)} / ${screens.length - 1}</span>`;
  }

  let solver = null, hintN = 0;
  function done(msg) {
    bNext.disabled = false; bNext.classList.add('pulse');
    bHint.hidden = true; bSolve.hidden = true; bSkip.hidden = true;
    if (cur + 1 > best) { best = cur + 1; save(best); }
    if (msg) feedback(msg, 'ok');
    dots();
  }
  function feedback(msg, kind) {
    let f = card.querySelector('.fb');
    if (!f) { f = $('<div class="fb"></div>'); card.appendChild(f); }
    f.className = 'fb ' + (kind || ''); f.innerHTML = msg;
    if (kind === 'bad') { f.classList.remove('shake'); void f.offsetWidth; f.classList.add('shake'); }
  }

  function show(i) {
    cur = i; const s = screens[i];
    card.innerHTML = ''; solver = null; hintN = 0;
    bNext.classList.remove('pulse');
    bBack.disabled = i === 0;
    const hints = s.hints || [];
    bHint.hidden = !hints.length; bSolve.hidden = true;
    bSkip.hidden = !s.optional;
    bNext.hidden = s.type === 'end';
    if (s.stars) card.appendChild($(`<div class="stars">${s.stars} izziv</div>`));
    if (s.title) card.appendChild($(`<h2>${s.title}</h2>`));
    if (s.intro) card.appendChild($(`<p class="intro">${s.intro}</p>`));
    const R = TYPES[s.type];
    const r = R(s, card);
    solver = r && r.solve;
    const already = i < best;
    bNext.disabled = !(s.type === 'info' || already);
    if (s.type === 'info') { if (i + 1 > best) { best = i + 1; save(best); } bHint.hidden = true; }
    if (already && s.type !== 'info' && s.type !== 'end') { bHint.hidden = true; feedback('To nalogo si že rešil/a. Lahko jo rešiš še enkrat ali klikneš Naprej.', 'ok'); }
    dots();
    card.scrollTop = 0; window.scrollTo(0, 0);
  }

  bNext.onclick = () => { if (cur < screens.length - 1) show(cur + 1); };
  bBack.onclick = () => { if (cur > 0) show(cur - 1); };
  bSkip.onclick = () => { if (cur + 1 > best) { best = cur + 1; save(best); } show(cur + 1); };
  bHint.onclick = () => {
    const h = screens[cur].hints || [];
    if (hintN < h.length) { feedback('💡 ' + h[hintN], 'hint'); hintN++; }
    if (hintN >= h.length && solver) { bHint.hidden = true; bSolve.hidden = false; }
  };
  bSolve.onclick = () => { if (solver) { solver(); feedback('Tukaj je rešitev. Dobro si jo oglej, nato klikni Naprej.', 'hint'); done(); } };

  /* ---------- vrste zaslonov ---------- */
  const TYPES = {};
  TYPES.info = (s, c) => { c.appendChild($(`<div class="body">${s.html}</div>`)); };
  TYPES.end = (s, c) => {
    c.appendChild($(`<div class="end"><div class="big">🎉</div><h2>Končano!</h2>
      <p>${esc(P.endText || 'Ta korak je opravljen.')}</p>
      <p class="arrow">Zdaj klikni velik gumb <b>»Naprej«</b> spodaj desno, pod tem okvirjem. ⬇</p>
      <button class="btn ghost" id="again">Začni ta korak znova</button></div>`));
    c.querySelector('#again').onclick = () => show(0);
    tell('koncano');
  };
  TYPES.check = (s, c) => {
    c.appendChild($(`<div class="body">${s.html}</div>`));
    const l = $(`<label class="chk"><input type="checkbox"> ${s.label}</label>`); c.appendChild(l);
    const x = l.querySelector('input');
    x.onchange = () => { if (x.checked) done('Odlično.'); };
    return { solve: () => { x.checked = true; } };
  };

  TYPES.choose = (s, c) => {
    const box = $('<div class="opts"></div>'); c.appendChild(box);
    const btns = shuffle(s.options).map((o) => {
      const b = $(`<button class="opt">${o.t}</button>`);
      b.onclick = () => {
        if (o.ok) { btns.forEach((x) => (x.disabled = true)); b.classList.add('good'); done('✅ ' + (o.why || 'Pravilno!')); }
        else { b.classList.add('bad'); b.disabled = true; feedback('❌ ' + (o.why || 'Ne še. Poskusi drugo možnost.'), 'bad'); }
      };
      box.appendChild(b); b._o = o; return b;
    });
    return { solve: () => btns.forEach((b) => { b.disabled = true; if (b._o.ok) b.classList.add('good'); }) };
  };

  TYPES.order = (s, c) => {
    const list = $('<ol class="olist"></ol>'), pool = $('<div class="pool"></div>');
    c.appendChild($('<p class="small">Klikaj korake v pravem vrstnem redu. Najprej tistega, ki je prvi.</p>'));
    c.appendChild(list); c.appendChild(pool);
    let k = 0;
    const btns = shuffle(s.items.map((t, i) => ({ t, i }))).map((o) => {
      const b = $(`<button class="chip">${o.t}</button>`);
      b.onclick = () => {
        if (o.i === k) { list.appendChild($(`<li>${o.t}</li>`)); b.remove(); k++; if (k === s.items.length) done('✅ Pravi vrstni red!'); else feedback('Dobro. Kaj pride naslednje?', ''); }
        else { b.classList.add('wob'); setTimeout(() => b.classList.remove('wob'), 400); feedback('❌ Ne še. ' + (k === 0 ? 'Kaj narediš čisto na začetku?' : 'Kaj moraš narediti pred tem?'), 'bad'); }
      };
      pool.appendChild(b); return b;
    });
    return { solve: () => { list.innerHTML = s.items.map((t) => `<li>${t}</li>`).join(''); pool.innerHTML = ''; } };
  };

  TYPES.match = (s, c) => {
    const wrap = $('<div class="match"><div class="col l"></div><div class="col r"></div></div>'); c.appendChild(wrap);
    c.appendChild($('<p class="small">Klikni levo, nato pravo razlago desno.</p>'));
    let sel = null, n = 0;
    const L = s.pairs.map((p, i) => { const b = $(`<button class="opt">${p[0]}</button>`); b._i = i; b.onclick = () => { L.forEach((x) => x.classList.remove('sel')); sel = b; b.classList.add('sel'); }; wrap.querySelector('.l').appendChild(b); return b; });
    const R = shuffle(s.pairs.map((p, i) => ({ t: p[1], i }))).map((o) => {
      const b = $(`<button class="opt">${o.t}</button>`); b._i = o.i;
      b.onclick = () => {
        if (!sel) { feedback('Najprej klikni pojem na levi.', 'hint'); return; }
        if (sel._i === o.i) { sel.classList.remove('sel'); sel.classList.add('good'); sel.disabled = true; b.classList.add('good'); b.disabled = true; sel = null; n++; if (n === s.pairs.length) done('✅ Vse povezano!'); else feedback('Pravilno.', ''); }
        else { b.classList.add('bad'); setTimeout(() => b.classList.remove('bad'), 500); feedback('❌ To ne spada skupaj. Poskusi drugo.', 'bad'); }
      };
      wrap.querySelector('.r').appendChild(b); return b;
    });
    return { solve: () => { L.concat(R).forEach((b) => { b.classList.add('good'); b.disabled = true; }); } };
  };

  /* ---- robot na mreži ---- */
  const TOK = { U: '↑', D: '↓', L: '←', R: '→', P: '■', ')': ')' };
  const tokLabel = (t) => t[0] === 'N' ? `ponovi ${t.slice(1)}× (` : TOK[t];
  function expand(tokens) {
    let i = 0;
    function block(top) {
      const out = [];
      while (i < tokens.length) {
        const t = tokens[i++];
        if (t === ')') { if (top) throw new Error('Preveč zaklepajev »)«. Pobriši enega.'); return out; }
        if (t[0] === 'N') { const n = +t.slice(1); const inner = block(false); if (inner._open) throw new Error('Zanko »ponovi« moraš zapreti z gumbom »)«.'); for (let k = 0; k < n; k++) out.push(...inner); }
        else out.push(t);
      }
      if (!top) out._open = true;
      return out;
    }
    return block(true);
  }
  TYPES.grid = (s, c) => {
    const n = s.n || 5, target = new Set(s.target.map(([r, k]) => r + ',' + k));
    const tools = s.tools || ['R', 'L', 'D', 'U', 'P'];
    const loops = s.loops || [];
    const ui = $(`<div class="gridtask">
      <div class="g" style="grid-template-columns:repeat(${n},var(--cs))"></div>
      <div class="side">
        <div class="legend"><span class="lt"></span> pobarvaj ta polja &nbsp; <span class="lp"></span> pobarval robot</div>
        <div class="prog" aria-label="Program"></div>
        <div class="tools"></div>
        <div class="row"><button class="btn run">▶ Zaženi</button><button class="btn ghost del">⌫ Briši zadnjega</button><button class="btn ghost clr">Pobriši vse</button></div>
        <div class="count"></div>
      </div></div>`);
    c.appendChild(ui);
    const g = ui.querySelector('.g'), prog = ui.querySelector('.prog'), cnt = ui.querySelector('.count');
    const cells = [];
    for (let r = 0; r < n; r++) for (let k = 0; k < n; k++) { const d = $(`<div class="cell${target.has(r + ',' + k) ? ' t' : ''}"></div>`); if (r === 0 && k === 0) d.dataset.s = 'S'; g.appendChild(d); cells.push(d); }
    let program = (s.start || []).slice(), running = false;
    const fixed = !!s.locked;
    const count = () => program.length; // šteje vsak gumb v programu, tudi »)«
    function draw() {
      prog.innerHTML = program.length ? program.map((t) => `<span class="tk${t[0] === 'N' || t === ')' ? ' loop' : ''}">${tokLabel(t)}</span>`).join('') : '<span class="ph">Tvoj program je prazen. Klikaj ukaze spodaj.</span>';
      cnt.innerHTML = `Ukazov: <b>${count()}</b>${s.max ? ` &nbsp;(največ ${s.max})` : ''} &nbsp;<span class="small">Šteje vsak gumb v programu, tudi »)«.</span>`;
    }
    const tb = ui.querySelector('.tools');
    if (!fixed) {
      tools.forEach((t) => { const b = $(`<button class="btn tool">${TOK[t]}</button>`); b.onclick = () => { program.push(t); draw(); }; tb.appendChild(b); });
      loops.forEach((m) => { const b = $(`<button class="btn tool loop">ponovi ${m}× (</button>`); b.onclick = () => { program.push('N' + m); draw(); }; tb.appendChild(b); });
      if (loops.length) { const b = $(`<button class="btn tool loop">)</button>`); b.onclick = () => { program.push(')'); draw(); }; tb.appendChild(b); }
      tb.appendChild($('<div class="tiphelp">→ ← ↓ ↑ premakne robota za 1 polje. ■ pobarva polje, na katerem robot stoji.</div>'));
    } else { ui.querySelector('.del').hidden = true; ui.querySelector('.clr').hidden = true; }
    ui.querySelector('.del').onclick = () => { if (!running) { program.pop(); draw(); } };
    ui.querySelector('.clr').onclick = () => { if (!running) { program = []; draw(); reset(); } };
    function reset() { cells.forEach((d) => { d.classList.remove('p', 'bot', 'miss', 'wrong'); }); }
    function put(r, k, cls) { cells[r * n + k].classList.add(cls); }
    ui.querySelector('.run').onclick = () => {
      if (running) return;
      let acts;
      try { acts = expand(program); } catch (e) { feedback('❌ ' + e.message, 'bad'); return; }
      if (!acts.length) { feedback('Program je prazen. Klikni nekaj ukazov.', 'hint'); return; }
      reset(); running = true;
      let r = 0, k = 0, i = 0; const painted = new Set();
      cells[0].classList.add('bot');
      const step = () => {
        if (i >= acts.length) return finish();
        const a = acts[i++];
        if (a === 'P') { painted.add(r + ',' + k); put(r, k, 'p'); }
        else {
          const nr = r + (a === 'D') - (a === 'U'), nk = k + (a === 'R') - (a === 'L');
          if (nr < 0 || nk < 0 || nr >= n || nk >= n) { running = false; feedback(`❌ Robot bi padel z mreže (ukaz ${TOK[a]}). Popravi program in poskusi znova.`, 'bad'); return; }
          cells[r * n + k].classList.remove('bot'); r = nr; k = nk; cells[r * n + k].classList.add('bot');
        }
        setTimeout(step, s.fast ? 120 : 260);
      };
      const finish = () => {
        running = false;
        let wrong = 0, miss = 0;
        painted.forEach((x) => { if (!target.has(x)) { wrong++; const [a, b] = x.split(','); put(+a, +b, 'wrong'); } });
        target.forEach((x) => { if (!painted.has(x)) { miss++; const [a, b] = x.split(','); put(+a, +b, 'miss'); } });
        if (!wrong && !miss) {
          if (s.max && count() > s.max) { feedback(`Slika je prava! 👍 A program ima ${count()} ukazov, dovoljenih je ${s.max}. Skrajšaj ga z zanko »ponovi«.`, 'hint'); return; }
          done(s.win || '✅ Bravo! Robot je narisal točno pravo sliko.');
        } else {
          const parts = [];
          const f = (n, a, b, c, d) => n === 1 ? a : n === 2 ? b : n < 5 ? c : d;
          if (miss) parts.push(`<b>${miss}</b> ${f(miss, 'polje manjka', 'polji manjkata', 'polja manjkajo', 'polj manjka')} (utripa oranžno)`);
          if (wrong) parts.push(`<b>${wrong}</b> ${f(wrong, 'polje je pobarvano', 'polji sta pobarvani', 'polja so pobarvana', 'polj je pobarvanih')} napačno (rdeče)`);
          feedback('❌ Še ne. ' + parts.join(', ') + '. To je hrošč: poišči, pri katerem ukazu gre robot narobe.', 'bad');
        }
      };
      setTimeout(step, 200);
    };
    draw();
    return { solve: () => { program = s.solution.slice(); draw(); } };
  };

  /* ---- diagram poteka (SVG) ---- */
  const FN = [
    { id: 'z', k: 'o', x: 3.5, y: 9.0, t: 'ZAČETEK' },
    { id: 'i', k: 'r', x: 3.5, y: 7.9, t: 'Izmisli si število', w: 3.9 },
    { id: 'v', k: 'r', x: 3.5, y: 6.8, t: 'Vprašaj: »Tvoj ugib?«', w: 3.9 },
    { id: 'e', k: 'd', x: 3.5, y: 5.35, t: 'ugib = število?' },
    { id: 'l', k: 'd', x: 3.5, y: 3.45, t: 'ugib < število?' },
    { id: 'm1', k: 'r', x: 1.7, y: 1.75, t: 'Izpiši »Več!«', w: 2.7 },
    { id: 'm2', k: 'r', x: 5.3, y: 1.75, t: 'Izpiši »Manj!«', w: 2.7 },
    { id: 'b', k: 'r', x: 8.0, y: 5.35, t: 'Izpiši »Bravo!«', w: 2.9 },
    { id: 'k', k: 'o', x: 8.0, y: 3.85, t: 'KONEC' },
  ];
  function flowSVG() {
    const S = 56, X = (x) => x * S + 10, Y = (y) => (9.6 - y) * S;
    let h = `<svg viewBox="0 0 590 500" class="flow" xmlns="http://www.w3.org/2000/svg"><defs><marker id="ah" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#333"/></marker></defs>`;
    const ln = (pts, arrow) => `<polyline points="${pts.map(([x, y]) => X(x) + ',' + Y(y)).join(' ')}" fill="none" stroke="#333" stroke-width="2" ${arrow ? 'marker-end="url(#ah)"' : ''}/>`;
    const lab = (x, y, t) => `<text x="${X(x)}" y="${Y(y)}" class="lab">${t}</text>`;
    h += ln([[3.5, 8.6], [3.5, 8.3]], 1) + ln([[3.5, 7.5], [3.5, 7.2]], 1) + ln([[3.5, 6.4], [3.5, 6.0]], 1);
    h += ln([[5.3, 5.35], [6.55, 5.35]], 1) + lab(5.6, 5.5, 'da') + ln([[8.0, 4.95], [8.0, 4.25]], 1);
    h += ln([[3.5, 4.7], [3.5, 4.1]], 1) + lab(3.65, 4.3, 'ne');
    h += ln([[1.7, 3.45], [1.7, 2.15]], 1) + lab(1.2, 2.7, 'da') + ln([[5.3, 3.45], [5.3, 2.15]], 1) + lab(5.45, 2.7, 'ne');
    h += ln([[1.7, 1.35], [1.7, 0.8], [5.3, 0.8], [5.3, 1.35]], 0) + ln([[1.7, 0.8], [0.3, 0.8], [0.3, 6.8], [1.55, 6.8]], 1);
    FN.forEach((n) => {
      const cx = X(n.x), cy = Y(n.y);
      let shp;
      if (n.k === 'o') shp = `<ellipse cx="${cx}" cy="${cy}" rx="70" ry="22" class="so"/>`;
      else if (n.k === 'r') { const w = (n.w || 3.4) * S; shp = `<rect x="${cx - w / 2}" y="${cy - 22}" width="${w}" height="44" class="sr"/>`; }
      else shp = `<polygon points="${cx},${cy - 36} ${cx + 100},${cy} ${cx},${cy + 36} ${cx - 100},${cy}" class="sd"/>`;
      h += `<g class="node" data-id="${n.id}">${shp}<text x="${cx}" y="${cy + 5}" text-anchor="middle">${n.t}</text></g>`;
    });
    return h + '</svg>';
  }
  window.flowSVG = flowSVG;
  TYPES.trace = (s, c) => {
    const w = $(`<div class="trace"><div class="fl">${flowSVG()}</div><div class="tside"><div class="qa"></div></div></div>`);
    c.appendChild(w);
    const qa = w.querySelector('.qa');
    const nodes = {}; w.querySelectorAll('.node').forEach((g) => (nodes[g.dataset.id] = g));
    let i = 0, waitAns = false;
    const mark = () => { Object.values(nodes).forEach((g) => g.classList.remove('cur')); nodes[s.path[i].n].classList.add('cur'); s.path.slice(0, i).forEach((p) => nodes[p.n].classList.add('was')); };
    function ask() {
      const p = s.path[i];
      if (p.a) {
        waitAns = true;
        qa.innerHTML = `<p><b>${p.q}</b></p><button class="btn ans">da</button> <button class="btn ans">ne</button>`;
        qa.querySelectorAll('.ans').forEach((b) => (b.onclick = () => {
          if (b.textContent === p.a) { waitAns = false; feedback('✅ ' + (p.why || 'Prav.') + ' Zdaj klikni lik, kamor kaže puščica »' + p.a + '«.', ''); qa.innerHTML = `<p>Odgovor: <b>${p.a}</b></p>`; }
          else feedback('❌ Poglej še enkrat: ' + (p.why || ''), 'bad');
        }));
      } else qa.innerHTML = i === 0 ? `<p>Začnemo pri liku, ki je obarvan. Klikni lik, ki pride <b>naslednji</b>.</p>` : `<p>Klikni lik, ki pride <b>naslednji</b>.</p>`;
    }
    Object.values(nodes).forEach((g) => (g.onclick = () => {
      if (i >= s.path.length - 1) return;
      if (waitAns) { feedback('Najprej odgovori na vprašanje: da ali ne?', 'hint'); return; }
      if (g.dataset.id === s.path[i + 1].n) { i++; mark(); if (i === s.path.length - 1) { qa.innerHTML = ''; done('✅ ' + s.win); } else ask(); }
      else { g.classList.add('no'); setTimeout(() => g.classList.remove('no'), 450); feedback('❌ Ne še. Sledi puščici iz obarvanega lika.', 'bad'); }
    }));
    mark(); ask();
    return { solve: () => { i = s.path.length - 1; mark(); qa.innerHTML = ''; } };
  };

  TYPES.guess = (s, c) => {
    const secret = 1 + Math.floor(Math.random() * 100); let tries = 0;
    const w = $(`<div class="guess"><p>Računalnik si je izmislil število od <b>1</b> do <b>100</b>.</p>
      <div class="row"><input type="number" min="1" max="100" inputmode="numeric" placeholder="ugib"><button class="btn go2">Ugibaj</button></div>
      <ul class="hist"></ul></div>`);
    c.appendChild(w);
    const inp = w.querySelector('input'), hist = w.querySelector('.hist');
    const go = () => {
      const v = parseInt(inp.value, 10);
      if (!(v >= 1 && v <= 100)) { feedback('Vpiši celo število od 1 do 100.', 'hint'); return; }
      tries++;
      const r = v === secret ? 'Bravo!' : v < secret ? 'Več!' : 'Manj!';
      hist.insertAdjacentHTML('afterbegin', `<li><b>${v}</b> → ${r}</li>`); inp.value = ''; inp.focus();
      if (v === secret) { w.querySelector('.go2').disabled = true; done(`✅ Uganil/a si v <b>${tries}</b> poskusih. ${tries <= 7 ? 'Odlično, to je pametna strategija!' : 'Namig za naslednjič: vedno ugibaj <b>sredino</b> (50, nato 25 ali 75 …). Tako nikoli ne rabiš več kot 7 poskusov.'}`); }
      else feedback(r === 'Več!' ? '⬆ Število je <b>večje</b>.' : '⬇ Število je <b>manjše</b>.', '');
    };
    w.querySelector('.go2').onclick = go; inp.onkeydown = (e) => { if (e.key === 'Enter') go(); };
    return { solve: () => { hist.insertAdjacentHTML('afterbegin', `<li>Skrito število je bilo <b>${secret}</b>.</li>`); } };
  };

  TYPES.cards = (s, c) => {
    const nums = shuffle(Array.from({ length: 90 }, (_, i) => i + 10)).slice(0, s.n || 8);
    const w = $(`<div class="cards"><div class="deck"></div>
      <div class="memo">V glavi si zapomnim: <span class="mem">nič</span> &nbsp; · &nbsp; Primerjav: <b class="cmp">0</b></div>
      <div class="ctrl"></div></div>`);
    c.appendChild(w);
    const deck = w.querySelector('.deck'), ctrl = w.querySelector('.ctrl'), memEl = w.querySelector('.mem'), cmpEl = w.querySelector('.cmp');
    const cs = nums.map((v) => { const d = $(`<div class="card">?</div>`); deck.appendChild(d); return d; });
    let i = 0, mem = null, cmp = 0;
    function turn() {
      cs[i].textContent = nums[i]; cs[i].classList.add('up');
      if (mem === null) { ctrl.innerHTML = `<button class="btn" data-a="keep">Zapomni si ${nums[i]}</button>`; }
      else ctrl.innerHTML = `<p>Primerjaj: karta <b>${nums[i]}</b> ali v glavi <b>${mem}</b>?</p><button class="btn" data-a="keep">${nums[i]} je večje: zapomni si ${nums[i]}</button> <button class="btn" data-a="drop">${nums[i]} je manjše: zavrzi karto</button>`;
      ctrl.querySelectorAll('button').forEach((b) => (b.onclick = () => act(b.dataset.a)));
    }
    function act(a) {
      const v = nums[i];
      if (mem !== null) {
        const right = v > mem ? 'keep' : 'drop';
        if (a !== right) { feedback(`❌ Pozor: ${v} je ${v > mem ? 'VEČJE' : 'MANJŠE'} od ${mem}. Poskusi znova.`, 'bad'); return; }
        cmp++; cmpEl.textContent = cmp;
      }
      if (a === 'keep') mem = v;
      memEl.textContent = mem; cs[i].classList.add(a === 'keep' ? 'kept' : 'gone');
      feedback(a === 'keep' ? 'Zapomnil/a si novo največje število.' : 'Karto zavržeš, v glavi ostane ' + mem + '.', '');
      i++;
      if (i < nums.length) { ctrl.innerHTML = `<button class="btn go2">Obrni naslednjo karto</button>`; ctrl.querySelector('button').onclick = turn; }
      else { ctrl.innerHTML = ''; done(`✅ Največje število je <b>${mem}</b>. Pri ${nums.length} kartah si naredil/a <b>${cmp}</b> primerjav. Prvo karto si si samo zapomnil/a, vsako naslednjo pa enkrat primerjal/a.`); }
    }
    ctrl.innerHTML = `<button class="btn go2">Obrni prvo karto</button>`; ctrl.querySelector('button').onclick = turn;
    return { solve: () => { cs.forEach((d, k) => { d.textContent = nums[k]; d.classList.add('up'); }); mem = Math.max(...nums); memEl.textContent = mem; ctrl.innerHTML = ''; } };
  };

  tell('zacetek');
  show(cur);
})();
