import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";
import { H3 } from "../content";
import { S, hooks } from "../deck";

let sel = 0;
let selAt = 0;
let fallbackActive = false;

export function h3select(i: number): void {
  if (i < 0 || i >= H3.length) return;
  sel = i;
  selAt = performance.now();
  const c = H3[i];
  const title = document.getElementById("h3title");
  const text = document.getElementById("h3text");
  const src = document.getElementById("h3src");
  if (title !== null) title.innerHTML = c.name;
  if (text !== null) text.innerHTML = c.text;
  if (src !== null) src.innerHTML = c.src;
  document.querySelectorAll("#h3chips .chip").forEach((ch, j) => ch.classList.toggle("on", j === i));
  document.querySelectorAll(".h3label").forEach((l, j) => l.classList.toggle("sel", j === i));
}

function glowTexture(): THREE.Texture {
  const c = document.createElement("canvas");
  c.width = 128;
  c.height = 128;
  const g = c.getContext("2d");
  if (g !== null) {
    const grad = g.createRadialGradient(64, 64, 4, 64, 64, 64);
    grad.addColorStop(0, "rgba(255,225,154,1)");
    grad.addColorStop(0.35, "rgba(245,182,56,0.55)");
    grad.addColorStop(1, "rgba(245,182,56,0)");
    g.fillStyle = grad;
    g.fillRect(0, 0, 128, 128);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function stripTags(s: string): string {
  return s.replace(/<[^>]+>/g, "");
}

export function initHarness3D(): void {
  const chips = document.getElementById("h3chips");
  if (chips !== null) {
    chips.innerHTML = "";
    H3.forEach((c, i) => {
      const b = document.createElement("button");
      b.className = "chip" + (i === 0 ? " on" : "");
      b.textContent = i + " " + stripTags(c.name);
      b.setAttribute("aria-label", "Destacar " + stripTags(c.name));
      b.onclick = () => h3select(i);
      chips.appendChild(b);
    });
  }
  (window as unknown as { h3select: (i: number) => void }).h3select = h3select;

  const canvas = document.getElementById("h3d");
  const labelLayer = document.getElementById("h3labels");
  if (!(canvas instanceof HTMLCanvasElement) || labelLayer === null) return;

  let renderer: THREE.WebGLRenderer | null = null;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  } catch {
    renderer = null;
  }
  if (renderer === null) {
    canvas.style.display = "none";
    fallback2d();
    return;
  }
  // Sem GPU no projetor: falha de contexto cai no SVG 2D via h3fallback().
  const gl = renderer.getContext();
  if (gl === null || gl.isContextLost()) {
    canvas.style.display = "none";
    fallback2d();
    return;
  }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(46, 16 / 10, 0.1, 200);
  camera.position.set(7.5, 6.2, 10.5);

  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.minDistance = 8;
  controls.maxDistance = 24;
  controls.maxPolarAngle = Math.PI * 0.62;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.7;
  controls.addEventListener("start", () => {
    controls.autoRotate = false;
  });

  scene.add(new THREE.AmbientLight(0x8b98a8, 0.55));
  const key = new THREE.DirectionalLight(0xfff4dd, 2.2);
  key.position.set(6, 10, 5);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.camera.left = -9;
  key.shadow.camera.right = 9;
  key.shadow.camera.top = 9;
  key.shadow.camera.bottom = -9;
  scene.add(key);
  const rim = new THREE.PointLight(0xf5b638, 120, 60);
  rim.position.set(-7, 3, -5);
  scene.add(rim);
  const fill = new THREE.PointLight(0x3b7bd6, 80, 60);
  fill.position.set(7, -2, 6);
  scene.add(fill);

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: 0.35 }));
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -4.4;
  ground.receiveShadow = true;
  scene.add(ground);

  const glowTex = glowTexture();
  const labelRenderer = new CSS2DRenderer();
  labelRenderer.setSize(1, 1);
  labelRenderer.domElement.style.position = "absolute";
  labelRenderer.domElement.style.inset = "0";
  labelRenderer.domElement.style.pointerEvents = "none";
  labelLayer.appendChild(labelRenderer.domElement);

  // Anel do harness: toro luminoso + trilha de pacotes.
  const ring = new THREE.Mesh(
    new THREE.TorusGeometry(5, 0.07, 16, 128),
    new THREE.MeshStandardMaterial({
      color: 0xf5b638,
      emissive: 0xf5b638,
      emissiveIntensity: 1.6,
      metalness: 0.4,
      roughness: 0.3,
    }),
  );
  ring.rotation.x = Math.PI / 2;
  ring.position.y = 0.6;
  scene.add(ring);
  const ringGlow = new THREE.Sprite(
    new THREE.SpriteMaterial({ map: glowTex, transparent: true, opacity: 0.16, depthWrite: false }),
  );
  ringGlow.scale.set(14, 14, 1);
  ringGlow.position.y = 0.6;
  scene.add(ringGlow);

  interface Body {
    group: THREE.Group;
    halo: THREE.Sprite;
    base: THREE.Vector3;
    label: CSS2DObject;
  }
  const bodies: Body[] = [];
  const proj: { x: number; y: number; r: number }[] = [];
  (window as unknown as { h3proj: { x: number; y: number; r: number }[] }).h3proj = proj;

  const packetGeo = new THREE.SphereGeometry(0.09, 12, 12);
  const packets: { mesh: THREE.Mesh; edge: number; u: number; speed: number }[] = [];

  H3.forEach((c, i) => {
    const group = new THREE.Group();
    group.position.set(c.pos[0], c.pos[1], c.pos[2]);
    let mesh: THREE.Mesh;
    if (c.sphere === true) {
      mesh = new THREE.Mesh(
        new THREE.SphereGeometry(1.15, 48, 32),
        new THREE.MeshPhysicalMaterial({
          color: 0xf5b638,
          metalness: 0.25,
          roughness: 0.22,
          clearcoat: 0.8,
          clearcoatRoughness: 0.25,
          emissive: 0xf5b638,
          emissiveIntensity: 0.55,
        }),
      );
    } else if (i === 1) {
      mesh = new THREE.Mesh(
        new THREE.BoxGeometry(2.3, 1.0, 1.3),
        new THREE.MeshPhysicalMaterial({
          color: 0x3b7bd6,
          metalness: 0.75,
          roughness: 0.3,
          clearcoat: 0.5,
          emissive: 0x3b7bd6,
          emissiveIntensity: 0.25,
        }),
      );
    } else if (i === 2) {
      mesh = new THREE.Mesh(
        new THREE.CylinderGeometry(0.85, 0.85, 1.3, 24),
        new THREE.MeshPhysicalMaterial({
          color: 0x3b7bd6,
          metalness: 0.9,
          roughness: 0.24,
          emissive: 0x3b7bd6,
          emissiveIntensity: 0.25,
        }),
      );
    } else if (i === 3) {
      mesh = new THREE.Mesh(
        new THREE.OctahedronGeometry(1.05),
        new THREE.MeshPhysicalMaterial({
          color: 0x3b7bd6,
          metalness: 0.6,
          roughness: 0.28,
          flatShading: true,
          emissive: 0x3b7bd6,
          emissiveIntensity: 0.25,
        }),
      );
    } else if (i === 4) {
      mesh = new THREE.Mesh(
        new THREE.TorusGeometry(0.95, 0.34, 20, 40),
        new THREE.MeshPhysicalMaterial({
          color: 0x3b7bd6,
          metalness: 0.7,
          roughness: 0.3,
          emissive: 0x3b7bd6,
          emissiveIntensity: 0.3,
        }),
      );
    } else {
      mesh = new THREE.Mesh(
        new THREE.BoxGeometry(4.0, 0.44, 2.2),
        new THREE.MeshPhysicalMaterial({
          color: 0x2f9e5f,
          metalness: 0.55,
          roughness: 0.35,
          emissive: 0x7bd88f,
          emissiveIntensity: 0.3,
        }),
      );
    }
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    group.add(mesh);

    const halo = new THREE.Sprite(
      new THREE.SpriteMaterial({ map: glowTex, transparent: true, opacity: 0, depthWrite: false }),
    );
    halo.scale.set(4.6, 4.6, 1);
    group.add(halo);

    const div = document.createElement("div");
    div.className = "h3label" + (i === 0 ? " sel" : "");
    div.textContent = i + " " + stripTags(c.name);
    const label = new CSS2DObject(div);
    label.position.set(0, c.sphere === true ? 1.7 : c.flat === true ? 0.9 : 1.25, 0);
    group.add(label);
    scene.add(group);
    bodies.push({ group, halo, base: group.position.clone(), label });

    if (i > 0) {
      // Aresta modelo -> componente com dois pacotes de luz.
      const a = new THREE.Vector3(0, 0, 0);
      const b = new THREE.Vector3(c.pos[0], c.pos[1], c.pos[2]);
      const lineGeo = new THREE.BufferGeometry().setFromPoints([a, b]);
      const line = new THREE.Line(
        lineGeo,
        new THREE.LineBasicMaterial({ color: 0x8b98a8, transparent: true, opacity: 0.4 }),
      );
      scene.add(line);
      for (let k = 0; k < 2; k++) {
        const pm = new THREE.Mesh(packetGeo, new THREE.MeshBasicMaterial({ color: 0xffe19a }));
        const glow = new THREE.Sprite(
          new THREE.SpriteMaterial({ map: glowTex, transparent: true, opacity: 0.9, depthWrite: false }),
        );
        glow.scale.set(0.9, 0.9, 1);
        pm.add(glow);
        scene.add(pm);
        packets.push({ mesh: pm, edge: i, u: k * 0.5 + i * 0.07, speed: 0.22 + (i % 3) * 0.04 });
      }
    }
  });

  // Pacotes orbitando o anel do harness.
  const ringPackets: THREE.Mesh[] = [];
  for (let k = 0; k < 6; k++) {
    const pm = new THREE.Mesh(packetGeo, new THREE.MeshBasicMaterial({ color: 0xf5b638 }));
    const glow = new THREE.Sprite(
      new THREE.SpriteMaterial({ map: glowTex, transparent: true, opacity: 0.85, depthWrite: false }),
    );
    glow.scale.set(1.1, 1.1, 1);
    pm.add(glow);
    scene.add(pm);
    ringPackets.push(pm);
  }

  const ray = new THREE.Raycaster();
  const ptr = new THREE.Vector2();
  let downAt: { x: number; y: number } | null = null;
  canvas.addEventListener("pointerdown", (e: PointerEvent) => {
    downAt = { x: e.clientX, y: e.clientY };
    controls.autoRotate = false;
  });
  canvas.addEventListener("pointerup", (e: PointerEvent) => {
    if (downAt === null) return;
    const moved = Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y);
    downAt = null;
    if (moved > 5) return;
    const r = canvas.getBoundingClientRect();
    ptr.x = ((e.clientX - r.left) / r.width) * 2 - 1;
    ptr.y = -((e.clientY - r.top) / r.height) * 2 + 1;
    ray.setFromCamera(ptr, camera);
    const hits = ray.intersectObjects(
      bodies.map((b) => b.group),
      true,
    );
    if (hits.length > 0) {
      let g: THREE.Object3D | null = hits[0].object;
      while (g !== null && !(g instanceof THREE.Group)) g = g.parent;
      const idx = bodies.findIndex((b) => b.group === g);
      if (idx >= 0) h3select(idx);
    }
  });

  const slideIdx = S("s-h3d");
  let raf = 0;
  let prevT = performance.now();
  const t0 = prevT;

  const sizeToStage = (): void => {
    const r = canvas.getBoundingClientRect();
    const w = Math.max(2, Math.round(r.width));
    const h = Math.max(2, Math.round(r.height));
    renderer.setSize(w, h, false);
    labelRenderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  sizeToStage();
  window.addEventListener("resize", sizeToStage);

  const tick = (): void => {
    const now = performance.now();
    const dt = Math.min((now - prevT) / 1000, 0.05);
    prevT = now;
    const t = (now - t0) / 1000;
    void dt;
    controls.update();
    const pulse = 1 + 0.1 * Math.max(0, 1 - (performance.now() - selAt) / 450);
    bodies.forEach((b, i) => {
      const active = i === sel;
      const target = active ? 1.14 * pulse : 1;
      b.group.scale.setScalar(b.group.scale.x + (target - b.group.scale.x) * 0.18);
      const mat = (b.group.children[0] as THREE.Mesh).material as THREE.MeshStandardMaterial;
      if ("emissiveIntensity" in mat) {
        const want = active ? 1.1 : cEmissive(i);
        mat.emissiveIntensity += (want - mat.emissiveIntensity) * 0.15;
      }
      const hm = b.halo.material as THREE.SpriteMaterial;
      hm.opacity += ((active ? 0.75 : 0) - hm.opacity) * 0.12;
      b.group.rotation.y += active ? 0.008 : 0.0015;
    });
    // Pacotes viajam pelas arestas como pontos de luz.
    packets.forEach((p) => {
      p.u = (p.u + p.speed * 0.016) % 1;
      const dir = p.edge % 2 === 1 ? p.u : 1 - p.u;
      const end = H3[p.edge].pos;
      p.mesh.position.set(end[0] * dir, end[1] * dir, end[2] * dir);
      const active = p.edge === sel;
      p.mesh.scale.setScalar(active ? 1.5 : 1);
    });
    ringPackets.forEach((pm, k) => {
      const a = t * 0.5 + (k / ringPackets.length) * Math.PI * 2;
      pm.position.set(Math.cos(a) * 5, 0.6 + Math.sin(t * 1.4 + k) * 0.06, Math.sin(a) * 5);
    });
    const activeSlide = document.querySelectorAll(".slide")[slideIdx];
    if (activeSlide !== undefined && activeSlide.classList.contains("active") && !fallbackActive) {
      renderer.render(scene, camera);
      labelRenderer.render(scene, camera);
      // Posições projetadas para testes de clique automatizados.
      const r = canvas.getBoundingClientRect();
      bodies.forEach((b, i) => {
        const v = b.group.position.clone().project(camera);
        proj[i] = {
          x: ((v.x + 1) / 2) * r.width * window.devicePixelRatio,
          y: ((1 - v.y) / 2) * r.height * window.devicePixelRatio,
          r: 90 * window.devicePixelRatio,
        };
      });
    }
    raf = requestAnimationFrame(tick);
  };
  tick();

  hooks.enter[slideIdx] = () => {
    if (fallbackActive) return;
    controls.autoRotate = true;
    sizeToStage();
  };
  const prevLeave = hooks.leave[slideIdx];
  hooks.leave[slideIdx] = () => {
    if (prevLeave !== undefined) prevLeave();
  };

  (window as unknown as { h3fallback: () => void }).h3fallback = () => {
    if (fallbackActive) return;
    fallbackActive = true;
    cancelAnimationFrame(raf);
    canvas.style.display = "none";
    labelLayer.style.display = "none";
    fallback2d();
  };
  canvas.addEventListener("webglcontextlost", (e: Event) => {
    e.preventDefault();
    (window as unknown as { h3fallback: () => void }).h3fallback();
  });
}

