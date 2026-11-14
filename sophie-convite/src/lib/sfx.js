/**
 * Efeitos sonoros sintetizados (Web Audio) — sem arquivos, sem direitos
 * autorais. Só soam após toque do usuário (regra de autoplay).
 */
let ac = null
let enabled = true
const NOTES = [1046.5, 1174.7, 1318.5, 1568.0, 1760.0, 2093.0] // dó6 → dó7 (pentatônica)

function ctx() {
  if (!enabled) return null
  try {
    ac ||= new (window.AudioContext || window.webkitAudioContext)()
    if (ac.state === 'suspended') ac.resume()
    return ac
  } catch {
    return null
  }
}

function bell(freq, at = 0, dur = 0.5, gain = 0.07) {
  const a = ctx()
  if (!a) return
  const t = a.currentTime + at
  const o = a.createOscillator()
  const o2 = a.createOscillator()
  const g = a.createGain()
  o.type = 'sine'
  o2.type = 'triangle'
  o.frequency.value = freq
  o2.frequency.value = freq * 2.01
  g.gain.setValueAtTime(0.0001, t)
  g.gain.exponentialRampToValueAtTime(gain, t + 0.01)
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur)
  const g2 = a.createGain()
  g2.gain.value = 0.25
  o.connect(g)
  o2.connect(g2).connect(g)
  g.connect(a.destination)
  o.start(t)
  o2.start(t)
  o.stop(t + dur + 0.05)
  o2.stop(t + dur + 0.05)
}

/** "plim" — sobe uma nota a cada estrelinha */
export const chime = (i = 0) => bell(NOTES[Math.min(i, NOTES.length - 1)])
/** arpejo de vitória */
export const fanfare = () => [0, 2, 3, 4, 5].forEach((n, k) => bell(NOTES[n], k * 0.09, 0.7, 0.06))
/** brilho curtinho (botões) */
export const sparkle = () => {
  bell(1568, 0, 0.25, 0.04)
  bell(2093, 0.06, 0.3, 0.035)
}
export const setSfxEnabled = (v) => (enabled = v)
