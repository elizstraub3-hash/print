import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useRef, useState } from 'react'
import { EVENT, CAKE } from '../config/event.js'
import { burstFrom, rain } from '../lib/glitter.js'
import { chime, fanfare, sparkle } from '../lib/sfx.js'
import useShake from '../lib/useShake.js'

/** Velinha listrada com chama animada */
function Candle({ lit, hue }) {
  return (
    <svg viewBox="0 0 40 120" className="h-full w-full overflow-visible" aria-hidden="true">
      <defs>
        <pattern id={`cd-st-${hue}`} width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)">
          <rect width="14" height="14" fill="#FFF6FB" />
          <rect width="7" height="14" fill={hue} />
        </pattern>
        <radialGradient id="cd-glow">
          <stop offset="0" stopColor="#FFF3B0" stopOpacity=".9" />
          <stop offset="1" stopColor="#FFE58F" stopOpacity="0" />
        </radialGradient>
        <linearGradient id="cd-flame" x1="0" y1="1" x2="0" y2="0">
          <stop offset="0" stopColor="#FF9F43" />
          <stop offset=".45" stopColor="#FFD166" />
          <stop offset="1" stopColor="#FFF8D6" />
        </linearGradient>
      </defs>
      <rect x="11" y="46" width="18" height="72" rx="5" fill={`url(#cd-st-${hue})`} stroke="#fff" strokeWidth="2" />
      <rect x="13" y="48" width="4" height="66" rx="2" fill="#fff" opacity=".6" />
      <path d="M20 46 V36" stroke="#5E4466" strokeWidth="2" strokeLinecap="round" />
      {lit && (
        <g className="candle-flame" style={{ transformOrigin: '20px 36px' }}>
          <circle cx="20" cy="22" r="24" fill="url(#cd-glow)" />
          <path d="M20 4 C27 16 28 26 20 36 C12 26 13 16 20 4 Z" fill="url(#cd-flame)" />
          <path d="M20 18 C23 24 23 29 20 33 C17 29 17 24 20 18 Z" fill="#fff" opacity=".85" />
        </g>
      )}
    </svg>
  )
}

/** fumacinha: 3 bolinhas que sobem ondulando */
function Smoke() {
  return (
    <span className="pointer-events-none absolute left-1/2 top-[8%] -translate-x-1/2" aria-hidden="true">
      {[0, 1, 2].map((i) => (
        <m.span
          key={i}
          className="absolute h-5 w-5 -translate-x-1/2 rounded-full bg-[radial-gradient(circle,rgba(170,160,180,.7),rgba(170,160,180,0)_70%)]"
          initial={{ opacity: 0.85, y: 0, x: 0, scale: 0.5 }}
          animate={{ opacity: 0, y: -70 - i * 14, x: [0, 8, -8, 4], scale: 2.2 }}
          transition={{ duration: 1.8, delay: i * 0.18, ease: 'easeOut' }}
        />
      ))}
    </span>
  )
}

const HUES = ['#F7A8CF', '#C9B5F2', '#A9DCF2', '#FFE58F', '#B9EBD2']

