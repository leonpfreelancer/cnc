// Worker cu fișiere statice (Cloudflare Workers + Static Assets).
// - /api/cerere      formularul „Cere prețul”
// - /sitemap.xml     generat pe domeniul curent
// - /robots.txt      generat pe domeniul curent (adresele *.workers.dev nu se indexează)
// - restul           fișierele din public/, iar în HTML canonical / og:url / og:image devin adrese absolute
import { handleCerere } from './cerere.js';

const PAGES = ['/', '/brad-craciun/', '/mangal/', '/raft-vin/', '/suport-laptop/'];

class Abs {
  constructor(origin, attr) { this.origin = origin; this.attr = attr; }
  element(el) { const v = el.getAttribute(this.attr); if (v && v.startsWith('/')) el.setAttribute(this.attr, this.origin + v); }
}
const isPreview = host => host.endsWith('.workers.dev') || host.endsWith('.pages.dev');

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = url.origin;

    if (url.pathname === '/api/cerere') return handleCerere(request, env);

    if (url.pathname === '/sitemap.xml') {
      const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
        PAGES.map(p => `  <url><loc>${origin}${p}</loc></url>`).join('\n') + `\n</urlset>\n`;
      return new Response(xml, { headers: { 'content-type': 'application/xml; charset=utf-8', 'cache-control': 'public, max-age=3600' } });
    }
    if (url.pathname === '/robots.txt') {
      const body = isPreview(url.hostname) ? 'User-agent: *\nDisallow: /\n'
        : `User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: ${origin}/sitemap.xml\n`;
      return new Response(body, { headers: { 'content-type': 'text/plain; charset=utf-8' } });
    }

    const res = await env.ASSETS.fetch(request);
    if (!(res.headers.get('content-type') || '').includes('text/html')) return res;
    return new HTMLRewriter()
      .on('link[rel="canonical"]', new Abs(origin, 'href'))
      .on('meta[property="og:url"]', new Abs(origin, 'content'))
      .on('meta[property="og:image"]', new Abs(origin, 'content'))
      .transform(res);
  },
};
