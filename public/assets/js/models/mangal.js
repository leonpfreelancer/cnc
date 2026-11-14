// Mangal tăiat cu laser — cutie de foc cu decor „ciorchine”, picioare-cadru, raft inferior.
// Model 3D de prezentare, reconstruit după video; dimensiunile reale se fac la comandă.
import { THREE, plate, B, circleHole, rectHole, slotHole, grapeHoles, steelMaterial, applyFinish } from '../viewer.js';

const T = 3;
const L = 600, Wd = 300, HB = 160;     // cutia de foc: lungime, lățime, înălțime
const Z0 = 640;                        // înălțimea fundului cutiei
const NOTCH = 18, NOTCH_W = 14;
const NOTCH_X = Array.from({ length: 10 }, (_, k) => -270 + 60 * k);

function longWall() {
  const s = new THREE.Shape(); s.moveTo(-L / 2, 0); s.lineTo(L / 2, 0); s.lineTo(L / 2, HB);
  [...NOTCH_X].reverse().forEach(x => { s.lineTo(x + NOTCH_W / 2, HB); s.lineTo(x, HB - NOTCH); s.lineTo(x - NOTCH_W / 2, HB); });
  s.lineTo(-L / 2, HB); s.closePath();
  [-170, 0, 170].forEach(cx => {
    grapeHoles(cx, 120, 7, [4, 3, 2, 1]).forEach(h => s.holes.push(h));
    s.holes.push(circleHole(cx, 62, 4));
  });
  for (let x = -270; x <= 270; x += 45) s.holes.push(circleHole(x, 24, 6));
  return s;
}
function shortWall() {
  const w = Wd + 2 * T, s = new THREE.Shape();
  s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(w / 2, HB); s.lineTo(-w / 2, HB); s.closePath();
  s.holes.push(slotHole(0, 118, 84, 20));
  for (let y = -105; y <= 105; y += 42) s.holes.push(circleHole(y, 24, 6));
  return s;
}
function bottomPlate() {
  const s = new THREE.Shape(); const x = L / 2 + T, y = Wd / 2 + T;
  s.moveTo(-x, -y); s.lineTo(x, -y); s.lineTo(x, y); s.lineTo(-x, y); s.closePath();
  for (const yy of [-80, 0, 80]) for (let xx = -260; xx <= 260; xx += 52) s.holes.push(circleHole(xx, yy, 6));
  return s;
}
function legFrame() {
  const w = Wd + 2 * T, s = new THREE.Shape(), h = Z0 - T;
  s.moveTo(-w / 2, 0); s.lineTo(-113, 0);
  for (let i = 1; i < 28; i++) { const a = Math.PI * i / 28; s.lineTo(-113 * Math.cos(a), 120 * Math.sin(a)); }
  s.lineTo(113, 0); s.lineTo(w / 2, 0); s.lineTo(w / 2, h); s.lineTo(-w / 2, h); s.closePath();
  s.holes.push(rectHole(-113, 232, 113, h - 40, 10));
  return s;
}
function shelf() {
  const s = new THREE.Shape(), x = 250, y = Wd / 2 + T;
  s.moveTo(-x, -y); s.lineTo(x, -y); s.lineTo(x, y); s.lineTo(-x, y); s.closePath();
  [-165, -55, 55, 165].forEach(cx => s.holes.push(rectHole(cx - 40, -100, cx + 40, 100, 10)));
  return s;
}
function skewer(x) {
  const g = new THREE.Group();
  const steel = new THREE.MeshStandardMaterial({ color: 0xc9ccd0, metalness: 1, roughness: 0.25 });
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(2.5, 2.5, 400, 10), steel); g.add(rod);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(13, 2.2, 8, 24), steel); ring.position.y = -214; ring.rotation.y = Math.PI / 2; g.add(ring);
  const meat = new THREE.MeshStandardMaterial({ color: 0x7a3b1c, roughness: 0.85, emissive: 0x2a0800, emissiveIntensity: 0.6 });
  for (let k = 0; k < 6; k++) {
    const m = new THREE.Mesh(new THREE.DodecahedronGeometry(17 + (k % 2) * 3, 0), meat);
    m.position.y = -105 + k * 42; m.rotation.set(k, k * 1.7, k * 0.6); m.scale.set(1, 0.85, 1.05); g.add(m);
  }
  g.children.forEach(c => { c.castShadow = true; });
  g.position.set(x, -5, Z0 + HB - NOTCH + 2.5);
  return g;
}

export async function build() {
  const steel = steelMaterial('negru');
  const o = [];
  o.push(plate(longWall(), T, B.XZ, [0, -Wd / 2, Z0], steel, [0, -190, 140], { name: 'Perete lung față' }));
  o.push(plate(longWall(), T, B.XZ, [0, Wd / 2 + T, Z0], steel, [0, 190, 140], { name: 'Perete lung spate' }));
  o.push(plate(shortWall(), T, B.YZ, [L / 2, 0, Z0], steel, [190, 0, 140], { name: 'Perete scurt dreapta' }));
  o.push(plate(shortWall(), T, B.YZ, [-L / 2 - T, 0, Z0], steel, [-190, 0, 140], { name: 'Perete scurt stânga' }));
  o.push(plate(bottomPlate(), T, B.XY, [0, 0, Z0 - T], steel, [0, 0, 70], { name: 'Fund cu orificii' }));
  o.push(plate(legFrame(), T, B.YZ, [250, 0, 0], steel, [170, 0, 0], { name: 'Cadru picior' }));
  o.push(plate(legFrame(), T, B.YZ, [-250 - T, 0, 0], steel, [-170, 0, 0], { name: 'Cadru picior' }));
  o.push(plate(shelf(), T, B.XY, [0, 0, 200], steel, [0, 0, -40], { name: 'Raft inferior' }));

  // jar + frigărui
  const fire = new THREE.Group(); fire.userData.noFit = true;
  const coals = new THREE.Mesh(new THREE.BoxGeometry(L - 20, Wd - 20, 14),
    new THREE.MeshStandardMaterial({ color: 0x1a0d08, emissive: 0xff5a14, emissiveIntensity: 1.6, roughness: 1 }));
  coals.position.set(0, 0, Z0 + 7); fire.add(coals);
  const glow = new THREE.PointLight(0xff6a1a, 2.2, 1400, 1.4); glow.position.set(0, 0, Z0 + 60); fire.add(glow);
  const skewers = new THREE.Group(); [-150, -90, -30, 30, 90, 150].forEach(x => skewers.add(skewer(x))); fire.add(skewers);
  o.push(fire);
  let fireOn = true;

  return {
    objects: o,
    view: { az: -62, el: 16, dist: 2.9 },
    animate: t => { if (!fire.visible) return; const f = 1.45 + 0.25 * Math.sin(t * 7.3) + 0.15 * Math.sin(t * 13.1 + 1); coals.material.emissiveIntensity = f; glow.intensity = 1.6 * f; },
    onExplode: t => { fire.visible = fireOn && t < 0.02; },
    controls: [
      { type: 'finish', label: 'Vopsea termorezistentă', value: 'negru', options: ['negru', 'antracit', 'brut'], set: v => applyFinish(steel, v) },
      { type: 'toggle', label: 'Jar și frigărui', value: true, set: v => { fireOn = v; fire.visible = v; } },
    ],
  };
}
