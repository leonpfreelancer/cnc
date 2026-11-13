#!/usr/bin/env python3
"""Generează paginile HTML statice din public/.
Rulare:  python3 tools/gen.py
Editează textele de mai jos (BRAND, PRODUCTS) și rulează din nou scriptul."""
import json, os, html

ROOT = os.path.join(os.path.dirname(__file__), '..', 'public')
BRAND = {
    'name': 'Atelier Laser', 'city': 'Chișinău',
    'legal': 'Î.I. Pascari Lilian',
    'phone': '+373 61 198 777', 'phone_raw': '+37361198777', 'wa': '37361198777',
}
E = html.escape

PRODUCTS = [
    {
        'slug': 'mangal', 'form': 'Mangal', 'name': 'Mangal tăiat cu laser',
        'short': 'Mangal', 'eyebrow': 'Oțel · tăiere laser · la comandă',
        'title': 'Mangal tăiat cu laser, la comandă în Chișinău',
        'desc': 'Mangal din oțel cu decor ciorchine tăiat cu laser, picioare-cadru și raft dedesubt. Îl facem la comandă în Chișinău. Vezi-l în 3D și cere prețul.',
        'lead': 'Cutie de foc din oțel cu decor „ciorchine de struguri” tăiat cu laser, crestături pentru frigărui, picioare-cadru și raft dedesubt. Îl facem la comandă, în Chișinău, pe dimensiunile tale.',
        'tags': ['Oțel', 'Vopsea termorezistentă', 'La comandă'],
        'facts': [('Laser', 'tăiere de precizie'), ('Decor', 'ciorchine sau al tău'), ('Vopsea', 'termorezistentă'), ('Mărime', 'la comandă')],
        'features': [
            'Cutie de foc cu orificii de aer pe toate laturile și fund perforat',
            'Crestături pe marginea de sus, pentru frigărui',
            'Decor „ciorchine de struguri” tăiat cu laser pe pereții lungi',
            'Mânere decupate pe laturile scurte',
            'Raft inferior pentru lemne, cărbune sau ustensile',
            'Vopsea termorezistentă, gata de primul foc',
        ],
        'steps': [('Tăiere laser', 'Toate piesele, cu decorul, se taie din tablă de oțel.'),
                  ('Asamblare', 'Pereții, fundul, picioarele și raftul se îmbină într-un corp rigid.'),
                  ('Vopsire termorezistentă', 'Vopsea care rezistă la temperatura focului.'),
                  ('Gata de grătar', 'Îl iei din atelier și aprinzi focul.')],
        'spec': [('Material', 'Oțel tăiat cu laser'), ('Finisaj', 'Vopsea termorezistentă (negru, antracit) sau oțel brut'),
                 ('Decor', 'Ciorchine de struguri sau model personalizat'), ('Componente', 'Cutie de foc, 2 picioare-cadru, raft inferior'),
                 ('Dimensiuni', 'La comandă, după spațiul tău'), ('Producție', 'Atelier propriu, Chișinău')],
        'faq': [('Pot alege dimensiunile și grosimea tablei?', 'Da. Mangalul se face la comandă: spune-ne lungimea, câte frigărui vrei să încapă și unde va sta, iar noi îți propunem varianta potrivită.'),
                ('Pot pune alt decor sau un nume?', 'Da. Laserul taie orice contur desenat vectorial: un nume, un monogram, un logo sau alt motiv în locul ciorchinelui.'),
                ('Cât durează și cum îl primesc?', 'Termenul și livrarea se stabilesc la comandă, după volum. Ne suni sau ne lași numărul în formular și revenim cu prețul și termenul.')],
        'video_alt': 'Video: cum se face mangalul, de la tăierea laser la primul foc',
    },
    {
        'slug': 'raft-vin', 'form': 'Raft pentru vin', 'name': 'Raft pentru vin cu nume gravat',
        'short': 'Raft pentru vin', 'eyebrow': 'Cadou · oțel · vopsire electrostatică',
        'title': 'Raft pentru vin cu nume gravat, tăiat cu laser — Chișinău',
        'desc': 'Raft din oțel pentru 6 sticle, 4 piese tăiate cu laser, vopsire în câmp electrostatic și nume gravat pe capac. Cadou gata de oferit. Vezi-l în 3D și cere prețul.',
        'lead': 'Raft din oțel pentru 6 sticle, din patru piese tăiate cu laser și vopsite în câmp electrostatic. Gravăm pe capac numele celui care îl primește. Scrie-l mai jos și vezi-l în 3D.',
        'tags': ['6 sticle', 'Nume gravat', 'Cadou'],
        'facts': [('6', 'sticle'), ('4', 'piese din oțel'), ('Gravură', 'nume pe capac'), ('Vopsire', 'electrostatică')],
        'features': [
            'Ține 6 sticle culcate, cum se păstrează corect vinul',
            'Patru piese din oțel tăiate cu laser, fără compromisuri la precizie',
            'Vopsire în câmp electrostatic, rezistentă ani de zile',
            'Numele gravat cu laser pe capac: cadou personal, nu de raft de magazin',
            'Decor ciorchine tăiat în panourile laterale',
            'Stă pe masă, pe bufet sau pe podea',
        ],
        'steps': [('Tăiere laser', 'Panourile, capacul și baza se taie din oțel.'),
                  ('Asamblare', 'Patru piese, un corp rigid.'),
                  ('Vopsire în câmp electrostatic', 'Strat uniform și rezistent.'),
                  ('Gata de cadou', 'Cu numele gravat, gata de oferit.')],
        'spec': [('Capacitate', '6 sticle standard'), ('Material', 'Oțel tăiat cu laser'), ('Piese', '4 (2 panouri, capac, bază)'),
                 ('Finisaj', 'Vopsire în câmp electrostatic: negru mat, antracit, bronz antic'), ('Personalizare', 'Nume sau text scurt gravat pe capac'),
                 ('Producție', 'Atelier propriu, Chișinău')],
        'faq': [('Ce pot grava pe capac?', 'Un nume, două nume, o dată sau un mesaj scurt. Previzualizarea 3D de sus îți arată cum arată textul. Ni-l trimiți odată cu cererea.'),
                ('Pot alege culoarea?', 'Da: negru mat, antracit sau bronz antic. Pentru altă culoare, scrie-ne în cerere.'),
                ('Îl puteți face pentru mai multe sticle?', 'Da, raftul se poate face la comandă și pentru alt număr de sticle. Spune-ne câte și unde va sta.')],
        'video_alt': 'Video: raftul pentru vin, de la tăierea laser la cadou',
    },
    {
        'slug': 'suport-laptop', 'form': 'Suport laptop WOODSTAND 01', 'name': 'WOODSTAND 01 — suport pentru laptop',
        'short': 'Suport laptop', 'eyebrow': 'Placaj de mesteacăn · CNC · prototip',
        'title': 'WOODSTAND 01 — suport de laptop din placaj, frezat CNC în Chișinău',
        'desc': 'Suport de laptop din placaj de mesteacăn 12 mm: 5 piese, 0 șuruburi, montaj în 2 minute, înclinare 13°. Frezat CNC în Chișinău. Vezi-l în 3D și cere prețul.',
        'lead': 'Suport de laptop din placaj de mesteacăn de 12 mm. Cinci piese care intră una în alta, fără șuruburi și fără lipici. Ridică laptopul la 13°, lasă aer pe dedesubt și nu acoperă porturile.',
        'tags': ['Placaj mesteacăn', '0 șuruburi', '13–16"'],
        'facts': [('5', 'piese, 0 șuruburi'), ('13°', 'înclinare'), ('2 min', 'montaj fără scule'), ('≈1 kg', 'masă')],
        'features': [
            'Pentru laptopuri de 13–16" (până la 356 × 248 mm)',
            'Îmbinări tab-and-slot: se montează și se demontează fără scule',
            'Fante de ventilație sub laptop',
            'Laterale retrase cu 40 mm: porturile din lateral rămân libere',
            'Opritor discret în față și picioare antiderapante',
            'Finisaj cu ulei-ceară, se transportă plat',
        ],
        'steps': [('Frezare CNC', 'Toate piesele se taie dintr-o singură placă de placaj.'),
                  ('Șlefuire', 'Muchii rotunjite fin, fețe netede.'),
                  ('Ulei-ceară', 'Două straturi, pune în valoare fibra mesteacănului.'),
                  ('Montaj în 2 minute', 'Fără scule: piesele intră una în alta.')],
        'spec': [('Platformă', '360 × 270 mm'), ('Înclinare', '13°'), ('Înălțime față / spate', '35 / 95,7 mm'),
                 ('Material', 'Placaj de mesteacăn 12 mm'), ('Îmbinări', 'Tab-and-slot, demontabil, fără șuruburi'),
                 ('Masă', '≈ 1 kg'), ('Stadiu', 'Prototip, precomenzi deschise')],
        'faq': [('Încape laptopul meu?', 'Platforma are 360 × 270 mm. Încap laptopuri de 13–16", până la 356 × 248 mm. Unul mai adânc poate depăși puțin în spate, fără probleme.'),
                ('Este bun pentru lucru toată ziua?', 'Pentru sesiuni lungi recomandăm o tastatură și un mouse externe, ca la orice suport care ridică laptopul. La 13°, suportul e gândit pentru tastat confortabil și răcire mai bună.'),
                ('E deja în vânzare?', 'Este în faza de prototip. Lasă-ne numărul și te anunțăm primul, cu prețul de lansare.')],
        'video_alt': 'Video: WOODSTAND 01, montaj și înclinare',
        'badge': 'Prototip · precomenzi',
    },
]