function cEmissive(i: number): number {
  if (i === 0) return 0.55;
  if (i === 5) return 0.3;
  return 0.25;
}

export function fallback2d(): void {
  const s = document.getElementById("fallback2d");
  if (s === null || !(s instanceof SVGSVGElement)) return;
  s.style.display = "block";
  const nodes: [string, number, number][] = [
    ["1 Prompt de sistema", 280, 180],
    ["2 Ferramentas", 620, 180],
    ["3 Middleware de contexto", 280, 420],
    ["4 Laço de execução", 620, 420],
    ["5 Proxy externo", 450, 560],
  ];
  s.innerHTML =
    `<circle cx="450" cy="300" r="190" fill="none" stroke="#f5b638" stroke-dasharray="10 8" stroke-width="3"/>` +
    `<text x="450" y="95" fill="#f5b638" text-anchor="middle" font-size="22">harness</text>` +
    `<circle cx="450" cy="300" r="60" fill="#f5b638"/>` +
    `<text x="450" y="308" text-anchor="middle" font-size="22" font-weight="bold">modelo</text>` +
    nodes
      .map(
        ([n, x, y], k) =>
          `<line x1="450" y1="300" x2="${x}" y2="${y}" stroke="#8b98a8"/>` +
          `<g class="fb" data-i="${k + 1}" tabindex="0" role="button" aria-label="${n}" style="cursor:pointer">` +
          `<rect x="${x - 120}" y="${y - 28}" width="240" height="56" rx="10" fill="${k === 4 ? "#2f9e5f" : "#3b7bd6"}"/>` +
          `<text x="${x}" y="${y + 7}" text-anchor="middle" fill="#fff" font-size="20">${n}</text></g>`,
      )
      .join("");
  s.querySelectorAll(".fb").forEach((g) => {
    const go = (): void => h3select(Number((g as SVGGElement).dataset.i));
    (g as SVGGElement).addEventListener("click", go);
    (g as SVGGElement).addEventListener("keydown", (e: Event) => {
      if ((e as KeyboardEvent).key === "Enter") go();
    });
  });
}
