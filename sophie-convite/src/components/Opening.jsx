import { m, AnimatePresence, useReducedMotion } from 'framer-motion'
import { useState } from 'react'
import { EVENT } from '../config/event.js'
import { DriftCloud, Rainbow, Twinkles, Heart, Bow, CloudEdge } from './Decor.jsx'
import Particles from './Particles.jsx'
import Pattern from './Pattern.jsx'

const TWINKLES = [
  [8, 14, 16, 0], [86, 10, 20, 0.6, '#E58DB8'], [18, 46, 12, 1.2], [90, 40, 14, 0.3, '#B9A4E6'],
  [72, 22, 10, 1.6], [12, 78, 14, 0.9, '#9FD3E6'], [84, 74, 18, 0.2], [30, 8, 10, 1.4, '#E58DB8'],
]

export default function Opening({ opened, onOpen }) {
  const reduce = useReducedMotion()
  const [bursting, setBursting] = useState(false)

  const handleOpen = () => {
    if (bursting) return
    if (reduce) return onOpen()
    setBursting(true)
    setTimeout(() => {
      onOpen()
      setBursting(false)
    }, 850)
  }

  return (
    <section
      id="abertura"
      aria-label="Abertura do convite"
      className="relative isolate flex min-h-[100svh] flex-col items-center justify-center overflow-hidden bg-gradient-to-b from-azul via-[#E6E0FA] to-rosa px-6 pb-16 pt-12 text-center"
    >
      <Pattern opacity={0.22} />

      {/* sol / brilho suave */}
      <div aria-hidden="true" className="absolute left-1/2 top-[18%] h-72 w-72 -translate-x-1/2 rounded-full bg-amarelo/70 blur-3xl" />

      {/* arco-íris */}
      <div aria-hidden="true" className="absolute left-1/2 top-[13%] w-[min(118vw,560px)] -translate-x-1/2">
        <m.div initial={{ opacity: 0, y: 30, scale: 0.92 }} animate={{ opacity: 0.95, y: 0, scale: 1 }} transition={{ duration: 1.4, ease: 'easeOut' }}>
          <Rainbow className="h-auto w-full" />
        </m.div>
      </div>

      {/* nuvens */}
      <DriftCloud className="left-[-14%] top-[30%] h-20 w-40 sm:h-28 sm:w-56" distance={22} duration={10} />
      <DriftCloud className="right-[-12%] top-[24%] h-16 w-36 sm:h-24 sm:w-48" distance={-20} duration={8} delay={1} />
      <DriftCloud className="bottom-[-3%] left-[-8%] h-28 w-60 opacity-95" distance={16} duration={11} />
      <DriftCloud className="bottom-[-5%] right-[-14%] h-32 w-72" distance={-18} duration={12} delay={0.5} />
      <DriftCloud className="bottom-[10%] right-[8%] h-12 w-24 opacity-80" distance={12} duration={7} />

      <Twinkles items={TWINKLES} />

      <m.div
        className="relative z-10 mt-[12vh] flex max-w-md flex-col items-center"
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.9, delay: 0.3 }}
      >
        <Bow className="mb-1 h-8 w-14" fill="#F2B6D2" />
        <p className="font-sans text-sm font-medium uppercase tracking-[0.32em] text-ameixaSoft">Você foi convidado para</p>
        <h1 className="mt-3 font-sans text-[clamp(1.35rem,6vw,1.9rem)] font-medium leading-tight text-ameixa">
          O Mundo Encantado da
          <span className="sophie-lettering mt-1 block font-script text-[clamp(4.6rem,24vw,7.5rem)] font-bold leading-[0.95]">
            {EVENT.childFirstName}
          </span>
        </h1>

        <div className="mt-4 flex items-center gap-2 rounded-full bg-white/75 px-5 py-2 shadow-soft ring-1 ring-white backdrop-blur-sm">
          <Heart className="h-4 w-4" fill="#E58DB8" />
          <span className="font-sans text-lg font-semibold text-ameixa">
            <span className="text-douradoEscuro">{EVENT.age}</span> aninhos
          </span>
          <Heart className="h-4 w-4" fill="#E58DB8" />
        </div>

        <div className="relative mt-9">
          <AnimatePresence>{bursting && <Particles />}</AnimatePresence>
          <m.button
            type="button"
            onClick={handleOpen}
            aria-controls="jogo"
            aria-expanded={opened}
            className="btn-magic relative z-10 min-h-[56px] px-8 text-lg"
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.96 }}
            animate={reduce || bursting ? undefined : { y: [0, -4, 0] }}
            transition={{ duration: 2.4, repeat: Infinity, ease: 'easeInOut' }}
          >
            <span aria-hidden="true">✨</span> {opened ? 'Ver o convite de novo' : 'Abrir convite mágico'}
          </m.button>
        </div>
        {!opened && <p className="mt-4 font-sans text-sm text-ameixaSoft">Toque para começar a magia</p>}
      </m.div>

      <CloudEdge fill="#F8CDE3" className="z-10" />

      {/* flash pastel na abertura */}
      <AnimatePresence>
        {bursting && (
          <m.div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 z-20 bg-white"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 0.55, 0] }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.85 }}
          />
        )}
      </AnimatePresence>
    </section>
  )
}
