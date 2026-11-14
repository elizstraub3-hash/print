import { useCallback, useEffect, useRef, useState } from 'react'
import { MUSIC } from '../config/event.js'

/**
 * Áudio controlado pelo convidado. Só chama play() dentro de um
 * clique/toque (exigência de autoplay de iOS/Android/Chrome).
 * status: 'unavailable' | 'paused' | 'loading' | 'playing' | 'error'
 */
export default function useMusic() {
  const src = (MUSIC.src || '').trim()
  const audioRef = useRef(null)
  const [status, setStatus] = useState(src ? 'paused' : 'unavailable')

  const getAudio = () => {
    if (!src) return null
    if (!audioRef.current) {
      const a = new Audio(src)
      a.loop = true
      a.preload = 'none'
      a.volume = MUSIC.volume ?? 0.5
      a.addEventListener('playing', () => setStatus('playing'))
      a.addEventListener('pause', () => setStatus((s) => (s === 'error' ? s : 'paused')))
      a.addEventListener('waiting', () => setStatus('loading'))
      a.addEventListener('error', () => setStatus('error'))
      audioRef.current = a
    }
    return audioRef.current
  }

  const play = useCallback(() => {
    const a = getAudio()
    if (!a) return
    setStatus('loading')
    const p = a.play()
    if (p && p.catch) p.catch(() => setStatus(a.error ? 'error' : 'paused'))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [src])

  const pause = useCallback(() => audioRef.current?.pause(), [])
  const toggle = useCallback(() => (status === 'playing' || status === 'loading' ? pause() : play()), [status, play, pause])

  // pausa quando o convidado sai da aba/app; não retoma sozinho
  useEffect(() => {
    const onHide = () => document.hidden && audioRef.current?.pause()
    document.addEventListener('visibilitychange', onHide)
    return () => {
      document.removeEventListener('visibilitychange', onHide)
      audioRef.current?.pause()
    }
  }, [])

  return { status, play, pause, toggle, available: status !== 'unavailable' && status !== 'error' }
}
