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
        'badge': 'Nou pentru Crăciun',
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
        'badge': 'Prototip, precomenzi deschise',
    },
]

import random

# ---------- decor: diorama (munți, brazi, sfere, foaie cu val) ----------
def logo():
    return ('<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#22302a"/>'
            '<path d="M9 23 16 7l7 16" fill="none" stroke="#eeede6" stroke-width="3.2" stroke-linejoin="round"/>'
            '<path d="M11.5 18h9" stroke="#3fa874" stroke-width="3"/></svg>')

def paper_svg(uid):
    """Foaia de hârtie cu marginea de jos în val și panglica verde dedesubt (motivul din referință)."""
    return f'''<svg class="paper-bg" viewBox="0 0 1200 600" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs>
<linearGradient id="rb{uid}" x1="0" x2="1"><stop offset="0" stop-color="#2f8f60" stop-opacity="0"/><stop offset=".3" stop-color="#2f8f60" stop-opacity=".9"/><stop offset=".62" stop-color="#47ad79" stop-opacity=".75"/><stop offset="1" stop-color="#2f8f60" stop-opacity=".05"/></linearGradient>
<linearGradient id="pp{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3f2ec"/><stop offset="1" stop-color="#e5e4dc"/></linearGradient>
<filter id="bl{uid}" x="-5%" y="-60%" width="110%" height="220%"><feGaussianBlur stdDeviation="9"/></filter></defs>
<path d="M0 478C210 568 360 408 600 458S980 568 1200 438V520C980 640 820 482 600 532S210 640 0 552Z" fill="url(#rb{uid})" filter="url(#bl{uid})"/>
<path d="M0 0H1200V430C980 560 820 400 600 450S210 560 0 470Z" fill="url(#pp{uid})"/>
</svg>'''

def mountains(uid):
    peaks = ('M0 360 40 262 92 204 128 226 178 140 226 182 268 150 336 236 398 206 468 262 520 244 600 300V360Z',
             'M70 360 150 220 196 168 236 44 258 76 288 30 334 146 382 204 432 246 520 304 560 360Z',
             'M0 360 66 300 124 262 172 286 240 232 302 282 362 318 420 360Z')
    return f'''<svg class="mountains" viewBox="0 0 600 360" preserveAspectRatio="xMidYMax meet" aria-hidden="true" focusable="false"><defs>
<linearGradient id="ma{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe2dc"/><stop offset="1" stop-color="#aeb8ab"/></linearGradient>
<linearGradient id="mb{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d2d6cf"/><stop offset="1" stop-color="#8d998a"/></linearGradient>
<linearGradient id="mc{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9cfc6"/><stop offset="1" stop-color="#7d8a7b"/></linearGradient>
<linearGradient id="fg{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset=".5" stop-color="#eeede6" stop-opacity="0"/><stop offset="1" stop-color="#eeede6" stop-opacity=".8"/></linearGradient>
<clipPath id="cl{uid}">{''.join(f'<path d="{d}"/>' for d in peaks)}</clipPath></defs>
<path fill="url(#ma{uid})" d="{peaks[0]}"/>
<path fill="url(#mb{uid})" d="{peaks[1]}"/>
<path fill="#f4f4ef" opacity=".6" d="M236 44 258 76 288 30 300 74 278 98 262 90 242 116 220 96Z"/>
<path fill="#6f7d6d" opacity=".22" d="M288 30 334 146 382 204 432 246 520 304 560 360H300L310 220 296 120Z"/>
<path fill="url(#mc{uid})" d="{peaks[2]}"/>
<rect width="600" height="360" fill="url(#fg{uid})" clip-path="url(#cl{uid})"/>
</svg>'''