def logo():
    return ('<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#ff6a1f"/>'
            '<path d="M9 23 16 7l7 16" fill="none" stroke="#1a0a02" stroke-width="3.2" stroke-linejoin="round"/>'
            '<path d="M11.5 18h9" stroke="#1a0a02" stroke-width="3"/></svg>')

def head(title, desc, path, image, extra_ld=None):
    ld = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": f"{BRAND['name']} · {BRAND['city']}",
          "legalName": BRAND['legal'], "telephone": BRAND['phone_raw'],
          "address": {"@type": "PostalAddress", "addressLocality": "Chișinău", "addressCountry": "MD"},
          "description": "Tăiere laser și CNC: mangaluri, rafturi pentru vin cu nume gravat, suporturi de laptop din placaj, la comandă."}
    lds = [ld] + ([extra_ld] if extra_ld else [])
    return f'''<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ro_MD">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{path}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e0e0f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@800&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="importmap">{{"imports":{{"three":"/assets/js/vendor/three.module.min.js","three/addons/controls/OrbitControls.js":"/assets/js/vendor/OrbitControls.js","three/addons/environments/RoomEnvironment.js":"/assets/js/vendor/RoomEnvironment.js"}}}}</script>
<script type="module" src="/assets/js/app.js"></script>
{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)}
</head>
<body>
'''

