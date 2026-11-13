// Vizualizator 3D comun pentru toate produsele (three.js r160).
// Unități: milimetri. Axa Z este „sus”; Y merge din față spre spate.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

export { THREE };

/* ---------- forme 2D ---------- */
export function roundedRect(shapeOrPath, x0, y0, x1, y1, r) {
  const s = shapeOrPath;
  r = Math.min(r, (x1 - x0) / 2, (y1 - y0) / 2);
  s.moveTo(x0 + r, y0);
  s.lineTo(x1 - r, y0); if (r) s.absarc(x1 - r, y0 + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x1, y1 - r); if (r) s.absarc(x1 - r, y1 - r, r, 0, Math.PI / 2, false);
  s.lineTo(x0 + r, y1); if (r) s.absarc(x0 + r, y1 - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x0, y0 + r); if (r) s.absarc(x0 + r, y0 + r, r, Math.PI, Math.PI * 1.5, false);
  return s;
}
export function circleHole(x, y, r) {
  const p = new THREE.Path(); p.absarc(x, y, r, 0, Math.PI * 2, true); return p;
}
export function rectHole(x0, y0, x1, y1, r = 0) {
  return roundedRect(new THREE.Path(), x0, y0, x1, y1, r);
}
export function slotHole(cx, cy, len, w) { // fantă orizontală cu capete rotunde
  const p = new THREE.Path(), r = w / 2, a = cx - len / 2 + r, b = cx + len / 2 - r;
  p.moveTo(a, cy - r); p.lineTo(b, cy - r); p.absarc(b, cy, r, -Math.PI / 2, Math.PI / 2, false);
  p.lineTo(a, cy + r); p.absarc(a, cy, r, Math.PI / 2, Math.PI * 1.5, false); return p;
}
export function polyShape(pts) {
  const s = new THREE.Shape(); s.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) s.lineTo(pts[i][0], pts[i][1]);
  s.closePath(); return s;
}
export function polyPath(pts) {
  const p = new THREE.Path(); p.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) p.lineTo(pts[i][0], pts[i][1]);
  p.closePath(); return p;
}
// Ciorchine de struguri (motivul din video-uri): rânduri de cercuri descrescătoare + frunză
export function grapeHoles(cx, topY, r, rows = [4, 3, 2, 1], gap = 1.15) {
  const out = []; const dx = r * 2 * gap, dy = r * 1.8 * gap;
  rows.forEach((n, i) => {
    for (let k = 0; k < n; k++) out.push(circleHole(cx + (k - (n - 1) / 2) * dx, topY - i * dy, r));
  });
  return out;
}