def pines(seed, n, w=600, h=220, cls=''):
    """Brazi stilizați, cu o jumătate luminată și una în umbră, așezați pe aceeași linie de bază."""
    rnd = random.Random(seed)
    trees = []
    for i in range(n):
        x = (i + 0.5) * w / n + rnd.uniform(-0.35, 0.35) * w / n
        th = h * rnd.uniform(0.42, 1.0)
        trees.append((th, x, th * rnd.uniform(0.34, 0.42)))
    trees.sort(key=lambda t: -t[0])
    pal = [('#5b8a60', '#2f5b3e'), ('#6a9668', '#3a684a'), ('#4f7f57', '#284f37')]
    out = []
    for th, x, tw in trees:
        lc, dc = rnd.choice(pal); base = h; trunk = th * 0.08
        out.append(f'<rect x="{x - tw * .05:.1f}" y="{base - trunk:.1f}" width="{tw * .1:.1f}" height="{trunk:.1f}" fill="#5c4b3b"/>')
        for k in range(4):
            yb = base - trunk - k * (th - trunk) * 0.21
            top = base - th + (3 - k) * th * 0.11
            hw = tw / 2 * (1 - k * 0.19)
            out.append(f'<path d="M{x - hw:.1f} {yb:.1f}L{x:.1f} {top:.1f}V{yb:.1f}Z" fill="{lc}"/><path d="M{x:.1f} {top:.1f}L{x + hw:.1f} {yb:.1f}H{x:.1f}Z" fill="{dc}"/>')
    return f'<svg class="pines {cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMax meet" aria-hidden="true" focusable="false">{"".join(out)}</svg>'

def orbs(spec):
    """Sfere de piatră care plutesc deasupra scenei: (stânga %, sus %, mărime px, clasă)."""
    return ''.join(f'<span class="orb {c}" style="left:{l}%;top:{t}%;--s:{s}px;--d:{i * 1.7:.1f}s" aria-hidden="true"></span>'
                   for i, (l, t, s, c) in enumerate(spec))

ICONS = {
    'talk': '<path d="M5 6.5h22a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H14l-6 5v-5H5a2 2 0 0 1-2-2v-12a2 2 0 0 1 2-2Z"/><path d="M9 12.5h14M9 16.5h9"/>',
    'cut': '<path d="M16 3v10"/><path d="m12.5 10 3.5 4 3.5-4"/><path d="M3 21h26v6H3z"/><path d="M11 21c1.5-2.5 3-3.5 5-3.5s3.5 1 5 3.5"/>',
    'join': '<path d="M5 9h10v18H5z"/><path d="M10 9v8"/><path d="M17 5h10v18H17z"/><path d="M22 23v-8"/>',
    'finish': '<path d="M16 3c4.5 6 8.5 10 8.5 15.5a8.5 8.5 0 0 1-17 0C7.5 13 11.5 9 16 3Z"/><path d="M12 19.5a4 4 0 0 0 4 4"/>',
    'engrave': '<path d="M21 4l7 7-14 14H7v-7L21 4Z"/><path d="M18 7l7 7"/><path d="M4 29h24"/>',
    'done': '<path d="M5 13h22v15H5z"/><path d="M3 9h26v4H3z"/><path d="M16 9v19"/><path d="M16 9c-2-5-8-6-8-2 0 2 4 2 8 2Zm0 0c2-5 8-6 8-2 0 2-4 2-8 2Z"/>',
}
def icon(name):
    return f'<svg class="ic" viewBox="0 0 32 32" width="40" height="40" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'

def icon_for(title):
    t = title.lower()
    for keys, ic in ((('spui', 'cerere'), 'talk'), (('gravur',), 'engrave'), (('tăiere', 'frezare', 'laser', 'cnc'), 'cut'),
                     (('asamblare', 'montaj'), 'join'), (('vopsi', 'ulei', 'șlefuire', 'finisaj'), 'finish'), (('gata',), 'done')):
        if any(k in t for k in keys): return ic
    return 'done'

def iconrow(steps):
    return '<ol class="iconrow">' + ''.join(f'<li>{icon(icon_for(a))}<h3>{a}</h3><p>{b}</p></li>' for a, b in steps) + '</ol>'

