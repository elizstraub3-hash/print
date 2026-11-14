/**
 * Cena 3D do unicórnio (three.js) — carregada sob demanda (chunk separado).
 * Animações procedurais sobre as articulações do GLB otimizado:
 *   Head, LegFrontR, LegFrontL, Tail, Body  (ver tools/optimize-model.html)
 */
import {
  WebGLRenderer, Scene, PerspectiveCamera, HemisphereLight, DirectionalLight, PMREMGenerator,
  Group, Mesh, PlaneGeometry, MeshBasicMaterial, CanvasTexture, SRGBColorSpace, NeutralToneMapping, MathUtils,
} from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js'

const MODEL_URL = `${import.meta.env.BASE_URL}models/unicornio.glb`
let modelPromise = null
const GOLD = /^(GoldenHorn|HornSpiral|Pendant|Flower\d_Center)/

/** Carrega (uma vez) e ajusta materiais para o visual "vinil/Blender" suave */
function loadModel() {
  if (!modelPromise) {
    modelPromise = new GLTFLoader().loadAsync(MODEL_URL).then((gltf) => {
      // chifre/pingente dourados ganham material próprio (o original
      // compartilha o amarelo com a crina, que deve continuar fosco)
      const goldMats = new Map()
      const tuned = new Set()
      gltf.scene.traverse((o) => {
        if (!o.isMesh) return
        if (GOLD.test(o.name)) {
          if (!goldMats.has(o.material)) {
            const g = o.material.clone()
            g.metalness = 0.55
            g.roughness = 0.3
            g.envMapIntensity = 1.1
            goldMats.set(o.material, g)
          }
          o.material = goldMats.get(o.material)
        } else if (!tuned.has(o.material)) {
          tuned.add(o.material)
          o.material.metalness = 0
          o.material.roughness = 0.58
          o.material.envMapIntensity = 0.9
        }
      })
      return gltf.scene
    })
    modelPromise.catch(() => (modelPromise = null))
  }
  return modelPromise
}

/** Sombra de contato barata (textura radial) */
function contactShadow() {
  const c = document.createElement('canvas')
  c.width = c.height = 128
  const g = c.getContext('2d')
  const grd = g.createRadialGradient(64, 64, 4, 64, 64, 64)
  grd.addColorStop(0, 'rgba(120,80,140,0.38)')
  grd.addColorStop(1, 'rgba(120,80,140,0)')
  g.fillStyle = grd
  g.fillRect(0, 0, 128, 128)
  const tex = new CanvasTexture(c)
  const mesh = new Mesh(new PlaneGeometry(3.2, 3.2), new MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }))
  mesh.rotation.x = -Math.PI / 2
  mesh.position.y = 0.005
  return mesh
}

const ease = {
  out: (t) => 1 - Math.pow(1 - t, 3),
  inOut: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  back: (t) => 1 + 2.7 * Math.pow(t - 1, 3) + 1.7 * Math.pow(t - 1, 2),
}
const seg = (t, a, b) => MathUtils.clamp((t - a) / (b - a), 0, 1)

/**
 * Animações. Cada uma recebe p (0..1) e devolve deslocamentos de pose.
 * hitAt = momento (0..1) em que a pata "clica" (dispara onHit).
 */
const ACTIONS = {
  // levanta a pata, abaixa a cabeça e "aperta" o botão; depois pulinho feliz
  tap: {
    duration: 1.15,
    hitAt: 0.42,
    pose(p) {
      const up = ease.out(seg(p, 0, 0.3))
      const down = ease.inOut(seg(p, 0.3, 0.42))
      const leg = -1.15 * up * (1 - down) - 0.25 * down * (1 - seg(p, 0.42, 0.6))
      const nod = 0.38 * ease.out(seg(p, 0, 0.35)) * (1 - ease.inOut(seg(p, 0.45, 0.75)))
      const squash = Math.sin(Math.PI * seg(p, 0.4, 0.55)) * 0.07
      const hopT = seg(p, 0.55, 0.95)
      return {
        legR: leg,
        headX: nod,
        lean: 0.12 * up * (1 - ease.inOut(seg(p, 0.45, 0.8))),
        y: Math.sin(Math.PI * hopT) * 0.45,
        squash: squash - Math.sin(Math.PI * hopT) * 0.03,
      }
    },
  },
  // carinho: inclina a cabeça e dá um pulinho
  pet: {
    duration: 0.9,
    hitAt: 0.3,
    pose(p) {
      const s = Math.sin(Math.PI * p)
      return { headZ: 0.28 * Math.sin(p * Math.PI * 2) , y: Math.sin(Math.PI * seg(p, 0.2, 0.8)) * 0.3, squash: -0.02 * s, tail: 0.6 * s }
    },
  },
  // comemoração: dois pulinhos + giro de 360°
  celebrate: {
    duration: 1.7,
    hitAt: 0.5,
    pose(p) {
      const h1 = Math.sin(Math.PI * seg(p, 0, 0.4))
      const h2 = Math.sin(Math.PI * seg(p, 0.45, 0.95))
      return { y: h1 * 0.35 + h2 * 0.6, spin: Math.PI * 2 * ease.inOut(seg(p, 0.45, 0.95)), legR: -0.6 * h1, legL: -0.6 * h2, tail: 0.5 * (h1 + h2) }
    },
  },
}

