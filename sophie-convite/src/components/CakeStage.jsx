import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useRef, useState } from 'react'
import { EVENT, CAKE } from '../config/event.js'
import { burstFrom, rain } from '../lib/glitter.js'
import { fanfare, sparkle } from '../lib/sfx.js'

const fill = (t) => t.replaceAll('{nome}', EVENT.childFirstName)

/** Plaquinha do topo redesenhada com o nome certo (cobre a original) */
function Topper() {
  const [x0, y0, x1, y1] = CAKE.topper.box
  const [kx, ky] = CAKE.topper.keepClear // canto inferior direito livre (o "5" fica na frente)
  const cx = (x0 + x1) / 2
  const name = fill(CAKE.topper.name)
  const size = Math.min(150, ((x1 - x0) * 0.86) / (name.length * 0.5))
  return (
    <svg viewBox={`0 0 ${CAKE.w} ${CAKE.h}`} className="pointer-events-none absolute inset-0 h-full w-full" aria-hidden="true">
      <defs>
        <clipPath id="tp-clip">
          <path d={`M0 0 H${CAKE.w} V${ky} H${kx} V${CAKE.h} H0 Z`} />
        </clipPath>
        <linearGradient id="tp-name" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#D9A8F0" />
          <stop offset=".55" stopColor="#B57BDD" />
          <stop offset="1" stopColor="#9452C4" />
        </linearGradient>
        <linearGradient id="tp-gold" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#FFF1B9" />
          <stop offset=".5" stopColor="#E3B65C" />
          <stop offset="1" stopColor="#B88832" />
        </linearGradient>
        <radialGradient id="tp-cream" cx=".45" cy=".35" r=".8">
          <stop offset="0" stopColor="#FFFFFF" />
          <stop offset="1" stopColor="#F7EEE6" />
        </radialGradient>
      </defs>
      <g clipPath="url(#tp-clip)">
        {/* nuvem da plaquinha */}
        <g fill="url(#tp-cream)" stroke="url(#tp-gold)" strokeWidth="9" strokeLinejoin="round">
          <path
            d={`M${x0 + 40} ${y1 - 4}
              C${x0 - 6} ${y1 - 8} ${x0 - 8} ${y0 + 120} ${x0 + 34} ${y0 + 104}
              C${x0 + 20} ${y0 + 44} ${x0 + 96} ${y0 + 20} ${x0 + 140} ${y0 + 52}
              C${x0 + 170} ${y0 + 4} ${cx + 10} ${y0 - 4} ${cx + 30} ${y0 + 40}
              C${cx + 70} ${y0 + 10} ${x1 - 70} ${y0 + 26} ${x1 - 74} ${y0 + 82}
              C${x1 - 20} ${y0 + 80} ${x1 + 4} ${y0 + 150} ${x1 - 30} ${y0 + 178}
              C${x1 - 10} ${y1 - 10} ${x1 - 90} ${y1 + 6} ${x1 - 120} ${y1 - 20}
              C${cx + 40} ${y1 + 8} ${cx - 60} ${y1 + 6} ${cx - 90} ${y1 - 14}
              C${x0 + 120} ${y1 + 10} ${x0 + 70} ${y1 + 6} ${x0 + 40} ${y1 - 4} Z`}
          />
        </g>
        <path
          d={`M${x0 + 52} ${y1 - 22} C${x0 + 20} ${y1 - 30} ${x0 + 22} ${y0 + 128} ${x0 + 52} ${y0 + 118}`}
          stroke="#fff"
          strokeWidth="5"
          fill="none"
          strokeLinecap="round"
          opacity=".9"
        />
        {/* nome */}
        <text
          x={cx}
          y={y0 + 150}
          textAnchor="middle"
          fontFamily='"Dancing Script", cursive'
          fontWeight="700"
          fontSize={size}
          fill="url(#tp-name)"
          stroke="#fff"
          strokeWidth="12"
          strokeLinejoin="round"
          paintOrder="stroke"
        >
          {name}
        </text>
        <text x={cx} y={y0 + 150} textAnchor="middle" fontFamily='"Dancing Script", cursive' fontWeight="700" fontSize={size} fill="none" stroke="#7E3DAF" strokeWidth="2" opacity=".55">
          {name}
        </text>
        {/* coraçãozinho dourado */}
        <path
          transform={`translate(${cx - 16} ${y1 - 52}) scale(1.4)`}
          d="M12 21C5 15 1 11.5 1 7C1 3.5 3.7 1 7 1C9.2 1 11 2.2 12 4C13 2.2 14.8 1 17 1C20.3 1 23 3.5 23 7C23 11.5 19 15 12 21Z"
          fill="url(#tp-gold)"
          stroke="#fff"
          strokeWidth="1.5"
        />
      </g>
    </svg>
  )
}

/** Velinha listrada com chama animada */
function Candle({ lit }) {
  return (
    <svg viewBox="0 0 40 120" className="h-full w-full overflow-visible" aria-hidden="true">
      <defs>
        <pattern id="cd-stripes" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)">
          <rect width="14" height="14" fill="#FFF6FB" />
          <rect width="7" height="14" fill="#F7A8CF" />
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
      <rect x="11" y="46" width="18" height="72" rx="5" fill="url(#cd-stripes)" stroke="#E58DB8" strokeWidth="1.5" />
      <rect x="13" y="48" width="4" height="66" rx="2" fill="#fff" opacity=".6" />
      <path d="M20 46 V36" stroke="#5E4466" strokeWidth="2" strokeLinecap="round" />
      {lit && (
        <g className="candle-flame" style={{ transformOrigin: '20px 36px' }}>
          <circle cx="20" cy="22" r="22" fill="url(#cd-glow)" />
          <path d="M20 4 C27 16 28 26 20 36 C12 26 13 16 20 4 Z" fill="url(#cd-flame)" />
          <path d="M20 18 C23 24 23 29 20 33 C17 29 17 24 20 18 Z" fill="#fff" opacity=".85" />
        </g>
      )}
    </svg>
  )
}