export default function CakeStage() {
  const reduce = useReducedMotion()
  const stageRef = useRef(null)
  const cakeRef = useRef(null)
  const candleRefs = useRef([])
  const [lit, setLit] = useState(() => CAKE.candles.map(() => true))
  const [tilt, setTilt] = useState({ x: 0, y: 0 })
  const litCount = lit.filter(Boolean).length
  const allOut = litCount === 0

  const litRef = useRef(lit)
  litRef.current = lit

  const blowOne = (k) => {
    const L = litRef.current
    if (k == null) {
      const on = L.map((v, i) => (v ? i : -1)).filter((i) => i >= 0)
      if (!on.length) return
      k = on[Math.floor(Math.random() * on.length)]
    }
    if (!L[k]) return
    const next = L.map((v, i) => (i === k ? false : v))
    litRef.current = next // chacoalhadas rápidas não apagam a mesma velinha
    setLit(next)
    const left = next.filter(Boolean).length
    navigator.vibrate?.(left ? 25 : [30, 40, 60])
    if (left) {
      chime(CAKE.candles.length - left)
      burstFrom(candleRefs.current[k], { count: 18, speed: 4, size: [2, 4], life: [30, 50] })
    } else {
      fanfare()
      burstFrom(cakeRef.current, { count: 130, speed: 11 })
      rain({ count: 200, duration: 1300 })
      shake.disable()
    }
  }

  const shake = useShake(() => blowOne())

  const relight = () => {
    sparkle()
    setLit(CAKE.candles.map(() => true))
  }

  const onMove = (e) => {
    if (reduce || e.pointerType === 'touch') return
    const r = stageRef.current.getBoundingClientRect()
    setTilt({ x: ((e.clientY - r.top) / r.height - 0.5) * -6, y: ((e.clientX - r.left) / r.width - 0.5) * 14 })
  }

  return (
    <div className="relative mx-auto w-[min(100%,22rem)]">
      <p className="mb-3 font-script text-[clamp(1.9rem,8.5vw,2.4rem)] font-bold leading-tight text-rosaForte">Venha soprar as velinhas comigo!</p>

      <div ref={stageRef} onPointerMove={onMove} onPointerLeave={() => setTilt({ x: 0, y: 0 })} className="relative" style={{ perspective: '900px' }}>
        <m.div
          className="relative"
          style={{ transformStyle: 'preserve-3d' }}
          animate={reduce ? undefined : { rotateX: tilt.x, rotateY: tilt.y }}
          transition={{ type: 'spring', stiffness: 120, damping: 18 }}
        >
          {/* mesa redonda com toalha */}
          <div className="absolute inset-x-[-6%] bottom-[-2%] h-[28%]" aria-hidden="true">
            <div className="absolute inset-x-[3%] bottom-0 top-[42%] rounded-b-[46%] bg-gradient-to-b from-[#FCE4F0] to-[#F5C6DE] shadow-[0_18px_30px_-14px_rgba(160,90,140,.55)]">
              <div className="absolute inset-x-0 bottom-[-6px] h-4 bg-[radial-gradient(circle_at_50%_0,#F5C6DE_62%,transparent_64%)] bg-[length:22px_16px] bg-repeat-x" />
              <div className="absolute inset-x-[4%] top-[18%] h-[3px] rounded-full bg-gradient-to-r from-transparent via-dourado to-transparent opacity-80" />
            </div>
            <div className="absolute inset-x-0 top-0 h-[62%] rounded-[50%] bg-[radial-gradient(ellipse_at_50%_40%,#FFFFFF_0%,#FFF4FA_45%,#F8D7E8_100%)] ring-2 ring-white" />
            <div className="absolute inset-x-[2%] top-[4%] h-[56%] rounded-[50%] border-2 border-dashed border-dourado/50" />
          </div>
          <div className="absolute bottom-[9%] left-1/2 h-[6%] w-[72%] -translate-x-1/2 rounded-[50%] bg-[radial-gradient(ellipse,rgba(120,60,110,.38),transparent_70%)]" aria-hidden="true" />

          {/* bolo */}
          <div ref={cakeRef} className="relative mx-auto w-[84%] pb-[13%]" style={{ transform: 'translateZ(30px)' }}>
            <div className="relative" style={{ aspectRatio: `${CAKE.w} / ${CAKE.h}` }}>
              <img src={CAKE.src} alt={CAKE.alt} width={CAKE.w} height={CAKE.h} loading="lazy" decoding="async" className="absolute inset-0 h-full w-full drop-shadow-[0_10px_10px_rgba(120,60,110,.25)]" />
              {CAKE.candles.map(([x, y], k) => (
                <button
                  key={k}
                  ref={(el) => (candleRefs.current[k] = el)}
                  type="button"
                  onClick={() => (lit[k] ? blowOne(k) : allOut && relight())}
                  aria-label={lit[k] ? `Assoprar a velinha ${k + 1}` : `Velinha ${k + 1} apagada`}
                  className="absolute z-10 h-[15%] w-[8%] -translate-x-1/2 -translate-y-full before:absolute before:-inset-x-3 before:-inset-y-1 before:content-['']"
                  style={{ left: `${x * 100}%`, top: `${y * 100}%`, touchAction: 'manipulation' }}
                >
                  <Candle lit={lit[k]} hue={HUES[k % HUES.length]} />
                  <AnimatePresence>{!lit[k] && !reduce && <Smoke key="s" />}</AnimatePresence>
                </button>
              ))}
            </div>
          </div>
        </m.div>
      </div>

      {/* instruções / estado */}
      <div className="mt-3 text-center" aria-live="polite">
        <>
          {allOut ? (
            <m.div key="done" initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }}>
              <p className="font-script text-4xl font-bold text-rosaForte">Parabéns, {EVENT.childFirstName}! 🎉</p>
              <button type="button" onClick={relight} className="mt-2 min-h-[44px] px-4 font-sans text-sm font-medium text-ameixaSoft underline underline-offset-4">
                Acender as velinhas de novo
              </button>
            </m.div>
          ) : shake.status === 'listening' ? (
            <m.div key="shake" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <m.p
                className="font-sans text-lg font-semibold text-ameixa"
                animate={reduce ? undefined : { rotate: [-4, 4, -4] }}
                transition={{ duration: 0.4, repeat: Infinity }}
              >
                📳 Chacoalhe o celular!
              </m.p>
              <p className="font-sans text-sm text-ameixaSoft">
                Faltam {litCount} {litCount === 1 ? 'velinha' : 'velinhas'}
              </p>
            </m.div>
          ) : (
            <m.div key="start" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              {shake.status === 'idle' && (
                <button type="button" onClick={shake.enable} className="btn-magic min-h-[56px] px-7 text-lg">
                  📳 Chacoalhar o celular
                </button>
              )}
              <p className="mt-2 font-sans text-sm text-ameixaSoft">
                {shake.status === 'idle'
                  ? 'Toque no botão e chacoalhe — ou toque em cada velinha.'
                  : shake.status === 'denied'
                  ? 'Sem acesso ao movimento do celular: toque em cada velinha para assoprar.'
                  : 'Toque em cada velinha para assoprar!'}
              </p>
            </m.div>
          )}
        </>
      </div>
    </div>
  )
}
