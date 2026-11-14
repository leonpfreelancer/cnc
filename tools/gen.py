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

def asset_version():
    """Hash din conținutul JS/CSS/JSON. Se pune în adrese (?v=…), ca browserul să ia fișierele noi după fiecare actualizare."""
    import hashlib, glob
    h = hashlib.sha1()
    files = glob.glob(os.path.join(ROOT, 'assets', 'js', '**', '*'), recursive=True) + glob.glob(os.path.join(ROOT, 'assets', 'css', '*'))
    for f in sorted(files):
        if os.path.isfile(f): h.update(f.encode()); h.update(open(f, 'rb').read())
    return h.hexdigest()[:10]

def import_map(v):
    """three din vendor + toate modulele proprii mapate pe adrese versionate (și importurile relative trec prin hartă)."""
    import glob
    m = {"three": "/assets/js/vendor/three.module.min.js",
         "three/addons/controls/OrbitControls.js": "/assets/js/vendor/OrbitControls.js",
         "three/addons/environments/RoomEnvironment.js": "/assets/js/vendor/RoomEnvironment.js"}
    for f in sorted(glob.glob(os.path.join(ROOT, 'assets', 'js', '*.js')) + glob.glob(os.path.join(ROOT, 'assets', 'js', 'models', '*.js'))):
        u = '/' + os.path.relpath(f, ROOT).replace(os.sep, '/')
        m[u] = f'{u}?v={v}'
    return json.dumps({"imports": m}, separators=(',', ':'))