# ---------- schelet pagină ----------
def head(title, desc, path, image, extra_ld=None):
    V = asset_version()
    ld = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": f"{BRAND['name']} · {BRAND['city']}",
          "legalName": BRAND['legal'], "telephone": BRAND['phone_raw'],
          "address": {"@type": "PostalAddress", "addressLocality": "Chișinău", "addressCountry": "MD"},
          "description": "Tăiere laser și frezare CNC în Chișinău: brazi de Crăciun din lemn cu nume gravat, mangaluri, rafturi pentru vin cu nume gravat, suporturi de laptop din placaj, piese din lemn pe CNC până la 900 × 600 mm, la comandă."}
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
<meta name="theme-color" content="#a5b6a2">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&display=swap" rel="stylesheet">
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
  <a class="logo" href="/" aria-label="{BRAND['name']} {BRAND['city']}, pagina principală">{logo()}<span>{BRAND['name']}<small>{BRAND['city']}</small></span></a>
  <nav class="nav" aria-label="Produse">{links}<a href="/#servicii">Frezare CNC</a><a href="/#cere-pret">Contact</a></nav>
  <a class="btn btn-ghost btn-sm call" href="tel:{BRAND['phone_raw']}">Sună {BRAND['phone']}</a>
</div></header>
'''

def quote_section(selected):
    opts = ''.join(f'<option{" selected" if p["form"] == selected else ""}{" data-engrave" if p.get("engrave") else ""}>{p["form"]}</option>' for p in PRODUCTS)
    for extra in ('Frezare CNC lemn', 'Altă comandă'):
        opts += f'<option{" selected" if selected == extra else ""}>{extra}</option>'
    return f'''<section id="cere-pret"><div class="wrap quote">
  <div class="sec-head">
    <h2>Află prețul în aceeași zi</h2>
    <p class="lead">Lasă-ne numărul și ce ai ales. Revenim cu prețul și termenul, fără obligații. Dacă preferi, sună-ne direct.</p>
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
      <div class="field"><label for="f-tel">Telefon (obligatoriu)</label><input id="f-tel" name="telefon" type="tel" autocomplete="tel" required maxlength="30" placeholder="+373 …"></div>
    </div>
    <div class="f-row">
      <div class="field"><label for="f-contact">Cum să te contactăm</label><select id="f-contact" name="contact"><option>Apel</option><option>Viber</option><option>WhatsApp</option><option>Telegram</option></select></div>
      <div class="field"><label for="f-fin">Finisaj sau culoare</label><input id="f-fin" name="finisaj" maxlength="60" placeholder="ex. negru mat"></div>
    </div>
    <div class="field" data-engrave-field hidden><label for="f-gr">Text de gravat</label><input id="f-gr" name="gravura" maxlength="40" placeholder="ex. FAMILIA ROTARU"></div>
    <div class="field"><label for="f-det">Detalii: dimensiuni, idee, termen</label><textarea id="f-det" name="detalii" maxlength="1500" placeholder="Spune-ne ce ai nevoie. Poți descrie dimensiunile sau ideea."></textarea></div>
    <div class="hp" aria-hidden="true"><label for="f-web">Nu completa</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
    <button class="btn btn-primary" type="submit">Trimite cererea de preț</button>
    <p class="status" role="status" aria-live="polite"></p>
    <p class="note">Folosim datele doar ca să-ți răspundem la cerere.</p>
  </form>
</div></section>
'''

def footer():
    links = ''.join(f'<a href="/{p["slug"]}/">{p["short"]}</a>' for p in PRODUCTS)
    return f'''<footer><div class="wrap">
  <div class="f-brand"><a class="logo" href="/">{logo()}<span>{BRAND['name']}<small>{BRAND['city']}</small></span></a>
  <p>Tăiere laser și frezare CNC, produse la comandă.</p></div>
  <nav class="f-links" aria-label="Produse">{links}<a href="/#servicii">Frezare CNC</a></nav>
  <div class="f-legal"><a href="tel:{BRAND['phone_raw']}">{BRAND['phone']}</a><span>{BRAND['legal']}, Chișinău, Republica Moldova</span><span>© <span data-year>2026</span></span></div>
