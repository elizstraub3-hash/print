import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useCallback, useEffect, useRef, useState } from 'react'
import { EVENT, STORY } from '../config/event.js'
import { chime, fanfare, sparkle } from '../lib/sfx.js'
import { burstFrom, rain } from '../lib/glitter.js'
import { PuffyStar } from './UnlockGame.jsx'

const fill = (t) => (t || '').replaceAll('{nome}', EVENT.childFirstName)
const RATIO_V = 720 / 1280

/** contador ⭐ x/5 */
function Slots({ count }) {
  return (
    <div className="flex items-center gap-1.5 rounded-full bg-white/85 px-3 py-1.5 shadow-soft ring-2 ring-white" role="status" aria-label={`${count} de 5 estrelinhas`}>
      {Array.from({ length: 5 }, (_, k) => (
        <m.span key={k} className="h-6 w-6" initial={false} animate={k < count ? { scale: [1.9, 1], opacity: 1 } : { scale: 1, opacity: 0.5 }} transition={{ duration: 0.5 }}>
          <svg viewBox="0 0 24 24" className="h-full w-full" aria-hidden="true">
            <path d="M12 2l2.9 6.3 6.9.7-5.2 4.6 1.5 6.8L12 17l-6.1 3.4 1.5-6.8L2.2 9l6.9-.7z" fill={k < count ? '#FFC93D' : '#fff'} stroke={k < count ? '#D99A1E' : '#B79BEA'} strokeWidth="1.6" strokeLinejoin="round" />
          </svg>
        </m.span>
      ))}
      <span className="ml-1 font-sans text-base font-bold tabular-nums text-[#7B2E9E]">{count}/5</span>
    </div>
  )
}

/** Estrela tocável: brilho pulsante + estrelinhas em volta */
function TapStar({ x, y, idx, onTap }) {
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
      className="pointer-events-auto absolute z-20 grid h-24 w-24 place-items-center rounded-full"
      style={{ left: `${x}%`, top: `${y}%`, x: '-50%', y: '-50%', touchAction: 'manipulation' }}
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 2.4, opacity: 0, transition: { duration: 0.45 } }}
      transition={{ type: 'spring', stiffness: 200, damping: 13, delay: 0.5 + idx * 0.3 }}
    >
      <span className="story-star-ring absolute inset-3 rounded-full" aria-hidden="true" />
      {[0, 1, 2, 3].map((k) => (
        <span key={k} className="story-mini-star absolute text-lg" style={{ '--a': `${k * 90 + 45}deg`, animationDelay: `${k * 0.25}s` }} aria-hidden="true">
          ✦
        </span>
      ))}
      <span className="story-star-bob block h-14 w-14">
        <PuffyStar tint="#FFD36B" id={`st${idx}`} face={false} />
      </span>
      <span className="absolute -bottom-1 rounded-full bg-white/90 px-2 py-0.5 font-sans text-xs font-bold text-[#7B2E9E] shadow-soft">toque!</span>
    </m.button>
  )
}

/** Caixa que cobre a tela mantendo a proporção da imagem (estrelas ficam no lugar certo) */
function CoverBox({ ratio, children, cam, dur, reduce }) {
  const [c0, c1] = cam || [[1, 0, 0], [1.1, 0, 0]]
  return (
    <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2" style={{ width: `max(100vw, calc(100svh * ${ratio}))`, aspectRatio: String(ratio) }}>
      <m.div
        className="absolute inset-0 [will-change:transform]"
        initial={{ scale: c0[0], x: `${c0[1]}%`, y: `${c0[2]}%` }}
        animate={reduce ? undefined : { scale: c1[0], x: `${c1[1]}%`, y: `${c1[2]}%` }}
        transition={{ duration: dur + 3, ease: 'easeInOut' }}
      >
        {children}
      </m.div>
    </div>
  )
}

