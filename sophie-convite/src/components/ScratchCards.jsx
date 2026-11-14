import { m, AnimatePresence } from 'framer-motion'
import { useCallback, useEffect, useRef, useState } from 'react'
import { EVENT, SCRATCH_CARDS } from '../config/event.js'
import { burstFrom } from '../lib/glitter.js'
import { chime, fanfare } from '../lib/sfx.js'
import Reveal from './Reveal.jsx'
import Pattern from './Pattern.jsx'

const fill = (t) => t.replaceAll('{nome}', EVENT.childFirstName)
const REVEAL_AT = 0.5 // 50% raspado → revela tudo

/** Texto da missão desenhado em SVG sobre a arte (escala junto com o cartão) */
function MissionText({ card }) {
  const [x0, y0, x1, y1] = card.textBox
  const bw = (x1 - x0) * card.w
  const bh = (y1 - y0) * card.h
  const lines = card.lines.map(fill)
  const longest = Math.max(...lines.map((l) => l.length))
  const size = Math.min(bh / (lines.length * 1.18), bw / (longest * 0.5))
  const cx = ((x0 + x1) / 2) * card.w
  const top = y0 * card.h + (bh - size * 1.18 * lines.length) / 2 + size * 0.95
  return (
    <svg viewBox={`0 0 ${card.w} ${card.h}`} className="pointer-events-none absolute inset-0 h-full w-full" role="img" aria-label={lines.join(' ')}>
      <text
        x={cx}
        y={top}
        textAnchor="middle"
        fontFamily="Fredoka, ui-rounded, system-ui, sans-serif"
        fontWeight="600"
        fontSize={size}
        fill="#6A1B7C"
        stroke="#fff"
        strokeWidth={size * 0.16}
        strokeLinejoin="round"
        paintOrder="stroke"
      >
        {lines.map((l, i) => (
          <tspan key={i} x={cx} dy={i ? size * 1.18 : 0}>
            {l}
          </tspan>
        ))}
      </text>
    </svg>
  )
}

