import { m } from 'framer-motion'
import { useMemo } from 'react'
import { Sparkle } from './Unicorn.jsx'
import { Heart } from './Decor.jsx'

const COLORS = ['#EBCB85', '#F8CDE3', '#DCCCF7', '#CDECF7', '#FFF0B9', '#D6EEDC', '#E58DB8']

/** Explosão de partículas brilhantes a partir do centro do elemento pai */
export default function Particles({ count = 28, radius = 220, duration = 1.1 }) {
  const parts = useMemo(
    () =>
      Array.from({ length: count }, (_, i) => {
        const a = (i / count) * Math.PI * 2 + Math.random() * 0.4
        const r = radius * (0.45 + Math.random() * 0.55)
        return {
          x: Math.cos(a) * r,
          y: Math.sin(a) * r,
          size: 10 + Math.random() * 14,
          color: COLORS[i % COLORS.length],
          heart: i % 5 === 0,
          delay: Math.random() * 0.12,
          rot: Math.random() * 180,
        }
      }),
    [count, radius]
  )
  return (
    <div className="pointer-events-none absolute left-1/2 top-1/2 z-30" aria-hidden="true">
      {parts.map((p, i) => (
        <m.div
          key={i}
          className="absolute"
          style={{ width: p.size, height: p.size, marginLeft: -p.size / 2, marginTop: -p.size / 2 }}
          initial={{ x: 0, y: 0, scale: 0.2, opacity: 1, rotate: 0 }}
          animate={{ x: p.x, y: p.y, scale: [0.2, 1.2, 0.6], opacity: [1, 1, 0], rotate: p.rot }}
          transition={{ duration, delay: p.delay, ease: [0.16, 1, 0.3, 1] }}
        >
          {p.heart ? (
            <Heart className="h-full w-full" fill={p.color} />
          ) : (
            <svg viewBox="-12 -12 24 24" className="h-full w-full">
              <Sparkle x={0} y={0} s={11} fill={p.color} />
            </svg>
          )}
        </m.div>
      ))}
    </div>
  )
}
