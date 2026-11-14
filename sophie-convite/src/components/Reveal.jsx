import { m } from 'framer-motion'

/** Entrada suave ao rolar (uma vez). Com reduced-motion o MotionConfig zera o deslocamento. */
export default function Reveal({ children, delay = 0, y = 24, className = '', as = 'div' }) {
  const C = m[as]
  return (
    <C
      className={className}
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '0px 0px -12% 0px' }}
      transition={{ duration: 0.7, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </C>
  )
}