/** Um cartão: arte + texto + camada preta raspável no formato do cartão */
function ScratchCard({ card, index, revealed, onReveal }) {
  const wrapRef = useRef(null)
  const canvasRef = useRef(null)
  const stateRef = useRef({ total: 0, drawing: false, last: null, checkAt: 0 })

  // desenha a silhueta preta usando a própria arte como máscara
  const paintCover = useCallback(() => {
    const cv = canvasRef.current
    const wrap = wrapRef.current
    if (!cv || !wrap || revealed) return
    const img = new Image()
    img.src = card.img
    img.decode
      ? img.decode().then(draw, () => {})
      : (img.onload = draw)
    function draw() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2)
      const w = wrap.clientWidth
      const h = wrap.clientHeight
      if (!w || !h) return
      cv.width = Math.round(w * dpr)
      cv.height = Math.round(h * dpr)
      const ctx = cv.getContext('2d', { willReadFrequently: true })
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      ctx.globalCompositeOperation = 'source-over'
      ctx.drawImage(img, 0, 0, w, h)
      ctx.globalCompositeOperation = 'source-in'
      const g = ctx.createLinearGradient(0, 0, w, h)
      g.addColorStop(0, '#2A1F33')
      g.addColorStop(0.5, '#120D17')
      g.addColorStop(1, '#2A1F33')
      ctx.fillStyle = g
      ctx.fillRect(0, 0, w, h)
      ctx.globalCompositeOperation = 'source-atop'
      // brilhos dourados
      let seed = index * 97 + 13
      const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647)
      for (let i = 0; i < 70; i++) {
        ctx.fillStyle = `rgba(235,203,133,${0.25 + rnd() * 0.6})`
        const s = 1 + rnd() * 2.2
        ctx.beginPath()
        ctx.arc(rnd() * w, rnd() * h, s, 0, Math.PI * 2)
        ctx.fill()
      }
      ctx.fillStyle = '#EBCB85'
      ctx.textAlign = 'center'
      ctx.font = `600 ${Math.round(w * 0.085)}px Fredoka, system-ui, sans-serif`
      ctx.fillText('✨ Raspe aqui ✨', w / 2, h * 0.53)
      ctx.font = `500 ${Math.round(w * 0.05)}px Fredoka, system-ui, sans-serif`
      ctx.fillStyle = 'rgba(255,255,255,.75)'
      ctx.fillText(`Missão ${index + 1}`, w / 2, h * 0.63)
      ctx.globalCompositeOperation = 'source-over'
      stateRef.current.total = countCovered(ctx, cv)
    }
  }, [card.img, index, revealed])

  useEffect(() => {
    paintCover()
    const ro = new ResizeObserver(() => paintCover())
    if (wrapRef.current) ro.observe(wrapRef.current)
    return () => ro.disconnect()
  }, [paintCover])

  const scratchAt = (x, y) => {
    const cv = canvasRef.current
    const ctx = cv.getContext('2d', { willReadFrequently: true })
    const dpr = cv.width / cv.clientWidth
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
    ctx.globalCompositeOperation = 'destination-out'
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'
    ctx.lineWidth = Math.max(34, cv.clientWidth * 0.11)
    const st = stateRef.current
    ctx.beginPath()
    if (st.last) ctx.moveTo(st.last.x, st.last.y)
    else ctx.moveTo(x - 0.1, y)
    ctx.lineTo(x, y)
    ctx.stroke()
    st.last = { x, y }
    const now = performance.now()
    if (now > st.checkAt) {
      st.checkAt = now + 180
      const left = countCovered(ctx, cv)
      if (st.total && 1 - left / st.total >= REVEAL_AT) onReveal(index)
    }
  }

  const pos = (e) => {
    const r = canvasRef.current.getBoundingClientRect()
    return { x: e.clientX - r.left, y: e.clientY - r.top }
  }
  const down = (e) => {
    if (revealed) return
    e.preventDefault()
    canvasRef.current.setPointerCapture?.(e.pointerId)
    stateRef.current.drawing = true
    stateRef.current.last = null
    const p = pos(e)
    scratchAt(p.x, p.y)
  }
  const move = (e) => {
    if (!stateRef.current.drawing || revealed) return
    e.preventDefault()
    const p = pos(e)
    scratchAt(p.x, p.y)
  }
  const up = () => {
    stateRef.current.drawing = false
    stateRef.current.last = null
  }

  return (
    <div className="w-full shrink-0 px-2">
      <div ref={wrapRef} className="relative mx-auto w-[min(100%,22rem)]" style={{ aspectRatio: `${card.w} / ${card.h}` }}>
        <img src={card.img} alt="" aria-hidden="true" loading="lazy" decoding="async" width={card.w} height={card.h} className="absolute inset-0 h-full w-full drop-shadow-[0_12px_16px_rgba(190,120,170,.3)]" />
        <MissionText card={card} />
        <AnimatePresence>
          {!revealed && (
            <m.canvas
              ref={canvasRef}
              aria-hidden="true"
              className="absolute inset-0 h-full w-full cursor-grab active:cursor-grabbing"
              style={{ touchAction: 'none' }}
              onPointerDown={down}
              onPointerMove={move}
              onPointerUp={up}
              onPointerCancel={up}
              onPointerLeave={up}
              exit={{ opacity: 0, scale: 1.04 }}
              transition={{ duration: 0.5 }}
            />
          )}
        </AnimatePresence>
      </div>
      <div className="mt-3 flex min-h-[44px] items-center justify-center">
        {revealed ? (
          <p className="font-sans text-sm font-semibold text-rosaForte" aria-live="polite">
            Missão revelada! 🎉
          </p>
        ) : (
          <button type="button" onClick={() => onReveal(index)} className="min-h-[44px] px-4 font-sans text-sm font-medium text-ameixaSoft underline decoration-rosaForte/60 underline-offset-4">
            Revelar sem raspar
          </button>
        )}
      </div>
    </div>
  )
}