def header(active=None):
    links = ''.join(f'<a href="/{p["slug"]}/"{" aria-current=\"page\"" if active == p["slug"] else ""}>{p["short"]}</a>' for p in PRODUCTS)
    return f'''<header class="top"><div class="wrap">
  <a class="logo" href="/" aria-label="{BRAND['name']} {BRAND['city']}, pagina principală">{logo()}<span>{BRAND['name']}<br><small>{BRAND['city']}</small></span></a>
  <nav class="nav" aria-label="Produse">{links}<a href="/#contact">Contact</a></nav>
  <a class="btn btn-ghost btn-sm call" href="tel:{BRAND['phone_raw']}">Sună {BRAND['phone']}</a>
</div></header>
'''

def quote_section(selected):
    opts = ''.join(f'<option{" selected" if p["form"] == selected else ""}>{p["form"]}</option>' for p in PRODUCTS)
    opts += f'<option{" selected" if selected == "Altă comandă" else ""}>Altă comandă</option>'
    return f'''<section id="cere-pret" class="band"><div class="wrap quote">
  <div class="sec-head">
    <span class="eyebrow">Cere prețul</span>
    <h2>Află prețul în aceeași zi</h2>
    <p class="lead">Lasă-ne numărul și ce ai ales. Te contactăm cu prețul și termenul, fără obligații. Dacă preferi, sună-ne direct.</p>
    <div class="contact-list">
      <a href="tel:{BRAND['phone_raw']}">{BRAND['phone']}<small>Apel sau Viber</small></a>
      <a href="https://wa.me/{BRAND['wa']}" rel="noopener">WhatsApp<small>Scrie-ne, trimite poze sau schițe</small></a>
    </div>
  </div>
  <form class="q" novalidate>
    <div class="f-row">
      <div class="field"><label for="f-produs">Produs</label><select id="f-produs" name="produs">{opts}</select></div>
      <div class="field"><label for="f-cant">Cantitate</label><input id="f-cant" name="cantitate" type="number" min="1" max="999" value="1" inputmode="numeric"></div>
    </div>
    <div class="f-row">
      <div class="field"><label for="f-nume">Nume</label><input id="f-nume" name="nume" autocomplete="name" maxlength="80"></div>
      <div class="field"><label for="f-tel">Telefon *</label><input id="f-tel" name="telefon" type="tel" autocomplete="tel" required maxlength="30" placeholder="+373 …"></div>
    </div>
    <div class="f-row">
      <div class="field"><label for="f-contact">Cum să te contactăm</label><select id="f-contact" name="contact"><option>Apel</option><option>Viber</option><option>WhatsApp</option><option>Telegram</option></select></div>
      <div class="field"><label for="f-fin">Finisaj / culoare</label><input id="f-fin" name="finisaj" maxlength="60" placeholder="ex. negru mat"></div>
    </div>
    <div class="field" data-only="raft-vin" hidden><label for="f-gr">Text gravat pe capac</label><input id="f-gr" name="gravura" maxlength="40" placeholder="ex. ANDREI"></div>
    <div class="field"><label for="f-det">Detalii (dimensiuni, idee, termen)</label><textarea id="f-det" name="detalii" maxlength="1500" placeholder="Spune-ne ce ai nevoie. Poți descrie dimensiunile sau ideea."></textarea></div>
    <div class="hp" aria-hidden="true"><label for="f-web">Nu completa</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
    <button class="btn btn-primary" type="submit">Trimite cererea de preț</button>
    <p class="status" role="status" aria-live="polite"></p>
    <p class="note">Folosim datele doar ca să-ți răspundem la cerere.</p>
  </form>
</div></section>
'''

