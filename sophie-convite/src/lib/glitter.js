/**
 * Glitter em canvas único, fixo na tela (pointer-events: none).
 * Partículas: lantejoulas que "piscam" (giro 3D simulado), estrelinhas e
 * corações. O loop só roda enquanto há partículas → zero custo parado.
 */
const COLORS = ['#F7A8CF', '#F8CDE3', '#E9B8FF', '#C9B5F2', '#A9DCF2', '#FFE58F', '#EBCB85', '#FFFFFF', '#B9EBD2']
let canvas, ctx, raf = 0, parts = [], dpr = 1, last = 0
const reduce = () => window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

function ensure() {
  if (canvas) return
  canvas = document.createElement('canvas')
  canvas.setAttribute('aria-hidden', 'true')
  Object.assign(canvas.style, { position: 'fixed', inset: '0', width: '100%', height: '100%', pointerEvents: 'none', zIndex: '70' })
  document.body.appendChild(canvas)
  ctx = canvas.getContext('2d')
  const size = () => {
    dpr = Math.min(window.devicePixelRatio || 1, 2)
    canvas.width = Math.round(window.innerWidth * dpr)
    canvas.height = Math.round(window.innerHeight * dpr)
  }
  size()
  window.addEventListener('resize', size, { passive: true })
}

const rand = (a, b) => a + Math.random() * (b - a)

function spawn(x, y, opts) {
  const { speed = 9, spread = Math.PI * 2, angle = -Math.PI / 2, gravity = 0.16, size = [3, 7], life = [55, 95] } = opts
  const a = angle + rand(-spread / 2, spread / 2)
  const v = rand(speed * 0.35, speed)
  const r = Math.random()
  return {
    x, y,
    vx: Math.cos(a) * v,
    vy: Math.sin(a) * v,
    g: gravity,
    s: rand(size[0], size[1]),
    rot: rand(0, Math.PI),
    vr: rand(-0.25, 0.25),
    flip: rand(0, Math.PI * 2),
    vf: rand(0.15, 0.4),
    c: COLORS[(Math.random() * COLORS.length) | 0],
    shape: r < 0.62 ? 0 : r < 0.9 ? 1 : 2, // 0 lantejoula, 1 estrela, 2 coração
    life: rand(life[0], life[1]),
    age: 0,
  }
}

function drawStar(s) {
  ctx.beginPath()
  for (let i = 0; i < 4; i++) {
    const a = (i * Math.PI) / 2
    ctx.lineTo(Math.cos(a) * s * 1.6, Math.sin(a) * s * 1.6)
    ctx.lineTo(Math.cos(a + Math.PI / 4) * s * 0.45, Math.sin(a + Math.PI / 4) * s * 0.45)
  }
  ctx.closePath()
  ctx.fill()
}
function drawHeart(s) {
  ctx.beginPath()
  ctx.moveTo(0, s * 0.9)
  ctx.bezierCurveTo(-s * 1.6, -s * 0.2, -s * 0.6, -s * 1.3, 0, -s * 0.45)
  ctx.bezierCurveTo(s * 0.6, -s * 1.3, s * 1.6, -s * 0.2, 0, s * 0.9)
  ctx.fill()
}

function frame(now) {
  const dt = Math.min(2.5, (now - (last || now)) / 16.67 || 1)
  last = now
  ctx.setTransform(1, 0, 0, 1, 0, 0)
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  const H = window.innerHeight + 40
  let n = 0
  for (const p of parts) {
    p.age += dt
    if (p.age > p.life || p.y > H) continue
    p.vx *= Math.pow(0.985, dt)
    p.vy = p.vy * Math.pow(0.985, dt) + p.g * dt
    p.x += p.vx * dt
    p.y += p.vy * dt + Math.sin((p.age + p.flip) * 0.15) * 0.3
    p.rot += p.vr * dt
    p.flip += p.vf * dt
    const fade = Math.min(1, (p.life - p.age) / 20)
    const shimmer = Math.abs(Math.cos(p.flip)) // simula a lantejoula girando
    ctx.save()
    ctx.translate(p.x, p.y)
    ctx.rotate(p.rot)
    ctx.globalAlpha = fade * (0.55 + 0.45 * shimmer)
    ctx.fillStyle = shimmer > 0.92 ? '#FFFFFF' : p.c
    if (p.shape === 0) {
      ctx.scale(1, 0.25 + 0.75 * shimmer)
      ctx.fillRect(-p.s / 2, -p.s / 2, p.s, p.s)
    } else if (p.shape === 1) drawStar(p.s * 0.8)
    else drawHeart(p.s * 0.8)
    ctx.restore()
    parts[n++] = p
  }
  parts.length = n
  if (n) raf = requestAnimationFrame(frame)
  else {
    ctx.setTransform(1, 0, 0, 1, 0, 0)
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    raf = 0
    last = 0
  }
}

function run() {
  if (!raf) raf = requestAnimationFrame(frame)
}

const MAX = 700 // limite para celulares mais simples

/** Explosão a partir de um ponto (coordenadas da janela) */
export function burst(x, y, { count = 70, ...opts } = {}) {
  if (reduce()) return
  ensure()
  const room = Math.max(0, MAX - parts.length)
  for (let i = 0; i < Math.min(count, room); i++) parts.push(spawn(x, y, opts))
  run()
}

/** Explosão a partir do centro de um elemento */
export function burstFrom(el, opts) {
  if (!el) return
  const r = el.getBoundingClientRect()
  burst(r.left + r.width / 2, r.top + r.height / 2, opts)
}

/** Chuva de glitter caindo do topo da tela */
export function rain({ count = 220, duration = 1600 } = {}) {
  if (reduce()) return
  ensure()
  const w = window.innerWidth
  const waves = 8
  for (let k = 0; k < waves; k++) {
    setTimeout(() => {
      const room = Math.max(0, MAX - parts.length)
      for (let i = 0; i < Math.min(count / waves, room); i++) {
        parts.push(spawn(rand(0, w), rand(-30, -5), { speed: 2.5, angle: Math.PI / 2, spread: 1.2, gravity: 0.05, life: [160, 240], size: [3, 8] }))
      }
      run()
    }, (k * duration) / waves)
  }
}