/** conta pixels ainda cobertos (amostragem a cada 6 px para ser rápido) */
function countCovered(ctx, cv) {
  const { data } = ctx.getImageData(0, 0, cv.width, cv.height)
  const step = 6
  let n = 0
  for (let y = 0; y < cv.height; y += step) {
    const row = y * cv.width * 4
    for (let x = 0; x < cv.width; x += step) if (data[row + x * 4 + 3] > 100) n++
  }
  return n
}

export default function ScratchCards() {
  const cards = SCRATCH_CARDS.enabled ? SCRATCH_CARDS.cards : []
  const [i, setI] = useState(0)
  const [revealed, setRevealed] = useState(() => cards.map(() => false))
  const trackRef = useRef(null)
  if (!cards.length) return null
  const count = revealed.filter(Boolean).length

  const reveal = (k) => {
    setRevealed((r) => {
      if (r[k]) return r
      const next = r.map((v, j) => (j === k ? true : v))
      const n = next.filter(Boolean).length
      setTimeout(() => {
        n === cards.length ? fanfare() : chime(n)
        burstFrom(trackRef.current, { count: n === cards.length ? 140 : 70, speed: 10 })
        navigator.vibrate?.(20)
      }, 0)
      return next
    })
  }
  const go = (d) => setI((v) => (v + d + cards.length) % cards.length)

  return (
    <section id="raspadinhas" aria-labelledby="rasp-titulo" className="relative overflow-hidden bg-gradient-to-b from-amarelo/60 via-[#FFF6FA] to-rosa/70 px-4 py-14">
      <Pattern opacity={0.2} />
      <div className="relative mx-auto max-w-md text-center">
        <Reveal>
          <h2 id="rasp-titulo" className="font-bubble bubble-pink text-[clamp(1.75rem,8vw,2.4rem)] leading-tight">
            {SCRATCH_CARDS.title}
          </h2>
          <p className="mx-auto mt-1 max-w-[30ch] font-sans text-base text-ameixa">{fill(SCRATCH_CARDS.subtitle)}</p>
        </Reveal>

        <div className="mt-5 overflow-hidden" ref={trackRef}>
          <m.div className="flex" animate={{ x: `${-i * 100}%` }} transition={{ type: 'spring', stiffness: 260, damping: 30 }}>
            {cards.map((c, k) => (
              <div key={c.img} className="w-full shrink-0" aria-hidden={k !== i} inert={k !== i ? '' : undefined}>
                <ScratchCard card={c} index={k} revealed={revealed[k]} onReveal={reveal} />
              </div>
            ))}
          </m.div>
        </div>

        {/* navegação */}
        <div className="mt-1 flex items-center justify-center gap-1.5">
          <button type="button" onClick={() => go(-1)} className="stepper-btn shrink-0 !bg-white/90 shadow-soft" aria-label="Raspadinha anterior">
            ‹
          </button>
          <div className="flex gap-1.5" role="tablist" aria-label="Escolher raspadinha">
            {cards.map((_, k) => (
              <button
                key={k}
                type="button"
                role="tab"
                aria-selected={k === i}
                aria-label={`Raspadinha ${k + 1}${revealed[k] ? ' (revelada)' : ''}`}
                onClick={() => setI(k)}
                className="grid h-11 w-8 place-items-center"
              >
                <span className={`block h-3 rounded-full transition-all ${k === i ? 'w-6 bg-rosaForte' : revealed[k] ? 'w-3 bg-dourado' : 'w-3 bg-white ring-1 ring-rosa'}`} />
              </button>
            ))}
          </div>
          <button type="button" onClick={() => go(1)} className="stepper-btn shrink-0 !bg-white/90 shadow-soft" aria-label="Próxima raspadinha">
            ›
          </button>
        </div>
        <p className="mt-2 font-sans text-sm text-ameixaSoft" role="status">
          {count}/{cards.length} missões reveladas
        </p>
        <p className="mx-auto mt-3 max-w-[32ch] rounded-2xl bg-white/80 px-4 py-3 font-sans text-base font-medium text-ameixa shadow-soft">{fill(SCRATCH_CARDS.hint)}</p>
      </div>
    </section>
  )
}
