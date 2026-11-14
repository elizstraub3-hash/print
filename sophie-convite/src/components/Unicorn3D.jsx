import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react'
import { useReducedMotion } from 'framer-motion'

export const POSTER = `${import.meta.env.BASE_URL}img/unicornio-3d.webp`

/**
 * Unicórnio 3D (WebGL). Mostra a imagem renderizada (poster) na hora e
 * troca pelo 3D animado quando o modelo carrega. Se o aparelho não tiver
 * WebGL, o poster continua — nada quebra.
 * ref.play('tap' | 'pet' | 'celebrate', { onHit }) → Promise
 */
const Unicorn3D = forwardRef(function Unicorn3D(
  { className = '', label = 'Unicórnio 3D da Sophie', onPet, yaw, eager = false },
  ref
) {
  const reduce = useReducedMotion()
  const wrapRef = useRef(null)
  const canvasRef = useRef(null)
  const sceneRef = useRef(null)
  const [ready, setReady] = useState(false)

  useImperativeHandle(ref, () => ({
    play: (name, opts) => {
      if (sceneRef.current) return sceneRef.current.play(name, opts)
      opts?.onHit?.() // ainda carregando: não trava o fluxo
      return Promise.resolve()
    },
  }))

  useEffect(() => {
    let disposed = false
    let io
    let onMove
    let onVis
    const boot = async () => {
      try {
        const { createUnicornScene } = await import('../three/unicornScene.js')
        if (disposed || !canvasRef.current) return
        const s = await createUnicornScene(canvasRef.current, {
          reduceMotion: !!reduce,
          yaw,
          onFirstFrame: () => !disposed && setReady(true),
        })
        if (disposed) return s.dispose()
        sceneRef.current = s
        let visible = false
        io = new IntersectionObserver(([e]) => {
          visible = e.isIntersecting
          visible && !document.hidden ? s.start() : s.stop()
        })
        io.observe(wrapRef.current)
        onVis = () => (document.hidden || !visible ? s.stop() : s.start())
        document.addEventListener('visibilitychange', onVis)
        onMove = (ev) => {
          const r = wrapRef.current?.getBoundingClientRect()
          if (!r) return
          s.look(((ev.clientX - (r.left + r.width / 2)) / (window.innerWidth / 2)) * 1.2)
        }
        window.addEventListener('pointermove', onMove, { passive: true })
      } catch (err) {
        // sem WebGL / falha de rede → mantém o poster
        if (import.meta.env.DEV) console.warn('Unicórnio 3D indisponível:', err)
      }
    }
    // espera o navegador ficar livre para não atrasar a primeira pintura
    const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 120))
    const handle = eager ? (boot(), null) : idle(boot)
    return () => {
      disposed = true
      if (handle && window.cancelIdleCallback) window.cancelIdleCallback(handle)
      io?.disconnect()
      onMove && window.removeEventListener('pointermove', onMove)
      onVis && document.removeEventListener('visibilitychange', onVis)
      sceneRef.current?.dispose()
      sceneRef.current = null
    }
  }, [reduce, yaw, eager])

  const pet = () => {
    if (!onPet) return
    const p = sceneRef.current ? sceneRef.current.play('pet', { onHit: onPet }) : (onPet(), null)
    return p
  }

  const Tag = onPet ? 'button' : 'div'
  return (
    <Tag
      ref={wrapRef}
      type={onPet ? 'button' : undefined}
      onClick={onPet ? pet : undefined}
      aria-label={onPet ? `${label} — toque para fazer carinho` : undefined}
      role={onPet ? undefined : 'img'}
      {...(!onPet && { 'aria-label': label })}
      className={`relative block select-none ${onPet ? 'cursor-pointer rounded-[2rem]' : ''} ${className}`}
      style={{ touchAction: 'manipulation', WebkitTapHighlightColor: 'transparent' }}
    >
      <img
        src={POSTER}
        alt=""
        aria-hidden="true"
        draggable="false"
        decoding="async"
        className={`pointer-events-none absolute inset-0 h-full w-full object-contain transition-opacity duration-500 ${ready ? 'opacity-0' : 'opacity-100'}`}
      />
      <canvas ref={canvasRef} aria-hidden="true" className={`absolute inset-0 h-full w-full transition-opacity duration-500 ${ready ? 'opacity-100' : 'opacity-0'}`} />
    </Tag>
  )
})

export default Unicorn3D
