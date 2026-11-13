# Atelier Laser · Chișinău — site de prezentare

Site static cu modele 3D interactive pentru patru produse și formular „Cere prețul”.
Rulează ca **Cloudflare Worker cu fișiere statice**: paginile din `public/` sunt servite direct, iar `src/worker.js` se ocupă de formular (`/api/cerere`), `sitemap.xml`, `robots.txt` și adresele absolute din HTML.

| Pagina | Ce are |
| --- | --- |
| `/` | erou cu 3D (comutare între produse), carduri, „Cum lucrăm”, servicii (frezare CNC lemn 900 × 600 mm, tăiere laser metal), formular |
| `/brad-craciun/` | brad de Crăciun din placaj: geometria reală din fișierele CNC, **numele familiei se vede live gravat**, ghirlandă LED, desfacerea arată ordinea corectă de montaj |
| `/mangal/` | mangal tăiat cu laser: 3D cu jar și frigărui, desfacere în piese, culori |
| `/raft-vin/` | raft pentru vin: 3D cu sticle, **numele gravat se vede live pe capac**, culori |
| `/suport-laptop/` | WOODSTAND 01: geometria reală din scriptul Fusion 360, cu laptop de referință |

Ce alege omul în 3D (culoarea, textul gravat) ajunge automat în formular.

## Publicare pe Cloudflare (Workers)

1. Cloudflare → **Workers & Pages** → **Create** → **Import a repository** → `leonpfreelancer/cnc`.
2. Lasă setările implicite: build command gol, deploy command **`npx wrangler deploy`**. Toată configurația e în `wrangler.toml`.
3. **Numele Worker-ului trebuie să fie același cu `name` din `wrangler.toml`** (acum `cnc`). Dacă Worker-ul tău are alt nume, schimbă linia `name = "cnc"`.
4. După deploy, site-ul apare la `https://cnc.<cont>.workers.dev`. Adresele `.workers.dev` nu se indexează în Google.
5. **Domeniul**: Worker → **Settings** → **Domains & Routes** → **Add** → **Custom domain** → scrie domeniul (DNS-ul trebuie să fie în Cloudflare).

Orice `git push` pe `main` republică site-ul automat.

## Cererile de preț pe Telegram

1. În Telegram, scrie-i lui **@BotFather** → `/newbot` → primești un **token**.
2. Trimite orice mesaj botului tău, apoi deschide în browser
   `https://api.telegram.org/bot<TOKEN>/getUpdates` și copiază numărul de la `"chat":{"id": …}`.
3. Cloudflare → Worker-ul tău → **Settings** → **Variables and Secrets** → **Add** → tip **Secret**:
   - `TELEGRAM_BOT_TOKEN` = tokenul
   - `TELEGRAM_CHAT_ID` = numărul chat-ului
4. Secretele se aplică imediat, fără build nou. De acum fiecare cerere vine ca mesaj în Telegram.

Dacă Telegram nu e configurat și nici KV, formularul răspunde cu eroare, iar site-ul îi arată omului numărul de telefon.

### Opțional: păstrarea cererilor în KV

`npx wrangler kv namespace create CERERI`, apoi decomentează blocul `[[kv_namespaces]]` din `wrangler.toml` și pune id-ul primit.
Cererile se păstrează un an, iar de la același IP se acceptă cel mult 5 cereri pe oră.

## Modificări

- **Texte, telefon, nume firmă**: în `tools/gen.py` (`BRAND`, `PRODUCTS`), apoi `python3 tools/gen.py` regenerează paginile din `public/`.
- **Modele 3D**: `public/assets/js/models/*.js`. Raftul pentru vin și mangalul sunt reconstruite după video-uri. Dimensiunile sunt constante la începutul fiecărui fișier și se pot potrivi cu desenele reale. WOODSTAND 01 și bradul folosesc contururile reale de frezare (`woodstand-data.json`, `brad-data.json`).
- **Video-uri**: `public/assets/media/` (720p, comprimate pentru web).
- **Imagini pentru link-uri** (Facebook, Viber, Telegram): `public/assets/img/og-*.jpg`.

## Rulare locală

```bash
npx wrangler dev
```

Deschide `http://localhost:8787`. Pentru Telegram local, pune `TELEGRAM_BOT_TOKEN` și `TELEGRAM_CHAT_ID` în fișierul `.dev.vars` (nu se urcă în git).

## Tehnic

- three.js r160 inclus local în `public/assets/js/vendor/` (licență MIT, vezi `three-LICENSE.txt`), fără CDN.
- `src/worker.js` transformă `canonical`, `og:url` și `og:image` în adrese absolute pe domeniul curent și generează `sitemap.xml` și `robots.txt`.
- `src/cerere.js`: validare, capcană anti-spam, Telegram, KV opțional cu limită de 5 cereri/oră/IP.
- `public/_headers`: antete de securitate și cache, aplicate de Cloudflare pe fișierele statice.
