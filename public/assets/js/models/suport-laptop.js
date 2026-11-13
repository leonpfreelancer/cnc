// WOODSTAND 01 — suport de laptop din placaj de mesteacăn 12 mm, 5 piese, tab-and-slot.
// Geometria vine direct din scriptul parametric Fusion 360 (contururile reale de frezare).
import { THREE, woodMaterials } from '../viewer.js';

export async function build() {
  const D = await (await fetch(new URL('./woodstand-data.json', import.meta.url))).json();
  const mats = woodMaterials();
  const objs = [];
  const shapeFrom = p => { const s = new THREE.Shape(); s.moveTo(p[0][0], p[0][1]); for (let i = 1; i < p.length; i++) s.lineTo(p[i][0], p[i][1]); s.closePath(); return s; };
  D.parts.forEach(p => {
    const sh = shapeFrom(p.outer);
    p.holes.forEach(h => sh.holes.push(new THREE.Path(h.map(q => new THREE.Vector2(q[0], q[1])))));
    const geo = new THREE.ExtrudeGeometry(sh, { depth: D.T, bevelEnabled: false, curveSegments: 1 });
    p.frames.forEach((f, k) => {
      const m = new THREE.Mesh(geo, mats); m.castShadow = m.receiveShadow = true; m.name = p.name;
      const M = new THREE.Matrix4().makeBasis(new THREE.Vector3(...f.x), new THREE.Vector3(...f.y), new THREE.Vector3(...f.z));
      M.setPosition(f.o[0], f.o[1], f.o[2]);
      m.matrixAutoUpdate = false; m.matrix.copy(M); m.userData.base = M.clone(); m.userData.ex = new THREE.Vector3(...p.explode[k]);
      objs.push(m);
    });
  });
  // laptop generic 16" (referință, nu se vinde)
  const Lp = D.laptop, root = new THREE.Group(), lap = new THREE.Group(); root.add(lap); root.userData.noFit = true;
  const alu = new THREE.MeshStandardMaterial({ color: 0x8a8f96, roughness: 0.35, metalness: 0.7 });
  const base = new THREE.Mesh(new THREE.BoxGeometry(Lp.w, Lp.d, Lp.t), alu); base.position.set(Lp.w / 2, Lp.d / 2, Lp.t / 2); base.castShadow = true; lap.add(base);
  const kb = new THREE.Mesh(new THREE.BoxGeometry(Lp.w - 50, Lp.d * 0.42, 0.6), new THREE.MeshStandardMaterial({ color: 0x222428, roughness: 0.6 }));
  kb.position.set(Lp.w / 2, Lp.d * 0.62, Lp.t + 0.3); lap.add(kb);
  const hinge = new THREE.Group(); hinge.position.set(0, Lp.d, Lp.t); hinge.rotation.x = THREE.MathUtils.degToRad(280); lap.add(hinge);
  const lid = new THREE.Mesh(new THREE.BoxGeometry(Lp.w, 236, 6), alu); lid.position.set(Lp.w / 2, -118, 3); lid.castShadow = true; hinge.add(lid);
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(Lp.w - 24, 214), new THREE.MeshStandardMaterial({ color: 0x0c0f13, roughness: 0.2, emissive: 0x0b1a2a, emissiveIntensity: 0.7 }));
  scr.position.set(Lp.w / 2, -118, -0.1); scr.rotation.x = Math.PI; hinge.add(scr);
  const LM = new THREE.Matrix4().makeBasis(new THREE.Vector3(...Lp.x), new THREE.Vector3(...Lp.y), new THREE.Vector3(...Lp.z)); LM.setPosition(...Lp.o);
  root.matrixAutoUpdate = false; root.matrix.copy(LM); root.visible = false;
  objs.push(root);
  let lapOn = false;
  return {
    objects: objs,
    view: { az: -60, el: 24, dist: 3.0 },
    onExplode: t => { root.visible = lapOn && t < 0.02; },
    controls: [
      { type: 'toggle', label: 'Cu laptop 16"', value: false, set: v => { lapOn = v; root.visible = v; } },
    ],
  };
}
