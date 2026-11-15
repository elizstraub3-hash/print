import { useCallback, useEffect, useRef, useState } from 'react'
import { MUSIC } from '../config/event.js'
import { createMusicBox } from './musicBox.js'

/**
 * Música do convite. Com MUSIC.src (MP3) toca o arquivo; sem MP3 toca a
 * "caixinha de música mágica" original sintetizada. Só começa após um toque.
 * status: 'paused' | 'loading' | 'playing'
 */
export default function useMusic() {
  const src = (MUSIC.src || '').trim()
  const engine = useRef(null)
  const [status, setStatus] = useState('paused')

  const get = () => {
    if (engine.current) return engine.current
    if (src) {
      const a = new Audio(src)
      a.loop = true
      a.preload = 'auto'
      a.volume = MUSIC.volume ?? 0.5
      let fallback = null // se o MP3 falhar, toca a caixinha de música
      engine.current = {
        play: () =>
          fallback
            ? fallback.play()
            : a.play().catch((err) => {
                if (a.error) {
                  fallback = createMusicBox(0.32)
                  return fallback.play()
                }
                throw err
              }),
        pause: () => (fallback ? fallback.pause() : a.pause()),
        audio: a,
      }
    } else {
      engine.current = createMusicBox(MUSIC.volume ?? 0.35)
    }
    return engine.current
  }

  const play = useCallback(() => {
    const e = get()
    setStatus('loading')
    Promise.resolve()
      .then(() => e.play())
      .then(() => setStatus('playing'))
      .catch(() => setStatus('paused'))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [src])

  const pause = useCallback(() => {
    engine.current?.pause()
    setStatus('paused')
  }, [])
  const toggle = useCallback(() => (status === 'paused' ? play() : pause()), [status, play, pause])

  useEffect(() => {
    const onHide = () => document.hidden && pause()
    document.addEventListener('visibilitychange', onHide)
    return () => {
      document.removeEventListener('visibilitychange', onHide)
      engine.current?.pause()
    }
  }, [pause])

  return { status, play, pause, toggle, available: true }
}