/* ---------- materiale ---------- */
function rnd(seed) { let s = seed; return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; }
export function woodMaterials() {
  const R = rnd(11);
  const c = document.createElement('canvas'); c.width = c.height = 1024; const g = c.getContext('2d');
  g.fillStyle = '#e4cda4'; g.fillRect(0, 0, 1024, 1024);
  for (let i = 0; i < 520; i++) {
    const y = R() * 1024; g.strokeStyle = `rgba(150,105,55,${0.03 + R() * 0.07})`; g.lineWidth = 0.6 + R() * 2.2;
    g.beginPath(); g.moveTo(0, y); for (let x = 0; x <= 1024; x += 32) g.lineTo(x, y + Math.sin(x / 120 + y) * 4 + R() * 1.5); g.stroke();
  }
  const face = new THREE.CanvasTexture(c); face.wrapS = face.wrapT = THREE.RepeatWrapping; face.repeat.set(1 / 300, 1 / 300);
  face.colorSpace = THREE.SRGBColorSpace; face.anisotropy = 8;
  const e = document.createElement('canvas'); e.width = 64; e.height = 256; const h = e.getContext('2d');
  for (let i = 0; i < 9; i++) { h.fillStyle = i % 2 ? '#dcbd88' : '#c29c62'; h.fillRect(0, i * 256 / 9, 64, 256 / 9); h.fillStyle = 'rgba(80,52,20,.4)'; h.fillRect(0, i * 256 / 9, 64, 1.5); }
  const edge = new THREE.CanvasTexture(e); edge.wrapS = edge.wrapT = THREE.RepeatWrapping; edge.repeat.set(1 / 40, 1 / 12); edge.colorSpace = THREE.SRGBColorSpace;
  return [new THREE.MeshStandardMaterial({ map: face, roughness: 0.62 }), new THREE.MeshStandardMaterial({ map: edge, roughness: 0.75 })];
}
export const FINISHES = {
  negru: { label: 'Negru mat', color: 0x1d1e20, metalness: 0.35, roughness: 0.62 },
  antracit: { label: 'Antracit', color: 0x3a3d42, metalness: 0.45, roughness: 0.5 },
  bronz: { label: 'Bronz antic', color: 0x5a4632, metalness: 0.6, roughness: 0.45 },
  brut: { label: 'Oțel brut', color: 0x8d9298, metalness: 0.9, roughness: 0.42 },
};
export function steelMaterial(key = 'negru') {
  const f = FINISHES[key];
  return new THREE.MeshStandardMaterial({ color: f.color, metalness: f.metalness, roughness: f.roughness });
}
export function applyFinish(mat, key) {
  const f = FINISHES[key]; mat.color.setHex(f.color); mat.metalness = f.metalness; mat.roughness = f.roughness; mat.needsUpdate = true;
}

/* ---------- piese ---------- */
// Extrudă o formă 2D cu grosimea t și o așază cu baza (x, y, z) și originea o.
export function plate(shape, t, basis, o, mats, explode = [0, 0, 0], opts = {}) {
  const geo = new THREE.ExtrudeGeometry(shape, { depth: t, bevelEnabled: false, curveSegments: opts.seg || 24 });
  const mesh = new THREE.Mesh(geo, mats);
  mesh.castShadow = true; mesh.receiveShadow = true;
  const M = new THREE.Matrix4().makeBasis(new THREE.Vector3(...basis[0]), new THREE.Vector3(...basis[1]), new THREE.Vector3(...basis[2]));
  M.setPosition(o[0], o[1], o[2]);
  mesh.matrixAutoUpdate = false; mesh.matrix.copy(M);
  mesh.userData.base = M.clone(); mesh.userData.ex = new THREE.Vector3(...explode);
  if (opts.name) mesh.name = opts.name;
  return mesh;
}
export const B = { // baze uzuale
  XY: [[1, 0, 0], [0, 1, 0], [0, 0, 1]],   // placă orizontală, extrudată în sus
  XZ: [[1, 0, 0], [0, 0, 1], [0, -1, 0]],  // placă verticală în planul XZ, extrudată spre -Y (față)
  YZ: [[0, 1, 0], [0, 0, 1], [1, 0, 0]],   // placă verticală în planul YZ, extrudată spre +X
};

