import { m, AnimatePresence } from 'framer-motion'
import { useEffect, useState } from 'react'
import { EVENT } from '../config/event.js'
import { DATE_LONG, TIME_LABEL, SHORT_ADDRESS, MAPS_URL, getCountdown } from '../lib/event-utils.js'
import { CalendarIcon, ClockIcon, PinIcon } from './Icons.jsx'
import Reveal from './Reveal.jsx'
import Pattern from './Pattern.jsx'
import { Heart } from './Decor.jsx'
import CakeStage from './CakeStage.jsx'

const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1)

function InfoCard({ icon: Icon, label, children, tint, delay }) {
  return (
    <Reveal delay={delay}>
      <div className="flex items-start gap-4 rounded-3xl bg-white/90 p-5 text-left shadow-soft ring-1 ring-white">
        <span className={`grid h-12 w-12 shrink-0 place-items-center rounded-2xl ${tint} text-ameixa`}>
          <Icon className="h-6 w-6" />
        </span>
        <div className="min-w-0">
          <p className="font-sans text-xs font-semibold uppercase tracking-[0.2em] text-ameixaSoft">{label}</p>
          <div className="mt-1 font-sans text-[1.06rem] font-medium leading-snug text-ameixa">{children}</div>
        </div>
      </div>
    </Reveal>
  )
}

function Unit({ value, label }) {
  const v = String(value).padStart(2, '0')
  return (
    <div className="flex flex-col items-center rounded-2xl bg-white/90 px-1 py-3 shadow-soft ring-1 ring-white">
      <div className="relative h-9 overflow-hidden font-sans text-[1.9rem] font-semibold leading-9 tabular-nums text-ameixa">
        <AnimatePresence mode="popLayout" initial={false}>
          <m.span key={v} className="block" initial={{ y: -20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: 20, opacity: 0 }} transition={{ duration: 0.3 }}>
            {v}
          </m.span>
        </AnimatePresence>
      </div>
      <span className="mt-1 font-sans text-[0.7rem] font-semibold uppercase tracking-[0.12em] text-ameixaSoft">{label}</span>
    </div>
  )
}

function Countdown() {
  const [c, setC] = useState(() => getCountdown())
  useEffect(() => {
    if (c.phase === 'after') return
    const id = setInterval(() => setC(getCountdown()), 1000)
    return () => clearInterval(id)
  }, [c.phase])

  if (c.phase === 'live')
    return (
      <p className="rounded-3xl bg-white/90 px-5 py-5 font-sans text-lg font-semibold text-ameixa shadow-soft">
        ✨ A festa está acontecendo agora! ✨
      </p>
    )
  if (c.phase === 'after')
    return (
      <p className="rounded-3xl bg-white/90 px-5 py-5 font-sans text-lg font-medium text-ameixa shadow-soft">
        Essa festa mágica já aconteceu. Obrigada por fazer parte da história da {EVENT.childFirstName}! 💖
      </p>
    )
  return (
    <div>
      <p className="mb-3 font-sans text-sm font-semibold uppercase tracking-[0.2em] text-ameixaSoft">
        {c.isToday ? 'É hoje! Faltam só' : 'Faltam'}
      </p>
      {/* leitores de tela recebem um resumo, sem anúncios a cada segundo */}
      <p className="sr-only">
        Faltam {c.days} dias, {c.hours} horas e {c.minutes} minutos para a festa.
      </p>
      <div className="grid grid-cols-4 gap-2" aria-hidden="true">
        <Unit value={c.days} label={c.days === 1 ? 'dia' : 'dias'} />
        <Unit value={c.hours} label="horas" />
        <Unit value={c.minutes} label="min" />
        <Unit value={c.seconds} label="seg" />
      </div>
    </div>
  )
}

export default function Details() {
  return (
    <section id="informacoes" aria-labelledby="info-titulo" className="relative overflow-hidden bg-gradient-to-b from-[#FFFAFC] via-lilas/50 to-azul/70 px-5 py-16">
      <Pattern opacity={0.2} />
      <div className="relative mx-auto max-w-md text-center">
        <Reveal>
          <p className="font-sans text-xs font-semibold uppercase tracking-[0.3em] text-ameixaSoft">Anote na agenda</p>
          <h2 id="info-titulo" className="mt-2 font-script text-[clamp(2.4rem,11vw,3.2rem)] font-bold leading-tight text-rosaForte">
            Quando e onde
          </h2>
        </Reveal>

        <Reveal className="mt-6">
          <CakeStage />
        </Reveal>

        <div className="mt-8 grid gap-3">
          <InfoCard icon={CalendarIcon} label="Data" tint="bg-rosa" delay={0.05}>
            {cap(DATE_LONG)}
          </InfoCard>
          <InfoCard icon={ClockIcon} label="Horário" tint="bg-amarelo" delay={0.1}>
            {TIME_LABEL} · almoço e tarde de alegria
          </InfoCard>
          <InfoCard icon={PinIcon} label="Local" tint="bg-menta" delay={0.15}>
            <span className="block">{EVENT.venueName}</span>
            <a href={MAPS_URL} target="_blank" rel="noopener noreferrer" className="mt-0.5 block py-1 text-[0.95rem] font-normal text-ameixaSoft underline decoration-dourado decoration-2 underline-offset-4 hover:text-ameixa">
              {SHORT_ADDRESS}
            </a>
          </InfoCard>
        </div>

        <Reveal delay={0.2} className="mt-8">
          <div className="flex items-center justify-center gap-2 pb-3" aria-hidden="true">
            <Heart className="h-3 w-3" fill="#E58DB8" />
            <span className="font-sans text-sm text-ameixaSoft">{getCountdown().phase === 'before' ? 'contagem regressiva · horário de Brasília' : 'horário de Brasília'}</span>
            <Heart className="h-3 w-3" fill="#E58DB8" />
          </div>
          <Countdown />
        </Reveal>
      </div>
    </section>
  )
}
