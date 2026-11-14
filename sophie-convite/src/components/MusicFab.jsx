import { m } from 'framer-motion'
import { MusicIcon, MuteIcon } from './Icons.jsx'

/** Botão flutuante de música — só aparece se houver MP3 configurado */
export default function MusicFab({ music }) {
  if (!music.available) return null
  const playing = music.status === 'playing' || music.status === 'loading'
  return (
    <m.button
      type="button"
      onClick={music.toggle}
      aria-pressed={playing}
      aria-label={playing ? 'Desligar música' : 'Ligar música'}
      className="fixed right-4 top-[max(1rem,env(safe-area-inset-top))] z-50 grid h-14 w-14 place-items-center rounded-full bg-white/90 text-ameixa shadow-glow backdrop-blur"
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      whileTap={{ scale: 0.9 }}
    >
      {playing ? <MusicIcon className="h-6 w-6" /> : <MuteIcon className="h-6 w-6" />}
      {playing && <span className="absolute inset-0 animate-ping rounded-full ring-2 ring-rosa motion-reduce:hidden" aria-hidden="true" />}
    </m.button>
  )
}
