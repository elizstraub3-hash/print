import { MAPS_URL, hasGifts } from '../lib/event-utils.js'
import ArtButton from './ArtButton.jsx'
import { scrollToSection } from '../lib/scrollTo.js'
import { MUSIC } from '../config/event.js'
import { PLAY_YT_EVENT } from './MusicCard.jsx'
import Reveal from './Reveal.jsx'

const go = (id) => () => scrollToSection(id)

/** Menu de atalhos com os botões ilustrados */
export default function MagicMenu({ music }) {
  const playing = music.status === 'playing' || music.status === 'loading'
  const items = [
    { art: 'sobre', label: 'Sobre a festa: data, horário e local', onClick: go('informacoes') },
    { art: 'confirmar', label: 'Confirmar presença', onClick: go('confirmar') },
    { art: 'localizacao', label: 'Ver localização no Google Maps (abre em nova aba)', href: MAPS_URL },
    { art: 'joguinho', label: 'Mini joguinho: Escadinha do Unicórnio', onClick: go('pulos') },
    music.available && {
      art: 'musica',
      label: playing ? 'Desligar música' : 'Ligar música',
      onClick: music.toggle,
      pressed: playing,
      badge: playing ? '♪ tocando' : 'desligada',
      glitter: !playing,
    },
    !music.available && !MUSIC.src && MUSIC.youtubeId && {
      art: 'musica',
      label: 'Ouvir a música da festa',
      onClick: () => window.dispatchEvent(new Event(PLAY_YT_EVENT)),
    },
    hasGifts() && { art: 'presentes', label: 'Lista de presentes: lojas sugeridas', onClick: go('presentes') },
  ].filter(Boolean)

  return (
    <nav aria-label="Menu do convite" className="relative mx-auto mt-10 max-w-md">
      <Reveal>
        <p className="text-center font-sans text-xs font-semibold uppercase tracking-[0.3em] text-ameixaSoft">Menu mágico</p>
      </Reveal>
      <ul className="mt-3 grid grid-cols-2 gap-x-2 gap-y-1">
        {items.map((it, i) => (
          <li key={it.art} className={items.length % 2 && i === items.length - 1 ? 'col-span-2 mx-auto w-1/2' : ''}>
            <Reveal delay={0.05 * i} y={14}>
              <ArtButton {...it} />
            </Reveal>
          </li>
        ))}
      </ul>
    </nav>
  )
}
