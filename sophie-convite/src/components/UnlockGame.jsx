import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useCallback, useEffect, useRef, useState } from 'react'
import { EVENT, CHILD_IMAGES, BACKGROUNDS } from '../config/event.js'
import { chime, fanfare, sparkle } from '../lib/sfx.js'
import { burst, burstFrom, rain } from '../lib/glitter.js'
import { DriftCloud } from './Decor.jsx'
import Pattern from './Pattern.jsx'

const GOAL = 5
const TINTS = ['#D9B8FF', '#A9DCF2', '#FFE58F', '#B9EBD2', '#FFC9A8']
const HEAD = CHILD_IMAGES.gameHead || '/img/unicornio-3d.webp'
const BG = BACKGROUNDS.game

export function PuffyStar({ tint, id, face = true }) {
  const g = `ps-${id}`
  return (
    <svg viewBox="0 0 100 100" className="h-full w-full overflow-visible" aria-hidden="true">
      <defs>
        <radialGradient id={`${g}-b`} cx="38%" cy="30%" r="80%">
          <stop offset="0" stopColor="#FFE6F3" />
          <stop offset=".45" stopColor="#F7A8CF" />
          <stop offset="1" stopColor={tint} />
        </radialGradient>
        <linearGradient id={`${g}-s`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#FFFFFF" stopOpacity=".95" />
          <stop offset="1" stopColor="#FFFFFF" stopOpacity="0" />
        </linearGradient>
      </defs>
      {/* sombra */}
      <ellipse cx="50" cy="94" rx="26" ry="4" fill="#B98BB4" opacity=".25" />
      <path
        d="M50 6 C54 6 56 9 58 14 L65 30 C66 33 68 34 71 34.5 L88 37 C96 38 98 45 92 50 L80 62 C78 64 77 66 77.5 69 L80.5 86 C82 94 75 98 68 94 L53 86 C51 85 49 85 47 86 L32 94 C25 98 18 94 19.5 86 L22.5 69 C23 66 22 64 20 62 L8 50 C2 45 4 38 12 37 L29 34.5 C32 34 34 33 35 30 L42 14 C44 9 46 6 50 6 Z"
        fill={`url(#${g}-b)`}
        stroke="#fff"
        strokeWidth="3"
      />
      {/* brilho de volume */}
      <path d="M40 18 C44 12 50 12 48 20 L44 30 C41 36 33 37 31 40 C29 36 35 27 40 18 Z" fill={`url(#${g}-s)`} />
      {/* glitter */}
      {[[62, 44, 1.6], [36, 58, 1.3], [58, 70, 1.1], [70, 56, 1.4], [44, 46, 1]].map(([x, y, r], i) => (
        <circle key={i} cx={x} cy={y} r={r} fill="#fff" opacity=".9" />
      ))}
      {face && (
        <g stroke="#6B4E71" strokeWidth="2.4" fill="none" strokeLinecap="round">
          <path d="M39 52 Q42.5 55.5 46 52" />
          <path d="M54 52 Q57.5 55.5 61 52" />
          <path d="M46 60 Q50 63.5 54 60" />
        </g>
      )}
      {face && (
        <>
          <ellipse cx="36" cy="59" rx="4" ry="2.4" fill="#F27DB2" opacity=".45" />
          <ellipse cx="64" cy="59" rx="4" ry="2.4" fill="#F27DB2" opacity=".45" />
        </>
      )}
    </svg>
  )
}

/** Cadeado-coração que vai se enchendo de estrelinhas */
function HeartLock({ filled, total, open }) {
  return (
    <svg viewBox="0 0 120 130" className="h-full w-full overflow-visible" aria-hidden="true">
      <defs>
        <linearGradient id="lk-b" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#FFF4FA" />
          <stop offset="1" stopColor="#F5C6DE" />
        </linearGradient>
        <linearGradient id="lk-g" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#FFF1B9" />
          <stop offset="1" stopColor="#D2A24E" />
        </linearGradient>
        <clipPath id="lk-clip">
          <path d="M60 122 C24 98 8 80 8 58 C8 42 20 32 34 32 C45 32 54 38 60 48 C66 38 75 32 86 32 C100 32 112 42 112 58 C112 80 96 98 60 122 Z" />
        </clipPath>
      </defs>
      {/* argola */}
      <m.path
        d="M38 46 V30 C38 16 48 8 60 8 C72 8 82 16 82 30 V46"
        stroke="url(#lk-g)"
        strokeWidth="9"
        fill="none"
        strokeLinecap="round"
        style={{ originX: '82px', originY: '46px' }}
        animate={open ? { rotate: 32, y: -12 } : { rotate: 0, y: 0 }}
        transition={{ type: 'spring', stiffness: 160, damping: 10 }}
      />
      <path d="M60 122 C24 98 8 80 8 58 C8 42 20 32 34 32 C45 32 54 38 60 48 C66 38 75 32 86 32 C100 32 112 42 112 58 C112 80 96 98 60 122 Z" fill="url(#lk-b)" stroke="#fff" strokeWidth="4" />
      {/* "líquido" mágico subindo conforme as estrelas entram */}
      <g clipPath="url(#lk-clip)">
        <m.rect
          x="0"
          width="120"
          height="130"
          fill="#F7A8CF"
          opacity=".55"
          initial={false}
          animate={{ y: 122 - (filled / total) * 92 }}
          transition={{ type: 'spring', stiffness: 90, damping: 14 }}
        />
      </g>
      <path d="M60 122 C24 98 8 80 8 58 C8 42 20 32 34 32 C45 32 54 38 60 48 C66 38 75 32 86 32 C100 32 112 42 112 58 C112 80 96 98 60 122 Z" fill="none" stroke="#E7A6C8" strokeWidth="2" />
      {/* fechadura */}
      {!open && (
        <g>
          <circle cx="60" cy="72" r="8" fill="#B07AA6" />
          <path d="M57 76 H63 L61.5 90 H58.5 Z" fill="#B07AA6" />
        </g>
      )}
      {open && <path d="M45 74 L55 84 L76 62" stroke="#fff" strokeWidth="8" fill="none" strokeLinecap="round" strokeLinejoin="round" />}
      <path d="M26 50 C30 42 38 40 42 44" stroke="#fff" strokeWidth="4" fill="none" strokeLinecap="round" opacity=".85" />
    </svg>
  )
}

export default function UnlockGame({ unlocked, onUnlock, onSkip, onContinue }) {
  const reduce = useReducedMotion()
  const canvasRef = useRef(null)
  const wrapRef = useRef(null)
  const lockRef = useRef(null)
  const gameRef = useRef(null)
  const [got, setGot] = useState(unlocked ? GOAL : 0)
  const [phase, setPhase] = useState(unlocked ? 'won' : 'ready') // ready | playing | won
  const [failed, setFailed] = useState(false)
  const phaseRef = useRef(phase)
  phaseRef.current = phase

  // cria o motor do jogo (carregado sob demanda)
  useEffect(() => {
    let dead = false
    let io
    const onVis = () => {
      const g = gameRef.current
      if (!g) return
      if (document.hidden) g.pause()
    }
    import('../game/runner.js')
      .then(({ createRunner }) =>
        createRunner(canvasRef.current, {
          headSrc: HEAD,
          bgSrc: BG,
          goal: GOAL,
          onJump: () => {},
          onStar: (n, x, y) => {
            chime(n - 1)
            burst(x, y, { count: 24, speed: 6, size: [2, 5], life: [35, 60] })
            navigator.vibrate?.(15)
            setGot(n)
          },
          onGoal: () => {
            gameRef.current?.pause()
            fanfare()
            burstFrom(lockRef.current, { count: 140, speed: 13 })
            rain({ count: 260 })
            setPhase('won')
            onUnlock()
          },
        })
      )
      .then((g) => {
        if (dead) return g.dispose()
        gameRef.current = g
        // pausa quando sai da tela; retoma sozinho só se estava jogando
        io = new IntersectionObserver(([e]) => {
          if (!e.isIntersecting) g.pause()
          else if (phaseRef.current === 'playing' && !document.hidden) g.start()
        })
        io.observe(wrapRef.current)
        document.addEventListener('visibilitychange', onVis)
      })
      .catch(() => !dead && setFailed(true))
    return () => {
      dead = true
      io?.disconnect()
      document.removeEventListener('visibilitychange', onVis)
      gameRef.current?.dispose()
      gameRef.current = null
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const play = useCallback(() => {
    const g = gameRef.current
    if (!g) return
    if (phaseRef.current === 'won') {
      g.reset()
      setGot(0)
    }
    setPhase('playing')
    sparkle()
    g.start()
  }, [])

  const press = (e) => {
    if (phaseRef.current !== 'playing') return
    e.preventDefault()
    const g = gameRef.current
    if (!g) return
    if (!g.running && !document.hidden) g.start() // voltou de outra aba
    g.jump()
  }
  const onKey = (e) => {
    if ([' ', 'Enter', 'ArrowUp', 'w', 'W'].includes(e.key)) {
      if (phaseRef.current === 'ready' || phaseRef.current === 'won') return
      press(e)
    }
  }

  const done = phase === 'won'
  return (
    <section id="jogo" aria-labelledby="jogo-titulo" className="relative overflow-hidden bg-gradient-to-b from-rosa via-[#EADCF8] to-azul px-4 pb-14 pt-12">
      <Pattern opacity={0.2} />
      <DriftCloud className="left-[-14%] top-20 h-14 w-36 opacity-80" distance={16} />
      <DriftCloud className="right-[-16%] top-6 h-16 w-40 opacity-80" distance={-16} duration={10} />

      <div className="relative mx-auto max-w-md text-center">
        <p className="font-bubble bubble-pink text-[clamp(1.9rem,8.8vw,2.5rem)] leading-none">Ei, convidado!</p>
        <h2 id="jogo-titulo" className="mx-auto mt-2 max-w-[22ch] text-balance font-sans text-[clamp(1.25rem,5.4vw,1.6rem)] font-semibold leading-snug text-ameixa">
          Você precisa desbloquear o convite da {EVENT.childFirstName}!
        </h2>
        <p className="mt-2 font-sans text-base text-ameixaSoft">
          Ajude a {EVENT.childFirstName} a pular nos tijolinhos e pegar <strong className="font-semibold text-ameixa">5 estrelinhas</strong>.
        </p>

        {/* placar: cadeado-coração + estrelinhas */}
        <div className="mt-4 flex items-center justify-center gap-3">
          <div ref={lockRef} className="h-14 w-12">
            <m.div animate={done && !reduce ? { scale: [1, 1.3, 1], rotate: [0, -10, 10, 0] } : {}} transition={{ duration: 0.8 }}>
              <HeartLock filled={got} total={GOAL} open={done} />
            </m.div>
          </div>
          <ol className="flex gap-1" aria-hidden="true">
            {Array.from({ length: GOAL }, (_, i) => (
              <m.li
                key={i}
                className="h-9 w-9"
                initial={false}
                animate={i < got ? { scale: [1.6, 1], opacity: 1, filter: 'grayscale(0)' } : { scale: 1, opacity: 0.45, filter: 'grayscale(1)' }}
                transition={{ duration: 0.4 }}
              >
                <PuffyStar tint={TINTS[i]} id={`hud${i}`} face={false} />
              </m.li>
            ))}
          </ol>
          <p className="sr-only" role="status" aria-live="polite">
            {got} de {GOAL} estrelinhas
          </p>
        </div>

        {/* tela do jogo */}
        <div
          ref={wrapRef}
          role="application"
          aria-label="Jogo: toque na tela ou aperte espaço para a Sophie pular"
          tabIndex={0}
          onPointerDown={press}
          onKeyDown={onKey}
          className="relative mx-auto mt-4 aspect-[4/5] w-full max-w-[24rem] select-none overflow-hidden rounded-[2rem] bg-azul shadow-soft ring-4 ring-white/80"
          style={{ touchAction: phase === 'playing' ? 'none' : 'manipulation', WebkitUserSelect: 'none', WebkitTouchCallout: 'none' }}
        >
          <canvas ref={canvasRef} className="absolute inset-0 h-full w-full" aria-hidden="true" />

          {phase === 'playing' && got === 0 && (
            <p className="pointer-events-none absolute inset-x-0 top-4 font-sans text-base font-semibold text-ameixa [text-shadow:0_1px_0_#fff,0_0_8px_#fff]">
              Toque na tela para pular! 👆 <br />
              <span className="text-sm font-medium">Toque 2 vezes para pular mais alto</span>
            </p>
          )}

          {/* tela inicial */}
          <AnimatePresence>
            {phase === 'ready' && (
              <m.div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-white/45 p-6 backdrop-blur-[1px]" exit={{ opacity: 0 }}>
                <m.img
                  src={HEAD}
                  alt=""
                  aria-hidden="true"
                  className="h-28 w-auto drop-shadow-[0_8px_10px_rgba(150,100,160,.35)]"
                  animate={reduce ? undefined : { y: [0, -18, 0] }}
                  transition={{ duration: 0.9, repeat: Infinity, ease: 'easeInOut' }}
                />
                <button type="button" onClick={play} disabled={failed} className="btn-magic mt-4 min-h-[60px] px-9 text-xl">
                  ▶ Jogar
                </button>
                {failed && <p className="mt-2 text-sm text-ameixa">Não foi possível carregar o jogo. Use “Pular o jogo” abaixo.</p>}
              </m.div>
            )}
          </AnimatePresence>

          {/* vitória */}
          <AnimatePresence>
            {done && (
              <m.div
                className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-white/75 p-5 backdrop-blur-[2px]"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: reduce ? 0 : 0.2 }}
                role="alert"
                onPointerDown={(e) => e.stopPropagation()}
              >
                <m.img
                  src={HEAD}
                  alt=""
                  aria-hidden="true"
                  className="h-28 w-auto drop-shadow-[0_8px_10px_rgba(150,100,160,.35)]"
                  initial={{ y: 30, scale: 0.6 }}
                  animate={reduce ? { y: 0, scale: 1 } : { y: [30, -20, 0], scale: [0.6, 1.1, 1], rotate: [0, -8, 8, 0] }}
                  transition={{ duration: 0.9, delay: 0.3 }}
                />
                <p className="mt-1 font-bubble bubble-pink text-[2.1rem] leading-none">Parabéns!</p>
                <p className="mt-1 font-sans text-xl font-semibold text-ameixa">Você desbloqueou o convite!</p>
                <button type="button" onClick={onContinue} className="btn-magic mt-4 min-h-[56px] px-8 text-lg">
                  Ver o convite <span aria-hidden="true">✨</span>
                </button>
                <button type="button" onClick={play} className="mt-2 min-h-[44px] px-4 font-sans text-sm font-medium text-ameixaSoft underline underline-offset-4">
                  Jogar de novo
                </button>
              </m.div>
            )}
          </AnimatePresence>
        </div>

        {!done && (
          <button type="button" onClick={onSkip} className="mt-5 min-h-[44px] px-4 font-sans text-sm font-medium text-ameixaSoft underline decoration-rosaForte/60 underline-offset-4">
            Prefiro pular o jogo
          </button>
        )}
      </div>
    </section>
  )
}
