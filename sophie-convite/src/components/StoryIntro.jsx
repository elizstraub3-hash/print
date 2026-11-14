import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useCallback, useEffect, useRef, useState } from 'react'
import { EVENT, STORY, CHILD_IMAGES, TEXT_ART } from '../config/event.js'
import { POSTER } from './Unicorn3D.jsx'
import { Rainbow, Cloud } from './Decor.jsx'
import { sparkle } from '../lib/sfx.js'

const fill = (t) => t.replaceAll('{nome}', EVENT.childFirstName)

/** céu: noite estrelada que vai amanhecendo em tons pastel a cada cena */
const SKIES = [
  'linear-gradient(180deg,#1E1638 0%,#3B2A68 45%,#8E5FA8 100%)',
  'linear-gradient(180deg,#2C2152 0%,#6A4C93 50%,#E59BC6 100%)',
  'linear-gradient(180deg,#5C4A9A 0%,#B48AD8 50%,#F8CDE3 100%)',
  'linear-gradient(180deg,#9FCBEA 0%,#DCCCF7 50%,#F8CDE3 100%)',
]

/** céu estrelado em UMA camada (gradientes) com brilho via CSS → leve */
function Stars() {
  return <div className="story-stars pointer-events-none absolute inset-0" aria-hidden="true" />
}

function SceneArt({ art }) {
  if (art === 'sky')
    return (
      <div className="absolute inset-0" aria-hidden="true">
        <m.div className="absolute left-1/2 top-[40%] w-[130%] -translate-x-1/2" initial={{ opacity: 0, y: 60 }} animate={{ opacity: 0.9, y: 0 }} transition={{ duration: 2.5, ease: 'easeOut' }}>
          <Rainbow className="h-auto w-full" />
        </m.div>
        <m.div className="absolute bottom-[14%] left-[-20%] w-[80%]" animate={{ x: [0, 30] }} transition={{ duration: 6, ease: 'linear' }}>
          <Cloud className="h-auto w-full" />
        </m.div>
        <m.div className="absolute bottom-[8%] right-[-25%] w-[85%]" animate={{ x: [0, -30] }} transition={{ duration: 6, ease: 'linear' }}>
          <Cloud className="h-auto w-full" />
        </m.div>
      </div>
    )
  if (art === 'princess')
    return (
      <div className="absolute inset-x-0 bottom-[11%] top-[30%] flex items-end justify-center" aria-hidden="true">
        <div className="absolute bottom-[4%] left-1/2 h-[70%] w-[78%] -translate-x-1/2 rounded-full bg-[radial-gradient(circle,rgba(255,240,185,.85),rgba(248,205,227,.4)_40%,transparent_68%)]" />
        {CHILD_IMAGES.photo ? (
          <m.img
            src={CHILD_IMAGES.photo}
            alt=""
            className="relative h-full w-auto object-contain [will-change:transform,opacity]"
            initial={{ opacity: 0, scale: 0.9, y: 30 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ duration: 1.8, ease: 'easeOut' }}
          />
        ) : (
          <img src={POSTER} alt="" className="relative h-[70%] w-auto" />
        )}
      </div>
    )
  if (art === 'unicorn')
    return (
      <div className="absolute inset-0" aria-hidden="true">
        <m.img
          src={POSTER}
          alt=""
          className="absolute top-[42%] h-[34%] w-auto [will-change:transform,left]"
          initial={{ left: '-45%', rotate: -8 }}
          animate={{ left: ['-45%', '22%', '18%'], y: [0, -30, 0, -14, 0], rotate: [-8, 4, 0] }}
          transition={{ duration: 3.4, ease: 'easeInOut' }}
        />
        <m.div className="absolute left-0 top-[58%] h-2 w-[60%] rounded-full bg-gradient-to-r from-transparent via-white/80 to-amarelo/80" initial={{ scaleX: 0, originX: 0 }} animate={{ scaleX: 1 }} transition={{ duration: 2.4 }} />
      </div>
    )
  if (art === 'invite')
    return (
      <div className="absolute inset-x-0 top-[34%] flex justify-center" aria-hidden="true">
        {TEXT_ART.invite?.src && (
          <m.img
            src={TEXT_ART.invite.src}
            alt=""
            className="w-[86%] max-w-[24rem] [will-change:transform,opacity] [transform:translateZ(0)]"
            initial={{ opacity: 0, scale: 0.8, rotate: -6, y: 60 }}
            animate={{ opacity: 1, scale: 1, rotate: 0, y: 0 }}
            transition={{ type: 'spring', stiffness: 70, damping: 11, delay: 0.3 }}
          />
        )}
      </div>
    )
  return null
}