PRODUCTS = [
    {
        'slug': 'brad-craciun', 'form': 'Brad de Crăciun cu nume', 'name': 'Brad de Crăciun din lemn, cu numele familiei',
        'short': 'Brad de Crăciun', 'eyebrow': 'Placaj de mesteacăn · CNC · gravură', 'engrave': True,
        'title': 'Brad de Crăciun din lemn cu numele familiei, tăiat pe CNC — Chișinău',
        'desc': 'Brad de Crăciun din placaj de mesteacăn, 58 cm: 2 piese în cruce și o stea, 0 șuruburi, cu numele familiei gravat. Tăiat pe CNC în Chișinău. Vezi-l în 3D și cere prețul.',
        'lead': 'Două piese din placaj de mesteacăn de 12 mm care intră una în alta, în cruce, și o stea în vârf. Gravăm pe ramuri numele familiei tale. Se montează în 10 secunde, fără șuruburi, iar după sărbători îl desfaci și îl păstrezi plat până la anul. Scrie numele mai jos și vezi-l în 3D.',
        'tags': ['Placaj mesteacăn', 'Nume gravat', '58 cm'],
        'facts': [('58 cm', 'înălțime cu steaua'), ('3', 'piese, 0 șuruburi'), ('10 s', 'montaj fără scule'), ('Gravură', 'numele familiei')],
        'features': [
            'Două piese în cruce și o stea, din placaj de mesteacăn de 12 mm',
            'Numele familiei și anul, gravate pe ramurile din față',
            'Se montează în 10 secunde, fără scule, fără șuruburi, fără lipici',
            '27 de găuri pentru globulețe mici, panglici sau ghirlandă',
            'Se desface plat și ocupă puțin loc până la anul',
            'Finisaj cu ulei-ceară, fără vopsea',
        ],
        'steps': [('Frezare CNC', 'Toate piesele se taie dintr-o singură placă de placaj de 900 × 600 mm.'),
                  ('Gravură', 'Numele familiei se gravează pe ramurile din față.'),
                  ('Șlefuire și ulei-ceară', 'Muchii netede, fibra mesteacănului pusă în valoare.'),
                  ('Montaj în 10 secunde', 'Piesa cu vârf intră de sus peste cealaltă, apoi pui steaua.')],
        'spec': [('Înălțime', '≈ 58 cm cu steaua'), ('Lățime', '≈ 41 cm; în cruce ocupă 41 × 41 cm'), ('Material', 'Placaj de mesteacăn 12 mm'),
                 ('Piese', '2 piese în cruce + stea'), ('Gravură', 'Numele familiei și anul'), ('Finisaj', 'Ulei-ceară'),
                 ('Masă', '≈ 2 kg'), ('Producție', 'Atelier propriu, Chișinău')],
        'faq': [('Ce putem grava?', 'Numele familiei, un nume sau un mesaj scurt, plus anul. Scrie-l în previzualizarea 3D de sus ca să vezi cum arată, apoi trimite-ni-l odată cu cererea.'),
                ('Cum se montează?', 'Ții în picioare piesa cu vârful tăiat drept, cobori peste ea, în cruce, piesa cu vârf și pui steaua sus. Fără scule, în 10 secunde. Se desface la fel de ușor.'),
                ('Pot comanda mai mulți, cadou pentru rude sau colegi?', 'Da. Pentru mai mulți brazi, prețul pe bucată scade. Spune-ne câte bucăți vrei și ce nume gravăm pe fiecare.')],
        'video_alt': 'Video: bradul de Crăciun, de la frezarea CNC la montaj și luminițe',
        'badge': 'Nou · Crăciun',
    },
    {
        'slug': 'casuta', 'form': 'Căsuță de iarnă cu lumină', 'name': 'Căsuță de iarnă cu lumină și numele familiei',
        'short': 'Căsuță de iarnă', 'eyebrow': 'Placaj de mesteacăn · CNC · gravură', 'engrave': True,
        'title': 'Căsuță de iarnă din lemn cu lumină și numele familiei, tăiată pe CNC — Chișinău',
        'desc': 'Căsuță-felinar din placaj de mesteacăn: 7 piese, 0 șuruburi, lumânare LED înăuntru și numele familiei gravat pe acoperiș. Tăiată pe CNC în Chișinău. Vezi-o în 3D și cere prețul.',
        'lead': 'Șapte piese din placaj de mesteacăn care intră una în alta, cu ușă, ferestre cu ochiuri, o stea și o inimă decupate pe CNC. Înăuntru pui o lumânare LED, stingi lumina și ferestrele se aprind cald. Pe acoperiș gravăm numele familiei tale. Scrie-l mai jos și vezi-o în 3D.',
        'tags': ['Placaj mesteacăn', 'Nume gravat', 'Lumânare LED'],
        'facts': [('7', 'piese, 0 șuruburi'), ('22 cm', 'lungime, 21 cm înălțime'), ('LED', 'lumânare inclusă'), ('Gravură', 'numele pe acoperiș')],
        'features': [
            'Șapte piese din placaj de mesteacăn de 6 mm, tăiate pe CNC',
            'Numele familiei gravat pe acoperișul din față',
            'Ușă cu arc, ferestre cu ochiuri, stea și inimă decupate',
            'Lumânare LED inclusă: fără foc deschis, sigură pentru copii',
            'Gaură în bază: schimbi bateria fără să desfaci căsuța',
            'Finisaj cu ulei-ceară, fără vopsea',
        ],
        'steps': [('Frezare CNC', 'Toate piesele, cu ferestrele și ușa, se taie dintr-o bucată de placaj.'),
                  ('Gravură', 'Numele familiei se gravează cu laserul pe acoperiș.'),
                  ('Șlefuire și ulei-ceară', 'Muchii netede, fibra mesteacănului pusă în valoare.'),
                  ('Montaj și lumină', 'Piesele intră una în alta, pui lumânarea LED înăuntru.')],
        'spec': [('Dimensiuni', '≈ 22 × 15 × 21 cm (lungime × adâncime × înălțime)'), ('Material', 'Placaj de mesteacăn 6 mm'),
                 ('Piese', '7: bază, 2 pereți, 2 frontoane, 2 panouri de acoperiș'), ('Gravură', 'Numele familiei pe acoperiș'),
                 ('Lumină', 'Lumânare LED cu baterie, inclusă'), ('Finisaj', 'Ulei-ceară'), ('Producție', 'Atelier propriu, Chișinău')],
        'faq': [('Ce putem grava?', 'Numele familiei, un nume sau un mesaj scurt. Scrie-l în previzualizarea 3D de sus ca să vezi cum arată, apoi trimite-ni-l odată cu cererea.'),
                ('Pot pune o lumânare adevărată?', 'Nu, căsuța e din lemn, de aceea vine cu lumânare LED. Lumina e caldă și pâlpâie ca o flacără, fără niciun risc.'),
                ('Pot comanda mai multe, cadou pentru rude sau colegi?', 'Da. Pentru mai multe căsuțe, prețul pe bucată scade. Spune-ne câte bucăți vrei și ce nume gravăm pe fiecare.')],
        'video_alt': 'Video: căsuța de iarnă, de la frezarea CNC la lumina aprinsă',
        'badge': 'Nou · cadou de iarnă', 'gandit': 'gândită',
    },
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
        'tags': ['6 sticle', 'Nume gravat', 'Cadou'], 'engrave': True,
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
    V = asset_version()
    ld = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": f"{BRAND['name']} · {BRAND['city']}",
          "legalName": BRAND['legal'], "telephone": BRAND['phone_raw'],
          "address": {"@type": "PostalAddress", "addressLocality": "Chișinău", "addressCountry": "MD"},
          "description": "Tăiere laser și frezare CNC în Chișinău: brazi de Crăciun și căsuțe de iarnă din lemn cu nume gravat, mangaluri, rafturi pentru vin cu nume gravat, suporturi de laptop din placaj, piese din lemn pe CNC până la 900 × 600 mm, la comandă."}
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
<link rel="stylesheet" href="/assets/css/site.css?v={V}">
<script type="importmap">{import_map(V)}</script>
<script type="module" src="/assets/js/app.js?v={V}"></script>
{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)}
</head>
<body>
'''

def header(active=None):
    links = ''.join(f'<a href="/{p["slug"]}/"{" aria-current=\"page\"" if active == p["slug"] else ""}>{p["short"]}</a>' for p in PRODUCTS)
    return f'''<header class="top"><div class="wrap">
  <a class="logo" href="/" aria-label="{BRAND['name']} {BRAND['city']}, pagina principală">{logo()}<span>{BRAND['name']}<br><small>{BRAND['city']}</small></span></a>
  <nav class="nav" aria-label="Produse">{links}<a href="/#servicii">Frezare CNC</a><a href="/#contact">Contact</a></nav>
  <a class="btn btn-ghost btn-sm call" href="tel:{BRAND['phone_raw']}">Sună {BRAND['phone']}</a>