export default function CakeStage() {
  const reduce = useReducedMotion()
  const stageRef = useRef(null)
  const cakeRef = useRef(null)
  const [lit, setLit] = useState(true)
  const [tilt, setTilt] = useState({ x: 0, y: 0 })

  const onMove = (e) => {
    if (reduce) return
    const r = stageRef.current.getBoundingClientRect()
    const px = (e.clientX - r.left) / r.width - 0.5
    const py = (e.clientY - r.top) / r.height - 0.5
    setTilt({ x: py * -6, y: px * 14 })
  }

  const blow = () => {
    if (lit) {
      setLit(false)
      fanfare()
      burstFrom(cakeRef.current, { count: 120, speed: 11 })
      rain({ count: 160, duration: 1200 })
      navigator.vibrate?.([30, 40, 30])
    } else {
      setLit(true)
      sparkle()
    }
  }

  return (
    <div className="relative mx-auto w-[min(100%,22rem)]">
      <div
        ref={stageRef}
        onPointerMove={onMove}
        onPointerLeave={() => setTilt({ x: 0, y: 0 })}
        className="relative"
        style={{ perspective: '900px' }}
      >
        <m.div
          className="relative"
          style={{ transformStyle: 'preserve-3d' }}
          animate={{ rotateX: tilt.x, rotateY: tilt.y }}
          transition={{ type: 'spring', stiffness: 120, damping: 18 }}
        >
          {/* mesa redonda com toalha */}
          <div className="absolute inset-x-[-6%] bottom-[-2%] h-[30%]" style={{ transformStyle: 'preserve-3d' }} aria-hidden="true">
            {/* saia da toalha (frente) */}
            <div className="absolute inset-x-[3%] bottom-0 top-[42%] rounded-b-[46%] bg-gradient-to-b from-[#FCE4F0] to-[#F5C6DE] shadow-[0_18px_30px_-14px_rgba(160,90,140,.55)]">
              <div className="absolute inset-x-0 bottom-[-6px] h-4 bg-[radial-gradient(circle_at_50%_0,#F5C6DE_62%,transparent_64%)] bg-[length:22px_16px] bg-repeat-x" />
              <div className="absolute inset-x-[4%] top-[18%] h-[3px] rounded-full bg-gradient-to-r from-transparent via-dourado to-transparent opacity-80" />
            </div>
            {/* tampo (elipse em perspectiva) */}
            <div className="absolute inset-x-0 top-0 h-[62%] rounded-[50%] bg-[radial-gradient(ellipse_at_50%_40%,#FFFFFF_0%,#FFF4FA_45%,#F8D7E8_100%)] ring-2 ring-white" style={{ transform: 'translateZ(0)' }} />
            <div className="absolute inset-x-[2%] top-[4%] h-[56%] rounded-[50%] border-2 border-dashed border-dourado/50" />
          </div>

          {/* sombra de contato */}
          <div className="absolute bottom-[10%] left-1/2 h-[6%] w-[70%] -translate-x-1/2 rounded-[50%] bg-[radial-gradient(ellipse,rgba(120,60,110,.38),transparent_70%)]" aria-hidden="true" />

          {/* bolo */}
          <div ref={cakeRef} className="relative mx-auto w-[82%] pb-[14%]" style={{ transform: 'translateZ(30px)' }}>
            <div className="relative" style={{ aspectRatio: `${CAKE.w} / ${CAKE.h}` }}>
              <img src={CAKE.src} alt={fill(CAKE.alt)} width={CAKE.w} height={CAKE.h} loading="lazy" decoding="async" className="absolute inset-0 h-full w-full drop-shadow-[0_10px_10px_rgba(120,60,110,.25)]" />
              {CAKE.topper && <Topper />}
              {/* velinha */}
              <button
                type="button"
                onClick={blow}
                aria-label={lit ? `Assoprar a velinha da ${EVENT.childFirstName}` : 'Acender a velinha de novo'}
                aria-pressed={!lit}
                className="absolute z-10 h-[24%] w-[13%] -translate-x-1/2 -translate-y-full rounded-full before:absolute before:-inset-x-4 before:-inset-y-2 before:content-['']"
                style={{ left: `${CAKE.candle.x * 100}%`, top: `${CAKE.candle.y * 100}%`, touchAction: 'manipulation' }}
              >
                <Candle lit={lit} />
                <AnimatePresence>
                  {!lit && !reduce && (
                    <m.span
                      key="smoke"
                      className="pointer-events-none absolute left-1/2 top-0 h-10 w-6 -translate-x-1/2 rounded-full bg-[radial-gradient(circle,rgba(160,150,170,.55),transparent_70%)]"
                      initial={{ opacity: 0.9, y: 0, scale: 0.6 }}
                      animate={{ opacity: 0, y: -50, scale: 1.8 }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 1.6 }}
                    />
                  )}
                </AnimatePresence>
              </button>
            </div>
          </div>
        </m.div>
      </div>

      <div className="mt-2 text-center" aria-live="polite">
        <AnimatePresence mode="wait">
          {lit ? (
            <m.p key="a" className="font-sans text-base font-semibold text-ameixa" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              Toque na velinha para assoprar! 🕯️
            </m.p>
          ) : (
            <m.p key="b" className="font-script text-3xl font-bold text-rosaForte" initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}>
              Parabéns, {EVENT.childFirstName}! 🎉
            </m.p>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
