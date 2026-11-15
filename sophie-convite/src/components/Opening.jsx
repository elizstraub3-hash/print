import { m, useReducedMotion } from 'framer-motion'
import { useRef, useState } from 'react'
import { EVENT, TITLE_ART, BACKGROUNDS } from '../config/event.js'
import { DriftCloud, Rainbow, Twinkles, Heart, CloudEdge } from './Decor.jsx'
import Pattern, { PhotoPattern } from './Pattern.jsx'
import { burstFrom } from '../lib/glitter.js'
import { sparkle } from '../lib/sfx.js'

const TWINKLES = [
  [8, 14, 16, 0], [88, 9, 20, 0.6, '#E58DB8'], [6, 48, 12, 1.2], [92, 44, 14, 0.3, '#B9A4E6'],
  [80, 26, 10, 1.6], [12, 80, 14, 0.9, '#9FD3E6'], [88, 76, 18, 0.2], [26, 6, 10, 1.4, '#E58DB8'],
]

function TextTitle() {
  return (
    <>
      <p className="font-sans text-[clamp(1.2rem,5.4vw,1.6rem)] font-medium text-ameixa">O Mundo Encantado da</p>
      <span className="block font-bubble bubble-pink text-[clamp(3.4rem,17vw,5.5rem)] leading-[0.95]">{EVENT.childFirstName}</span>
      <span className="mt-2 inline-flex items-center gap-2 rounded-full bg-white/75 px-5 py-1.5 font-sans text-lg font-semibold text-ameixa shadow-soft">
        <Heart className="h-4 w-4" fill="#E58DB8" /> {EVENT.age} aninhos <Heart className="h-4 w-4" fill="#E58DB8" />
      </span>
    </>
  )
}

export default function Opening({ opened, onOpen }) {
  const reduce = useReducedMotion()
  const [hop, setHop] = useState(0)
  const btnRef = useRef(null)
  const uniWrapRef = useRef(null)
  const [busy, setBusy] = useState(false)
  const [pressed, setPressed] = useState(false)

  const handleOpen = async () => {
    if (busy) return
    setBusy(true)
    sparkle()
    // a Layla dá um pulinho e "aperta" o botão junto com o convidado
    setHop((h) => h + 1)
    await new Promise((r) => setTimeout(r, reduce ? 0 : 420))
    setPressed(true)
    navigator.vibrate?.(20)
    burstFrom(btnRef.current, { count: 120, speed: 11 })
    setTimeout(() => setPressed(false), 160)
    await new Promise((r) => setTimeout(r, reduce ? 0 : 600))
    onOpen()
    setBusy(false)
  }

  const petUnicorn = () => {
    setHop((h) => h + 1)
    sparkle()
    burstFrom(uniWrapRef.current, { count: 40, speed: 7, angle: -Math.PI / 2, spread: 2 })
  }

  return (
    <section
      id="abertura"
      aria-label="Abertura do convite"
      className="relative isolate flex min-h-[100svh] flex-col items-center justify-center overflow-hidden bg-gradient-to-b from-azul via-[#E6E0FA] to-rosa px-4 pb-14 pt-[max(4.25rem,calc(env(safe-area-inset-top)+3.5rem))] text-center"
    >
      {BACKGROUNDS.opening ? <PhotoPattern src={BACKGROUNDS.opening} veil={0.62} /> : <Pattern opacity={0.2} />}
      <div aria-hidden="true" className="absolute left-1/2 top-[30%] h-80 w-80 -translate-x-1/2 rounded-full bg-white/50 blur-3xl" />

      {!TITLE_ART.src && (
        <div aria-hidden="true" className="absolute left-1/2 top-[10%] w-[min(118vw,560px)] -translate-x-1/2 opacity-90">
          <Rainbow className="h-auto w-full" />
        </div>
      )}

      <DriftCloud className="left-[-16%] top-[14%] h-16 w-36 sm:h-24 sm:w-52" distance={22} duration={10} />
      <DriftCloud className="right-[-14%] top-[6%] h-14 w-32 sm:h-20 sm:w-44" distance={-20} duration={8} delay={1} />
      <DriftCloud className="bottom-[2%] left-[-10%] h-24 w-56 opacity-95" distance={16} duration={11} />
      <DriftCloud className="bottom-[-2%] right-[-16%] h-28 w-64" distance={-18} duration={12} delay={0.5} />
      <Twinkles items={TWINKLES} />

      <div className="relative z-10 flex w-full max-w-md flex-col items-center">
        <m.p
          className="font-sans text-xs font-semibold uppercase tracking-[0.3em] text-ameixaSoft"
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          ✦ O Mundo Encantado da {EVENT.childFirstName} ✦
        </m.p>

        <h1 className="mt-2 w-full">
          {TITLE_ART.src ? (
            <m.img
              src={TITLE_ART.src}
              alt={TITLE_ART.alt}
              width={TITLE_ART.width}
              height={TITLE_ART.height}
              fetchpriority="high"
              decoding="async"
              className="mx-auto h-auto w-[min(94vw,27rem)]"
              initial={{ opacity: 0, scale: 0.85, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ type: 'spring', stiffness: 110, damping: 13, delay: 0.15 }}
            />
          ) : (
            <TextTitle />
          )}
        </h1>

        {/* Layla acenando logo acima do botão */}
        <m.div
          ref={uniWrapRef}
          className="relative z-10 -mb-5 mt-[-0.5rem] h-[clamp(9.5rem,24svh,13rem)] w-[clamp(9.5rem,24svh,13rem)]"
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.45 }}
        >
          <div aria-hidden="true" className="absolute inset-x-[-12%] bottom-[2%] h-[38%] rounded-[50%] bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,.95)_0%,rgba(255,255,255,.7)_45%,rgba(255,255,255,0)_70%)]" />
          <button type="button" onClick={petUnicorn} aria-label="Layla, a unicórnio da Sophie — toque para fazer carinho" className="relative block h-full w-full" style={{ touchAction: 'manipulation' }}>
            <m.img
              key={hop}
              src="/img/layla/layla-acenando.webp"
              alt=""
              draggable="false"
              className="pointer-events-none mx-auto h-full w-auto object-contain drop-shadow-[0_12px_14px_rgba(190,120,170,.35)]"
              initial={false}
              animate={reduce ? undefined : hop ? { y: [0, -34, 6, 0], rotate: [0, -6, 4, 0], scaleY: [1, 1.05, 0.92, 1] } : { y: [0, -6, 0] }}
              transition={hop ? { duration: 0.75, ease: 'easeOut' } : { duration: 2.6, repeat: Infinity, ease: 'easeInOut' }}
            />
          </button>
        </m.div>

        <div className="relative">
          <m.button
            ref={btnRef}
            type="button"
            onClick={handleOpen}
            disabled={busy}
            aria-controls="jogo"
            aria-expanded={opened}
            className="btn-magic relative min-h-[58px] px-8 text-lg disabled:cursor-wait"
            animate={pressed ? { scale: 0.9, y: 3 } : { scale: 1, y: 0 }}
            transition={{ type: 'spring', stiffness: 600, damping: 18 }}
            whileHover={busy ? undefined : { scale: 1.04 }}
          >
            <span aria-hidden="true">✨</span> {opened ? 'Ver o convite de novo' : 'Abrir convite mágico'}
          </m.button>
        </div>
        {!opened && <p className="mt-3 font-sans text-sm text-ameixaSoft">Toque no botão — a Layla te ajuda!</p>}
      </div>

      <CloudEdge fill="#F8CDE3" className="z-10" />
    </section>
  )
}
