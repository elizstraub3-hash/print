import { m } from 'framer-motion'

/**
 * Flutuação suave e lenta (só transform → leve no celular).
 * Com "reduzir movimento" ligado, o MotionConfig desliga sozinho.
 */
export default function Float({ children, className = '', y = 6, duration = 5, delay = 0, rotate = 0 }) {
  return (
    <m.div
      className={className}
      animate={{ y: [0, -y, 0], rotate: rotate ? [-rotate, rotate, -rotate] : 0 }}
      transition={{ duration, delay, repeat: Infinity, ease: 'easeInOut' }}
    >
      {children}
    </m.div>
  )
}
