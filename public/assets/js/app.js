// Logica paginilor: vizualizatoare 3D, controale, formularul „Cere prețul”.
const PHONE = '+373 61 198 777';
const MODELS = {
  'mangal': () => import('./models/mangal.js'),
  'raft-vin': () => import('./models/raft-vin.js'),
  'suport-laptop': () => import('./models/suport-laptop.js'),
};
const SWATCH = { negru: '#1d1e20', antracit: '#3a3d42', bronz: '#5a4632', brut: '#8d9298' };
const FIN_LABEL = { negru: 'Negru mat', antracit: 'Antracit', bronz: 'Bronz antic', brut: 'Oțel brut' };

/* ---------- 3D ---------- */
async function initViewer(box) {
  const ctlBox = document.querySelector(box.dataset.controls || '#none');
  let viewerMod;
  try { viewerMod = await import('./viewer.js'); }
  catch (e) { box.querySelector('.loading').textContent = 'Modelul 3D nu s-a putut încărca.'; return; }
  const v = viewerMod.createViewer(box, { autoRotate: true });
  const loading = box.querySelector('.loading');
  const state = { explode: 0 };

  async function load(slug) {
    if (loading) loading.hidden = false;
    const mod = await MODELS[slug]();
    const model = await mod.build();
    v.setModel(model);
    if (loading) loading.hidden = true;
    if (ctlBox) renderControls(ctlBox, model, v, state);
    return model;
  }
  // file (taburi) pe pagina principală
  const tabs = box.dataset.tabs ? document.querySelector(box.dataset.tabs) : null;
  if (tabs) {
    const btns = [...tabs.querySelectorAll('button[data-model]')];
    btns.forEach(b => b.addEventListener('click', () => {
      btns.forEach(x => x.setAttribute('aria-selected', String(x === b)));
      const link = document.querySelector('#hero-link'); if (link) link.href = b.dataset.href;
      state.explode = 0; load(b.dataset.model);
    }));
  }
  await load(box.dataset.model);
}

function renderControls(el, model, v, state) {
  el.innerHTML = '';
  // explodare
  const ex = document.createElement('label'); ex.className = 'ctl';
  ex.innerHTML = `Desfă în piese <input type="range" min="0" max="100" value="${state.explode * 100}" aria-label="Desfă modelul în piese">`;
  const r = ex.querySelector('input');
  r.addEventListener('input', () => { state.explode = r.value / 100; v.setExplode(state.explode); v.controls.autoRotate = false; });
  el.appendChild(ex);
  (model.controls || []).forEach((c, i) => {
    if (c.type === 'finish') {
      const w = document.createElement('div'); w.className = 'ctl';
      w.innerHTML = `<span>${c.label}</span><div class="swatches" role="group" aria-label="${c.label}"></div>`;
      const g = w.querySelector('.swatches');
      c.options.forEach(o => {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'sw'; b.style.background = SWATCH[o];
        b.title = FIN_LABEL[o]; b.setAttribute('aria-label', FIN_LABEL[o]); b.setAttribute('aria-pressed', String(o === c.value));
        b.addEventListener('click', () => { g.querySelectorAll('.sw').forEach(x => x.setAttribute('aria-pressed', String(x === b))); c.value = o; c.set(o); syncForm('finisaj', FIN_LABEL[o]); });
        g.appendChild(b);
      });
      el.appendChild(w);
    } else if (c.type === 'toggle') {
      const id = `t${i}${Math.random().toString(36).slice(2, 6)}`;
      const w = document.createElement('label'); w.className = 'toggle'; w.htmlFor = id;
      w.innerHTML = `<input type="checkbox" id="${id}" ${c.value ? 'checked' : ''}> ${c.label}`;
      w.querySelector('input').addEventListener('change', e => { c.value = e.target.checked; c.set(c.value); });
      el.appendChild(w);
    } else if (c.type === 'text') {
      const id = `x${i}`;
      const w = document.createElement('label'); w.className = 'ctl'; w.htmlFor = id;
      w.innerHTML = `${c.label} <input type="text" id="${id}" maxlength="${c.max || 20}" value="${c.value}" placeholder="${c.placeholder || ''}" autocomplete="off">`;
      const inp = w.querySelector('input');
      inp.addEventListener('input', () => { c.value = inp.value; c.set(inp.value); syncForm('gravura', inp.value); });
      el.appendChild(w);
    }
  });
}
// ce alege omul în 3D ajunge automat în formular
function syncForm(name, value) {
  const f = document.querySelector(`form.q [name="${name}"]`); if (f) f.value = value;
}

/* ---------- formular ---------- */
function initForm(form) {
  const st = form.querySelector('.status');
  const prod = form.querySelector('[name="produs"]');
  const engr = form.querySelector('[data-only="raft-vin"]');
  const upd = () => { if (engr) engr.hidden = prod.value !== 'Raft pentru vin'; };
  prod?.addEventListener('change', upd); upd();
  // butoanele „Cere prețul” din carduri preselectează produsul
  document.querySelectorAll('[data-quote]').forEach(a => a.addEventListener('click', () => { if (prod) { prod.value = a.dataset.quote; upd(); } }));

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    if (!data.telefon || data.telefon.replace(/\D/g, '').length < 6) { st.className = 'status err'; st.textContent = 'Scrie un număr de telefon ca să te putem suna.'; form.telefon.focus(); return; }
    const btn = form.querySelector('button[type=submit]'); btn.disabled = true; st.className = 'status'; st.textContent = 'Se trimite…';
    try {
      const res = await fetch('/api/cerere', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ ...data, pagina: location.pathname }) });
      const j = await res.json().catch(() => ({}));
      if (!res.ok || !j.ok) throw new Error(j.error || res.status);
      st.className = 'status ok'; st.textContent = 'Mulțumim! Am primit cererea și te contactăm cât mai repede cu prețul.';
      form.reset(); upd();
    } catch (err) {
      st.className = 'status err'; st.textContent = `Cererea nu a ajuns. Sună-ne direct: ${PHONE}.`;
    } finally { btn.disabled = false; }
  });
}

document.querySelectorAll('[data-viewer]').forEach(initViewer);
document.querySelectorAll('form.q').forEach(initForm);
document.querySelectorAll('[data-year]').forEach(e => { e.textContent = new Date().getFullYear(); });
