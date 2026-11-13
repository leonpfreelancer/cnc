export function onRequest({ request }) {
  const o = new URL(request.url).origin;
  // adresele *.pages.dev nu se indexează, ca să nu concureze cu domeniul principal
  const body = o.endsWith('.pages.dev') ? 'User-agent: *\nDisallow: /\n' : `User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: ${o}/sitemap.xml\n`;
  return new Response(body, { headers: { 'content-type': 'text/plain; charset=utf-8' } });
}
