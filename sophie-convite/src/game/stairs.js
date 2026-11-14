/**
 * "Escadinha do Unicórnio" — toque para pular para a próxima nuvem que passa.
 * Fácil para crianças: área de pouso generosa, nuvem lenta, errar não tira pontos.
 */
const W = 360 // largura virtual
const STEP_GAP = 118
const STEP_H = 26
const UNI = 122 // tamanho do unicórnio (a imagem tem margem transparente)
const COLORS = [
  ['#F7B8D6', '#E58DB8'],
  ['#D9C6F7', '#B79BEA'],
  ['#BFE3F5', '#8CC7E6'],
  ['#FFE9A8', '#E8C56B'],
  ['#C8EBD6', '#94D2AE'],
]

const load = (src) =>
  new Promise((res, rej) => {
    const i = new Image()
    i.onload = () => res(i)
    i.onerror = rej
    i.src = src
  })

function rr(ctx, x, y, w, h, r) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.arcTo(x + w, y, x + w, y + h, r)
  ctx.arcTo(x + w, y + h, x, y + h, r)
  ctx.arcTo(x, y + h, x, y, r)
  ctx.arcTo(x, y, x + w, y, r)
  ctx.closePath()
}

export async function createStairs(canvas, { uniSrc, onJump, onMiss, onMilestone }) {
  const ctx = canvas.getContext('2d')
  const uni = await load(uniSrc)
  let dpr = 1, scale = 1, H = 480
  const resize = () => {
    dpr = Math.min(window.devicePixelRatio || 1, 2)
    const w = canvas.clientWidth || 320
    const h = canvas.clientHeight || 420
    canvas.width = Math.round(w * dpr)
    canvas.height = Math.round(h * dpr)
    scale = w / W
    H = h / scale
  }
  resize()
  const ro = new ResizeObserver(() => {
    resize()
    draw()
  })
  ro.observe(canvas)

  let S
  const stepW = (n) => Math.max(112, 150 - n * 2) // fica só um pouquinho menor
  const speed = (n) => Math.min(105, 52 + n * 3.5) // e um pouquinho mais rápida
  function reset() {
    const baseY = H - 70
    S = {
      t: 0,
      count: 0,
      cam: 0, // deslocamento vertical da câmera (mundo sobe)
      camTarget: 0,
      steps: [{ x: W / 2, y: baseY, w: 170, c: 0, moving: false }],
      ux: W / 2,
      uy: baseY, // base do unicórnio (mundo)
      jump: null, // {t0, from, to, ok}
      squash: 0,
      parts: [],
      msg: null,
    }
    spawn()
  }
  function spawn() {
    const last = S.steps[S.steps.length - 1]
    const n = S.count
    S.steps.push({ x: W / 2, y: last.y - STEP_GAP, w: stepW(n), c: (last.c + 1) % COLORS.length, moving: true, phase: Math.random() * Math.PI * 2, sp: speed(n), dir: Math.random() < 0.5 ? -1 : 1 })
  }
  const current = () => S.steps[S.steps.length - 2]
  const next = () => S.steps[S.steps.length - 1]

  function tryJump() {
    if (S.jump) return false
    S.jump = { t: 0, from: S.uy, to: next().y, dur: 0.55 }
    return true
  }

  function burst(x, y, n = 16) {
    for (let i = 0; i < n; i++) {
      const a = Math.random() * Math.PI * 2
      S.parts.push({ x, y, vx: Math.cos(a) * 140, vy: Math.sin(a) * 140 - 60, life: 0.8, c: COLORS[i % 5][0] })
    }
  }

  function step(dt) {
    S.t += dt
    // nuvem que se move: vai e volta (pingue-pongue suave)
    const nx = next()
    if (nx.moving) {
      const half = nx.w / 2 + 8
      nx.x += nx.dir * nx.sp * dt
      if (nx.x > W - half) (nx.x = W - half), (nx.dir = -1)
      if (nx.x < half) (nx.x = half), (nx.dir = 1)
    }
    // pulo
    if (S.jump) {
      const J = S.jump
      J.t += dt
      const p = Math.min(1, J.t / J.dur)
      const apex = J.to - 70
      if (p < 0.6) {
        const q = p / 0.6
        S.uy = J.from + (apex - J.from) * (1 - (1 - q) * (1 - q))
      } else {
        // decide no topo do pulo: pousa na próxima ou volta
        if (J.ok == null) {
          const target = next()
          J.ok = Math.abs(S.ux - target.x) < target.w / 2 + 22 // pouso generoso
          if (J.ok) target.moving = false
        }
        const q = (p - 0.6) / 0.4
        const land = J.ok ? J.to : J.from
        S.uy = apex + (land - apex) * (q * q)
        if (J.ok) S.ux += (next().x - S.ux) * Math.min(1, dt * 6) // escorrega pro centrinho
      }
      if (p >= 1) {
        S.squash = 1
        if (J.ok) {
          S.count++
          burst(S.ux, S.uy, 14)
          S.camTarget = S.count * STEP_GAP
          spawn()
          if (S.steps.length > 8) S.steps.splice(0, S.steps.length - 8)
          const m = S.count % 5 === 0
          S.msg = { text: m ? `Uhuu! ${S.count} pulos!` : ['Isso!', 'Uau!', 'Mandou bem!', 'Que pulo!'][S.count % 4], t: 1.1, big: m }
          onJump?.(S.count)
          if (m) onMilestone?.(S.count)
        } else {
          S.msg = { text: 'Quase! Tenta de novo 💕', t: 1.1 }
          onMiss?.()
        }
        S.jump = null
      }
    }
    S.squash = Math.max(0, S.squash - dt * 4)
    S.cam += (S.camTarget - S.cam) * Math.min(1, dt * 4)
    for (const p of S.parts) {
      p.life -= dt
      p.vy += 400 * dt
      p.x += p.vx * dt
      p.y += p.vy * dt
    }
    S.parts = S.parts.filter((p) => p.life > 0)
    if (S.msg) S.msg.t -= dt
  }

  function draw() {
    if (!S) return
    ctx.setTransform(dpr * scale, 0, 0, dpr * scale, 0, 0)
    // céu que muda conforme sobe (azul → lilás → rosa)
    const k = Math.min(1, S.count / 25)
    const g = ctx.createLinearGradient(0, 0, 0, H)
    g.addColorStop(0, `hsl(${200 + k * 80}, 70%, ${90 - k * 6}%)`)
    g.addColorStop(1, `hsl(${320 - k * 20}, 75%, 93%)`)
    ctx.fillStyle = g
    ctx.fillRect(0, 0, W, H)
    // estrelinhas e nuvens de fundo (parallax)
    for (let i = 0; i < 18; i++) {
      const x = (i * 97) % W
      const y = (((i * 61 + S.cam * 0.3) % (H + 40)) + H + 40) % (H + 40) - 20
      ctx.fillStyle = i % 3 ? 'rgba(255,255,255,.7)' : 'rgba(235,203,133,.8)'
      ctx.beginPath()
      ctx.arc(x, y, 1.5 + (i % 3), 0, Math.PI * 2)
      ctx.fill()
    }
    ctx.save()
    ctx.translate(0, S.cam)
    // degraus
    for (const st of S.steps) {
      const [f, e] = COLORS[st.c]
      const x = st.x - st.w / 2
      rr(ctx, x, st.y + 2, st.w, STEP_H, 13)
      ctx.fillStyle = e
      ctx.fill()
      rr(ctx, x, st.y, st.w, STEP_H - 5, 12)
      ctx.fillStyle = f
      ctx.fill()
      ctx.fillStyle = 'rgba(255,255,255,.7)'
      rr(ctx, x + 12, st.y + 4, st.w - 24, 4, 2)
      ctx.fill()
      ctx.strokeStyle = '#fff'
      ctx.lineWidth = 2.5
      rr(ctx, x, st.y, st.w, STEP_H, 12)
      ctx.stroke()
      // fofura: nuvenzinhas nas pontas
      ctx.fillStyle = '#fff'
      for (const cx of [x + 6, x + st.w - 6]) {
        ctx.beginPath()
        ctx.arc(cx, st.y + 10, 11, 0, Math.PI * 2)
        ctx.fill()
      }
      if (st.moving) {
        // setinhas indicando o movimento
        ctx.fillStyle = 'rgba(94,68,104,.35)'
        ctx.font = '600 13px Fredoka, system-ui'
        ctx.textAlign = 'center'
        ctx.fillText('⟵ ⟶', st.x, st.y + STEP_H + 16)
      }
    }
    // sombra + unicórnio
    const cur = S.jump ? next() : current()
    ctx.fillStyle = 'rgba(120,70,130,.18)'
    ctx.beginPath()
    ctx.ellipse(S.ux, (S.jump ? Math.max(S.uy, cur.y) : S.uy) + 2, 26, 6, 0, 0, Math.PI * 2)
    ctx.fill()
    const sq = S.squash * 0.18
    const air = S.jump ? 0.08 : 0
    const bob = S.jump ? 0 : Math.sin(S.t * 3) * 2
    ctx.save()
    ctx.translate(S.ux, S.uy + 4 + bob)
    ctx.scale(1 + sq - air, 1 - sq + air)
    ctx.rotate(S.jump ? Math.sin(Math.min(1, S.jump.t / S.jump.dur) * Math.PI) * -0.18 : 0)
    ctx.drawImage(uni, -UNI / 2, -UNI, UNI, UNI)
    ctx.restore()
    for (const p of S.parts) {
      ctx.globalAlpha = Math.max(0, p.life / 0.8)
      ctx.fillStyle = p.c
      ctx.fillRect(p.x - 3, p.y - 3, 6, 6)
    }
    ctx.globalAlpha = 1
    ctx.restore()
    // mensagem
    if (S.msg && S.msg.t > 0) {
      ctx.globalAlpha = Math.min(1, S.msg.t * 2)
      ctx.textAlign = 'center'
      ctx.font = `700 ${S.msg.big ? 30 : 24}px "Dancing Script", cursive`
      ctx.lineWidth = 6
      ctx.strokeStyle = '#fff'
      const y = 70 - (1.1 - S.msg.t) * 20
      ctx.strokeText(S.msg.text, W / 2, y)
      ctx.fillStyle = '#CF4A92'
      ctx.fillText(S.msg.text, W / 2, y)
      ctx.globalAlpha = 1
    }
  }

  let raf = 0, running = false, last = 0
  const frame = (now) => {
    const dt = Math.min(0.033, (now - last) / 1000 || 0)
    last = now
    step(dt)
    draw()
    if (running) raf = requestAnimationFrame(frame)
  }
  reset()
  draw()
  return {
    start() {
      if (running) return
      running = true
      last = performance.now()
      raf = requestAnimationFrame(frame)
    },
    pause() {
      running = false
      cancelAnimationFrame(raf)
    },
    get running() {
      return running
    },
    jump: tryJump,
    reset() {
      reset()
      draw()
    },
    dispose() {
      running = false
      cancelAnimationFrame(raf)
      ro.disconnect()
    },
  }
}