</div></header>
'''

def quote_section(selected):
    opts = ''.join(f'<option{" selected" if p["form"] == selected else ""}{" data-engrave" if p.get("engrave") else ""}>{p["form"]}</option>' for p in PRODUCTS)
    for extra in ('Frezare CNC lemn', 'Altă comandă'):
        opts += f'<option{" selected" if selected == extra else ""}>{extra}</option>'
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
    <div class="field" data-engrave-field hidden><label for="f-gr">Text de gravat (nume)</label><input id="f-gr" name="gravura" maxlength="40" placeholder="ex. FAMILIA ROTARU"></div>
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
    s = head(f"{BRAND['name']} {BRAND['city']} — brazi de Crăciun și căsuțe cu lumină, cu nume, mangaluri, rafturi pentru vin, la comandă",
             'Atelier de tăiere laser și frezare CNC în Chișinău: brazi de Crăciun din lemn cu numele familiei, căsuțe de iarnă cu lumină, mangaluri din oțel, rafturi pentru vin cu nume gravat, suporturi de laptop din placaj, piese din lemn pe CNC până la 900 × 600 mm. Cere prețul.',
             '/', '/assets/img/og-home.jpg')
    s += header()
    s += f'''<main>
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">Atelier laser · CNC · {BRAND['city']}</span>
    <h1 style="margin-top:14px">Obiecte din metal și lemn, <span class="accent">tăiate la milimetru</span></h1>
    <p class="lead">Brazi de Crăciun și căsuțe de iarnă din lemn cu numele familiei, mangaluri, rafturi pentru vin cu nume gravat, suporturi de laptop din placaj și piese din lemn pe CNC, după desenul tău. Le facem la comandă în atelierul nostru din Chișinău. Rotește-le în 3D, apoi cere prețul.</p>
    <div class="row"><a class="btn btn-primary" href="#cere-pret">Cere prețul</a><a class="btn btn-ghost" href="#produse">Vezi produsele</a></div>
  </div>
  <div>
    <div class="tabs" role="tablist" id="hero-tabs" aria-label="Alege produsul">{tabs}</div>
    {viewer(PRODUCTS[0]['slug'], 'hero-controls', tabs='#hero-tabs')}
    <p style="margin-top:10px"><a id="hero-link" href="/{PRODUCTS[0]['slug']}/" style="color:var(--accent);font-weight:600;text-decoration:none">Deschide pagina produsului →</a></p>
  </div>
</div></section>

<section id="produse"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Produse</span><h2>Cinci produse, făcute la comandă</h2>
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

<section id="servicii"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Tăiem la comandă</span><h2>Lemn pe CNC, metal cu laser</h2>
  <p class="lead">Pe lângă produsele de mai sus, tăiem piese după schița, poza sau fișierul tău. Dacă nu ai desen, îl facem noi în CAD.</p></div>
  <div class="svc">
    <article class="card"><div class="body">
      <div class="tags"><span class="tag">Frezare CNC</span><span class="tag">Lemn</span></div>
      <h3>Placaj, MDF, lemn masiv, plastic</h3>
      <div class="fact"><b>900 × 600 mm</b><span>suprafața de lucru a frezei CNC</span></div>
      <ul class="list"><li>Piese plane și decupaje: litere, panouri, cutii, mobilier mic, decor</li><li>Îmbinări fără șuruburi, ca la WOODSTAND 01</li><li>Din fișier DXF sau după schița ta</li></ul>
      <div class="row"><a class="btn btn-primary btn-sm" href="#cere-pret" data-quote="Frezare CNC lemn">Cere prețul pentru frezare</a></div>
    </div></article>
    <article class="card"><div class="body">
      <div class="tags"><span class="tag">Tăiere laser</span><span class="tag">Metal</span></div>
      <h3>Oțel tăiat, asamblat și vopsit</h3>
      <div class="fact"><b>De la idee la piesă</b><span>tăiere, asamblare, vopsire</span></div>
      <ul class="list"><li>Mangaluri, rafturi, decor pentru casă și curte</li><li>Nume, monograme și logo-uri tăiate sau gravate</li><li>Vopsire electrostatică sau termorezistentă</li></ul>
      <div class="row"><a class="btn btn-ghost btn-sm" href="#cere-pret" data-quote="Altă comandă">Trimite ideea</a></div>
    </div></article>
  </div>
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
  <div><div class="sec-head"><span class="eyebrow">Ce primești</span><h2>{p['short']}, {p.get('gandit', 'gândit')} până la detaliu</h2></div>
  <ul class="list">{feats}</ul></div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Cum îl facem</span><h2>Patru pași, în atelierul nostru</h2></div>
  <ol class="steps">{steps}</ol>
</div></section>

<section class="band"><div class="wrap split split-eq">
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
