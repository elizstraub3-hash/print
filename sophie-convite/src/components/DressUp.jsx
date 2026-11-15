import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useRef, useState } from 'react'
import { EVENT, DRESSUP } from '../config/event.js'
import { burstFrom, rain } from '../lib/glitter.js'
import { fanfare, sparkle } from '../lib/sfx.js'
import Reveal from './Reveal.jsx'
import Pattern from './Pattern.jsx'

/** Provador mágico: arrastar o vestido do guarda-roupa até a Sophie */
export default function DressUp() {
  const reduce = useReducedMotion()
  const [open, setOpen] = useState(false)
  const [worn, setWorn] = useState(null) // índice do vestido vestido
  const [drag, setDrag] = useState(null) // { i, x, y, over }
  const [showReal, setShowReal] = useState(false)
  const [slide, setSlide] = useState(0)
  const swipeRef = useRef(null)
  const dollRef = useRef(null)
  if (!DRESSUP?.enabled) return null
  const { doll, fit, dresses, reveal } = DRESSUP

  const wear = (i) => {
    setWorn(i)
    setOpen(false)
    fanfare()
    burstFrom(dollRef.current, { count: 140, speed: 12 })
    rain({ count: 150, duration: 1200 })
    navigator.vibrate?.([20, 40, 20])
  }
  const takeOff = () => {
    setWorn(null)
    setShowReal(false)
    sparkle()
  }

  const isOver = (x, y) => {
    const r = dollRef.current?.getBoundingClientRect()
    return !!r && x > r.left && x < r.right && y > r.top && y < r.bottom
  }
  const onDown = (i) => (e) => {
    e.preventDefault()
    e.currentTarget.setPointerCapture?.(e.pointerId)
    setDrag({ i, x: e.clientX, y: e.clientY, over: false, moved: false, sx: e.clientX, sy: e.clientY })
  }
  const onMove = (e) => {
    if (!drag) return
    setDrag((d) => d && { ...d, x: e.clientX, y: e.clientY, over: isOver(e.clientX, e.clientY), moved: d.moved || Math.hypot(e.clientX - d.sx, e.clientY - d.sy) > 8 })
  }
  const onUp = (e) => {
    if (!drag) return
    const d = drag
    setDrag(null)
    if (!d.moved || isOver(e.clientX, e.clientY)) wear(d.i) // toque simples também veste
  }

  const dw = worn != null ? dresses[worn] : null
  const dressH = fit.height * 100
  const dressW = dw ? (dressH * (dw.w / dw.h) * doll.h) / doll.w : 0

  return (
    <section id="transformacao" aria-labelledby="dress-titulo" className="relative overflow-hidden bg-gradient-to-b from-[#FFFAFC] via-lilas/40 to-rosa/60 px-5 py-14 text-center">
      <Pattern opacity={0.2} />
      <div className="relative mx-auto max-w-md">
        <Reveal>
          <p className="font-sans text-xs font-bold uppercase tracking-[0.3em] text-ameixaSoft">Provador mágico</p>
          <h2 id="dress-titulo" className="mt-2 font-bubble bubble-pink text-[clamp(1.7rem,7.8vw,2.3rem)] leading-tight">
            Vista a {EVENT.childFirstName}!
          </h2>
          <p className="story-caption mx-auto mt-3 max-w-[28ch] text-lg">
            {worn == null ? `Abra o guarda-roupa e arraste um vestido até a ${EVENT.childFirstName}! 👗` : `Que linda! A ${EVENT.childFirstName} está com o ${dresses[worn].name}! 💖`}
          </p>
        </Reveal>

        {/* Sophie */}
        <div className="relative mx-auto mt-5 w-full max-w-[22rem] rounded-[2rem] bg-[radial-gradient(circle_at_50%_38%,#FFF0B9_0%,#F8CDE3_45%,#DCCCF7_100%)] px-6 pt-4 shadow-soft ring-4 ring-white">
          <div ref={dollRef} className={`relative mx-auto w-[66%] transition ${drag?.over ? 'scale-[1.03] drop-shadow-[0_0_24px_rgba(255,214,107,.95)]' : ''}`} style={{ aspectRatio: `${doll.w} / ${doll.h}` }}>
            <img src={doll.src} alt={`${EVENT.childFirstName} com a fantasia de unicórnio e a varinha`} className="absolute inset-0 h-full w-full object-contain" draggable="false" />
            <AnimatePresence>
              {dw && (
                <m.img
                  key={worn}
                  src={dw.src}
                  alt={`${EVENT.childFirstName} vestindo o ${dw.name}`}
                  draggable="false"
                  className="pointer-events-none absolute max-w-none drop-shadow-[0_6px_8px_rgba(120,60,120,.25)]"
                  style={{ top: `${fit.top * 100}%`, height: `${dressH}%`, width: `${dressW}%`, left: `${fit.centerX * 100 - dressW / 2}%` }}
                  initial={reduce ? false : { opacity: 0, scale: 1.4, y: -30 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  transition={{ type: 'spring', stiffness: 170, damping: 14 }}
                />
              )}
            </AnimatePresence>
            {drag?.over && <div className="pointer-events-none absolute inset-0 rounded-full border-4 border-dashed border-dourado/80" aria-hidden="true" />}
          </div>
        </div>

        {/* botões */}
        <div className="mt-5 flex flex-col items-center gap-2">
          {worn == null ? (
            <button type="button" onClick={() => setOpen((o) => !o)} aria-expanded={open} aria-controls="guarda-roupa" className="btn-magic min-h-[56px] px-8 text-lg">
              {open ? '✖ Fechar guarda-roupa' : '🚪 Abrir o guarda-roupa mágico'}
            </button>
          ) : (
            <>
              <button type="button" onClick={() => setOpen(true) || setWorn(null)} className="btn-ghost min-h-[48px] px-6">
                👗 Trocar de vestido
              </button>
              {reveal?.src && worn === 0 && (
                <button type="button" onClick={() => setShowReal(true)} className="btn-magic min-h-[56px] px-8 text-lg">
                  ✨ Ver a {EVENT.childFirstName} de verdade
                </button>
              )}
              <button type="button" onClick={takeOff} className="min-h-[44px] px-4 font-sans text-sm font-semibold text-ameixaSoft underline underline-offset-4">
                Tirar o vestido e brincar de novo
              </button>
            </>
          )}
        </div>

        {/* guarda-roupa */}
        <AnimatePresence>
          {open && worn == null && (
            <m.div
              id="guarda-roupa"
              className="mx-auto mt-4 max-w-[22rem] overflow-hidden rounded-[1.6rem] border-[6px] border-[#E9B8D6] bg-gradient-to-b from-[#FFF4FA] to-[#F6DDF0] p-4 shadow-soft"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <div className="mx-auto mb-3 h-1.5 w-3/4 rounded-full bg-dourado/70" aria-hidden="true" />
              <p className="font-sans text-sm font-bold text-ameixa">Arraste o vestido até a {EVENT.childFirstName} (ou toque nele)</p>
              <div className="mt-3 flex items-center justify-center gap-2">
                <button type="button" onClick={() => setSlide((v) => (v - 1 + dresses.length) % dresses.length)} aria-label="Vestido anterior" className="stepper-btn shrink-0 !h-12 !w-12 !bg-white shadow-soft">‹</button>
                <div
                  className="relative w-44 overflow-hidden"
                  onTouchStart={(e) => (swipeRef.current = e.touches[0].clientX)}
                  onTouchEnd={(e) => {
                    const dx = e.changedTouches[0].clientX - (swipeRef.current ?? e.changedTouches[0].clientX)
                    if (!drag?.moved && Math.abs(dx) > 50) setSlide((v) => (v + (dx < 0 ? 1 : -1) + dresses.length) % dresses.length)
                  }}
                >
                  <AnimatePresence mode="wait" initial={false}>
                    {(() => {
                      const d = dresses[slide]
                      return (
                        <m.button
                          key={slide}
                          type="button"
                          onPointerDown={onDown(slide)}
                          onPointerMove={onMove}
                          onPointerUp={onUp}
                          onPointerCancel={() => setDrag(null)}
                          onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && (e.preventDefault(), wear(slide))}
                          aria-label={`${d.name}: vestir na ${EVENT.childFirstName}`}
                          className={`flex w-44 flex-col items-center rounded-2xl bg-white p-2 shadow-soft ring-2 ring-rosa/60 ${drag?.i === slide && drag?.moved ? 'opacity-40' : ''}`}
                          style={{ touchAction: 'pan-y' }}
                          initial={{ opacity: 0, x: 40 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -40 }}
                          transition={{ duration: 0.2 }}
                        >
                          <img src={d.src} alt="" draggable="false" className="pointer-events-none h-40 w-auto object-contain" />
                          <span className="mt-1 font-sans text-xs font-bold text-ameixa">{d.name}</span>
                        </m.button>
                      )
                    })()}
                  </AnimatePresence>
                </div>
                <button type="button" onClick={() => setSlide((v) => (v + 1) % dresses.length)} aria-label="Próximo vestido" className="stepper-btn shrink-0 !h-12 !w-12 !bg-white shadow-soft">›</button>
              </div>
              <div className="mt-2 flex justify-center gap-1.5" aria-hidden="true">
                {dresses.map((_, k) => (
                  <span key={k} className={`h-2 rounded-full transition-all ${k === slide ? 'w-5 bg-rosaForte' : 'w-2 bg-rosa'}`} />
                ))}
              </div>
              <p className="mt-1 font-sans text-xs font-semibold text-ameixaSoft">{slide + 1} de {dresses.length} vestidos</p>
            </m.div>
          )}
        </AnimatePresence>
      </div>

      {/* vestido sendo arrastado */}
      {drag?.moved && (
        <img
          src={dresses[drag.i].src}
          alt=""
          aria-hidden="true"
          className="pointer-events-none fixed z-[90] h-40 w-auto -translate-x-1/2 -translate-y-1/2 drop-shadow-[0_12px_18px_rgba(120,60,120,.4)]"
          style={{ left: drag.x, top: drag.y }}
        />
      )}

      {/* foto real */}
      <AnimatePresence>
        {showReal && (
          <m.div className="fixed inset-0 z-[85] flex items-center justify-center bg-[#2B1D4A]/80 p-5" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={() => setShowReal(false)} role="dialog" aria-modal="true" aria-label="A Sophie com o vestido encantado">
            <m.div initial={{ scale: 0.85 }} animate={{ scale: 1 }} className="w-full max-w-[24rem] text-center">
              <img src={reveal.src} alt={`${EVENT.childFirstName} com o vestido encantado ao lado da Layla`} className="w-full rounded-[1.6rem] ring-4 ring-white" />
              <p className="story-caption mt-3 text-lg">Olha como a {EVENT.childFirstName} ficou linda! 💖</p>
              <button type="button" className="btn-ghost mt-3 px-6">Fechar</button>
            </m.div>
          </m.div>
        )}
      </AnimatePresence>
    </section>
  )
}
