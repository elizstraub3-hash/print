/**
 * Mini-jogo "Pula, Sophie!" — runner infinito em canvas, pensado para
 * crianças pequenas: chão contínuo (não existe "perder"), pulo duplo,
 * estrelas com área de coleta generosa e velocidade tranquila.
 */
const VH = 440 // altura virtual do mundo (unidades)
const GROUND = VH - 58
const GRAVITY = 1500
const JUMP_V = -610
const JUMP2_V = -560
const SPEED = 115
const HELP_AFTER = 20 // s: depois disso, estrelas mais baixas (ajuda automática)
const EASY_Y = GROUND - 100
const BRICK = 34
const HEAD_H = 74
const BRICK_COLORS = [
  ['#F7B8D6', '#E58DB8'],
  ['#D9C6F7', '#B79BEA'],
  ['#BFE3F5', '#8CC7E6'],
  ['#FFE9A8', '#E8C56B'],
  ['#C8EBD6', '#94D2AE'],
]
const STAR_TINTS = ['#D9B8FF', '#A9DCF2', '#FFE58F', '#B9EBD2', '#FFC9A8']

const loadImg = (src) =>
  new Promise((res, rej) => {
    const i = new Image()
    i.decoding = 'async'
    i.onload = () => res(i)
    i.onerror = rej
    i.src = src
  })

function starPath(ctx, r) {
  ctx.beginPath()
  for (let i = 0; i < 10; i++) {
    const a = -Math.PI / 2 + (i * Math.PI) / 5
    const rr = i % 2 ? r * 0.5 : r
    ctx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr)
  }
  ctx.closePath()
}

/** pré-renderiza cada estrela "fofinha" num canvas pequeno (rápido de desenhar) */
function makeStarSprite(tint, r = 27, scale = 2) {
  const s = Math.ceil((r + 6) * 2 * scale)
  const c = document.createElement('canvas')
  c.width = c.height = s
  const g = c.getContext('2d')
  g.scale(scale, scale)
  g.translate(s / scale / 2, s / scale / 2)
  g.lineJoin = 'round'
  const grd = g.createRadialGradient(-r * 0.3, -r * 0.4, 2, 0, 0, r * 1.2)
  grd.addColorStop(0, '#FFE6F3')
  grd.addColorStop(0.5, '#F7A8CF')
  grd.addColorStop(1, tint)
  starPath(g, r)
  g.fillStyle = grd
  g.fill()
  g.lineWidth = 3
  g.strokeStyle = '#fff'
  g.stroke()
  // brilho e glitter
  g.fillStyle = 'rgba(255,255,255,.8)'
  g.beginPath()
  g.ellipse(-r * 0.25, -r * 0.45, r * 0.16, r * 0.08, -0.6, 0, Math.PI * 2)
  g.fill()
  for (const [x, y] of [[0.3, 0.1], [-0.25, 0.25], [0.1, 0.4]]) {
    g.beginPath()
    g.arc(x * r, y * r, 1.2, 0, Math.PI * 2)
    g.fill()
  }
  // carinha
  g.strokeStyle = '#6B4E71'
  g.lineWidth = 1.8
  g.lineCap = 'round'
  g.beginPath()
  g.arc(-r * 0.2, -r * 0.02, r * 0.09, Math.PI * 0.15, Math.PI * 0.85)
  g.stroke()
  g.beginPath()
  g.arc(r * 0.2, -r * 0.02, r * 0.09, Math.PI * 0.15, Math.PI * 0.85)
  g.stroke()
  g.beginPath()
  g.arc(0, r * 0.1, r * 0.1, Math.PI * 0.1, Math.PI * 0.9)
  g.stroke()
  return { canvas: c, size: s / scale }
}

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.arcTo(x + w, y, x + w, y + h, r)
  ctx.arcTo(x + w, y + h, x, y + h, r)
  ctx.arcTo(x, y + h, x, y, r)
  ctx.arcTo(x, y, x + w, y, r)
  ctx.closePath()
}

