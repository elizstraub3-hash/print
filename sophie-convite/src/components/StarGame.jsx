import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useState } from 'react'
import { EVENT } from '../config/event.js'
import { Cloud, CloudEdge } from './Decor.jsx'
import Particles from './Particles.jsx'
import Pattern from './Pattern.jsx'

// posições em % dentro do "céu" — afastadas das bordas e entre si
const STARS = [
  { left: 16, top: 20, peek: 'right' },
  { left: 72, top: 13, peek: 'left' },
  { left: 46, top: 47, peek: 'bottom' },
  { left: 82, top: 64, peek: 'left' },
  { left: 20, top: 77, peek: 'right' },
]

const CLOUDS = [
  { left: 24, top: 16, w: 34 },
  { left: 52, top: 6, w: 30 },
  { left: 34, top: 50, w: 36 },
  { left: 60, top: 62, w: 30 },
  { left: 2, top: 70, w: 34 },
  { left: 66, top: 34, w: 26 },
  { left: -6, top: 38, w: 26 },
]

function StarShape({ found }) {
  return (
    <svg viewBox="0 0 48 48" className="h-full w-full" aria-hidden="true">
      <defs>
        <linearGradient id="sg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#FFF6D6" />
          <stop offset="1" stopColor="#E6BE68" />
        </linearGradient>
      </defs>
      <path
        d="M24 4 L29.5 17 L43.5 18.2 L32.8 27.4 L36 41.2 L24 33.8 L12 41.2 L15.2 27.4 L4.5 18.2 L18.5 17 Z"
        fill={found ? 'url(#sg)' : '#FFF9E4'}
        stroke={found ? '#D2A34F' : '#EBCB85'}
        strokeWidth="2.5"
        strokeLinejoin="round"
      />
      {found ? (
        <path d="M17 24 L22 29 L31 19" stroke="#fff" strokeWidth="3.2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      ) : (
        <>
          <circle cx="19" cy="23" r="1.8" fill="#6B4E71" />
          <circle cx="29" cy="23" r="1.8" fill="#6B4E71" />
          <path d="M21 28 Q24 30.5 27 28" stroke="#6B4E71" strokeWidth="1.8" fill="none" strokeLinecap="round" />
        </>
      )}
    </svg>
  )
}

