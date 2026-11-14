import { useCallback, useEffect, useRef, useState } from 'react'

/**
 * Detecta o celular sendo chacoalhado (DeviceMotion).
 * iPhone (iOS 13+) exige pedir permissão a partir de um toque → enable().
 * status: 'unsupported' | 'idle' | 'listening' | 'denied'
 */
export default function useShake(onShake, { threshold = 17, gap = 320 } = {}) {
  // decidido uma única vez (celular/tablet com sensor de movimento)
  const [supported] = useState(
    () => typeof window !== 'undefined' && 'DeviceMotionEvent' in window && (matchMedia('(pointer: coarse)').matches || navigator.maxTouchPoints > 0)
  )
  const [status, setStatus] = useState(supported ? 'idle' : 'unsupported')
  const cb = useRef(onShake)
  cb.current = onShake
  const last = useRef({ x: 0, y: 0, z: 0, t: 0, init: false })

  const handler = useCallback(
    (e) => {
      const a = e.accelerationIncludingGravity || e.acceleration
      if (!a || a.x == null) return
      const L = last.current
      if (!L.init) {
        Object.assign(L, { x: a.x, y: a.y, z: a.z, init: true })
        return
      }
      const delta = Math.abs(a.x - L.x) + Math.abs(a.y - L.y) + Math.abs(a.z - L.z)
      L.x = a.x
      L.y = a.y
      L.z = a.z
      const now = performance.now()
      if (delta > threshold && now - L.t > gap) {
        L.t = now
        cb.current?.(delta)
      }
    },
    [threshold, gap]
  )

  const enable = useCallback(async () => {
    if (!supported) return false
    // começa a ouvir já; navegadores sem pedido de permissão (Android) funcionam direto
    window.addEventListener('devicemotion', handler, { passive: true })
    setStatus('listening')
    const DME = window.DeviceMotionEvent
    if (typeof DME.requestPermission === 'function') {
      // iPhone (e Chrome recente): pedido feito dentro do toque. Se o navegador
      // demorar a responder, seguimos ouvindo; só desistimos se for negado.
      const r = await Promise.race([
        DME.requestPermission().catch(() => 'denied'),
        new Promise((res) => setTimeout(() => res('pending'), 2500)),
      ])
      if (r === 'denied') {
        window.removeEventListener('devicemotion', handler)
        setStatus('denied')
        return false
      }
    }
    return true
  }, [supported, handler])

  const disable = useCallback(() => {
    window.removeEventListener('devicemotion', handler)
    setStatus((s) => (s === 'listening' ? 'idle' : s))
  }, [handler])

  useEffect(() => () => window.removeEventListener('devicemotion', handler), [handler])
  return { status, enable, disable }
}
