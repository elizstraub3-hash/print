import { useEffect, useRef, useState } from 'react'
import { MUSIC } from '../config/event.js'
import { MusicIcon } from './Icons.jsx'
import { scrollToSection } from '../lib/scrollTo.js'

export const PLAY_YT_EVENT = 'convite:tocar-musica'
const ID = String(MUSIC.youtubeId || '').replace(/[^\w-]/g, '')

/**
 * Player oficial do YouTube (youtube-nocookie), carregado só quando o
 * convidado toca — não pesa a página e respeita as regras de autoplay.
 * Só aparece quando não há MP3 configurado.
 */
export default function MusicCard() {
  const [on, setOn] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    const play = () => {
      setOn(true)
      scrollToSection('musica')
    }
    window.addEventListener(PLAY_YT_EVENT, play)
    return () => window.removeEventListener(PLAY_YT_EVENT, play)
  }, [])

  if (MUSIC.src || !ID) return null
  return (
    <div id="musica" ref={ref} className="mx-auto mt-8 max-w-[22rem] scroll-mt-24 rounded-[1.75rem] bg-white/90 p-3 text-center shadow-soft ring-1 ring-white">
      <p className="flex items-center justify-center gap-2 font-sans text-base font-semibold text-ameixa">
        <MusicIcon className="h-5 w-5 text-rosaForte" /> {MUSIC.title || 'Música da festa'}
      </p>
      <div className="relative mt-2 overflow-hidden rounded-2xl bg-black" style={{ aspectRatio: '16 / 9', minHeight: 200 }}>
        {on ? (
          <iframe
            className="absolute inset-0 h-full w-full"
            src={`https://www.youtube-nocookie.com/embed/${ID}?autoplay=1&playsinline=1&rel=0&modestbranding=1`}
            title={MUSIC.title || 'Música da festa'}
            allow="autoplay; encrypted-media; picture-in-picture"
            allowFullScreen
            referrerPolicy="strict-origin-when-cross-origin"
          />
        ) : (
          <button type="button" onClick={() => setOn(true)} className="group absolute inset-0 grid place-items-center" aria-label={`Tocar ${MUSIC.title || 'a música da festa'}`}>
            <img src={`https://i.ytimg.com/vi/${ID}/hqdefault.jpg`} alt="" loading="lazy" className="absolute inset-0 h-full w-full object-cover opacity-90" />
            <span className="relative grid h-16 w-16 place-items-center rounded-full bg-white/95 text-2xl text-rosaForte shadow-glow transition group-active:scale-90">▶</span>
          </button>
        )}
      </div>
      <p className="mt-2 font-sans text-xs text-ameixaSoft">Toque no play — a música continua enquanto você navega pelo convite 🎶</p>
    </div>
  )
}
