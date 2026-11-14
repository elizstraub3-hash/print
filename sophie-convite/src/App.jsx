import { LazyMotion, domAnimation, MotionConfig, AnimatePresence, m } from 'framer-motion'
import { useCallback, useEffect, useState } from 'react'
import Opening from './components/Opening.jsx'
import StarGame from './components/StarGame.jsx'
import Invitation from './components/Invitation.jsx'
import Details from './components/Details.jsx'
import Actions from './components/Actions.jsx'
import Finale from './components/Finale.jsx'
import MusicFab from './components/MusicFab.jsx'
import useMusic from './lib/useMusic.js'
import { MUSIC } from './config/event.js'

const scrollToId = (id) => {
  const el = document.getElementById(id)
  if (!el) return
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' })
  // foco no título da seção para teclado/leitor de tela
  const heading = el.querySelector('h2')
  if (heading) {
    heading.setAttribute('tabindex', '-1')
    heading.focus({ preventScroll: true })
  }
}

export default function App() {
  const [opened, setOpened] = useState(false)
  const music = useMusic()

  const handleOpen = useCallback(() => {
    if (MUSIC.startOnOpen && music.status === 'paused') music.play() // dentro do clique → permitido
    if (opened) return scrollToId('jogo')
    setOpened(true)
  }, [opened, music])

  useEffect(() => {
    if (opened) requestAnimationFrame(() => setTimeout(() => scrollToId('jogo'), 60))
  }, [opened])

  return (
    <LazyMotion features={domAnimation} strict>
      <MotionConfig reducedMotion="user">
        <a href="#convite" className="skip-link">Pular para o convite</a>
        {opened && <MusicFab music={music} />}
        <main className="relative w-full overflow-x-clip">
          <Opening opened={opened} onOpen={handleOpen} />
          <AnimatePresence>
            {opened && (
              <m.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.6 }}>
                <StarGame onFinish={() => scrollToId('convite')} />
                <Invitation />
                <Details />
                <Actions music={music} />
                <Finale />
              </m.div>
            )}
          </AnimatePresence>
        </main>
      </MotionConfig>
    </LazyMotion>
  )
}