def footer():
    links = ''.join(f'<a href="/{p["slug"]}/">{p["short"]}</a><br>' for p in PRODUCTS)
    return f'''<footer><div class="wrap">
  <div><a class="logo" href="/">{logo()}<span>{BRAND['name']}<br><small>{BRAND['city']}</small></span></a>
  <p style="margin-top:12px">Tăiere laser și CNC · produse la comandă</p></div>
  <div>{links}</div>
  <div><a href="tel:{BRAND['phone_raw']}">{BRAND['phone']}</a><br>{BRAND['legal']} · Chișinău, Republica Moldova<br>© <span data-year>2026</span></div>
</div></footer>
<div class="mbar"><a class="btn btn-primary" href="#cere-pret">Cere prețul</a><a class="btn btn-ghost" href="tel:{BRAND['phone_raw']}">Sună</a></div>
</body></html>
'''

def viewer(slug, ctl_id, badge=None, tabs=None):
    b = f'<span class="badge">{badge}</span>' if badge else ''
    t = f' data-tabs="{tabs}"' if tabs else ''
    return (f'<div class="viewer" data-viewer data-model="{slug}" data-controls="#{ctl_id}"{t}>'
            f'<div class="loading">Se încarcă modelul 3D…</div>{b}<span class="hint">Trage pentru rotire · ciupește pentru zoom</span></div>'
            f'<div class="controls" id="{ctl_id}"></div>')

def home():
    cards = ''
    for p in PRODUCTS:
        cards += f'''<article class="card">
  <a class="media" href="/{p['slug']}/"><img src="/assets/media/{p['slug']}-poster.jpg" alt="{E(p['name'])}" loading="lazy" width="720" height="1280"></a>
  <div class="body"><div class="tags">{''.join(f'<span class="tag">{t}</span>' for t in p['tags'])}</div>
  <h3>{p['name']}</h3><p style="color:var(--muted)">{p['desc'].split('. Vezi')[0]}.</p>
  <div class="row"><a class="btn btn-ghost btn-sm" href="/{p['slug']}/">Vezi în 3D</a><a class="btn btn-primary btn-sm" href="#cere-pret" data-quote="{p['form']}">Cere prețul</a></div></div>
</article>'''
    tabs = ''.join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-model="{p["slug"]}" data-href="/{p["slug"]}/">{p["short"]}</button>' for i, p in enumerate(PRODUCTS))
    s = head(f"{BRAND['name']} {BRAND['city']} — mangaluri, rafturi pentru vin, suporturi de laptop la comandă",
             'Atelier de tăiere laser și CNC în Chișinău: mangaluri din oțel, rafturi pentru vin cu nume gravat, suporturi de laptop din placaj. Vezi produsele în 3D și cere prețul.',
             '/', '/assets/img/og-home.jpg')
    s += header()
    s += f'''<main>
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">Atelier laser · CNC · {BRAND['city']}</span>
    <h1 style="margin-top:14px">Obiecte din metal și lemn, <span class="accent">tăiate la milimetru</span></h1>
    <p class="lead">Mangaluri, rafturi pentru vin cu nume gravat și suporturi de laptop din placaj. Le facem la comandă în atelierul nostru din Chișinău. Rotește-le în 3D, apoi cere prețul.</p>
    <div class="row"><a class="btn btn-primary" href="#cere-pret">Cere prețul</a><a class="btn btn-ghost" href="#produse">Vezi produsele</a></div>
  </div>
  <div>
    <div class="tabs" role="tablist" id="hero-tabs" aria-label="Alege produsul">{tabs}</div>
    {viewer(PRODUCTS[0]['slug'], 'hero-controls', tabs='#hero-tabs')}
    <p style="margin-top:10px"><a id="hero-link" href="/{PRODUCTS[0]['slug']}/" style="color:var(--accent);font-weight:600;text-decoration:none">Deschide pagina produsului →</a></p>
  </div>
</div></section>

<section id="produse"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Produse</span><h2>Trei produse, făcute la comandă</h2>
  <p class="lead">Fiecare are pagina lui cu model 3D interactiv, video din atelier și formular de preț.</p></div>
  <div class="cards">{cards}</div>
</div></section>

<section class="band"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Cum lucrăm</span><h2>De la cerere la produs gata</h2></div>
  <ol class="steps">
    <li><h3>Ne spui ce vrei</h3><p>Produsul, dimensiunile, culoarea sau numele de gravat.</p></li>
    <li><h3>Tăiere laser sau CNC</h3><p>Oțelul se taie cu laser, lemnul pe freza CNC, la precizie de atelier.</p></li>
    <li><h3>Asamblare și finisaj</h3><p>Vopsire electrostatică, vopsea termorezistentă sau ulei-ceară.</p></li>
    <li><h3>Gata de folosit</h3><p>Îți dăm produsul gata de folosit sau de oferit cadou.</p></li>
  </ol>
</div></section>

<section><div class="wrap split" style="grid-template-columns:1fr auto">
  <div class="sec-head" style="margin:0"><span class="eyebrow">Ai altă idee?</span><h2>Tăiem orice contur desenat</h2>
  <p class="lead">Un logo pe metal, un nume, un decor pentru casă sau o piesă tehnică: trimite-ne o schiță, o poză sau un fișier DXF și îți spunem prețul.</p></div>
  <a class="btn btn-primary" href="#cere-pret" data-quote="Altă comandă">Trimite ideea</a>
</div></section>
</main>
<div id="contact"></div>
'''
    s += quote_section(PRODUCTS[0]['form']) + footer()
    return s

