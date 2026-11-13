const PAGES = ['/', '/mangal/', '/raft-vin/', '/suport-laptop/'];
export function onRequest({ request }) {
  const o = new URL(request.url).origin;
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    PAGES.map(p => `  <url><loc>${o}${p}</loc></url>`).join('\n') + `\n</urlset>\n`;
  return new Response(xml, { headers: { 'content-type': 'application/xml; charset=utf-8', 'cache-control': 'public, max-age=3600' } });
}