</div></footer>
<div class="mbar"><a class="btn btn-primary" href="#cere-pret">Cere prețul</a><a class="btn btn-ghost" href="tel:{BRAND['phone_raw']}">Sună</a></div>
</body></html>
'''

def viewer(slug, badge=None, tabs=None, ctl='#ctl'):
    b = f'<span class="badge">{badge}</span>' if badge else ''
    t = f' data-tabs="{tabs}"' if tabs else ''
    return (f'<div class="viewer" data-viewer data-model="{slug}" data-controls="{ctl}" data-ground="30"{t}>'
            f'<div class="loading">Se încarcă modelul 3D…</div>{b}<span class="hint">Trage ca să rotești, ciupește pentru zoom</span></div>')

def diorama(uid, viewer_html, orb_spec, seed):
    return (f'<div class="diorama">{orbs(orb_spec)}{mountains(uid)}{pines(seed, 4, 300, 220, "pines-r")}'
            f'{pines(seed + 1, 11, 600, 200, "pines-l")}<div class="shelf" aria-hidden="true"></div><div class="scene">{viewer_html}</div></div>')

# ---------- pagini ----------
def home():
    cards = ''
    for p in PRODUCTS:
        cards += f'''<article class="card">
  <a class="media" href="/{p['slug']}/" tabindex="-1" aria-hidden="true"><img src="/assets/media/{p['slug']}-poster.jpg" alt="" loading="lazy" width="720" height="1280"></a>
  <div class="body"><h3><a href="/{p['slug']}/">{p['name']}</a></h3><p>{p['desc'].split('. Vezi')[0]}.</p>
  <ul class="tags">{''.join(f'<li>{t}</li>' for t in p['tags'])}</ul>
  <div class="row"><a class="btn btn-primary btn-sm" href="#cere-pret" data-quote="{p['form']}">Cere prețul</a><a class="btn btn-ghost btn-sm" href="/{p['slug']}/">Vezi în 3D</a></div></div>
</article>'''
    tabs = ''.join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-model="{p["slug"]}" data-href="/{p["slug"]}/">{p["short"]}</button>' for i, p in enumerate(PRODUCTS))
    s = head(f"{BRAND['name']} {BRAND['city']} — brazi de Crăciun cu nume, mangaluri, rafturi pentru vin, la comandă",
             'Atelier de tăiere laser și frezare CNC în Chișinău: brazi de Crăciun din lemn cu numele familiei, mangaluri din oțel, rafturi pentru vin cu nume gravat, suporturi de laptop din placaj, piese din lemn pe CNC până la 900 × 600 mm. Cere prețul.',
             '/', '/assets/img/og-home.jpg')
    s += header()
    orb_spec = [(38, 2, 44, ''), (60, 9, 18, ''), (86, 4, 58, ''), (94, 30, 22, 'o-hide'), (3, 6, 26, 'o-hide'), (47, 5, 14, 'o-hide')]
    s += f'''<main>
<section class="hero"><div class="wrap">
  <div class="stage stage-home">
    <div class="paper">{paper_svg('h')}<div class="paper-text">
      <h1>Obiecte din lemn și metal, tăiate la milimetru</h1>
      <p class="lead">Brazi de Crăciun cu numele familiei, mangaluri, rafturi pentru vin cu nume gravat și suporturi de laptop din placaj. Le tăiem pe CNC și cu laser în atelierul nostru din {BRAND['city']}.</p>
      <div class="row"><a class="btn btn-primary" href="#cere-pret">Cere prețul</a><a class="btn btn-ghost" href="#produse">Vezi produsele</a></div>
    </div></div>
    {diorama('h', viewer(PRODUCTS[0]['slug'], tabs='#hero-tabs', ctl='#hero-controls'), orb_spec, 11)}
  </div>
  <div class="under">
    <div class="tabs" role="tablist" id="hero-tabs" aria-label="Alege produsul">{tabs}</div>
    <div class="controls" id="hero-controls"></div>
    <a id="hero-link" class="textlink" href="/{PRODUCTS[0]['slug']}/">Deschide pagina produsului</a>
  </div>
</div></section>

<section id="produse"><div class="wrap">
  <div class="sec-head"><h2>Patru produse, făcute la comandă</h2>
  <p class="lead">Fiecare are pagina lui cu model 3D, video din atelier și formular de preț.</p></div>
  <div class="cards">{cards}</div>
  <div class="shelf shelf-cards" aria-hidden="true"></div>
</div></section>

