import { m } from 'framer-motion'
import { EVENT, PHOTOS } from '../config/event.js'
import Reveal from './Reveal.jsx'
import Pattern from './Pattern.jsx'

const TILT = [-3, 2.5, -1.5, 3, -2.5, 1.5]

/** Fotos da aniversariante em estilo "polaroid" — oculta se PHOTOS estiver vazio */
export default function Gallery() {
  const photos = (PHOTOS || []).filter((p) => p && p.src)
  if (!photos.length) return null
  return (
    <section id="fotos" aria-labelledby="fotos-titulo" className="relative overflow-hidden bg-[#FFFAFC] px-5 pb-14 pt-4">
      <Pattern opacity={0.2} />
      <div className="relative mx-auto max-w-md text-center">
        <Reveal>
          <h2 id="fotos-titulo" className="font-bubble bubble-pink text-[clamp(1.75rem,8vw,2.4rem)]">
            Momentos da {EVENT.childFirstName}
          </h2>
        </Reveal>
        <div className={`mt-6 grid gap-4 ${photos.length === 1 ? 'grid-cols-1' : 'grid-cols-2'}`}>
          {photos.map((p, i) => (
            <m.figure
              key={p.src}
              className={`rounded-2xl bg-white p-2 pb-3 shadow-soft ring-1 ring-rosa/40 ${photos.length % 2 && i === photos.length - 1 && photos.length > 1 ? 'col-span-2 mx-auto w-1/2' : ''}`}
              initial={{ opacity: 0, y: 24, rotate: 0 }}
              whileInView={{ opacity: 1, y: 0, rotate: TILT[i % TILT.length] }}
              viewport={{ once: true, margin: '0px 0px -10% 0px' }}
              transition={{ type: 'spring', stiffness: 90, damping: 14, delay: (i % 2) * 0.1 }}
            >
              <img src={p.src} alt={p.alt || `Foto da ${EVENT.childFirstName}`} loading="lazy" decoding="async" className="aspect-[4/5] w-full rounded-xl object-cover" />
              {p.caption && <figcaption className="mt-2 font-bubble text-lg text-ameixa normal-case">{p.caption}</figcaption>}
            </m.figure>
          ))}
        </div>
      </div>
    </section>
  )
}
