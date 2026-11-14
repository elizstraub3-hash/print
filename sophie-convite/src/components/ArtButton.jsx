import { m } from 'framer-motion'
import Float from './Float.jsx'
import { burstFrom } from '../lib/glitter.js'
import { sparkle } from '../lib/sfx.js'

export const ART = {
  confirmar: '/img/botoes/confirmar.webp',
  localizacao: '/img/botoes/localizacao.webp',
  presentes: '/img/botoes/presentes.webp',
  joguinho: '/img/botoes/joguinho.webp',
  musica: '/img/botoes/musica.webp',
  sobre: '/img/botoes/sobre.webp',
}

/**
 * Botão ilustrado. A arte é só visual: por baixo existe um <a>/<button>
 * real com nome acessível, foco visível, área de toque grande e estado.
 *  - href  → link (externo abre em nova aba)
 *  - onClick → botão
 *  - disabled → arte esmaecida + legenda explicando o motivo
 */
const PHASE = { sobre: 0, confirmar: 1.2, localizacao: 2.1, joguinho: 0.6, musica: 1.7, presentes: 2.6 }

export default function ArtButton({ art, label, href, onClick, disabled, note, badge, pressed, className = '', glitter = true }) {
  const external = href && /^https?:/.test(href)
  const Tag = href && !disabled ? m.a : m.button
  const handle = (e) => {
    if (disabled) return
    if (glitter) {
      sparkle()
      burstFrom(e.currentTarget, { count: 45, speed: 8 })
    }
    onClick?.(e)
  }
  return (
    <div className={`relative ${className}`}>
      <Float y={disabled ? 0 : 5} duration={5.5} delay={PHASE[art] || 0}>
      <Tag
        {...(href && !disabled
          ? { href, ...(external && { target: '_blank', rel: 'noopener noreferrer' }) }
          : { type: 'button', disabled, 'aria-pressed': pressed })}
        onClick={handle}
        aria-label={label}
        aria-describedby={note ? `${art}-note` : undefined}
        className={`art-btn group relative block w-full ${disabled ? 'cursor-not-allowed' : ''}`}
        whileHover={disabled ? undefined : { y: -3, scale: 1.02 }}
        whileTap={disabled ? undefined : { scale: 0.94 }}
        transition={{ type: 'spring', stiffness: 500, damping: 20 }}
      >
        <img
          src={ART[art]}
          alt=""
          aria-hidden="true"
          loading="lazy"
          decoding="async"
          draggable="false"
          width="700"
          height="318"
          className={`pointer-events-none h-auto w-full select-none drop-shadow-[0_10px_14px_rgba(190,120,170,.28)] ${disabled ? 'opacity-50 grayscale-[60%]' : ''}`}
        />
        {badge && (
          <span className="absolute right-[6%] top-[6%] rounded-full bg-white/95 px-2.5 py-0.5 font-sans text-xs font-semibold text-ameixa shadow-soft ring-1 ring-rosa" aria-hidden="true">
            {badge}
          </span>
        )}
      </Tag>
      </Float>
      {note && (
        <p id={`${art}-note`} className="mt-1 text-center font-sans text-sm text-ameixaSoft">
          {note}
        </p>
      )}
    </div>
  )
}
