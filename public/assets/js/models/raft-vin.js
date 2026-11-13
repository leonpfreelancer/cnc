// Raft pentru vin — 4 piese din oțel tăiat cu laser, 6 sticle, nume gravat pe capac.
// Model 3D de prezentare, reconstruit după video; dimensiunile reale se stabilesc la comandă.
import { THREE, plate, B, circleHole, slotHole, grapeHoles, steelMaterial, applyFinish } from '../viewer.js';

const T = 2;            // grosime tablă (mm), doar pentru vizualizare
const W = 300, H = 360, D = 200;
const COLS = [-65, 65], ROWS = [80, 180, 280];
let showBottles = true;

function panelShape(holeR, decorTop) {
  const s = new THREE.Shape();
  s.moveTo(-W / 2, 0); s.lineTo(-115, 0);
  for (let i = 1; i < 24; i++) s.lineTo(-115 + 230 * i / 24, 28 * Math.sin(Math.PI * i / 24));
  s.lineTo(115, 0); s.lineTo(W / 2, 0); s.lineTo(W / 2, H); s.lineTo(-W / 2, H); s.closePath();
  COLS.forEach(x => ROWS.forEach(z => s.holes.push(circleHole(x, z, holeR))));
  grapeHoles(0, decorTop, holeR > 20 ? 5 : 6, [3, 2, 1]).forEach(h => s.holes.push(h));
  if (holeR < 20) { // punctele decorative de pe fața din față
    [[-118, 240], [-112, 132], [118, 226], [112, 120], [0, 120], [0, 235]].forEach(([x, z]) => s.holes.push(circleHole(x, z, 4)));
    s.holes.push(circleHole(0, 178, 9));
  }
  return s;
}
function topShape() {
  const s = new THREE.Shape(); const x0 = -170, x1 = 170, y0 = -20, y1 = 222, r = 12;
  s.moveTo(x0 + r, y0); s.lineTo(x1 - r, y0); s.absarc(x1 - r, y0 + r, r, -Math.PI / 2, 0); s.lineTo(x1, y1 - r);
  s.absarc(x1 - r, y1 - r, r, 0, Math.PI / 2); s.lineTo(x0 + r, y1); s.absarc(x0 + r, y1 - r, r, Math.PI / 2, Math.PI);
  s.lineTo(x0, y0 + r); s.absarc(x0 + r, y0 + r, r, Math.PI, Math.PI * 1.5);
  s.holes.push(circleHole(-148, 2, 4)); s.holes.push(circleHole(148, 200, 4));
  return s;
}
function bottomShape() {
  const s = new THREE.Shape(); s.moveTo(-W / 2, 0); s.lineTo(W / 2, 0); s.lineTo(W / 2, D); s.lineTo(-W / 2, D); s.closePath();
  s.holes.push(slotHole(0, D / 2, 170, 46)); return s;
}
function bottle() {
  const pts = [[0, 0], [36, 0], [37, 4], [37, 198], [33, 222], [22, 240], [14.5, 252], [14.5, 300], [15.5, 302], [15.5, 307], [0, 307]]
    .map(([r, l]) => new THREE.Vector2(r, l));
  const g = new THREE.Group();
  const glass = new THREE.Mesh(new THREE.LatheGeometry(pts, 40), new THREE.MeshPhysicalMaterial({ color: 0x163222, roughness: 0.12, metalness: 0.1, clearcoat: 1 }));
  const label = new THREE.Mesh(new THREE.CylinderGeometry(37.4, 37.4, 90, 40, 1, true), new THREE.MeshStandardMaterial({ color: 0xebe2cd, roughness: 0.8, side: THREE.DoubleSide }));
  label.position.y = 105;
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(15.8, 15.8, 52, 32), new THREE.MeshStandardMaterial({ color: 0x8e1427, roughness: 0.35, metalness: 0.5 }));
  cap.position.y = 281;
  [glass, label, cap].forEach(m => { m.castShadow = true; g.add(m); });
  return g;
}
function engravingTexture(text, color) {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 320; const g = c.getContext('2d');
  g.clearRect(0, 0, c.width, c.height); g.fillStyle = color; g.textAlign = 'center'; g.textBaseline = 'middle';
  let size = 170; const t = (text || '').toUpperCase().slice(0, 18);
  do { g.font = `800 ${size}px Archivo, Arial, sans-serif`; size -= 6; } while (g.measureText(t).width > 940 && size > 40);
  if ('letterSpacing' in g) g.letterSpacing = '12px';
  g.fillText(t, 512, 168);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8; return tex;
}

export async function build() {
  const steel = steelMaterial('negru');
  const objs = [];
  objs.push(plate(panelShape(16, 330), T, B.XZ, [0, 0, 0], steel, [0, -130, 0], { name: 'Panou față' }));
  objs.push(plate(panelShape(42, 345), T, B.XZ, [0, D + T, 0], steel, [0, 130, 0], { name: 'Panou spate' }));
  objs.push(plate(topShape(), T, B.XY, [0, 0, H], steel, [0, 0, 170], { name: 'Capac' }));
  objs.push(plate(bottomShape(), T, B.XY, [0, 0, 40], steel, [0, 0, -25], { name: 'Bază' }));

  // gravura pe capac
  let name = 'ANDREI', finish = 'negru';
  const engr = new THREE.Mesh(new THREE.PlaneGeometry(250, 78), new THREE.MeshStandardMaterial({ transparent: true, roughness: 0.35, metalness: 0.9, depthWrite: false }));
  const engrHolder = new THREE.Group(); engrHolder.add(engr);
  engr.position.set(0, 101, H + T + 0.15);
  const setEngr = () => { engr.material.map?.dispose(); engr.material.map = engravingTexture(name, finish === 'brut' ? '#4a4d52' : '#d7dade'); engr.material.needsUpdate = true; engr.visible = !!name.trim(); };
  setEngr();
  // capacul se mișcă la explodare: gravura îl urmează
  engrHolder.matrixAutoUpdate = false; engrHolder.userData.base = new THREE.Matrix4(); engrHolder.userData.ex = new THREE.Vector3(0, 0, 170);
  objs.push(engrHolder);

  const bottles = new THREE.Group(); bottles.userData.noFit = true;
  COLS.forEach(x => ROWS.forEach(z => { const b = bottle(); b.rotation.z = Math.PI; b.position.set(x, 262, z); bottles.add(b); }));
  objs.push(bottles);

  return {
    objects: objs,
    view: { az: -58, el: 18, dist: 2.7 },
    onExplode: t => { bottles.visible = t < 0.02 && showBottles; },
    controls: [
      { type: 'finish', label: 'Finisaj', value: finish, options: ['negru', 'antracit', 'bronz', 'brut'],
        set: v => { finish = v; applyFinish(steel, v); setEngr(); } },
      { type: 'text', label: 'Nume gravat pe capac', value: name, max: 18, placeholder: 'ex. ANDREI',
        set: v => { name = v; setEngr(); } },
      { type: 'toggle', label: 'Cu sticle', value: true, set: v => { showBottles = v; bottles.visible = v; } },
    ],
  };
}