<section class="band"><div class="wrap">
  <div class="sec-head"><h2>De la cerere la produs gata</h2></div>
  {iconrow([('Ne spui ce vrei', 'Produsul, dimensiunile, culoarea sau numele de gravat.'),
            ('Tăiere laser sau CNC', 'Oțelul se taie cu laser, lemnul pe freza CNC, la precizie de atelier.'),
            ('Asamblare și finisaj', 'Vopsire electrostatică, vopsea termorezistentă sau ulei-ceară.'),
            ('Gata de folosit', 'Îți dăm produsul gata de folosit sau de oferit cadou.')])}
</div></section>

<section id="servicii"><div class="wrap">
  <div class="sec-head"><h2>Lemn pe CNC, metal cu laser</h2>
  <p class="lead">Pe lângă produsele de mai sus, tăiem piese după schița, poza sau fișierul tău. Dacă nu ai desen, îl facem noi în CAD.</p></div>
  <div class="svc">
    <article class="panel">
      <h3>Frezare CNC în lemn</h3>
      <p class="big"><b>900 × 600 mm</b> suprafața de lucru a frezei</p>
      <ul class="list"><li>Placaj, MDF, lemn masiv, plastic</li><li>Litere, panouri, cutii, mobilier mic, decor</li><li>Îmbinări fără șuruburi, ca la bradul și suportul nostru</li><li>Din fișier DXF sau după schița ta</li></ul>
      <div class="row"><a class="btn btn-primary btn-sm" href="#cere-pret" data-quote="Frezare CNC lemn">Cere prețul pentru frezare</a></div>
    </article>
    <article class="panel">
      <h3>Tăiere laser în metal</h3>
      <p class="big"><b>De la idee la piesă</b> tăiere, asamblare, vopsire</p>
      <ul class="list"><li>Mangaluri, rafturi, decor pentru casă și curte</li><li>Nume, monograme și logo-uri tăiate sau gravate</li><li>Vopsire electrostatică sau termorezistentă</li></ul>
      <div class="row"><a class="btn btn-ghost btn-sm" href="#cere-pret" data-quote="Altă comandă">Trimite ideea</a></div>
    </article>
  </div>
</div></section>
</main>
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
    spec = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in p['spec'])
    faq = ''.join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in p['faq'])
    orb_spec = [(70, 2, 40, ''), (80, 12, 16, ''), (8, 4, 24, 'o-hide'), (93, 22, 28, 'o-hide')]
    meta = p['eyebrow'].replace(' · ', ', ')
    s += f'''<main>
<section class="p-hero"><div class="wrap">
  <p class="crumbs"><a href="/">Acasă</a> / {p['short']}</p>
  <div class="p-grid">
    <div>
      <div class="stage stage-prod"><div class="paper">{paper_svg('p')}</div>{diorama('p', viewer(p['slug'], p.get('badge')), orb_spec, 23)}</div>
      <div class="controls" id="ctl"></div>
    </div>
    <div class="p-info">
      <h1>{p['name']}</h1>
      <p class="meta">{meta}</p>
      <p class="lead">{p['lead']}</p>
      <div class="facts">{facts}</div>
      <div class="row"><a class="btn btn-primary" href="#cere-pret">Cere prețul</a><a class="btn btn-ghost" href="tel:{BRAND['phone_raw']}">Sună {BRAND['phone']}</a></div>
    </div>
  </div>
</div></section>

<section><div class="wrap split">
  <div class="frame"><video src="/assets/media/{p['slug']}.mp4" poster="/assets/media/{p['slug']}-poster.jpg" controls playsinline preload="none" aria-label="{E(p['video_alt'])}"></video></div>
  <div><div class="sec-head"><h2>Ce primești</h2></div>
  <ul class="list">{feats}</ul></div>
</div></section>

<section class="band"><div class="wrap">
  <div class="sec-head"><h2>Cum îl facem în atelier</h2></div>
  {iconrow(p['steps'])}
</div></section>

<section><div class="wrap split split-eq">
  <div class="panel"><h2>Specificații</h2><table class="spec">{spec}</table></div>
  <div class="panel"><h2>Întrebări frecvente</h2>{faq}</div>
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