export default function StarGame({ onFinish }) {
  const reduce = useReducedMotion()
  const [found, setFound] = useState([])
  const [lastFound, setLastFound] = useState(null)
  const total = STARS.length
  const done = found.length === total

  const catchStar = (i) => {
    if (found.includes(i)) return
    setFound((f) => [...f, i])
    setLastFound(i)
    if (navigator.vibrate) navigator.vibrate(18)
  }

  return (
    <section
      id="jogo"
      aria-labelledby="jogo-titulo"
      className="relative overflow-hidden bg-gradient-to-b from-rosa via-[#EADCF8] to-azul px-5 py-16"
    >
      <Pattern opacity={0.2} />
      <div className="relative mx-auto max-w-md text-center">
        <p className="font-sans text-xs font-semibold uppercase tracking-[0.3em] text-ameixaSoft">Mini jogo mágico</p>
        <h2 id="jogo-titulo" className="mt-2 font-sans text-[clamp(1.5rem,6.4vw,2rem)] font-semibold leading-tight text-ameixa">
          Encontre as 5 estrelinhas mágicas
        </h2>
        <p className="mt-2 font-sans text-base text-ameixaSoft">Elas estão escondidas entre as nuvens. Toque em cada uma!</p>

        {/* contador */}
        <div className="mt-5 flex items-center justify-center gap-3">
          <div className="flex gap-1.5" aria-hidden="true">
            {STARS.map((_, i) => (
              <span
                key={i}
                className={`h-2.5 w-6 rounded-full transition-colors duration-500 ${i < found.length ? 'bg-dourado' : 'bg-white/80'}`}
              />
            ))}
          </div>
          <m.span
            key={found.length}
            initial={reduce ? false : { scale: 1.4 }}
            animate={{ scale: 1 }}
            className="min-w-[3.5rem] rounded-full bg-white/85 px-3 py-1 font-sans text-lg font-semibold tabular-nums text-ameixa shadow-soft"
            role="status"
            aria-live="polite"
            aria-label={`${found.length} de ${total} estrelinhas encontradas`}
          >
            {found.length}/{total}
          </m.span>
        </div>

        {/* céu do jogo */}
        <div className="relative mx-auto mt-6 aspect-[4/5] w-full max-w-sm overflow-hidden rounded-[2rem] bg-gradient-to-b from-[#BFE4F4] via-[#E3DBFA] to-[#FBE0EE] shadow-soft ring-4 ring-white/70">
          {CLOUDS.map((c, i) => (
            <m.div
              key={i}
              aria-hidden="true"
              className="pointer-events-none absolute z-20"
              style={{ left: `${c.left}%`, top: `${c.top}%`, width: `${c.w}%` }}
              animate={reduce ? undefined : { x: [0, i % 2 ? -8 : 8, 0] }}
              transition={{ duration: 6 + i, repeat: Infinity, ease: 'easeInOut' }}
            >
              <Cloud className="h-auto w-full drop-shadow-sm" />
            </m.div>
          ))}

          {STARS.map((s, i) => {
            const isFound = found.includes(i)
            return (
              <m.button
                key={i}
                type="button"
                onClick={() => catchStar(i)}
                disabled={isFound}
                aria-label={isFound ? `Estrelinha ${i + 1} encontrada` : `Estrelinha mágica ${i + 1}`}
                aria-pressed={isFound}
                className="star-btn absolute z-10 grid h-16 w-16 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full"
                style={{ left: `${s.left}%`, top: `${s.top}%`, zIndex: isFound ? 30 : 10 }}
                animate={
                  isFound
                    ? { scale: reduce ? 1 : [1, 1.5, 1.1], rotate: reduce ? 0 : 360 }
                    : reduce
                    ? undefined
                    : { scale: [1, 1.08, 1], rotate: [-6, 6, -6] }
                }
                transition={isFound ? { duration: 0.6 } : { duration: 2 + i * 0.3, repeat: Infinity, ease: 'easeInOut' }}
                whileTap={{ scale: 0.9 }}
              >
                <span className={`block h-12 w-12 ${isFound ? 'drop-shadow-[0_0_12px_rgba(235,203,133,.95)]' : ''}`}>
                  <StarShape found={isFound} />
                </span>
                <AnimatePresence>{lastFound === i && !reduce && <Particles key={found.length} count={12} radius={70} duration={0.8} />}</AnimatePresence>
              </m.button>
            )
          })}

          {/* conclusão */}
          <AnimatePresence>
            {done && (
              <m.div
                className="absolute inset-0 z-40 flex items-center justify-center bg-white/55 p-5 backdrop-blur-[3px]"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
              >
                <m.div
                  className="relative w-full rounded-3xl bg-white/95 px-5 py-7 shadow-soft ring-1 ring-rosa"
                  initial={{ scale: 0.8, y: 20 }}
                  animate={{ scale: 1, y: 0 }}
                  transition={{ type: 'spring', stiffness: 220, damping: 16, delay: 0.5 }}
                  role="alert"
                >
                  {!reduce && <Particles count={22} radius={170} />}
                  <p className="text-4xl" aria-hidden="true">🌟</p>
                  <p className="mt-2 font-script text-3xl font-bold text-rosaForte">Parabéns!</p>
                  <p className="mt-1 font-sans text-lg font-medium leading-snug text-ameixa">
                    Você encontrou a magia da {EVENT.childFirstName}!
                  </p>
                  <button type="button" onClick={onFinish} className="btn-magic mt-5 min-h-[52px] px-7">
                    Descobrir a festa <span aria-hidden="true">→</span>
                  </button>
                </m.div>
              </m.div>
            )}
          </AnimatePresence>
        </div>

        {!done && (
          <button type="button" onClick={onFinish} className="btn-ghost mt-6 min-h-[48px] px-6">
            Pular jogo e ver o convite
          </button>
        )}
      </div>
      <CloudEdge fill="#FFFAFC" />
    </section>
  )
}