export async function createRunner(canvas, { headSrc, bgSrc, goal = 5, onStar, onGoal, onJump }) {
  const ctx = canvas.getContext('2d')
  let [head, bg] = await Promise.all([loadImg(headSrc), loadImg(bgSrc).catch(() => null)])
  const stars = STAR_TINTS.map((t) => makeStarSprite(t))
  let headW = (HEAD_H * head.width) / head.height

  let dpr = 1
  let scale = 1
  let VW = 320
  const resize = () => {
    dpr = Math.min(window.devicePixelRatio || 1, 1.5)
    const w = canvas.clientWidth || 320
    const h = canvas.clientHeight || 400
    canvas.width = Math.round(w * dpr)
    canvas.height = Math.round(h * dpr)
    scale = h / VH
    VW = w / scale
    cache = null // refaz os desenhos pré-prontos no novo tamanho
  }
  let cache = null
  resize()
  const ro = new ResizeObserver(() => {
    resize()
    draw(0)
  })
  ro.observe(canvas)

  // ---------- estado ----------
  let S
  const reset = () => {
    S = {
      t: 0,
      dist: 0,
      px: 0,
      y: GROUND, // base da cabeça
      vy: 0,
      jumps: 0,
      onGround: true,
      squash: 0,
      plats: [],
      items: [],
      parts: [],
      nextX: 0,
      chunk: 0,
      got: 0,
      done: false,
    }
    S.px = VW * 0.26
    S.nextX = VW * 0.72
    generate()
  }

  function generate() {
    while (S.nextX < S.dist + VW + 260) {
      const k = S.chunk++
      const x = S.nextX
      if (S.t > HELP_AFTER) {
        // modo ajuda: tijolinho baixo + estrela que sai com um pulo simples
        S.plats.push({ x, y: GROUND - 92, n: 3, c: k })
        S.items.push({ x: x - 50, y: EASY_Y, tint: k % 5, taken: false })
        S.nextX += 3 * BRICK + 150
      } else if (k === 0) {
        // 1ª estrela: baixinha, um pulo simples já pega
        S.items.push({ x: x + 40, y: GROUND - 92, tint: k % 5, taken: false })
        S.nextX += 230
      } else if (k % 3 === 1) {
        // degrau baixo com estrela em cima
        const n = 3 + (k % 2)
        S.plats.push({ x, y: GROUND - 92, n, c: k })
        S.items.push({ x: x + (n * BRICK) / 2, y: GROUND - 92 - 58, tint: k % 5, taken: false })
        S.nextX += n * BRICK + 70
      } else if (k % 3 === 2) {
        // degrau alto logo depois (escadinha)
        const n = 3
        S.plats.push({ x, y: GROUND - 178, n, c: k })
        S.items.push({ x: x + (n * BRICK) / 2, y: GROUND - 178 - 58, tint: k % 5, taken: false })
        S.nextX += n * BRICK + 190
      } else {
        // estrela no "ar" sobre o chão (pulo duplo) + tijolinho decorativo
        S.items.push({ x: x + 30, y: GROUND - 150, tint: k % 5, taken: false })
        S.nextX += 220
      }
    }
    // limpa o que já passou
    const left = S.dist - 120
    S.plats = S.plats.filter((p) => p.x + p.n * BRICK > left)
    S.items = S.items.filter((i) => i.x > left && !(i.taken && i.fade <= 0))
  }

  // ---------- física ----------
  function step(dt) {
    S.t += dt
    if (!S.done) S.dist += SPEED * dt
    const wx = S.dist + S.px // posição do jogador no mundo
    const prevY = S.y
    S.vy = Math.min(S.vy + GRAVITY * dt, 900)
    S.y += S.vy * dt
    S.onGround = false
    // chão contínuo
    if (S.y >= GROUND) {
      if (S.vy > 200) S.squash = 1
      S.y = GROUND
      S.vy = 0
      S.jumps = 0
      S.onGround = true
    }
    // plataformas (só por cima — dá para atravessar de baixo, mais fácil)
    for (const p of S.plats) {
      const x0 = p.x - headW * 0.35
      const x1 = p.x + p.n * BRICK + headW * 0.35
      if (wx > x0 && wx < x1 && S.vy >= 0 && prevY <= p.y + 2 && S.y >= p.y) {
        if (S.vy > 200) S.squash = 1
        S.y = p.y
        S.vy = 0
        S.jumps = 0
        S.onGround = true
      }
    }
    S.squash = Math.max(0, S.squash - dt * 5)

    // estrelas (área de coleta generosa)
    const cx = wx
    const cy = S.y - HEAD_H * 0.5
    for (const it of S.items) {
      if (it.taken) {
        it.fade = (it.fade ?? 1) - dt * 3
        continue
      }
      const dx = it.x - cx
      const dy = it.y - cy
      if (dx * dx + dy * dy < 58 * 58) {
        it.taken = true
        it.fade = 1
        S.got++
        for (let i = 0; i < 14; i++) {
          const a = Math.random() * Math.PI * 2
          S.parts.push({ x: it.x, y: it.y, vx: Math.cos(a) * 160, vy: Math.sin(a) * 160 - 60, life: 0.7, c: STAR_TINTS[i % 5] })
        }
        const r = canvas.getBoundingClientRect()
        onStar?.(S.got, r.left + (it.x - S.dist) * scale, r.top + it.y * scale)
        // modo infinito: a meta só avisa (uma vez); o jogo continua
        if (S.got === goal) setTimeout(() => onGoal?.(), 350)
      }
    }
    // partículas
    for (const p of S.parts) {
      p.life -= dt
      p.vy += 500 * dt
      p.x += p.vx * dt
      p.y += p.vy * dt
    }
    S.parts = S.parts.filter((p) => p.life > 0)
    generate()
  }

  // ---------- desenho ----------
  // ---------- desenhos pré-prontos (feitos uma vez, só copiados a cada quadro) ----------
  function mk(w, h) {
    const c = document.createElement('canvas')
    c.width = Math.ceil(w * dpr * scale)
    c.height = Math.ceil(h * dpr * scale)
    const g = c.getContext('2d')
    g.setTransform(dpr * scale, 0, 0, dpr * scale, 0, 0)
    return { c, g, w, h }
  }
  function buildCache() {
    // fundo: 2 tiles (normal + espelhado) já com o véu claro
    let bgc = null
    if (bg) {
      const tileW = (bg.width / bg.height) * VH
      bgc = mk(tileW * 2, VH)
      bgc.g.drawImage(bg, 0, 0, tileW, VH)
      bgc.g.save()
      bgc.g.translate(tileW * 2, 0)
      bgc.g.scale(-1, 1)
      bgc.g.drawImage(bg, 0, 0, tileW, VH)
      bgc.g.restore()
      bgc.g.fillStyle = 'rgba(255,252,254,.66)'
      bgc.g.fillRect(0, 0, tileW * 2, VH)
    } else {
      bgc = mk(VW, VH)
      const gr = bgc.g.createLinearGradient(0, 0, 0, VH)
      gr.addColorStop(0, '#CDECF7')
      gr.addColorStop(1, '#F8CDE3')
      bgc.g.fillStyle = gr
      bgc.g.fillRect(0, 0, VW, VH)
    }
    // chão de nuvens: faixa que repete a cada 46
    const period = 46
    const gw = Math.ceil(VW / period + 3) * period
    const gnd = mk(gw, VH - GROUND + 20)
    const gy = 20 // deslocamento interno
    gnd.g.fillStyle = '#FFFFFF'
    gnd.g.fillRect(0, gy + 12, gw, VH)
    gnd.g.fillStyle = '#F3EAF8'
    for (let x = 0; x <= gw + period; x += period) {
      gnd.g.beginPath()
      gnd.g.arc(x, gy + 18, 26, Math.PI, 0)
      gnd.g.fill()
    }
    gnd.g.fillStyle = '#FFFFFF'
    for (let x = 0; x <= gw + period; x += period) {
      gnd.g.beginPath()
      gnd.g.arc(x + 4, gy + 22, 25, Math.PI, 0)
      gnd.g.fill()
    }
    // tijolinhos: um por cor
    const bricks = BRICK_COLORS.map(([fill, edge]) => {
      const b = mk(BRICK, 30)
      const g = b.g
      roundRect(g, 1, 1, BRICK - 2, 26, 7)
      g.fillStyle = edge
      g.fill()
      roundRect(g, 1, 1, BRICK - 2, 21, 7)
      g.fillStyle = fill
      g.fill()
      g.fillStyle = 'rgba(255,255,255,.65)'
      roundRect(g, 6, 4, BRICK - 14, 4, 2)
      g.fill()
      g.strokeStyle = '#fff'
      g.lineWidth = 2
      roundRect(g, 1, 1, BRICK - 2, 26, 7)
      g.stroke()
      return b
    })
    cache = { bgc, gnd, gy, period, bricks }
  }

  function drawBg() {
    const { bgc } = cache
    const w = bgc.w
    const off = bg ? -((S.dist * 0.3) % w) : 0
    for (let x = off; x < VW; x += w) ctx.drawImage(bgc.c, x, 0, w, bgc.h)
  }

  function drawGround() {
    const { gnd, gy, period } = cache
    const off = -(S.dist % period) - period
    ctx.drawImage(gnd.c, off, GROUND - gy, gnd.w, gnd.h)
  }

  function drawBricks() {
    for (const p of S.plats) {
      const sx = p.x - S.dist
      if (sx > VW + 10 || sx + p.n * BRICK < -10) continue
      for (let i = 0; i < p.n; i++) {
        const b = cache.bricks[(p.c + i) % BRICK_COLORS.length]
        ctx.drawImage(b.c, sx + i * BRICK, p.y, BRICK, 30)
      }
    }
  }

  function drawItems() {
    for (const it of S.items) {
      const sx = it.x - S.dist
      if (sx < -40 || sx > VW + 40) continue
      const bob = Math.sin(S.t * 3 + it.x * 0.05) * 4
      const spr = stars[it.tint]
      ctx.save()
      ctx.translate(sx, it.y + bob)
      if (it.taken) {
        const f = Math.max(0, it.fade)
        ctx.globalAlpha = f
        ctx.scale(1 + (1 - f) * 0.8, 1 + (1 - f) * 0.8)
        ctx.translate(0, -(1 - f) * 30)
      } else {
        ctx.rotate(Math.sin(S.t * 2 + it.x) * 0.12)
      }
      ctx.drawImage(spr.canvas, -spr.size / 2, -spr.size / 2, spr.size, spr.size)
      ctx.restore()
    }
  }

  function drawPlayer() {
    // sombra no chão
    const h = Math.max(0, GROUND - S.y)
    const sh = Math.max(0.35, 1 - h / 260)
    ctx.fillStyle = `rgba(150,100,160,${0.22 * sh})`
    ctx.beginPath()
    ctx.ellipse(S.px, GROUND + 4, 24 * sh, 6 * sh, 0, 0, Math.PI * 2)
    ctx.fill()

    const stretch = S.onGround ? 0 : Math.max(-0.12, Math.min(0.12, -S.vy / 5000))
    const sq = S.squash * 0.16
    const sx = 1 + sq - stretch * 0.6
    const sy = 1 - sq + stretch
    const bounce = S.onGround && !S.done ? Math.abs(Math.sin(S.t * 9)) * 3 : 0 // "corridinha"
    ctx.save()
    ctx.translate(S.px, S.y - bounce)
    ctx.rotate(S.onGround ? Math.sin(S.t * 9) * 0.05 : Math.max(-0.25, Math.min(0.25, S.vy * 0.0004)))
    ctx.scale(sx, sy)
    ctx.drawImage(head, -headW / 2, -HEAD_H, headW, HEAD_H)
    ctx.restore()
  }

  function drawParts() {
    for (const p of S.parts) {
      ctx.globalAlpha = Math.max(0, p.life / 0.7)
      ctx.fillStyle = p.c
      ctx.fillRect(p.x - S.dist - 3, p.y - 3, 6, 6)
    }
    ctx.globalAlpha = 1
  }

  function draw() {
    if (!cache) buildCache()
    ctx.setTransform(dpr * scale, 0, 0, dpr * scale, 0, 0)
    drawBg()
    drawGround()
    drawBricks()
    drawItems()
    drawPlayer()
    drawParts()
  }

  // ---------- loop ----------
  let raf = 0
  let running = false
  let last = 0
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
    jump() {
      if (S.done) return false
      if (S.onGround || S.jumps < 2) {
        S.vy = S.jumps === 0 && S.onGround ? JUMP_V : JUMP2_V
        S.jumps = S.onGround ? 1 : S.jumps + 1
        S.onGround = false
        S.squash = 0
        onJump?.(S.jumps)
        return true
      }
      return false
    },
    reset() {
      reset()
      draw()
    },
    /** troca o personagem (Sophie ou Layla) */
    async setHead(src) {
      head = await loadImg(src)
      headW = (HEAD_H * head.width) / head.height
      draw()
    },
    dispose() {
      running = false
      cancelAnimationFrame(raf)
      ro.disconnect()
    },
  }
}