/* ---------- vizualizatorul ---------- */
export function createViewer(container, opt = {}) {
  const canvas = document.createElement('canvas'); container.prepend(canvas);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: !!opt.preserve });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = opt.exposure ?? 1.0;
  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;
  scene.environmentIntensity = opt.envIntensity ?? 0.55;

  const cam = new THREE.PerspectiveCamera(30, 1, 10, 20000); cam.up.set(0, 0, 1);
  const controls = new OrbitControls(cam, canvas);
  controls.enableDamping = true; controls.dampingFactor = 0.08; controls.enablePan = false;
  controls.autoRotate = opt.autoRotate ?? true; controls.autoRotateSpeed = 0.8;

  scene.add(new THREE.HemisphereLight(0xfff6ea, 0x202022, 0.55));
  const key = new THREE.DirectionalLight(0xfff1dc, 1.6); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); key.shadow.bias = -0.0003; key.shadow.radius = 4; scene.add(key); scene.add(key.target);
  const rim = new THREE.DirectionalLight(0xffb27a, 0.5); scene.add(rim);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.ShadowMaterial({ opacity: 0.38 }));
  ground.receiveShadow = true; scene.add(ground);

  const root = new THREE.Group(); scene.add(root);
  let parts = [], explode = 0, size = 500, center = new THREE.Vector3(), anims = [], current = null, camT = 0;

  function setModel(model) {
    root.clear(); parts = []; current = model;
    model.objects.forEach(o => { root.add(o); if (o.userData.base) parts.push(o); });
    const box = new THREE.Box3();
    model.objects.forEach(o => { o.updateMatrixWorld(true); if (!o.userData.noFit) box.expandByObject(o); });
    box.getCenter(center); const s = box.getSize(new THREE.Vector3()); size = Math.max(s.x, s.y, s.z);
    ground.scale.set(size * 8, size * 8, 1); ground.position.set(center.x, center.y, box.min.z - 0.5);
    key.position.set(center.x - size * 0.9, center.y - size * 1.2, center.z + size * 2.2); key.target.position.copy(center);
    const sc = key.shadow.camera; sc.left = sc.bottom = -size * 1.4; sc.right = sc.top = size * 1.4; sc.near = 10; sc.far = size * 6; sc.updateProjectionMatrix();
    rim.position.set(center.x + size, center.y + size * 1.5, center.z + size * 0.6);
    controls.target.copy(center); camT = 0;
    const v = model.view || { az: -55, el: 22, dist: 2.6 };
    setView(v.az, v.el, v.dist);
    controls.minDistance = size * 1.1; controls.maxDistance = size * 5;
    anims = model.animate ? [model.animate] : [];
    setExplode(explode);
  }
  function setView(az, el, distK) {
    const a = THREE.MathUtils.degToRad(az), e = THREE.MathUtils.degToRad(el), d = size * distK;
    cam.position.set(center.x + d * Math.cos(e) * Math.cos(a), center.y + d * Math.cos(e) * Math.sin(a), center.z + d * Math.sin(e));
    controls.update();
  }
  function setExplode(t) {
    explode = t;
    parts.forEach(m => {
      m.matrix.copy(m.userData.base); const e = m.userData.ex;
      m.matrix.elements[12] += e.x * t; m.matrix.elements[13] += e.y * t; m.matrix.elements[14] += e.z * t;
      m.matrixWorldNeedsUpdate = true;
    });
    if (current && current.onExplode) current.onExplode(t);
    // modelele care cresc mult în înălțime la desfacere (ex. bradul) cer camerei să urce și să se depărteze
    const v = current && current.view;
    if (v && (v.liftZ || v.zoomOut)) {
      const off = cam.position.clone().sub(controls.target).multiplyScalar((1 + (v.zoomOut || 0) * t) / (1 + (v.zoomOut || 0) * camT));
      controls.target.z += (v.liftZ || 0) * (t - camT); cam.position.copy(controls.target).add(off); camT = t;
      controls.maxDistance = size * 5 * (1 + (v.zoomOut || 0));
    }
  }
  function resize() {
    const w = container.clientWidth, h = container.clientHeight; if (!w || !h) return;
    renderer.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(container); resize();
  // oprește rotirea automată la prima interacțiune
  canvas.addEventListener('pointerdown', () => { controls.autoRotate = false; }, { once: true });
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches; if (reduce) controls.autoRotate = false;

  let visible = true;
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(container);
  const clock = new THREE.Clock();
  renderer.setAnimationLoop(() => {
    if (!visible) return;
    const t = clock.getElapsedTime();
    anims.forEach(f => f(t));
    controls.update(); renderer.render(scene, cam);
  });
  return { scene, renderer, camera: cam, controls, setModel, setExplode, setView, get size() { return size; } };
}
