import { m, useReducedMotion } from 'framer-motion'
import { Sparkle } from './Unicorn.jsx'

/** Nuvem fofinha em SVG */
export function Cloud({ className = '', tone = '#FFFFFF', shade = '#F3EAF6' }) {
  return (
    <svg viewBox="0 0 200 100" className={className} aria-hidden="true">
      <path d="M38 90 C14 90 6 70 18 56 C10 36 34 22 52 32 C58 12 92 4 108 24 C122 8 158 14 158 40 C182 38 196 58 186 76 C182 86 172 90 160 90 Z" fill={shade} transform="translate(0 4)" />
      <path d="M38 90 C14 90 6 70 18 56 C10 36 34 22 52 32 C58 12 92 4 108 24 C122 8 158 14 158 40 C182 38 196 58 186 76 C182 86 172 90 160 90 Z" fill={tone} />
    </svg>
  )
}

/** Nuvem que flutua lentamente (transform-only → leve) */
export function DriftCloud({ className = '', distance = 24, duration = 9, delay = 0, ...rest }) {
  const reduce = useReducedMotion()
  return (
    <m.div
      className={`pointer-events-none absolute ${className}`}
      aria-hidden="true"
      animate={reduce ? undefined : { x: [0, distance, 0], y: [0, -4, 0] }}
      transition={{ duration, delay, repeat: Infinity, ease: 'easeInOut' }}
    >
      <Cloud className="h-full w-full" {...rest} />
    </m.div>
  )
}

/** Arco-íris pastel */
export function Rainbow({ className = '' }) {
  const bands = ['#F8CDE3', '#FFE2C6', '#FFF0B9', '#D6EEDC', '#CDECF7', '#DCCCF7']
  return (
    <svg viewBox="0 0 400 210" className={className} aria-hidden="true">
      {bands.map((c, i) => (
        <path key={c} d={`M${20 + i * 16} 205 A${180 - i * 16} ${180 - i * 16} 0 0 1 ${380 - i * 16} 205`} stroke={c} strokeWidth="17" fill="none" strokeLinecap="round" />
      ))}
    </svg>
  )
}

/** Estrelinhas piscando espalhadas */
export function Twinkles({ items }) {
  const reduce = useReducedMotion()
  return items.map(([left, top, size, delay, color], i) => (
    <m.svg
      key={i}
      viewBox="-12 -12 24 24"
      className="pointer-events-none absolute"
      style={{ left: `${left}%`, top: `${top}%`, width: size, height: size }}
      aria-hidden="true"
      animate={reduce ? undefined : { opacity: [0.35, 1, 0.35], scale: [0.85, 1.1, 0.85] }}
      transition={{ duration: 2.6, delay, repeat: Infinity, ease: 'easeInOut' }}
    >
      <Sparkle x={0} y={0} s={11} fill={color || '#EBCB85'} />
    </m.svg>
  ))
}

export function Heart({ className = '', fill = '#F8CDE3' }) {
  return (
    <svg viewBox="0 0 24 22" className={className} aria-hidden="true">
      <path d="M12 21 C5 15 1 11.5 1 7 C1 3.5 3.7 1 7 1 C9.2 1 11 2.2 12 4 C13 2.2 14.8 1 17 1 C20.3 1 23 3.5 23 7 C23 11.5 19 15 12 21 Z" fill={fill} />
    </svg>
  )
}

/** Laço decorativo */
export function Bow({ className = '', fill = '#F8CDE3' }) {
  return (
    <svg viewBox="0 0 80 44" className={className} aria-hidden="true">
      <path d="M38 20 C26 4 6 2 4 14 C2 28 22 32 38 24 Z" fill={fill} />
      <path d="M42 20 C54 4 74 2 76 14 C78 28 58 32 42 24 Z" fill={fill} />
      <path d="M36 24 L28 42 L36 38 L40 26 Z M44 24 L52 42 L44 38 L40 26 Z" fill={fill} opacity=".8" />
      <rect x="33" y="15" width="14" height="13" rx="6" fill="#fff" opacity=".55" />
    </svg>
  )
}

/** Divisor delicado entre seções */
export function Divider() {
  return (
    <div className="flex items-center justify-center gap-3 py-2" aria-hidden="true">
      <span className="h-px w-12 bg-gradient-to-r from-transparent to-dourado" />
      <Heart className="h-3 w-3" fill="#EBCB85" />
      <svg viewBox="-12 -12 24 24" className="h-4 w-4"><Sparkle x={0} y={0} s={11} /></svg>
      <Heart className="h-3 w-3" fill="#EBCB85" />
      <span className="h-px w-12 bg-gradient-to-l from-transparent to-dourado" />
    </div>
  )
}

/** Borda de nuvens (scallop) para transição suave entre seções */
export function CloudEdge({ fill = '#FFFFFF', className = '' }) {
  return (
    <svg viewBox="0 0 400 40" preserveAspectRatio="none" className={`pointer-events-none absolute inset-x-0 bottom-[-1px] h-8 w-full sm:h-10 ${className}`} aria-hidden="true">
      <path
        d="M0 40 L0 24 C14 8 34 8 46 22 C56 6 84 4 96 20 C108 2 140 4 150 22 C162 8 186 8 196 24 C208 4 240 4 252 20 C264 6 290 6 300 22 C312 4 344 6 354 22 C366 8 390 10 400 22 L400 40 Z"
        fill={fill}
      />
    </svg>
  )
}