export async function createUnicornScene(canvas, { reduceMotion = false, yaw = -0.5, onFirstFrame } = {}) {
  const renderer = new WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: 'low-power' })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2))
  renderer.outputColorSpace = SRGBColorSpace
  renderer.toneMapping = NeutralToneMapping
  renderer.toneMappingExposure = 0.92

  const scene = new Scene()
  const pmrem = new PMREMGenerator(renderer)
  const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture
  scene.environment = envTex
  pmrem.dispose()
  scene.add(new HemisphereLight(0xffffff, 0xd9c4e6, 0.7))
  const key = new DirectionalLight(0xfff6ee, 2.2)
  key.position.set(-3, 5, 5)
  scene.add(key)
  const rim = new DirectionalLight(0xf8cde3, 1.2)
  rim.position.set(-4, 3, -4)
  scene.add(rim)

  const camera = new PerspectiveCamera(28, 1, 0.1, 50)
  camera.position.set(0, 2.2, 9.2)
  camera.lookAt(0, 1.72, 0)

  const base = (await loadModel()).clone(true)
  const J = {}
  base.traverse((o) => {
    if (['Head', 'LegFrontR', 'LegFrontL', 'Tail', 'Body'].includes(o.name)) J[o.name] = { node: o, rest: o.rotation.clone(), pos: o.position.clone() }
  })
  const turntable = new Group() // giro da comemoração + olhar para o ponteiro
  const hop = new Group() // pulo/squash
  hop.add(base)
  turntable.add(hop)
  turntable.rotation.y = yaw
  scene.add(turntable)
  scene.add(contactShadow())
  const shadow = scene.children[scene.children.length - 1]

  // ---- tamanho ----
  const resize = () => {
    const w = canvas.clientWidth || 300
    const h = canvas.clientHeight || 300
    renderer.setSize(w, h, false)
    camera.aspect = w / h
    camera.updateProjectionMatrix()
  }
  const ro = new ResizeObserver(() => {
    resize()
    if (!running) render(performance.now())
  })
  ro.observe(canvas)
  resize()

  // ---- estado ----
  let running = false
  let raf = 0
  let action = null // { def, start, onHit, hit, resolve }
  const pointer = { x: 0, tx: 0 }
  const t0 = performance.now()
  let first = true

  function applyPose(now) {
    const t = (now - t0) / 1000
    const idle = reduceMotion ? 0 : 1
    let P = {}
    if (action) {
      const p = Math.min(1, (now - action.start) / (action.def.duration * 1000))
      P = action.def.pose(p)
      if (!action.hit && p >= action.def.hitAt) {
        action.hit = true
        action.onHit?.()
      }
      if (p >= 1) {
        const a = action
        action = null
        a.resolve()
      }
    }
    pointer.x += (pointer.tx - pointer.x) * 0.08
    const H = J.Head, LR = J.LegFrontR, LL = J.LegFrontL, T = J.Tail
    if (H) {
      H.node.rotation.x = H.rest.x + (P.headX || 0) + idle * Math.sin(t * 1.6) * 0.035
      H.node.rotation.z = H.rest.z + (P.headZ || 0) + idle * Math.sin(t * 1.1) * 0.05
      H.node.rotation.y = H.rest.y + pointer.x * 0.3
    }
    if (LR) LR.node.rotation.x = LR.rest.x + (P.legR || 0)
    if (LL) LL.node.rotation.x = LL.rest.x + (P.legL || 0)
    if (T) T.node.rotation.y = T.rest.y + idle * Math.sin(t * 2.4) * 0.28 + (P.tail || 0) * Math.sin(t * 14)
    const breathe = idle * Math.sin(t * 2) * 0.012
    hop.position.y = (P.y || 0)
    hop.rotation.x = P.lean || 0
    const sq = (P.squash || 0) - breathe
    hop.scale.set(1 + sq * 0.6, 1 - sq, 1 + sq * 0.6)
    turntable.rotation.y = yaw + pointer.x * 0.25 + (P.spin || 0)
    const lift = Math.max(0, P.y || 0)
    shadow.scale.setScalar(1 - lift * 0.35)
    shadow.material.opacity = 1 - lift * 0.5
  }

  function render(now) {
    applyPose(now)
    renderer.render(scene, camera)
    if (first) {
      first = false
      onFirstFrame?.()
    }
  }

  function loop(now) {
    render(now)
    raf = requestAnimationFrame(loop)
  }

  const api = {
    start() {
      if (running) return
      running = true
      if (reduceMotion && !action) return render(performance.now()), (running = false)
      raf = requestAnimationFrame(loop)
    },
    stop() {
      running = false
      cancelAnimationFrame(raf)
    },
    /** toca uma animação; resolve ao terminar. onHit = momento do "clique" */
    play(name, { onHit } = {}) {
      const def = ACTIONS[name]
      if (!def) return Promise.resolve()
      if (reduceMotion) {
        onHit?.()
        return Promise.resolve()
      }
      if (action) {
        action.onHit && !action.hit && action.onHit()
        action.resolve()
      }
      return new Promise((resolve) => {
        action = { def, start: performance.now(), onHit, hit: false, resolve }
        if (!running) {
          // anima mesmo fora do loop contínuo (ex.: logo após sair da tela)
          const tick = (now) => {
            render(now)
            if (action) requestAnimationFrame(tick)
          }
          requestAnimationFrame(tick)
        }
      })
    },
    look(x) {
      pointer.tx = MathUtils.clamp(x, -1, 1)
    },
    dispose() {
      api.stop()
      ro.disconnect()
      action?.resolve()
      shadow.geometry.dispose()
      shadow.material.map.dispose()
      shadow.material.dispose()
      envTex.dispose()
      renderer.dispose()
      // geometrias/materiais do modelo são compartilhados entre instâncias (cache) → não descartar
    },
  }
  render(performance.now())
  return api
}

/** Pré-carrega o modelo (chamado cedo para ganhar tempo) */
export const preloadUnicorn = () => loadModel().catch(() => {})
