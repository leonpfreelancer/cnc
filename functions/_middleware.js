// Transformă adresele relative din <link rel=canonical> și og:url / og:image în adrese absolute,
// folosind domeniul pe care rulează site-ul (orice domeniu legat în Cloudflare Pages).
class Abs {
  constructor(origin, attr) { this.origin = origin; this.attr = attr; }
  element(el) { const v = el.getAttribute(this.attr); if (v && v.startsWith('/')) el.setAttribute(this.attr, this.origin + v); }
}
export async function onRequest({ request, next }) {
  const res = await next();
  const ct = res.headers.get('content-type') || '';
  if (!ct.includes('text/html')) return res;
  const origin = new URL(request.url).origin;
  return new HTMLRewriter()
    .on('link[rel="canonical"]', new Abs(origin, 'href'))
    .on('meta[property="og:url"]', new Abs(origin, 'content'))
    .on('meta[property="og:image"]', new Abs(origin, 'content'))
    .transform(res);
}
