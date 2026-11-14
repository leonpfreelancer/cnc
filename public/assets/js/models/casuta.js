// CĂSUȚA 01 — căsuță-felinar din placaj de mesteacăn 6 mm: 7 piese tăiate pe CNC, nume gravat pe acoperiș,
// lumânare LED înăuntru. Model 3D de prezentare; dimensiunile sunt constantele de mai jos (mm).
import { THREE, plate, B, circleHole, rectHole, polyShape, polyPath, woodMaterials } from '../viewer.js';

const T = 6;              // grosime placaj
const W = 190, D = 130;   // amprenta pereților (X lățime, Y adâncime)
const HW = 125;           // înălțimea pereților până la streașină
const HALF = D / 2;       // acoperiș la 45°: coama e la HW + HALF
const C = Math.SQRT1_2;
const SLOPE = HALF * Math.SQRT2;   // lungimea pantei până la coamă
const OH = 14;            // streașina iese în afară

// fereastră cu 4 ochiuri (cruce de 4 mm) centrată în (cx, cy)
function windowPanes(cx, cy, w, h, bar = 4) {
  const hw = w / 2, hh = h / 2, b = bar / 2;
  return [[cx - hw, cy - hh, cx - b, cy - b], [cx + b, cy - hh, cx + hw, cy - b],
          [cx - hw, cy + b, cx - b, cy + hh], [cx + b, cy + b, cx + hw, cy + hh]].map(r => rectHole(...r, 1.5));
}
function doorHole(cx, y0, w, h) {
  const p = new THREE.Path(), r = w / 2;
  p.moveTo(cx - r, y0); p.lineTo(cx + r, y0); p.lineTo(cx + r, y0 + h - r);
  p.absarc(cx, y0 + h - r, r, 0, Math.PI, false); p.lineTo(cx - r, y0); return p;
}
function starPath(cx, cy, R, r) {
  const pts = []; for (let i = 0; i < 10; i++) { const a = Math.PI / 2 + i * Math.PI / 5, q = i % 2 ? r : R; pts.push([cx + q * Math.cos(a), cy + q * Math.sin(a)]); }
  return polyPath(pts);
}
function heartPath(cx, cy, s) {
  const p = new THREE.Path();
  p.moveTo(cx, cy - s); p.bezierCurveTo(cx + s * 1.3, cy - s * 0.1, cx + s * 0.9, cy + s * 0.95, cx, cy + s * 0.45);
  p.bezierCurveTo(cx - s * 0.9, cy + s * 0.95, cx - s * 1.3, cy - s * 0.1, cx, cy - s); return p;
}

function frontWall(back) {
  const s = polyShape([[-W / 2, 0], [W / 2, 0], [W / 2, HW], [-W / 2, HW]]);
  if (!back) s.holes.push(doorHole(0, 10, 36, 62));
  else s.holes.push(heartPath(0, 52, 15));
  [-54, 54].forEach(x => windowPanes(x, 78, 34, 40).forEach(h => s.holes.push(h)));
  return s;
}
function gable(star) {
  const s = polyShape([[T, 0], [D - T, 0], [D - T, HW + T], [HALF, HW + HALF], [T, HW + T]]);
  windowPanes(HALF, 70, 34, 44).forEach(h => s.holes.push(h));
  s.holes.push(star ? starPath(HALF, HW + 24, 14, 6) : circleHole(HALF, HW + 22, 11));
  return s;
}
function roofShape(front) {
  return polyShape([[-W / 2 - OH, -OH], [W / 2 + OH, -OH], [W / 2 + OH, SLOPE + (front ? T : 0)], [-W / 2 - OH, SLOPE + (front ? T : 0)]]);
}
function baseShape() {
  const s = polyShape([[-W / 2 - 10, -12], [W / 2 + 10, -12], [W / 2 + 10, D + 12], [-W / 2 - 10, D + 12]]);
  s.holes.push(circleHole(0, HALF, 21));   // gaura pentru lumânarea LED (se schimbă bateria de dedesubt)
  return s;
}

function engravingTexture(name) {
  const c = document.createElement('canvas'); c.width = 1200; c.height = 440; const g = c.getContext('2d');
  g.fillStyle = '#4a2a10'; g.textAlign = 'center'; g.textBaseline = 'middle';
  const fit = (t, size, maxW) => { do { g.font = `800 ${size}px Archivo, Arial, sans-serif`; size -= 4; } while (g.measureText(t).width > maxW && size > 30); };
  if ('letterSpacing' in g) g.letterSpacing = '8px';
  fit('FAMILIA', 92, 1000); g.fillText('FAMILIA', 600, 100);
  const n = (name || '').toUpperCase().trim().slice(0, 14);
  fit(n, 210, 1120); g.fillText(n, 600, 285);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8; return tex;
}
function flameTexture() {
  const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, 'rgba(255,240,200,1)'); gr.addColorStop(0.25, 'rgba(255,190,90,.8)'); gr.addColorStop(1, 'rgba(255,120,30,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c);
}

