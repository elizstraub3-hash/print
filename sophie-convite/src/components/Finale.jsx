import { m, useReducedMotion } from 'framer-motion'
import { EVENT, BACKGROUNDS } from '../config/event.js'
import { POSTER } from './Unicorn3D.jsx'
import Reveal from './Reveal.jsx'
import { Rainbow, DriftCloud, Twinkles, Cloud, Heart } from './Decor.jsx'
import Pattern, { PhotoPattern } from './Pattern.jsx'

export default function Finale() {
  const reduce = useReducedMotion()
  return (
    <section id="final" aria-labelledby="final-titulo" className="relative overflow-hidden bg-gradient-to-b from-amarelo/60 via-rosa to-lilas px-5 pb-10 pt-16 text-center">
      {BACKGROUNDS.finale ? <PhotoPattern src={BACKGROUNDS.finale} veil={0.62} /> : <Pattern opacity={0.22} />}
      <Twinkles items={[[8, 12, 18, 0], [90, 8, 14, 0.5, '#E58DB8'], [14, 52, 12, 1.1, '#9FD3E6'], [86, 46, 16, 0.3], [50, 6, 12, 1.5, '#B9A4E6']]} />
      <DriftCloud className="left-[-12%] top-24 h-16 w-36" distance={18} />
      <DriftCloud className="right-[-14%] top-10 h-20 w-44" distance={-18} duration={11} />

      <div className="relative mx-auto max-w-md">
        <Reveal>
          <h2 id="final-titulo" className="mx-auto max-w-[16ch] text-balance font-script text-[clamp(2.3rem,10.5vw,3.2rem)] font-bold leading-[1.1] text-ameixa">
            {EVENT.finalMessage}
          </h2>
        </Reveal>

        <div className="relative mx-auto mt-6 w-[min(84vw,330px)]">
          <Rainbow className="absolute left-1/2 top-[6%] w-[120%] -translate-x-1/2" />
          <m.div
            className="relative mx-auto w-[78%]"
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ type: 'spring', stiffness: 80, damping: 14 }}
          >
            <m.div animate={reduce ? undefined : { y: [0, -10, 0] }} transition={{ duration: 4.5, repeat: Infinity, ease: 'easeInOut' }}>
              <img src={POSTER} alt="Unicórnio da Sophie comemorando" loading="lazy" decoding="async" width="640" height="640" className="h-auto w-full drop-shadow-[0_16px_20px_rgba(190,140,190,.35)]" />
            </m.div>
          </m.div>
          <Cloud className="relative -mt-12 h-auto w-full drop-shadow-md" />
        </div>

        <Reveal delay={0.1}>
          <p className="mt-2 font-sans text-lg font-medium text-ameixa">
            Com amor, família da {EVENT.childFirstName}
          </p>
          <div className="mt-3 flex justify-center gap-2" aria-hidden="true">
            {['#E58DB8', '#B9A4E6', '#9FD3E6', '#A8D8B5', '#EBCB85'].map((c, i) => (
              <m.span key={c} animate={reduce ? undefined : { y: [0, -6, 0] }} transition={{ duration: 1.6, delay: i * 0.15, repeat: Infinity }}>
                <Heart className="h-4 w-4" fill={c} />
              </m.span>
            ))}
          </div>
          <a href="#abertura" className="btn-ghost mt-8 inline-flex min-h-[48px] px-6">Voltar ao início ↑</a>
        </Reveal>
      </div>
    </section>
  )
}
