import { m, AnimatePresence } from 'framer-motion'
import { useCallback, useEffect, useRef, useState } from 'react'
import { EVENT } from '../config/event.js'
import { POSTER } from './Unicorn3D.jsx'
import { chime, fanfare, sparkle } from '../lib/sfx.js'
import { burstFrom, rain } from '../lib/glitter.js'
import Pattern from './Pattern.jsx'
import Reveal from './Reveal.jsx'

const KEY = 'sophie-escadinha-recorde'
const readBest = () => {
  try {
    return Number(localStorage.getItem(KEY)) || 0
  } catch {
    return 0
  }
}

/** Jogo "Escadinha do Unicórnio": cada pulo certinho conta 1 */
export default function StairsGame() {
  const canvasRef = useRef(null)
  const wrapRef = useRef(null)
  const counterRef = useRef(null)
  const gameRef = useRef(null)
  const [count, setCount] = useState(0)
  const [best, setBest] = useState(readBest)
  const [playing, setPlaying] = useState(false)
  const [failed, setFailed] = useState(false)
  const playingRef = useRef(false)
  playingRef.current = playing

  useEffect(() => {
    let dead = false
    let io
    import('../game/stairs.js')
      .then(({ createStairs }) =>
        createStairs(canvasRef.current, {
          uniSrc: POSTER,
          onJump: (n) => {
            chime(n % 6)
            setCount(n)
            setBest((b) => {
              if (n <= b) return b
              try {
                localStorage.setItem(KEY, String(n))
              } catch {
                /* ok */
              }
              return n
            })
            navigator.vibrate?.(12)
          },
          onMilestone: (n) => {
            fanfare()
            burstFrom(counterRef.current, { count: 90, speed: 10 })
            if (n % 10 === 0) rain({ count: 160, duration: 1000 })
          },
        })
      )
      .then((g) => {
        if (dead) return g.dispose()
        gameRef.current = g
        io = new IntersectionObserver(([e]) => {
          if (!e.isIntersecting) g.pause()
          else if (playingRef.current) g.start()
        })
        io.observe(wrapRef.current)
      })
      .catch(() => !dead && setFailed(true))
    const onVis = () => document.hidden && gameRef.current?.pause()
    document.addEventListener('visibilitychange', onVis)
    return () => {
      dead = true
      io?.disconnect()
      document.removeEventListener('visibilitychange', onVis)
      gameRef.current?.dispose()
    }
  }, [])

  const start = useCallback(() => {
    const g = gameRef.current
    if (!g) return
    sparkle()
    setPlaying(true)
    g.start()
  }, [])

  const restart = () => {
    gameRef.current?.reset()
    setCount(0)
    start()
  }

  const press = (e) => {
    if (!playingRef.current) return
    e.preventDefault()
    const g = gameRef.current
    if (!g) return
    if (!g.running) g.start()
    g.jump()
  }

  return (
    <section id="pulos" aria-labelledby="pulos-titulo" className="relative overflow-hidden bg-gradient-to-b from-lilas/60 via-[#F4EEFF] to-azul/60 px-4 py-14">
      <Pattern opacity={0.18} />
      <div className="relative mx-auto max-w-md text-center">
        <Reveal>
          <h2 id="pulos-titulo" className="font-bubble bubble-purple text-[clamp(1.75rem,8vw,2.4rem)] leading-tight">
            Escadinha do Unicórnio
          </h2>
          <p className="mx-auto mt-1 max-w-[30ch] font-sans text-base font-medium text-ameixa">
            Toque na tela quando a nuvem passar embaixo do unicórnio. Quantos pulos você consegue?
          </p>
        </Reveal>

        <div className="mt-4 flex items-stretch justify-center gap-3">
          <div ref={counterRef} className="min-w-[7.5rem] rounded-2xl bg-white/90 px-4 py-2 shadow-soft ring-1 ring-white">
            <p className="font-sans text-xs font-semibold uppercase tracking-[0.18em] text-ameixaSoft">Pulos</p>
            <m.p key={count} initial={{ scale: 1.5 }} animate={{ scale: 1 }} className="font-sans text-3xl font-semibold tabular-nums text-ameixa" aria-live="polite">
              {count}
            </m.p>
          </div>
          <div className="min-w-[7.5rem] rounded-2xl bg-amarelo/80 px-4 py-2 shadow-soft ring-1 ring-dourado/50">
            <p className="font-sans text-xs font-semibold uppercase tracking-[0.18em] text-ameixaSoft">Recorde 🏆</p>
            <p className="font-sans text-3xl font-semibold tabular-nums text-ameixa">{best}</p>
          </div>
        </div>

        <div
          ref={wrapRef}
          role="application"
          aria-label="Escadinha do Unicórnio: toque na tela ou aperte espaço para pular"
          tabIndex={0}
          onPointerDown={press}
          onKeyDown={(e) => [' ', 'Enter', 'ArrowUp'].includes(e.key) && press(e)}
          className="relative mx-auto mt-4 aspect-[3/4] w-full max-w-[22rem] select-none overflow-hidden rounded-[2rem] bg-azul shadow-soft ring-4 ring-white/80"
          style={{ touchAction: playing ? 'none' : 'manipulation', WebkitTouchCallout: 'none', WebkitUserSelect: 'none' }}
        >
          <canvas ref={canvasRef} className="absolute inset-0 h-full w-full" aria-hidden="true" />
          <AnimatePresence>
            {!playing && (
              <m.div className="absolute inset-0 flex flex-col items-center justify-center bg-white/45 p-6" exit={{ opacity: 0 }}>
                <m.img
                  src={POSTER}
                  alt=""
                  aria-hidden="true"
                  className="h-32 w-32 object-contain"
                  animate={{ y: [0, -22, 0] }}
                  transition={{ duration: 0.9, repeat: Infinity, ease: 'easeInOut' }}
                />
                <button type="button" onClick={start} disabled={failed} className="btn-magic mt-3 min-h-[58px] px-9 text-xl">
                  ▶ Jogar
                </button>
                {failed && <p className="mt-2 text-sm text-ameixa">Não foi possível carregar o jogo agora.</p>}
              </m.div>
            )}
          </AnimatePresence>
        </div>
        {playing && (
          <button type="button" onClick={restart} className="mt-3 min-h-[44px] px-4 font-sans text-sm font-semibold text-ameixaSoft underline underline-offset-4">
            Recomeçar do zero
          </button>
        )}
        <p className="mt-2 font-sans text-sm text-ameixaSoft">Desafie a {EVENT.childFirstName} na festa! 🦄</p>
      </div>
    </section>
  )
}
