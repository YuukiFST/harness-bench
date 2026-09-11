import * as THREE from "three";

interface CoverScene {
  stop: () => void;
}

function makeScene(canvas: HTMLCanvasElement, seed: number): CoverScene {
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x0b0f14, 0.028);
  const camera = new THREE.PerspectiveCamera(60, 16 / 9, 0.1, 200);
  camera.position.set(0, 1.6, 14);

  const key = new THREE.DirectionalLight(0xfff2cf, 1.4);
  key.position.set(6, 8, 6);
  scene.add(key);
  const rim = new THREE.PointLight(0xf5b638, 60, 60);
  rim.position.set(-7, -2, 4);
  scene.add(rim);
  scene.add(new THREE.AmbientLight(0x33404f, 1.2));

  // Malha lenta: icosaedro em wireframe com material físico por baixo.
  const core = new THREE.Mesh(
    new THREE.IcosahedronGeometry(4.2, 1),
    new THREE.MeshStandardMaterial({
      color: 0x141d29,
      metalness: 0.85,
      roughness: 0.32,
      flatShading: true,
    }),
  );
  core.position.set(5.5, 0.4, -4);
  scene.add(core);
  const wire = new THREE.LineSegments(
    new THREE.WireframeGeometry(core.geometry),
    new THREE.LineBasicMaterial({ color: 0xf5b638, transparent: true, opacity: 0.28 }),
  );
  core.add(wire);

  // Partículas à deriva.
  const N = 420;
  const pos = new Float32Array(N * 3);
  let s = seed;
  const rnd = (): number => {
    s = (s * 16807) % 2147483647;
    return s / 2147483647;
  };
  for (let i = 0; i < N; i++) {
    pos[i * 3] = (rnd() - 0.5) * 30;
    pos[i * 3 + 1] = (rnd() - 0.5) * 14;
    pos[i * 3 + 2] = -8 + rnd() * 10;
  }
  const pg = new THREE.BufferGeometry();
  pg.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const pts = new THREE.Points(
    pg,
    new THREE.PointsMaterial({
      color: 0xf5b638,
      size: 0.055,
      transparent: true,
      opacity: 0.75,
      sizeAttenuation: true,
    }),
  );
  scene.add(pts);

  let raf = 0;
  let alive = true;
  const t0 = performance.now();
  const resize = (): void => {
    const r = canvas.getBoundingClientRect();
    const w = Math.max(2, r.width);
    const h = Math.max(2, r.height);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  resize();
  window.addEventListener("resize", resize);

  const tick = (): void => {
    if (!alive) return;
    const t = (performance.now() - t0) / 1000;
    core.rotation.y = t * 0.07;
    core.rotation.x = Math.sin(t * 0.1) * 0.2;
    pts.rotation.y = t * 0.012;
    pts.position.y = Math.sin(t * 0.25) * 0.3;
    // Só renderiza quando a capa/fecho está visível: economia de GPU no projetor.
    const slide = canvas.closest(".slide");
    if (slide !== null && slide.classList.contains("active")) renderer.render(scene, camera);
    raf = requestAnimationFrame(tick);
  };
  tick();

  return {
    stop: () => {
      alive = false;
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
      core.geometry.dispose();
      pg.dispose();
      renderer.dispose();
    },
  };
}

export function initCovers(): CoverScene[] {
  const out: CoverScene[] = [];
  const a = document.getElementById("coverbg1");
  const b = document.getElementById("coverbg2");
  if (a instanceof HTMLCanvasElement) {
    try {
      out.push(makeScene(a, 1234567));
    } catch {
      a.style.display = "none";
    }
  }
  if (b instanceof HTMLCanvasElement) {
    try {
      out.push(makeScene(b, 7654321));
    } catch {
      b.style.display = "none";
    }
  }
  return out;
}
