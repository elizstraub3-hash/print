import { m, useReducedMotion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'
import { burstFrom } from '../lib/glitter.js'
import { EVENT, BACKGROUNDS, TEXT_ART } from '../config/event.js'
import Float from './Float.jsx'
import { scrollToSection } from '../lib/scrollTo.js'
import Reveal from './Reveal.jsx'
import { Rainbow, DriftCloud, Twinkles, Cloud, Heart } from './Decor.jsx'
import Pattern, { PhotoPattern } from './Pattern.jsx'

const LAYLA_AUDIO = '/audio/layla-final.mp3'

export default function Finale() {
  const reduce = useReducedMotion()
  const laylaRef = useRef(null)
  const audioRef = useRef(null)
  const [neigh, setNeigh] = useState(0)

  // Layla "relincha" (fala) quando o convidado chega ao fim do convite
  const play = () => {
    const a = audioRef.current || (audioRef.current = new Audio(LAYLA_AUDIO))
    a.currentTime = 0
    a.play().catch(() => {}) // se o navegador bloquear, fica o toque na Layla
    setNeigh((n) => n + 1)
    burstFrom(laylaRef.current, { count: 60, speed: 9 })
  }
  useEffect(() => {
    const el = laylaRef.current
    if (!el) return
    let done = false
    const io = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting && !done) {
          done = true
          setTimeout(play, 400)
        }
      },
      { threshold: 0.6 }
    )
    io.observe(el)
    return () => {
      io.disconnect()
      audioRef.current?.pause()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])
  return (
    <section id="final" aria-labelledby="final-titulo" className="relative overflow-hidden bg-gradient-to-b from-amarelo/60 via-rosa to-lilas px-5 pb-10 pt-16 text-center">
      {BACKGROUNDS.finale ? <PhotoPattern src={BACKGROUNDS.finale} veil={0.62} /> : <Pattern opacity={0.22} />}
      <Twinkles items={[[8, 12, 18, 0], [90, 8, 14, 0.5, '#E58DB8'], [14, 52, 12, 1.1, '#9FD3E6'], [86, 46, 16, 0.3], [50, 6, 12, 1.5, '#B9A4E6']]} />
      <DriftCloud className="left-[-12%] top-24 h-16 w-36" distance={18} />
      <DriftCloud className="right-[-14%] top-10 h-20 w-44" distance={-18} duration={11} />

      <div className="relative mx-auto max-w-md">
        <Reveal>
          {TEXT_ART.finale?.src ? (
            <h2 id="final-titulo">
              <Float y={8} duration={5} rotate={0.6}>
                <img
                  src={TEXT_ART.finale.src}
                  alt={TEXT_ART.finale.alt}
                  width={TEXT_ART.finale.w}
                  height={TEXT_ART.finale.h}
                  loading="lazy"
                  decoding="async"
                  className="mx-auto h-auto w-[min(100%,25rem)] drop-shadow-[0_14px_18px_rgba(190,120,170,.3)]"
                />
              </Float>
            </h2>
          ) : (
            <h2 id="final-titulo" className="mx-auto max-w-[16ch] text-balance font-bubble bubble-purple text-[clamp(1.7rem,7.8vw,2.4rem)] leading-[1.1]">
              {EVENT.finalMessage}
            </h2>
          )}
        </Reveal>

        <div className="relative mx-auto mt-6 w-[min(84vw,330px)]">
          <Rainbow className="absolute left-1/2 top-[6%] w-[120%] -translate-x-1/2" />
          <m.div
            className="relative mx-auto w-[58%]"
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ type: 'spring', stiffness: 80, damping: 14 }}
          >
            <button ref={laylaRef} type="button" onClick={play} aria-label="Layla, a unicórnio da Sophie — toque para ouvir" className="relative block w-full" style={{ touchAction: 'manipulation' }}>
              <m.img
                key={neigh}
                src="/img/layla/layla-rindo.webp"
                alt=""
                loading="lazy"
                decoding="async"
                width="351"
                height="471"
                draggable="false"
                className="pointer-events-none h-auto w-full origin-bottom drop-shadow-[0_16px_20px_rgba(190,140,190,.35)]"
                initial={false}
                animate={reduce ? undefined : neigh ? { rotate: [0, -10, 4, -6, 0], y: [0, -26, 0, -12, 0], scaleY: [1, 1.06, 0.95, 1.03, 1] } : { y: [0, -10, 0] }}
                transition={neigh ? { duration: 1.4, ease: 'easeOut' } : { duration: 4.5, repeat: Infinity, ease: 'easeInOut' }}
              />
            </button>
          </m.div>
          <Cloud className="pointer-events-none relative -mt-10 h-auto w-full drop-shadow-md" />
        </div>
        <p className="mt-3 font-sans text-sm font-bold text-ameixa">Toque na Layla 💕</p>

        <Reveal delay={0.1}>
          <p className="mt-6 font-sans text-lg font-semibold text-ameixa">
            Com amor, família da {EVENT.childFirstName}
          </p>
          <div className="mt-3 flex justify-center gap-2" aria-hidden="true">
            {['#E58DB8', '#B9A4E6', '#9FD3E6', '#A8D8B5', '#EBCB85'].map((c, i) => (
              <m.span key={c} animate={reduce ? undefined : { y: [0, -6, 0] }} transition={{ duration: 1.6, delay: i * 0.15, repeat: Infinity }}>
                <Heart className="h-4 w-4" fill={c} />
              </m.span>
            ))}
          </div>
          <a href="#abertura" onClick={(e) => { e.preventDefault(); scrollToSection('abertura') }} className="btn-ghost mt-8 inline-flex min-h-[48px] px-6">Voltar ao início ↑</a>
        </Reveal>
      </div>
    </section>
  )
}