export default function StoryIntro({ onDone, onLeave, onFirstTap }) {
  const reduce = useReducedMotion()
  const scenes = STORY.scenes
  const [i, setI] = useState(-1) // -1 = tela "toque para começar"
  const [leaving, setLeaving] = useState(false)
  const timer = useRef(null)
  const btnRef = useRef(null)

  const iRef = useRef(i)
  iRef.current = i
  const doneRef = useRef(onDone)
  doneRef.current = onDone
  const leavingRef = useRef(false)

  const finish = useCallback(() => {
    if (leavingRef.current) return
    leavingRef.current = true
    onLeave?.()
    clearTimeout(timer.current)
    setLeaving(true)
    setTimeout(() => doneRef.current?.(), reduce ? 0 : 900)
  }, [reduce])

  const next = useCallback(() => {
    clearTimeout(timer.current)
    const v = iRef.current
    if (v + 1 >= scenes.length) finish()
    else setI(v + 1)
  }, [scenes.length, finish])

  // avanço automático
  // narração por cena: a cena dura o tempo da fala (+ respiro).
  // Um único <audio> destravado no toque inicial (exigência do iPhone).
  const voiceRef = useRef(null)
  const firstPlayed = useRef(false)
  useEffect(() => {
    if (i < 0 || leaving) return
    const src = scenes[i].audio
    const a = voiceRef.current
    const fallback = () => (timer.current = setTimeout(next, STORY.secondsPerScene * 1000))
    if (src && a) {
      a.onended = () => (timer.current = setTimeout(next, 700))
      a.onerror = fallback
      if (i === 0 && firstPlayed.current) {
        // já começou a tocar dentro do toque
      } else {
        a.src = src
        a.currentTime = 0
        a.play().catch(fallback)
      }
      // segurança: se o áudio travar, a história segue mesmo assim
      const guard = setTimeout(() => a.paused && a.currentTime === 0 && fallback(), 2500)
      return () => {
        clearTimeout(timer.current)
        clearTimeout(guard)
        a.onended = a.onerror = null
      }
    }
    fallback()
    return () => clearTimeout(timer.current)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [i, leaving])

  // ao sair (fim ou "pular"), silencia a narração
  useEffect(() => {
    if (leaving) voiceRef.current?.pause()
  }, [leaving])
  useEffect(() => () => voiceRef.current?.pause(), [])

  useEffect(() => {
    btnRef.current?.focus()
    const onKey = (e) => e.key === 'Escape' && finish()
    window.addEventListener('keydown', onKey)
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      window.removeEventListener('keydown', onKey)
      document.body.style.overflow = prev
    }
  }, [finish])

  // decodifica as imagens das cenas já na tela de título (sem travar no meio)
  useEffect(() => {
    ;[CHILD_IMAGES.photo, POSTER, TEXT_ART.invite?.src].filter(Boolean).forEach((src) => {
      const im = new Image()
      im.src = src
      im.decode?.().catch(() => {})
    })
  }, [])

  const begin = () => {
    const first = scenes[0]?.audio
    if (first) {
      const a = voiceRef.current || (voiceRef.current = new Audio())
      a.preload = 'auto'
      a.src = first
      a.play().then(() => (firstPlayed.current = true)).catch(() => {}) // dentro do toque
      firstPlayed.current = true
      // pré-carrega as próximas falas
      scenes.slice(1).forEach((sc) => sc.audio && fetch(sc.audio).catch(() => {}))
    } else {
      sparkle()
    }
    onFirstTap?.() // gesto do usuário: libera música
    setI(0)
  }

  const sky = SKIES[Math.max(0, Math.min(SKIES.length - 1, i))]

  return (
    <m.div
      role="dialog"
      aria-modal="true"
      aria-label={`Historinha de abertura do convite da ${EVENT.childFirstName}`}
      className="fixed inset-0 z-[80] overflow-hidden bg-[#140E26] text-white"
      animate={leaving ? { opacity: 0 } : { opacity: 1 }}
      transition={{ duration: 0.9, ease: 'easeInOut' }}
      onClick={(e) => i >= 0 && !e.target.closest('button') && next()}
    >
      {/* céu com "câmera" lenta (Ken Burns) */}
      <m.div
        key={`sky-${Math.max(0, i)}`}
        className="absolute inset-0"
        style={{ background: sky }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut' }}
      />
      {i < 3 && <Stars />}

      <AnimatePresence>
        {i >= 0 && (
          <m.div key={i} className="absolute inset-0" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.8 }}>
            <SceneArt art={scenes[i].art} />
            <div className="absolute inset-x-0 top-[13%] px-7 text-center">
              <m.p
                className="mx-auto max-w-[19ch] text-balance font-bubble bubble-story normal-case text-[clamp(1.5rem,6.6vw,2.1rem)] leading-[1.2]"
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1.2, delay: 0.3 }}
              >
                {fill(scenes[i].text)}
              </m.p>
            </div>
          </m.div>
        )}
      </AnimatePresence>

      {/* tela inicial */}
      {i < 0 && (
        <div className="absolute inset-0 flex flex-col items-center justify-center px-8 text-center">
          <m.p className="relative font-sans text-xs font-semibold uppercase tracking-[0.4em] text-white/80" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1.2 }}>
            Uma historinha mágica
          </m.p>
          <m.p
            className="relative mt-3 font-bubble bubble-story text-[clamp(1.9rem,8.6vw,2.7rem)] leading-tight"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1.6, delay: 0.3 }}
          >
            O Mundo Encantado da {EVENT.childFirstName}
          </m.p>
          <m.button
            ref={btnRef}
            type="button"
            onClick={begin}
            className="btn-magic relative mt-10 min-h-[58px] px-9 text-lg"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: [0, -5, 0] }}
            transition={{ opacity: { delay: 1.2 }, y: { duration: 2.4, repeat: Infinity } }}
          >
            ✨ Toque para começar
          </m.button>
        </div>
      )}

      {/* faixas de cinema + progresso + pular */}
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[9vh] min-h-[44px] bg-black/85" aria-hidden="true" />
      <div className="absolute inset-x-0 bottom-0 flex h-[9vh] min-h-[56px] items-center justify-between bg-black/85 px-4 pb-[env(safe-area-inset-bottom)]">
        <div className="flex flex-1 gap-1.5 pr-4" aria-hidden="true">
          {scenes.map((_, k) => (
            <span key={k} className="h-1 flex-1 overflow-hidden rounded-full bg-white/25">
              {k < i && <span className="block h-full w-full bg-white" />}
              {k === i && !leaving && (
                <m.span className="block h-full bg-white" initial={{ width: '0%' }} animate={{ width: '100%' }} transition={{ duration: STORY.secondsPerScene, ease: 'linear' }} />
              )}
            </span>
          ))}
        </div>
        <button type="button" onClick={finish} className="min-h-[44px] rounded-full px-4 font-sans text-sm font-semibold text-white/90 ring-1 ring-white/40">
          Pular história ›
        </button>
      </div>
    </m.div>
  )
}