export default function StoryIntro({ onDone, onLeave, onFirstTap }) {
  const reduce = useReducedMotion()
  const scenes = STORY.scenes
  const [i, setI] = useState(-1)
  const [leaving, setLeaving] = useState(false)
  const [count, setCount] = useState(0)
  const [pending, setPending] = useState([])
  const [timeDone, setTimeDone] = useState(false)
  const [magic, setMagic] = useState(false)
  const [segDur, setSegDur] = useState(6)
  const voiceRef = useRef(null)
  const iRef = useRef(i)
  iRef.current = i
  const pendingRef = useRef([])
  const countRef = useRef(0)
  const leavingRef = useRef(false)
  const doneRef = useRef(onDone)
  doneRef.current = onDone
  const boxRef = useRef(null)
  const btnRef = useRef(null)

  const finish = useCallback(() => {
    if (leavingRef.current) return
    leavingRef.current = true
    voiceRef.current?.pause()
    setLeaving(true)
    onLeave?.()
    setTimeout(() => doneRef.current?.(), reduce ? 0 : 900)
  }, [reduce, onLeave])

  const next = useCallback(() => {
    const v = iRef.current
    if (v + 1 >= scenes.length) finish()
    else setI(v + 1)
  }, [scenes.length, finish])

  const collect = useCallback((k, el) => {
    if (!pendingRef.current.includes(k)) return
    pendingRef.current = pendingRef.current.filter((x) => x !== k)
    setPending(pendingRef.current)
    countRef.current = Math.min(5, countRef.current + 1)
    setCount(countRef.current)
    if (countRef.current === 5) {
      fanfare()
      setMagic(true)
      rain({ count: 240, duration: 1600 })
    } else chime(countRef.current - 1)
    burstFrom(el || boxRef.current, { count: 50, speed: 9 })
    navigator.vibrate?.(20)
  }, [])

  // início de cada cena
  useEffect(() => {
    if (i < 0 || leaving) return
    const sc = scenes[i]
    if (sc.count != null) {
      countRef.current = sc.count
      setCount(sc.count)
    }
    setMagic(false)
    setSegDur(sc.seconds)
    pendingRef.current = (sc.stars || []).map((_, k) => k)
    setPending(pendingRef.current)
    setTimeDone(false)
    let audioOver = !sc.audio
    let minOver = false
    const check = () => audioOver && minOver && setTimeDone(true)
    const timers = [setTimeout(() => ((minOver = true), check()), sc.seconds * 1000)]
    const a = voiceRef.current
    if (sc.audio && a) {
      a.onended = a.onerror = () => ((audioOver = true), check())
      a.onloadedmetadata = () => a.duration && isFinite(a.duration) && setSegDur(Math.max(sc.seconds, a.duration))
      if (a.dataset.started === '1') {
        a.dataset.started = '0' // já começou dentro do toque inicial
        if (a.duration) setSegDur(Math.max(sc.seconds, a.duration))
      } else {
        a.src = sc.audio
        a.currentTime = 0
        a.play().catch(() => ((audioOver = true), check()))
      }
      timers.push(setTimeout(() => ((audioOver = true), check()), (sc.seconds + 12) * 1000))
    }
    if (sc.stars?.length) timers.push(setTimeout(() => [...pendingRef.current].forEach((k) => collect(k, boxRef.current)), (STORY.starTimeout || 10) * 1000))
    if (sc.celebrate) timers.push(setTimeout(() => (fanfare(), rain({ count: 200, duration: 1400 })), 600))
    return () => {
      timers.forEach(clearTimeout)
      if (a) {
        a.onended = a.onerror = a.onloadedmetadata = null
        a.pause()
      }
    }
  }, [i, leaving, scenes, collect])

  // ---- navegação estilo Stories ----
  const goTo = useCallback(
    (k) => {
      if (k < 0) k = 0
      if (k >= scenes.length) return finish()
      // ao pular uma cena com estrelas, elas contam como pegas
      if (k > iRef.current) {
        const cur = scenes[iRef.current]
        if (cur?.stars?.length) pendingRef.current = []
      }
      setPending([])
      setI(k)
    },
    [scenes, finish]
  )
  const swipe = useRef(null)
  const onTapZone = (dir) => (e) => {
    e.stopPropagation()
    goTo(iRef.current + dir)
  }
  const onTouchStart = (e) => (swipe.current = { x: e.touches[0].clientX, y: e.touches[0].clientY })
  const onTouchEnd = (e) => {
    const st = swipe.current
    swipe.current = null
    if (!st) return
    const dx = e.changedTouches[0].clientX - st.x
    const dy = e.changedTouches[0].clientY - st.y
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) goTo(iRef.current + (dx < 0 ? 1 : -1))
  }
  useEffect(() => {
    const k = (e) => {
      if (iRef.current < 0) return
      if (e.key === 'ArrowRight') goTo(iRef.current + 1)
      if (e.key === 'ArrowLeft') goTo(iRef.current - 1)
    }
    window.addEventListener('keydown', k)
    const vis = () => document.hidden && voiceRef.current?.pause()
    document.addEventListener('visibilitychange', vis)
    return () => {
      window.removeEventListener('keydown', k)
      document.removeEventListener('visibilitychange', vis)
    }
  }, [goTo])

  // avança quando o tempo acabou e não há estrelas pendentes
  useEffect(() => {
    if (i < 0 || leaving || !timeDone || pending.length) return
    const t = setTimeout(next, scenes[i]?.magic ? 2400 : 500)
    return () => clearTimeout(t)
  }, [timeDone, pending, i, leaving, next, scenes])

  useEffect(() => {
    scenes.forEach((sc) => [sc.image, sc.bg].filter(Boolean).forEach((src) => {
      const im = new Image()
      im.src = src
    }))
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
    const a = voiceRef.current || (voiceRef.current = new Audio())
    a.preload = 'auto'
    if (scenes[0]?.audio) {
      a.src = scenes[0].audio
      a.dataset.started = '1'
      a.play().catch(() => {})
    } else sparkle()
    setI(0)
  }

  const sc = i >= 0 ? scenes[i] : null
  const vertical = sc && !sc.bg
  return (
    <m.div
      role="dialog"
      aria-modal="true"
      aria-label={`Historinha: O Reino Encantado da ${EVENT.childFirstName}`}
      className="fixed inset-0 z-[80] overflow-hidden bg-[#2B1D4A] text-white"
      animate={leaving ? { opacity: 0 } : { opacity: 1 }}
      transition={{ duration: 0.9, ease: 'easeInOut' }}
    >
      {/* tela de título */}
      {i < 0 && (
        <div className="absolute inset-0 flex flex-col items-center justify-center px-8 text-center">
          <img src={scenes[0].image} alt="" className="absolute inset-0 h-full w-full object-cover" />
          <div className="absolute inset-0 bg-gradient-to-b from-[#2B1D4A]/30 via-[#2B1D4A]/45 to-[#2B1D4A]/70" />
          <m.p className="relative font-sans text-xs font-bold uppercase tracking-[0.4em] text-white" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1.2 }}>
            Uma historinha mágica
          </m.p>
          <m.p className="relative mt-3 font-bubble bubble-story text-[clamp(1.9rem,8.6vw,2.7rem)] leading-tight" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 1.4, delay: 0.3 }}>
            O Reino Encantado da {EVENT.childFirstName}
          </m.p>
          <p className="story-caption relative mt-4 max-w-[26ch] text-lg">Ajude a {EVENT.childFirstName} a encontrar as 5 estrelinhas para ganhar o seu vestido! ⭐</p>
          <m.button
            ref={btnRef}
            type="button"
            onClick={begin}
            className="btn-magic relative mt-8 min-h-[58px] px-9 text-lg"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: [0, -5, 0] }}
            transition={{ opacity: { delay: 1 }, y: { duration: 2.4, repeat: Infinity } }}
          >
            ▶ Começar a história
          </m.button>
          <p className="relative mt-3 font-sans text-sm font-semibold text-white">Ligue o som 🔊</p>
          <button type="button" onClick={finish} className="relative mt-6 min-h-[44px] rounded-full bg-black/25 px-5 font-sans text-sm font-semibold text-white ring-1 ring-white/60">
            Pular história ›
          </button>
        </div>
      )}

      {/* cena */}
      <AnimatePresence>
        {sc && (
          <m.div key={i} className="absolute inset-0" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.5 }} onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
            {/* toque à esquerda = voltar · à direita = avançar (como Stories) */}
            <button type="button" onClick={onTapZone(-1)} aria-label="Cena anterior" className="absolute inset-y-0 left-0 z-10 w-[30%]" style={{ touchAction: 'manipulation' }} />
            <button type="button" onClick={onTapZone(1)} aria-label="Próxima cena" className="absolute inset-y-0 right-0 z-10 w-[70%]" style={{ touchAction: 'manipulation' }} />
            {vertical ? (
              <div ref={boxRef} className="pointer-events-none absolute inset-0 z-[15]">
                <CoverBox ratio={RATIO_V} cam={sc.cam} dur={sc.seconds} reduce={reduce}>
                  <img src={sc.image} alt="" className="absolute inset-0 h-full w-full" draggable="false" />
                  <AnimatePresence>{(sc.stars || []).map(([x, y], k) => pending.includes(k) && <TapStar key={k} idx={k} x={x} y={y} onTap={(el) => collect(k, el)} />)}</AnimatePresence>
                </CoverBox>
              </div>
            ) : (
              <>
                <img src={sc.bg} alt="" aria-hidden="true" className="absolute inset-0 h-full w-full scale-110 object-cover" />
                <div className="pointer-events-none absolute inset-x-0 top-[6.5rem] z-[15] flex justify-center px-3">
                  <div ref={boxRef} className="relative w-full max-w-[34rem] overflow-hidden rounded-[1.4rem] shadow-[0_24px_60px_-12px_rgba(0,0,0,.55)] ring-[3px] ring-white/85" style={{ aspectRatio: '4 / 3.4' }}>
                    <m.div
                      className="absolute inset-0 [will-change:transform]"
                      initial={{ scale: sc.cam[0][0], x: `${sc.cam[0][1]}%`, y: `${sc.cam[0][2]}%` }}
                      animate={reduce ? undefined : { scale: sc.cam[1][0], x: `${sc.cam[1][1]}%`, y: `${sc.cam[1][2]}%` }}
                      transition={{ duration: sc.seconds + 3, ease: 'easeInOut' }}
                    >
                      <img src={sc.image} alt="" className="absolute inset-0 h-full w-full object-cover" draggable="false" />
                      <AnimatePresence>{(sc.stars || []).map(([x, y], k) => pending.includes(k) && <TapStar key={k} idx={k} x={x} y={y} onTap={(el) => collect(k, el)} />)}</AnimatePresence>
                    </m.div>
                    {magic && sc.magic && <div className="story-magic pointer-events-none absolute inset-0" aria-hidden="true" />}
                  </div>
                </div>
              </>
            )}
            {magic && sc.magic && vertical && <div className="story-magic pointer-events-none absolute inset-0" aria-hidden="true" />}

            {/* legenda */}
            <div className="pointer-events-none absolute inset-x-0 bottom-[max(1.6rem,calc(env(safe-area-inset-bottom)+1rem))] z-20 px-5 text-center">
              <m.p key={`t${i}`} className="story-caption mx-auto max-w-[28ch] text-[clamp(1.15rem,5vw,1.45rem)]" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.25 }} aria-live="polite">
                {fill(sc.text)}
              </m.p>
            </div>
          </m.div>
        )}
      </AnimatePresence>

      {sc && sc.count != null && (
        <div className="pointer-events-none absolute inset-x-0 top-[calc(max(0.6rem,env(safe-area-inset-top))+4.2rem)] z-30 flex justify-center">
          <Slots count={count} />
        </div>
      )}

      {/* barras estilo Stories + pular */}
      {sc && (
        <div className="absolute inset-x-0 top-0 z-40 bg-gradient-to-b from-black/40 to-transparent px-3 pb-6 pt-[max(0.6rem,env(safe-area-inset-top))]">
          <div className="flex gap-1" aria-hidden="true">
            {scenes.map((_, k) => (
              <span key={k} className="h-1 flex-1 overflow-hidden rounded-full bg-white/40">
                {k < i && <span className="block h-full w-full bg-white" />}
                {k === i && !leaving && (
                  <m.span key={`p${i}-${segDur}`} className="block h-full bg-white" initial={{ width: '0%' }} animate={{ width: '100%' }} transition={{ duration: segDur, ease: 'linear' }} />
                )}
              </span>
            ))}
          </div>
          <div className="mt-2 flex items-center justify-between">
            <span className="font-sans text-xs font-bold text-white [text-shadow:0_1px_2px_rgba(0,0,0,.5)]">
              {i + 1}/{scenes.length} · toque para avançar ›
            </span>
            <button type="button" onClick={finish} className="min-h-[40px] rounded-full bg-black/25 px-4 font-sans text-sm font-semibold text-white ring-1 ring-white/60">
              Pular história ›
            </button>
          </div>
        </div>
      )}
    </m.div>
  )
}
