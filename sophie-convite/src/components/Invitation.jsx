import { m, useReducedMotion } from 'framer-motion'
import { EVENT } from '../config/event.js'
import Unicorn from './Unicorn.jsx'
import Reveal from './Reveal.jsx'
import { Divider, Twinkles, DriftCloud, Cloud } from './Decor.jsx'
import Pattern from './Pattern.jsx'

export default function Invitation() {
  const reduce = useReducedMotion()
  return (
    <section id="convite" aria-labelledby="convite-titulo" className="relative overflow-hidden bg-[#FFFAFC] px-5 pb-16 pt-14">
      <Pattern opacity={0.28} />
      <DriftCloud className="left-[-10%] top-10 h-16 w-36 opacity-70" shade="#F1E6F7" tone="#FBF4FF" distance={14} />
      <DriftCloud className="right-[-12%] top-48 h-14 w-32 opacity-70" shade="#E1F0F7" tone="#F4FBFE" distance={-14} duration={10} />
      <Twinkles items={[[10, 30, 14, 0], [88, 18, 18, 0.8, '#E58DB8'], [86, 56, 12, 1.4, '#B9A4E6']]} />

      <div className="relative mx-auto max-w-md text-center">
        {/* unicórnio sobre o arco-íris */}
        <div className="relative mx-auto w-[min(78vw,300px)]">
          {/* halo suave no lugar do arco-íris: o unicórnio vira o protagonista */}
          <div aria-hidden="true" className="absolute left-1/2 top-[8%] aspect-square w-[92%] -translate-x-1/2 rounded-full bg-[radial-gradient(circle_at_50%_45%,#FFF0B9_0%,#F8CDE3_42%,rgba(220,204,247,.55)_64%,rgba(220,204,247,0)_72%)]" />
          <div aria-hidden="true" className="absolute left-1/2 top-[8%] aspect-square w-[92%] -translate-x-1/2 rounded-full ring-1 ring-dourado/50" />
          <m.div
            initial={{ opacity: 0, y: 40, scale: 0.85 }}
            whileInView={{ opacity: 1, y: 0, scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: 'spring', stiffness: 90, damping: 14 }}
          >
            <m.div
              animate={reduce ? undefined : { y: [0, -8, 0], rotate: [-1.2, 1.2, -1.2] }}
              transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
            >
              <Unicorn idPrefix="inv" className="relative h-auto w-full drop-shadow-[0_18px_24px_rgba(190,140,190,.35)]" />
            </m.div>
          </m.div>
          <Cloud className="relative mx-auto -mt-12 h-auto w-[92%] drop-shadow-[0_6px_8px_rgba(190,150,200,.25)]" shade="#EFE4F6" />
        </div>

        <Reveal delay={0.1}>
          <p className="mt-4 font-sans text-xs font-semibold uppercase tracking-[0.3em] text-ameixaSoft">Aniversário de</p>
          <h2 id="convite-titulo" className="mt-1">
            <span className="sophie-lettering block font-script text-[clamp(3.2rem,15vw,4.6rem)] font-bold leading-none">
              {EVENT.childFirstName}
            </span>
            <span className="mt-2 block font-sans text-[clamp(1.05rem,4.6vw,1.3rem)] font-medium text-ameixa">
              {EVENT.childFullName}
            </span>
          </h2>
        </Reveal>

        <Reveal delay={0.2}>
          <div className="mx-auto mt-5 flex w-fit items-center gap-3 rounded-full bg-gradient-to-r from-amarelo via-white to-amarelo px-6 py-2 ring-1 ring-dourado/60">
            <span className="font-script text-4xl font-bold leading-none text-douradoEscuro">{EVENT.age}</span>
            <span className="font-sans text-lg font-medium text-ameixa">anos de pura magia</span>
          </div>
        </Reveal>

        <Reveal delay={0.25}>
          <Divider />
        </Reveal>

        <Reveal delay={0.3}>
          <p className="mx-auto mt-3 max-w-[34ch] text-balance font-sans text-[1.08rem] leading-relaxed text-ameixa">
            {EVENT.message}
          </p>
        </Reveal>
      </div>
    </section>
  )
}
