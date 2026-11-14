import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useCallback, useEffect, useRef, useState } from 'react'
import { EVENT, STORY } from '../config/event.js'
import { sparkle, chime, fanfare } from '../lib/sfx.js'
import { burstFrom, rain } from '../lib/glitter.js'
import { PuffyStar } from './UnlockGame.jsx'

const fill = (t) => (t || '').replaceAll('{nome}', EVENT.childFirstName)
const TOTAL_STARS = 5
const TINTS = ['#FFE58F', '#FFD36B', '#FFE9A8', '#FFDD80', '#FFF0B9']

/** céu estrelado em UMA camada CSS (leve) */
const Stars = () => <div className="story-stars pointer-events-none absolute inset-0" aria-hidden="true" />

/** Estrela tocável dentro do quadro */
function TapStar({ x, y, onTap, idx }) {
  const ref = useRef(null)
  return (
    <m.button
      ref={ref}
      type="button"
      onClick={(e) => {
        e.stopPropagation()
        onTap(ref.current)
      }}
      aria-label="Pegar a estrelinha mágica"
      className="absolute z-20 grid h-[4.5rem] w-[4.5rem] -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full"
      style={{ left: `${x}%`, top: `${y}%`, touchAction: 'manipulation' }}
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 2.2, opacity: 0 }}
      transition={{ type: 'spring', stiffness: 220, damping: 14, delay: 0.6 + idx * 0.25 }}
    >
      <span className="story-star-ring absolute inset-0 rounded-full" aria-hidden="true" />
      <span className="story-star-bob block h-14 w-14">
        <PuffyStar tint="#FFD36B" id={`st${idx}`} face={false} />
      </span>
    </m.button>
  )
}

/** contador ⭐ x/5 (feito no site, não no vídeo) */
function Slots({ count }) {
  return (
    <div className="flex items-center gap-1.5 rounded-full bg-black/35 px-3 py-1.5 ring-1 ring-white/25" aria-label={`${count} de ${TOTAL_STARS} estrelinhas`} role="status">
      {Array.from({ length: TOTAL_STARS }, (_, k) => (
        <m.span key={k} className="h-6 w-6" initial={false} animate={k < count ? { scale: [1.8, 1], opacity: 1 } : { scale: 1, opacity: 0.35 }} transition={{ duration: 0.45 }}>
          <svg viewBox="0 0 24 24" className="h-full w-full" aria-hidden="true">
            <path d="M12 2l2.9 6.3 6.9.7-5.2 4.6 1.5 6.8L12 17l-6.1 3.4 1.5-6.8L2.2 9l6.9-.7z" fill={k < count ? TINTS[k] : 'none'} stroke={k < count ? '#fff' : 'rgba(255,255,255,.8)'} strokeWidth="1.6" strokeLinejoin="round" />
          </svg>
        </m.span>
      ))}
      <span className="ml-1 font-sans text-sm font-bold tabular-nums text-white">{count}/{TOTAL_STARS}</span>
    </div>
  )
}

