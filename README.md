# Atelier Laser · Chișinău — site de prezentare

Site static cu modele 3D interactive pentru trei produse și formular „Cere prețul”.
Rulează pe **Cloudflare Pages**: paginile sunt statice, iar formularul trimite cererile printr-o funcție Cloudflare (`functions/api/cerere.js`).

| Pagina | Ce are |
| --- | --- |
| `/` | erou cu 3D (comutare între produse), carduri, „Cum lucrăm”, servicii (frezare CNC lemn 900 × 600 mm, tăiere laser metal), formular |
| `/mangal/` | mangal tăiat cu laser: 3D cu jar și frigărui, desfacere în piese, culori |
| `/raft-vin/` | raft pentru vin: 3D cu sticle, **numele gravat se vede live pe capac**, culori |
| `/suport-laptop/` | WOODSTAND 01: geometria reală din scriptul Fusion 360, cu laptop de referință |

Ce alege omul în 3D (culoarea, textul gravat) ajunge automat în formular.

## Publicare pe Cloudflare Pages

1. Cloudflare → **Workers & Pages** → **Create** → **Pages** → **Connect to Git** → alege `leonpfreelancer/cnc`.
2. Setări de build:
   - Framework preset: **None**
   - Build command: *(gol)*
   - Build output directory: **`public`**
3. **Save and Deploy**. Site-ul apare la `https://<proiect>.pages.dev`. Adresa `.pages.dev` nu se indexează în Google (vezi `functions/robots.txt.js`).
4. **Domeniul**: proiect → **Custom domains** → **Set up a custom domain** → scrie domeniul. Dacă DNS-ul domeniului e deja în Cloudflare, înregistrarea se creează automat.

Orice `git push` pe `main` republică site-ul automat.

## Cererile de preț pe Telegram

1. În Telegram, scrie-i lui **@BotFather** → `/newbot` → primești un **token**.
2. Trimite orice mesaj botului tău, apoi deschide în browser
   `https://api.telegram.org/bot<TOKEN>/getUpdates` și copiază numărul de la `"chat":{"id": …}`.
3. Cloudflare → proiectul Pages → **Settings** → **Variables and Secrets** → adaugă ca **Secret**:
   - `TELEGRAM_BOT_TOKEN` = tokenul
   - `TELEGRAM_CHAT_ID` = numărul chat-ului
4. Redeploy (Deployments → ⋯ → Retry deployment). De acum fiecare cerere vine ca mesaj în Telegram.

Dacă Telegram nu e configurat și nici KV, formularul răspunde cu eroare, iar site-ul îi arată omului numărul de telefon.

### Opțional: păstrarea cererilor în KV

`npx wrangler kv namespace create CERERI`, apoi decomentează blocul `[[kv_namespaces]]` din `wrangler.toml` și pune id-ul primit.
Cererile se păstrează un an, iar de la același IP se acceptă cel mult 5 cereri pe oră.

## Modificări

- **Texte, telefon, nume firmă**: în `tools/gen.py` (`BRAND`, `PRODUCTS`), apoi `python3 tools/gen.py` regenerează paginile din `public/`.
- **Modele 3D**: `public/assets/js/models/*.js`. Raftul pentru vin și mangalul sunt reconstruite după video-uri. Dimensiunile sunt constante la începutul fiecărui fișier și se pot potrivi cu desenele reale. WOODSTAND 01 folosește contururile reale (`woodstand-data.json`).
- **Video-uri**: `public/assets/media/` (720p, comprimate pentru web).
- **Imagini pentru link-uri** (Facebook, Viber, Telegram): `public/assets/img/og-*.jpg`.

## Rulare locală

```bash
npx wrangler pages dev public --kv CERERI
```

Deschide `http://localhost:8788`. Cererile se salvează în KV-ul local.

## Tehnic

- three.js r160 inclus local în `public/assets/js/vendor/` (licență MIT, vezi `three-LICENSE.txt`), fără CDN.
- `functions/_middleware.js` transformă `canonical`, `og:url` și `og:image` în adrese absolute pe domeniul curent.
- `functions/sitemap.xml.js` și `functions/robots.txt.js` se generează pe domeniul curent.
