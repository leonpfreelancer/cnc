// POST /api/cerere — primește cererile „Cere prețul” din site.
// Notificare: Telegram (TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID) și/sau păstrare în KV (binding CERERI).
// Fără niciuna configurată, răspunde 503 și site-ul îi arată omului numărul de telefon.

const PRODUSE = ['Mangal', 'Raft pentru vin', 'Suport laptop WOODSTAND 01', 'Frezare CNC lemn', 'Altă comandă'];
const LIM = { nume: 80, telefon: 30, contact: 20, finisaj: 60, gravura: 40, detalii: 1500, pagina: 120 };

const json = (obj, status = 200) => new Response(JSON.stringify(obj), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
});
const clean = (v, n) => String(v ?? '').replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, n);

export async function onRequestPost({ request, env }) {
  let body;
  try {
    const ct = request.headers.get('content-type') || '';
    body = ct.includes('application/json') ? await request.json() : Object.fromEntries(await request.formData());
  } catch { return json({ ok: false, error: 'bad_request' }, 400); }

  // capcană pentru roboți: câmpul ascuns trebuie să fie gol
  if (clean(body.website, 200)) return json({ ok: true });

  const c = {};
  for (const k of Object.keys(LIM)) c[k] = clean(body[k], LIM[k]);
  c.detalii = String(body.detalii ?? '').replace(/[\u0000-\u0008\u000b-\u001f\u007f]/g, ' ').trim().slice(0, LIM.detalii);
  c.produs = PRODUSE.includes(body.produs) ? body.produs : 'Altă comandă';
  const q = parseInt(body.cantitate, 10); c.cantitate = Number.isFinite(q) && q > 0 && q < 1000 ? q : 1;
  if (c.telefon.replace(/\D/g, '').length < 6) return json({ ok: false, error: 'telefon' }, 422);

  const ip = request.headers.get('cf-connecting-ip') || '';
  // limită simplă: max. 5 cereri / oră / IP (doar dacă există KV)
  if (env.CERERI && ip) {
    const key = `rl:${ip}`; const n = parseInt(await env.CERERI.get(key) || '0', 10);
    if (n >= 5) return json({ ok: false, error: 'prea_multe' }, 429);
    await env.CERERI.put(key, String(n + 1), { expirationTtl: 3600 });
  }

  const when = new Date().toLocaleString('ro-MD', { timeZone: 'Europe/Chisinau' });
  const text = [
    `Cerere de preț — ${c.produs}`,
    `Telefon: ${c.telefon}` + (c.contact ? ` (${c.contact})` : ''),
    c.nume && `Nume: ${c.nume}`,
    `Cantitate: ${c.cantitate}`,
    c.finisaj && `Finisaj: ${c.finisaj}`,
    c.gravura && `Gravură: ${c.gravura}`,
    c.detalii && `Detalii: ${c.detalii}`,
    `Pagina: ${c.pagina || '-'} · ${when}`,
  ].filter(Boolean).join('\n');

  let delivered = false;
  if (env.CERERI) {
    await env.CERERI.put(`cerere:${Date.now()}:${crypto.randomUUID()}`, JSON.stringify({ ...c, ip, la: new Date().toISOString() }),
      { expirationTtl: 60 * 60 * 24 * 365 });
    delivered = true;
  }
  if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
    const r = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text, disable_web_page_preview: true }),
    });
    delivered = delivered || r.ok;
    if (!r.ok && !env.CERERI) return json({ ok: false, error: 'telegram' }, 502);
  }
  if (!delivered) return json({ ok: false, error: 'neconfigurat' }, 503);
  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: 'method' }, 405);
