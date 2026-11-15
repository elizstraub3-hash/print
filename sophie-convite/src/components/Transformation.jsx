import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useRef, useState } from 'react'
import { EVENT, TRANSFORM } from '../config/event.js'
import { burstFrom, rain } from '../lib/glitter.js'
import { fanfare, sparkle } from '../lib/sfx.js'
import Reveal from './Reveal.jsx'
import Pattern from './Pattern.jsx'

/** Antes × depois: o convidado usa a magia e a Sophie ganha o vestido encantado */
export default function Transformation() {
  const reduce = useReducedMotion()
  const [after, setAfter] = useState(false)
  const [flash, setFlash] = useState(0)
  const cardRef = useRef(null)
  if (!TRANSFORM?.enabled) return null
  const { before, after: aft } = TRANSFORM

  const toggle = () => {
    const next = !after
    setFlash((f) => f + 1)
    setTimeout(() => setAfter(next), reduce ? 0 : 280)
    if (next) {
      fanfare()
      burstFrom(cardRef.current, { count: 140, speed: 12 })
      rain({ count: 160, duration: 1200 })
    } else sparkle()
    navigator.vibrate?.(25)
  }

  return (
    <section id="transformacao" aria-labelledby="transf-titulo" className="relative overflow-hidden bg-gradient-to-b from-[#FFFAFC] via-lilas/40 to-rosa/60 px-5 py-14 text-center">
      <Pattern opacity={0.2} />
      <div className="relative mx-auto max-w-md">
        <Reveal>
          <p className="font-sans text-xs font-bold uppercase tracking-[0.3em] text-ameixaSoft">A magia das 5 estrelas</p>
          <h2 id="transf-titulo" className="mt-2 font-bubble bubble-pink text-[clamp(1.7rem,7.8vw,2.3rem)] leading-tight">
            A transformação da {EVENT.childFirstName}
          </h2>
        </Reveal>

        {/* seletor antes / depois */}
        <div className="mx-auto mt-5 inline-flex rounded-full bg-white/85 p-1 shadow-soft ring-1 ring-white" role="tablist" aria-label="Antes e depois">
          {[false, true].map((v) => (
            <button
              key={String(v)}
              type="button"
              role="tab"
              aria-selected={after === v}
              onClick={() => after !== v && toggle()}
              className={`min-h-[44px] rounded-full px-4 font-sans text-sm font-bold transition ${after === v ? 'bg-rosaForte text-white shadow-soft' : 'text-ameixa'}`}
            >
              {v ? 'Com o vestido ✨' : 'Antes'}
            </button>
          ))}
        </div>

        <div ref={cardRef} className="relative mx-auto mt-5 aspect-[3/4] w-full max-w-[22rem] overflow-hidden rounded-[2rem] bg-white shadow-soft ring-4 ring-white">
          <AnimatePresence mode="wait" initial={false}>
            {after ? (
              <m.img
                key="after"
                src={aft.src}
                alt={`${EVENT.childFirstName} com o vestido encantado, ao lado da Layla, em frente ao castelo`}
                width={aft.w}
                height={aft.h}
                loading="lazy"
                className="absolute inset-0 h-full w-full object-cover"
                initial={{ opacity: 0, scale: 1.08 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.7 }}
              />
            ) : (
              <m.div key="before" className="absolute inset-0 bg-[radial-gradient(circle_at_50%_40%,#FFF0B9_0%,#F8CDE3_45%,#DCCCF7_100%)]" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.5 }}>
                <img src={before.src} alt={`${EVENT.childFirstName} antes do vestido encantado, com a fantasia de unicórnio`} width={before.w} height={before.h} loading="lazy" className="absolute inset-x-0 bottom-0 mx-auto h-[94%] w-auto object-contain drop-shadow-[0_10px_14px_rgba(150,80,140,.3)]" />
              </m.div>
            )}
          </AnimatePresence>
          {/* clarão mágico */}
          <AnimatePresence>
            {flash > 0 && !reduce && (
              <m.div key={flash} className="pointer-events-none absolute inset-0 bg-white" initial={{ opacity: 0 }} animate={{ opacity: [0, 0.9, 0] }} transition={{ duration: 0.8 }} aria-hidden="true" />
            )}
          </AnimatePresence>
          <span className="absolute left-3 top-3 rounded-full bg-white/90 px-3 py-1 font-sans text-xs font-bold text-[#7B2E9E] shadow-soft">
            {after ? aft.label : before.label}
          </span>
        </div>

        <m.button
          type="button"
          onClick={toggle}
          className="btn-magic mt-5 min-h-[58px] px-8 text-lg"
          animate={reduce || after ? undefined : { scale: [1, 1.05, 1] }}
          transition={{ duration: 1.6, repeat: Infinity }}
        >
          {after ? '↺ Ver antes da magia' : '✨ Usar a magia das 5 estrelas'}
        </m.button>
        <p className="story-caption mx-auto mt-3 max-w-[28ch] text-lg">
          {after ? `Olha como a ${EVENT.childFirstName} ficou linda com o vestido encantado! 💖` : `Toque na magia e veja a ${EVENT.childFirstName} ganhar o vestido encantado!`}
        </p>
      </div>
    </section>
  )
}
