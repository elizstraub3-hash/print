import { LazyMotion, domAnimation, MotionConfig, m } from 'framer-motion'
import { lazy, Suspense, useCallback, useEffect, useState } from 'react'
import Opening from './components/Opening.jsx'
import UnlockGame from './components/UnlockGame.jsx'
import MusicFab from './components/MusicFab.jsx'
import ErrorBoundary from './components/ErrorBoundary.jsx'
import useMusic from './lib/useMusic.js'
import { setSfxEnabled } from './lib/sfx.js'
import { MUSIC, SOUND_EFFECTS } from './config/event.js'

// o restante do convite carrega em paralelo enquanto o convidado joga
const InviteBody = lazy(() => import('./components/InviteBody.jsx'))

const KEY = 'sophie-convite-desbloqueado'
const readUnlocked = () => {
  try {
    return localStorage.getItem(KEY) === '1'
  } catch {
    return false
  }
}
const saveUnlocked = () => {
  try {
    localStorage.setItem(KEY, '1')
  } catch {
    /* modo privado: tudo bem */
  }
}

const scrollToId = (id) => {
  const el = document.getElementById(id)
  if (!el) return false
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' })
  const heading = el.querySelector('h2')
  if (heading) {
    heading.setAttribute('tabindex', '-1')
    heading.focus({ preventScroll: true })
  }
  return true
}
/** rola quando o elemento existir (o corpo do convite é carregado sob demanda) */
const scrollWhenReady = (id, tries = 40) => {
  if (scrollToId(id) || tries <= 0) return
  setTimeout(() => scrollWhenReady(id, tries - 1), 50)
}

export default function App() {
  const [opened, setOpened] = useState(false)
  const [unlocked, setUnlocked] = useState(readUnlocked)
  const music = useMusic()

  useEffect(() => setSfxEnabled(SOUND_EFFECTS), [])
  // começa a baixar o corpo do convite assim que a página fica ociosa
  useEffect(() => {
    const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 1500))
    idle(() => import('./components/InviteBody.jsx'))
  }, [])

  const handleOpen = useCallback(() => {
    if (MUSIC.startOnOpen && music.status === 'paused') music.play() // ainda dentro do gesto do usuário
    if (opened) return scrollToId('jogo')
    setOpened(true)
  }, [opened, music])

  useEffect(() => {
    if (opened) requestAnimationFrame(() => setTimeout(() => scrollToId('jogo'), 60))
  }, [opened])

  const unlock = () => {
    setUnlocked(true)
    saveUnlocked()
  }
  const skip = () => {
    unlock()
    scrollWhenReady('convite')
  }

  return (
    <LazyMotion features={domAnimation} strict>
      <MotionConfig reducedMotion="user">
        {opened && <MusicFab music={music} />}
        <main className="relative w-full overflow-x-clip">
          <Opening opened={opened} onOpen={handleOpen} />
          {opened && (
            <m.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.6 }}>
              <UnlockGame unlocked={unlocked} onUnlock={unlock} onSkip={skip} onContinue={() => scrollWhenReady('convite')} />
              {unlocked && (
                <ErrorBoundary>
                  <Suspense fallback={<div className="h-screen bg-[#FFFAFC]" aria-busy="true" />}>
                    <InviteBody music={music} />
                  </Suspense>
                </ErrorBoundary>
              )}
            </m.div>
          )}
        </main>
      </MotionConfig>
    </LazyMotion>
  )
}
