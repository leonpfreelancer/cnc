// BRAD 01 — brad de Crăciun din placaj de mesteacăn 12 mm: 2 piese în cruce + stea, nume gravat.
// Geometria vine din fișierele reale de frezare CNC (brad-data.json, aceleași contururi ca în DXF).
// Desfacerea arată ordinea reală de montaj: piesa B stă jos, piesa A (cu vârf) vine de sus, apoi steaua.
import { THREE, woodMaterials } from '../viewer.js';

const ZONE = { x: 87.5, z: 127.5, w: 105, h: 75 };   // zona sigură a gravurii pe aripa dreaptă a piesei A (mm)

function engravingTexture(name, year) {
  const c = document.createElement('canvas'); c.width = 1050; c.height = 750; const g = c.getContext('2d');
  g.fillStyle = '#4a2a10'; g.textAlign = 'center'; g.textBaseline = 'middle';
  const fit = (t, size, maxW) => { do { g.font = `800 ${size}px "Bricolage Grotesque", Arial, sans-serif`; size -= 4; } while (g.measureText(t).width > maxW && size > 30); };
  const n = (name || '').toUpperCase().trim().slice(0, 14);
  if ('letterSpacing' in g) g.letterSpacing = '6px';
  fit('FAMILIA', 120, 900); g.fillText('FAMILIA', 525, 140);
  fit(n, 230, 1000); g.fillText(n, 525, 375);
  fit(year, 120, 900); g.fillText(year, 525, 615);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8; return tex;
}

function glowTexture() {
  const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, 'rgba(255,236,190,1)'); gr.addColorStop(0.18, 'rgba(255,200,110,.85)');
  gr.addColorStop(0.5, 'rgba(255,150,50,.22)'); gr.addColorStop(1, 'rgba(255,120,30,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c);
}

// puncte la distanță egală pe contur (pentru ghirlandă)
function sampleEdge(pts, step, minZ) {
  const out = []; let acc = 0;
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i], b = pts[(i + 1) % pts.length]; const L = Math.hypot(b[0] - a[0], b[1] - a[1]);
    let d = step - acc;
    while (d <= L) { const u = d / L; const x = a[0] + (b[0] - a[0]) * u, z = a[1] + (b[1] - a[1]) * u; if (z > minZ && Math.abs(x) > 8) out.push([x, z]); d += step; }
    acc = (acc + L) % step;
  }
  return out;
}

export async function build() {
  const D = await (await fetch(new URL('./brad-data.json' + new URL(import.meta.url).search, import.meta.url))).json();
  const mats = woodMaterials();
  const objs = [];
  const shapeFrom = p => { const s = new THREE.Shape(); s.moveTo(p[0][0], p[0][1]); for (let i = 1; i < p.length; i++) s.lineTo(p[i][0], p[i][1]); s.closePath(); return s; };
  const byCode = {};
  D.parts.forEach(p => {
    const sh = shapeFrom(p.outer);
    p.holes.forEach(h => sh.holes.push(new THREE.Path(h.map(q => new THREE.Vector2(q[0], q[1])))));
    const geo = new THREE.ExtrudeGeometry(sh, { depth: D.T, bevelEnabled: false, curveSegments: 1 });
    const m = new THREE.Mesh(geo, mats); m.castShadow = m.receiveShadow = true; m.name = p.name;
    const f = p.frame;
    const M = new THREE.Matrix4().makeBasis(new THREE.Vector3(...f.x), new THREE.Vector3(...f.y), new THREE.Vector3(...f.z));
    M.setPosition(f.o[0], f.o[1], f.o[2]);
    m.matrixAutoUpdate = false; m.matrix.copy(M); m.userData.base = M.clone(); m.userData.ex = new THREE.Vector3(...p.explode);
    objs.push(m); byCode[p.code] = p;
  });

  // gravura: pe fața din față a piesei A, aripa dreaptă; urmează piesa A la desfacere
  let name = 'ROTARU'; const year = String(new Date().getFullYear());
  const engr = new THREE.Mesh(new THREE.PlaneGeometry(ZONE.w, ZONE.h),
    new THREE.MeshStandardMaterial({ transparent: true, opacity: 0.88, roughness: 0.95, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 }));
  engr.rotation.x = Math.PI / 2; engr.position.set(ZONE.x, -6.2, ZONE.z);
  const engrHolder = new THREE.Group(); engrHolder.add(engr);
  engrHolder.matrixAutoUpdate = false; engrHolder.userData.base = new THREE.Matrix4(); engrHolder.userData.ex = new THREE.Vector3(...byCode['BRAD-A'].explode);
  const setEngr = () => { engr.material.map?.dispose(); engr.material.map = engravingTexture(name, year); engr.material.needsUpdate = true; engr.visible = !!name.trim(); };
  setEngr();
  objs.push(engrHolder);

  // ghirlandă LED pe conturul pieselor A și B (opțional, nu face parte din brad)
  const lights = new THREE.Group(); lights.userData.noFit = true; lights.visible = false;
  const gtex = glowTexture(); const bulbs = [];
  const R = (() => { let s = 3; return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; })();
  [['BRAD-A', (x, z) => new THREE.Vector3(x, 0, z)], ['BRAD-B', (x, z) => new THREE.Vector3(0, x, z)]].forEach(([code, map]) => {
    sampleEdge(byCode[code].outer, 34, 45).forEach(([x, z]) => {
      const pos = map(x + Math.sign(x) * 3, z + 3);
      const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: gtex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
      s.scale.set(40, 40, 1); s.position.copy(pos);
      const b = new THREE.Mesh(new THREE.SphereGeometry(3.4, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffe1a0 })); b.position.copy(pos);
      lights.add(s); lights.add(b); bulbs.push({ s, ph: R() * 6.28 });
    });
  });
  objs.push(lights);
  let lightsOn = false, exploded = false;

  return {
    objects: objs,
    view: { az: -68, el: 14, dist: 2.8, liftZ: 310, zoomOut: 0.72 },
    onExplode: t => { exploded = t > 0.02; lights.visible = lightsOn && !exploded; },
    animate: t => { if (lights.visible) bulbs.forEach(o => { o.s.material.opacity = 0.75 + 0.25 * Math.sin(t * 3.1 + o.ph); }); },
    controls: [
      { type: 'text', label: 'Numele familiei', value: name, max: 14, placeholder: 'ex. ROTARU', set: v => { name = v; setEngr(); } },
      { type: 'toggle', label: 'Cu ghirlandă LED', value: false, set: v => { lightsOn = v; lights.visible = v && !exploded; } },
    ],
  };
}