def product(p):
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p['name'], "description": p['desc'],
          "image": f"/assets/media/{p['slug']}-poster.jpg", "brand": {"@type": "Brand", "name": BRAND['name']}}
    s = head(p['title'], p['desc'], f"/{p['slug']}/", f"/assets/img/og-{p['slug']}.jpg", ld)
    s += header(p['slug'])
    facts = ''.join(f'<div class="fact"><b>{a}</b><span>{b}</span></div>' for a, b in p['facts'])
    feats = ''.join(f'<li>{f}</li>' for f in p['features'])
    steps = ''.join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a, b in p['steps'])
    spec = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in p['spec'])
    faq = ''.join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in p['faq'])
    s += f'''<main>
<section class="p-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Acasă</a> / {p['short']}</p>
  <div class="p-grid">
    <div>{viewer(p['slug'], 'ctl', p.get('badge'))}</div>
    <div class="p-info">
      <span class="eyebrow">{p['eyebrow']}</span>
      <h1 style="font-size:clamp(34px,4.4vw,56px)">{p['name']}</h1>
      <p class="lead">{p['lead']}</p>
      <div class="facts">{facts}</div>
      <div class="row"><a class="btn btn-primary" href="#cere-pret">Cere prețul</a><a class="btn btn-ghost" href="tel:{BRAND['phone_raw']}">Sună {BRAND['phone']}</a></div>
    </div>
  </div>
</div></section>

<section class="band"><div class="wrap split">
  <video src="/assets/media/{p['slug']}.mp4" poster="/assets/media/{p['slug']}-poster.jpg" controls playsinline preload="none" aria-label="{E(p['video_alt'])}"></video>
  <div><div class="sec-head"><span class="eyebrow">Ce primești</span><h2>{p['short']}, gândit până la detaliu</h2></div>
  <ul class="list">{feats}</ul></div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Cum îl facem</span><h2>Patru pași, în atelierul nostru</h2></div>
  <ol class="steps">{steps}</ol>
</div></section>

<section class="band"><div class="wrap split" style="grid-template-columns:1fr 1fr;align-items:start">
  <div><div class="sec-head"><span class="eyebrow">Specificații</span><h2>Pe scurt</h2></div><table class="spec">{spec}</table></div>
  <div><div class="sec-head"><span class="eyebrow">Întrebări</span><h2>Ce ne întreabă clienții</h2></div>{faq}</div>
</div></section>
</main>
'''
    s += quote_section(p['form']) + footer()
    return s

if __name__ == '__main__':
    open(os.path.join(ROOT, 'index.html'), 'w').write(home())
    for p in PRODUCTS:
        os.makedirs(os.path.join(ROOT, p['slug']), exist_ok=True)
        open(os.path.join(ROOT, p['slug'], 'index.html'), 'w').write(product(p))
    print('ok')