export async function build() {
  const mats = woodMaterials();
  const objs = [];
  const z0 = T;   // pereții stau pe bază
  objs.push(plate(baseShape(), T, B.XY, [0, 0, 0], mats, [0, 0, -70], { name: 'Bază' }));
  objs.push(plate(frontWall(false), T, B.XZ, [0, T, z0], mats, [0, -140, 0], { name: 'Perete față' }));
  objs.push(plate(frontWall(true), T, B.XZ, [0, D, z0], mats, [0, 140, 0], { name: 'Perete spate' }));
  objs.push(plate(gable(false), T, B.YZ, [-W / 2, 0, z0], mats, [-140, 0, 0], { name: 'Fronton stânga' }));
  objs.push(plate(gable(true), T, B.YZ, [W / 2 - T, 0, z0], mats, [140, 0, 0], { name: 'Fronton dreapta' }));
  const RF = [[1, 0, 0], [0, C, C], [0, -C, C]], RB = [[-1, 0, 0], [0, -C, C], [0, C, C]];
  const exF = [0, -110, 170], exB = [0, 110, 170];
  objs.push(plate(roofShape(true), T, RF, [0, 0, z0 + HW], mats, exF, { name: 'Acoperiș față' }));
  objs.push(plate(roofShape(false), T, RB, [0, D, z0 + HW], mats, exB, { name: 'Acoperiș spate' }));

  // gravura pe acoperișul din față: urmează panoul la desfacere
  let name = 'ROTARU';
  const engr = new THREE.Mesh(new THREE.PlaneGeometry(180, 66),
    new THREE.MeshStandardMaterial({ transparent: true, opacity: 0.9, roughness: 0.95, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 }));
  engr.position.set(0, SLOPE * 0.47, T + 0.3);
  const engrHolder = new THREE.Group(); engrHolder.add(engr);
  const M = new THREE.Matrix4().makeBasis(...RF.map(v => new THREE.Vector3(...v))); M.setPosition(0, 0, z0 + HW);
  engrHolder.matrixAutoUpdate = false; engrHolder.matrix.copy(M); engrHolder.userData.base = M.clone(); engrHolder.userData.ex = new THREE.Vector3(...exF);
  const setEngr = () => { engr.material.map?.dispose(); engr.material.map = engravingTexture(name); engr.material.needsUpdate = true; engr.visible = !!name.trim(); };
  setEngr();
  objs.push(engrHolder);

  // lumina dinăuntru: lumânare LED + interior cald văzut prin ferestre + lumină care iese pe masă
  const glow = new THREE.Group(); glow.userData.noFit = true;
  const inner = new THREE.Mesh(new THREE.BoxGeometry(W - 2 * T - 2, D - 2 * T - 2, HW - 2),
    new THREE.MeshBasicMaterial({ color: 0xffa64d, side: THREE.BackSide }));
  inner.position.set(0, HALF, z0 + HW / 2); glow.add(inner);
  const candle = new THREE.Mesh(new THREE.CylinderGeometry(19, 19, 36, 32), new THREE.MeshStandardMaterial({ color: 0xf3ead8, roughness: 0.6, emissive: 0x553311 }));
  candle.rotation.x = Math.PI / 2; candle.position.set(0, HALF, z0 + 18); glow.add(candle);
  const flame = new THREE.Sprite(new THREE.SpriteMaterial({ map: flameTexture(), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
  flame.scale.set(34, 46, 1); flame.position.set(0, HALF, z0 + 46); glow.add(flame);
  const lamp = new THREE.PointLight(0xffa24a, 1, 0, 1.25);
  lamp.position.set(0, HALF, z0 + 60); lamp.castShadow = true; lamp.shadow.mapSize.set(1024, 1024); lamp.shadow.bias = -0.002; lamp.shadow.camera.near = 4;
  glow.add(lamp);
  objs.push(glow);

  let lightOn = true, exploded = false, power = 1;
  const upd = () => { glow.visible = lightOn && !exploded; };
  const setPower = p => { power = p; lamp.intensity = 2600 * p; inner.material.color.setHex(0xffa64d).multiplyScalar(0.04 + 0.96 * p); };
  setPower(1);

  return {
    objects: objs,
    view: { az: -62, el: 16, dist: 2.95, liftZ: 120, zoomOut: 0.6 },
    onExplode: t => { exploded = t > 0.02; upd(); },
    animate: t => { if (glow.visible) { const f = 0.9 + 0.06 * Math.sin(t * 9.1) + 0.04 * Math.sin(t * 23.7); lamp.intensity = 2600 * power * f; flame.material.opacity = f; } },
    setName: v => { name = v; setEngr(); },   // folosit de scriptul video
    setPower,
    controls: [
      { type: 'text', label: 'Numele familiei', value: name, max: 14, placeholder: 'ex. ROTARU', set: v => { name = v; setEngr(); } },
      { type: 'toggle', label: 'Lumânare LED aprinsă', value: true, set: v => { lightOn = v; upd(); } },
    ],
  };
}

// contururile plane ale celor 7 piese (pentru planul de tăiere / video)
export function flatParts() {
  return [['Bază', baseShape()], ['Perete față', frontWall(false)], ['Perete spate', frontWall(true)],
          ['Fronton stânga', gable(false)], ['Fronton dreapta', gable(true)], ['Acoperiș față', roofShape(true)], ['Acoperiș spate', roofShape(false)]];
}
