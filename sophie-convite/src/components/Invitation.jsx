import { m } from 'framer-motion'
import { useRef } from 'react'
import { EVENT, CHILD_IMAGES } from '../config/event.js'
import Unicorn3D from './Unicorn3D.jsx'
import { burstFrom } from '../lib/glitter.js'
import { sparkle } from '../lib/sfx.js'
import Reveal from './Reveal.jsx'
import { Divider, Twinkles, DriftCloud, Cloud } from './Decor.jsx'
import Pattern from './Pattern.jsx'
import MagicMenu from './MagicMenu.jsx'

export default function Invitation({ music }) {
  const uniRef = useRef(null)
  return (
    <section id="convite" aria-labelledby="convite-titulo" className="relative overflow-hidden bg-[#FFFAFC] px-5 pb-8 pt-14">
      <Pattern opacity={0.28} />
      <DriftCloud className="left-[-10%] top-10 h-16 w-36 opacity-70" shade="#F1E6F7" tone="#FBF4FF" distance={14} />
      <DriftCloud className="right-[-12%] top-48 h-14 w-32 opacity-70" shade="#E1F0F7" tone="#F4FBFE" distance={-14} duration={10} />
      <Twinkles items={[[10, 30, 14, 0], [88, 18, 18, 0.8, '#E58DB8'], [86, 56, 12, 1.4, '#B9A4E6']]} />

      <div className="relative mx-auto max-w-md text-center">
        {/* unicórnio sobre o arco-íris */}
        <div className="relative mx-auto w-[min(84vw,330px)]">
          {/* halo suave no lugar do arco-íris: o unicórnio vira o protagonista */}
          <div aria-hidden="true" className="absolute left-1/2 top-[8%] aspect-square w-[92%] -translate-x-1/2 rounded-full bg-[radial-gradient(circle_at_50%_45%,#FFF0B9_0%,#F8CDE3_42%,rgba(220,204,247,.55)_64%,rgba(220,204,247,0)_72%)]" />
          <div aria-hidden="true" className="absolute left-1/2 top-[8%] aspect-square w-[92%] -translate-x-1/2 rounded-full ring-1 ring-dourado/50" />
          {CHILD_IMAGES.photo ? (
            <m.div
              ref={uniRef}
              className="relative mx-auto w-[86%] pt-2"
              initial={{ opacity: 0, y: 40, scale: 0.9 }}
              whileInView={{ opacity: 1, y: 0, scale: 1 }}
              viewport={{ once: true }}
              transition={{ type: 'spring', stiffness: 80, damping: 14 }}
            >
              <Cloud className="pointer-events-none absolute bottom-[-7%] left-1/2 h-auto w-[96%] -translate-x-1/2 drop-shadow-[0_6px_8px_rgba(190,150,200,.25)]" shade="#EFE4F6" />
              <img
                src={CHILD_IMAGES.photo}
                alt={CHILD_IMAGES.photoAlt}
                width="541"
                height="1100"
                loading="lazy"
                decoding="async"
                className="relative z-10 mx-auto h-auto w-[78%] drop-shadow-[0_14px_14px_rgba(190,120,170,.3)]"
              />
              <Twinkles items={[[80, 18, 22, 0], [86, 30, 12, 0.7, '#E58DB8'], [12, 40, 16, 0.4, '#B9A4E6'], [16, 70, 12, 1.1], [84, 62, 14, 0.9, '#9FD3E6']]} />
            </m.div>
          ) : (
            <m.div
              ref={uniRef}
              className="relative mx-auto aspect-square w-[88%]"
              initial={{ opacity: 0, y: 40, scale: 0.85 }}
              whileInView={{ opacity: 1, y: 0, scale: 1 }}
              viewport={{ once: true }}
              transition={{ type: 'spring', stiffness: 90, damping: 14 }}
            >
              <Unicorn3D
                className="h-full w-full"
                label="Unicórnio da Sophie"
                onPet={() => {
                  sparkle()
                  burstFrom(uniRef.current, { count: 50, speed: 8 })
                }}
              />
            </m.div>
          )}
          {!CHILD_IMAGES.photo && <Cloud className="pointer-events-none relative mx-auto -mt-16 h-auto w-[92%] drop-shadow-[0_6px_8px_rgba(190,150,200,.25)]" shade="#EFE4F6" />}
        </div>

        <Reveal delay={0.1}>
          {!CHILD_IMAGES.photo && <p className="mt-1 font-sans text-sm text-ameixaSoft">Toque no unicórnio para fazer carinho 💕</p>}
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
        <MagicMenu music={music} />
      </div>
    </section>
  )
}
