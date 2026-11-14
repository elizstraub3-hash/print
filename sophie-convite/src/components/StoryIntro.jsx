import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useCallback, useEffect, useRef, useState } from 'react'
import { EVENT, STORY } from '../config/event.js'
import { fanfare } from '../lib/sfx.js'
import { rain } from '../lib/glitter.js'

const fill = (t) => (t || '').replaceAll('{nome}', EVENT.childFirstName)

/** contador ⭐ x/5 — mostra quantas estrelas a história já reuniu */
function Slots({ count }) {
  return (
    <div className="flex items-center gap-1.5 rounded-full bg-black/35 px-3 py-1.5 ring-1 ring-white/25" aria-hidden="true">
      {Array.from({ length: 5 }, (_, k) => (
        <m.span key={k} className="h-5 w-5" initial={false} animate={k < count ? { scale: [1.8, 1], opacity: 1 } : { scale: 1, opacity: 0.4 }} transition={{ duration: 0.5 }}>
          <svg viewBox="0 0 24 24" className="h-full w-full">
            <path d="M12 2l2.9 6.3 6.9.7-5.2 4.6 1.5 6.8L12 17l-6.1 3.4 1.5-6.8L2.2 9l6.9-.7z" fill={k < count ? '#FFD36B' : 'none'} stroke="#fff" strokeWidth="1.6" strokeLinejoin="round" />
          </svg>
        </m.span>
      ))}
      <span className="ml-1 font-sans text-sm font-bold tabular-nums text-white">{count}/5</span>
    </div>
  )
}

/** Historinha de abertura em vídeo — o convidado só assiste (pode pular) */
export default function StoryIntro({ onDone, onLeave, onFirstTap }) {
  const reduce = useReducedMotion()
  const scenes = STORY.scenes
  const [i, setI] = useState(-1) // -1 = tela de título
  const [leaving, setLeaving] = useState(false)
  const voiceRef = useRef(null)
  const videoRef = useRef(null)
  const iRef = useRef(i)
  iRef.current = i
  const leavingRef = useRef(false)
  const doneRef = useRef(onDone)
  doneRef.current = onDone
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

  // cada cena termina quando o vídeo E a narração terminam (com limite de segurança)
  useEffect(() => {
    if (i < 0 || leaving) return
    const sc = scenes[i]
    let videoOver = false
    let audioOver = !sc.audio
    let advanced = false
    const go = () => {
      if (advanced || !(videoOver && audioOver)) return
      advanced = true
      setTimeout(next, 350)
    }
    const timers = []
    const v = videoRef.current
    const onEnd = () => ((videoOver = true), go())
    if (v) {
      v.addEventListener('ended', onEnd)
      v.addEventListener('error', onEnd)
      v.play?.().catch(() => {})
    }
    // se o vídeo não tocar (economia de bateria, rede), a cena segue pelo tempo
    timers.push(setTimeout(() => ((videoOver = true), go()), (sc.seconds + 1.5) * 1000))
    const a = voiceRef.current
    if (sc.audio && a) {
      a.onended = () => ((audioOver = true), go())
      a.onerror = () => ((audioOver = true), go())
      if (!(i === 0 && a.dataset.started === '1')) {
        a.src = sc.audio
        a.play().catch(() => ((audioOver = true), go()))
      }
      timers.push(setTimeout(() => ((audioOver = true), go()), (sc.seconds + 10) * 1000))
    }
    if (sc.stars === 5 && scenes[i - 1]?.stars !== 5) {
      timers.push(setTimeout(() => (fanfare(), rain({ count: 200, duration: 1500 })), 5600))
    }
    return () => {
      timers.forEach(clearTimeout)
      if (v) {
        v.removeEventListener('ended', onEnd)
        v.removeEventListener('error', onEnd)
      }
      if (a) a.onended = a.onerror = null
    }
  }, [i, leaving, next, scenes])

  // pré-carrega o próximo vídeo
  useEffect(() => {
    const n = scenes[i + 1]
    if (!n?.video) return
    const l = document.createElement('link')
    l.rel = 'preload'
    l.as = 'video'
    l.href = n.video
    document.head.appendChild(l)
    return () => l.remove()
  }, [i, scenes])

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
    const first = scenes[0]?.audio
    if (first) {
      a.src = first
      a.dataset.started = '1'
      a.play().catch(() => {}) // dentro do toque (exigência do iPhone)
    }
    onFirstTap?.()
    setI(0)
  }

  const sc = i >= 0 ? scenes[i] : null
  return (
    <m.div
      role="dialog"
      aria-modal="true"
      aria-label={`Historinha: O Reino Encantado da ${EVENT.childFirstName}`}
      className="fixed inset-0 z-[80] overflow-hidden bg-[#140E26] text-white"
      animate={leaving ? { opacity: 0 } : { opacity: 1 }}
      transition={{ duration: 0.9, ease: 'easeInOut' }}
    >
      {/* tela de título */}
      {i < 0 && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-[linear-gradient(180deg,#1E1638_0%,#3D2A6E_45%,#8E5FA8_100%)] px-8 text-center">
          <div className="story-stars pointer-events-none absolute inset-0" aria-hidden="true" />
          {scenes[0]?.poster && <img src={scenes[0].poster} alt="" className="absolute inset-0 h-full w-full object-cover opacity-35" />}
          <m.p className="relative font-sans text-xs font-semibold uppercase tracking-[0.4em] text-white/85" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1.2 }}>
            Uma historinha mágica
          </m.p>
          <m.p className="relative mt-3 font-bubble bubble-story text-[clamp(1.9rem,8.6vw,2.7rem)] leading-tight" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 1.4, delay: 0.3 }}>
            O Reino Encantado da {EVENT.childFirstName}
          </m.p>
          <m.button
            ref={btnRef}
            type="button"
            onClick={begin}
            className="btn-magic relative mt-10 min-h-[58px] px-9 text-lg"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: [0, -5, 0] }}
            transition={{ opacity: { delay: 1 }, y: { duration: 2.4, repeat: Infinity } }}
          >
            ▶ Assistir a historinha
          </m.button>
          <p className="relative mt-3 font-sans text-sm text-white/75">Ligue o som 🔊</p>
        </div>
      )}

      {/* cena em vídeo */}
      <AnimatePresence>
        {sc && (
          <m.div key={i} className="absolute inset-0" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.6 }}>
            <video
              ref={videoRef}
              className="absolute inset-0 h-full w-full object-cover"
              src={sc.video}
              poster={sc.poster}
              autoPlay
              muted
              playsInline
              preload="auto"
              aria-hidden="true"
            />
            {/* degradê para a legenda ficar legível */}
            <div className="pointer-events-none absolute inset-x-0 bottom-0 h-[42%] bg-gradient-to-t from-black/70 via-black/35 to-transparent" aria-hidden="true" />
            <div className="absolute inset-x-0 bottom-[calc(9vh+1.2rem)] px-6 text-center">
              <p className="font-sans text-[0.7rem] font-semibold uppercase tracking-[0.3em] text-white/80">{sc.title}</p>
              <m.p
                key={`t${i}`}
                className="mx-auto mt-2 max-w-[26ch] font-bubble bubble-story normal-case text-[clamp(1.2rem,5.4vw,1.65rem)] leading-[1.25]"
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.3 }}
                aria-live="polite"
              >
                {fill(sc.text)}
              </m.p>
            </div>
          </m.div>
        )}
      </AnimatePresence>

      {sc && sc.stars != null && (
        <div className="absolute inset-x-0 top-[calc(9vh+0.6rem)] z-30 flex justify-center">
          <Slots count={sc.stars} />
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