export default function StoryIntro({ onDone, onLeave, onFirstTap }) {
  const reduce = useReducedMotion()
  const scenes = STORY.scenes
  const [i, setI] = useState(-1) // -1 = tela de título
  const [leaving, setLeaving] = useState(false)
  const [stars, setStars] = useState(0) // total coletado
  const [pending, setPending] = useState([]) // índices das estrelas ainda na tela
  const [timeDone, setTimeDone] = useState(false)
  const [magic, setMagic] = useState(false)
  const timers = useRef([])
  const voiceRef = useRef(null)
  const firstPlayed = useRef(false)
  const iRef = useRef(i)
  iRef.current = i
  const doneRef = useRef(onDone)
  doneRef.current = onDone
  const leavingRef = useRef(false)
  const btnRef = useRef(null)
  const cardRef = useRef(null)

  const clearTimers = () => {
    timers.current.forEach(clearTimeout)
    timers.current = []
  }
  const later = (fn, ms) => timers.current.push(setTimeout(fn, ms))

  const finish = useCallback(() => {
    if (leavingRef.current) return
    leavingRef.current = true
    clearTimers()
    voiceRef.current?.pause()
    setLeaving(true)
    onLeave?.()
    setTimeout(() => doneRef.current?.(), reduce ? 0 : 900)
  }, [reduce, onLeave])

  const next = useCallback(() => {
    clearTimers()
    const v = iRef.current
    if (v + 1 >= scenes.length) finish()
    else setI(v + 1)
  }, [scenes.length, finish])

  // ---- início de cada cena: narração/tempo + estrelas ----
  useEffect(() => {
    if (i < 0 || leaving) return
    const sc = scenes[i]
    setTimeDone(false)
    setMagic(false)
    setStars(Math.min(TOTAL_STARS, starsBefore(i)))
    pendingRef.current = (sc.stars || []).map((_, k) => k)
    setPending(pendingRef.current)
    const minMs = (sc.seconds || STORY.secondsPerScene) * 1000
    let audioOver = !sc.audio
    let minOver = false
    const check = () => audioOver && minOver && setTimeDone(true)
    later(() => ((minOver = true), check()), sc.video ? 0 : Math.min(minMs, sc.audio ? 3500 : minMs))
    const a = voiceRef.current
    if (sc.audio && a) {
      a.onended = () => ((audioOver = true), check())
      a.onerror = () => ((audioOver = true), check())
      if (!(i === 0 && firstPlayed.current)) {
        a.src = sc.audio
        a.currentTime = 0
        a.play().catch(() => ((audioOver = true), check()))
      }
      later(() => ((audioOver = true), check()), minMs + 9000) // nunca trava
    } else if (sc.audio) {
      audioOver = true
    }
    // estrelas: se ninguém tocar, coletam sozinhas
    if (sc.stars?.length) later(() => collectAll(), (STORY.starTimeout || 9) * 1000)
    return () => {
      clearTimers()
      if (a) a.onended = a.onerror = null
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [i, leaving])

  // ---- avança quando o tempo acabou E não há estrelas pendentes ----
  useEffect(() => {
    if (i < 0 || leaving || !timeDone || pending.length) return
    const t = setTimeout(next, scenes[i]?.magic ? 2600 : 600)
    return () => clearTimeout(t)
  }, [timeDone, pending, i, leaving, next, scenes])

  const pendingRef = useRef(pending)
  pendingRef.current = pending
  // total = estrelas das cenas anteriores + as já pegas nesta (determinístico)
  const starsBefore = (idx) => scenes.slice(0, idx).reduce((n, x) => n + (x.stars?.length || 0), 0)

  const collect = (k, el) => {
    if (iRef.current < 0 || !pendingRef.current.includes(k)) return
    const rest = pendingRef.current.filter((x) => x !== k)
    pendingRef.current = rest
    setPending(rest)
    const sc = scenes[iRef.current]
    const total = Math.min(TOTAL_STARS, starsBefore(iRef.current) + (sc.stars.length - rest.length))
    setStars(total)
    if (total === TOTAL_STARS) {
      fanfare()
      setMagic(true)
      rain({ count: 220, duration: 1500 })
    } else chime(total - 1)
    if (el) burstFrom(el, { count: 40, speed: 8 })
    navigator.vibrate?.(18)
  }
  const collectAll = () => [...pendingRef.current].forEach((k) => collect(k, cardRef.current))

  // pré-carrega as imagens das cenas
  useEffect(() => {
    scenes.forEach((sc) => {
      if (!sc.image) return
      const im = new Image()
      im.src = sc.image
      im.decode?.().catch(() => {})
    })
  }, [scenes])

  useEffect(() => {
    btnRef.current?.focus()
    const onKey = (e) => e.key === 'Escape' && finish()
    window.addEventListener('keydown', onKey)
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      window.removeEventListener('keydown', onKey)
      document.body.style.overflow = prev
      voiceRef.current?.pause()
    }
  }, [finish])

  const begin = () => {
    const first = scenes[0]?.audio
    const a = voiceRef.current || (voiceRef.current = new Audio())
    a.preload = 'auto'
    if (first) {
      a.src = first
      a.play().catch(() => {}) // dentro do toque (iPhone)
      firstPlayed.current = true
    } else {
      sparkle()
    }
    scenes.slice(1).forEach((sc) => sc.audio && fetch(sc.audio).catch(() => {}))
    onFirstTap?.()
    setI(0)
  }

  const sc = i >= 0 ? scenes[i] : null
  const slotsVisible = scenes.slice(0, Math.max(0, i) + 1).some((s) => s.showSlots)
  const [c0, c1] = sc?.cam || [[1, 0, 0], [1.15, 0, 0]]
  const dur = sc ? sc.seconds || STORY.secondsPerScene : 6

  return (
    <m.div
      role="dialog"
      aria-modal="true"
      aria-label={`Historinha: O Reino Encantado da ${EVENT.childFirstName}`}
      className="fixed inset-0 z-[80] overflow-hidden text-white"
      style={{ background: 'linear-gradient(180deg,#1E1638 0%,#3D2A6E 45%,#8E5FA8 100%)' }}
      animate={leaving ? { opacity: 0 } : { opacity: 1 }}
      transition={{ duration: 0.9, ease: 'easeInOut' }}
      onClick={(e) => i >= 0 && !e.target.closest('button') && !pending.length && timeDone && next()}
    >
      <Stars />

      {/* ---------- tela de título ---------- */}
      {i < 0 && (
        <div className="absolute inset-0 flex flex-col items-center justify-center px-8 text-center">
          <m.p className="font-sans text-xs font-semibold uppercase tracking-[0.4em] text-white/80" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1.2 }}>
            Uma historinha mágica
          </m.p>
          <m.p className="mt-3 font-bubble bubble-story text-[clamp(1.9rem,8.6vw,2.7rem)] leading-tight" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 1.4, delay: 0.3 }}>
            O Reino Encantado da {EVENT.childFirstName}
          </m.p>
          <p className="mt-3 max-w-[28ch] font-sans text-base text-white/85">Ajude a {EVENT.childFirstName} a encontrar as 5 estrelinhas mágicas ⭐</p>
          <m.button
            ref={btnRef}
            type="button"
            onClick={begin}
            className="btn-magic mt-9 min-h-[58px] px-9 text-lg"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: [0, -5, 0] }}
            transition={{ opacity: { delay: 1 }, y: { duration: 2.4, repeat: Infinity } }}
          >
            ✨ Toque para começar
          </m.button>
        </div>
      )}

      {/* ---------- cenas ---------- */}
      <AnimatePresence>
        {sc && (
          <m.div key={i} className="absolute inset-0" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.7 }}>
            {sc.video ? (
              // vídeo vertical (quando existir): tela cheia
              <video className="absolute inset-0 h-full w-full object-cover" src={sc.video} autoPlay muted playsInline onEnded={() => setTimeDone(true)} />
            ) : (
              // quadro do storyboard em "livro de histórias", com câmera lenta
              <div className="absolute inset-x-0 top-[calc(9vh+3.6rem)] flex justify-center px-3">
                <div ref={cardRef} className="relative w-full max-w-[30rem] overflow-hidden rounded-[1.6rem] shadow-[0_20px_50px_-12px_rgba(0,0,0,.6)] ring-4 ring-white/85" style={{ aspectRatio: '4 / 3.3' }}>
                  <m.div
                    className="absolute inset-0 [will-change:transform]"
                    initial={{ scale: c0[0], x: `${c0[1]}%`, y: `${c0[2]}%` }}
                    animate={reduce ? undefined : { scale: c1[0], x: `${c1[1]}%`, y: `${c1[2]}%` }}
                    transition={{ duration: dur + 1.5, ease: 'easeInOut' }}
                  >
                    <img src={sc.image} alt="" className="absolute inset-0 h-full w-full object-cover" draggable="false" />
                    <AnimatePresence>
                      {(sc.stars || []).map(([x, y], k) => pending.includes(k) && <TapStar key={k} idx={k} x={x} y={y} onTap={(el) => collect(k, el)} />)}
                    </AnimatePresence>
                  </m.div>
                  {magic && <div className="story-magic pointer-events-none absolute inset-0" aria-hidden="true" />}
                </div>
              </div>
            )}

            {/* legenda */}
            <div className={`absolute inset-x-0 px-6 text-center ${sc.video ? 'bottom-[calc(9vh+1.5rem)]' : 'top-[calc(9vh+3.6rem+min(100vw-1.5rem,30rem)*0.825+1.2rem)]'}`}>
              <p className="font-sans text-[0.7rem] font-semibold uppercase tracking-[0.3em] text-white/70">
                Cena {i + 1} · {sc.title}
              </p>
              <m.p
                className="mx-auto mt-2 max-w-[24ch] font-bubble bubble-story normal-case text-[clamp(1.25rem,5.6vw,1.75rem)] leading-[1.25]"
                initial={{ opacity: 0, y: 14 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.9, delay: 0.25 }}
              >
                {fill(sc.text)}
              </m.p>
              {pending.length > 0 && (
                <m.p className="mt-3 font-sans text-base font-bold text-amarelo" animate={{ scale: [1, 1.08, 1] }} transition={{ duration: 1.2, repeat: Infinity }}>
                  👆 Toque {pending.length > 1 ? 'nas estrelinhas' : 'na estrelinha'}!
                </m.p>
              )}
            </div>
          </m.div>
        )}
      </AnimatePresence>

      {/* contador de estrelas */}
      {sc && slotsVisible && (
        <div className="absolute inset-x-0 top-[calc(9vh+0.6rem)] z-30 flex justify-center">
          <Slots count={stars} />
        </div>
      )}

      {/* faixas de cinema + progresso + pular */}
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[9vh] min-h-[44px] bg-black/85" aria-hidden="true" />
      <div className="absolute inset-x-0 bottom-0 z-40 flex h-[9vh] min-h-[56px] items-center justify-between bg-black/85 px-4 pb-[env(safe-area-inset-bottom)]">
        <div className="flex flex-1 gap-1 pr-4" aria-hidden="true">
          {scenes.map((_, k) => (
            <span key={k} className={`h-1 flex-1 rounded-full ${k <= i ? 'bg-white' : 'bg-white/25'}`} />
          ))}
        </div>
        <button type="button" onClick={finish} className="min-h-[44px] rounded-full px-4 font-sans text-sm font-semibold text-white/90 ring-1 ring-white/40">
          Pular história ›
        </button>
      </div>
    </m.div>
  )
}
