/**
 * "Caixinha de música mágica" — melodia ORIGINAL (sem direitos autorais),
 * sintetizada no próprio navegador (Web Audio). Gera o loop uma vez e repete.
 */
const BPM = 92
const BEAT = 60 / BPM
// melodia em 3/4 (valsinha): [nota MIDI, duração em tempos]
const MELODY = [
  [76, 1], [79, 1], [84, 1], [83, 2], [79, 1], [81, 1], [84, 1], [88, 1], [86, 3],
  [76, 1], [79, 1], [84, 1], [83, 2], [79, 1], [77, 1], [79, 1], [81, 1], [79, 3],
  [81, 1], [84, 1], [88, 1], [86, 2], [84, 1], [83, 1], [81, 1], [79, 1], [76, 3],
  [77, 1], [81, 1], [84, 1], [83, 1], [79, 1], [74, 1], [72, 3], [0, 3],
]
// acordes (um por compasso de 3 tempos): baixo + arpejo
const CHORDS = [
  [48, 52, 55], [53, 57, 60], [55, 59, 62], [48, 52, 55],
  [48, 52, 55], [53, 57, 60], [55, 59, 62], [48, 52, 55],
  [53, 57, 60], [55, 59, 62], [57, 60, 64], [52, 55, 59],
  [53, 57, 60], [55, 59, 62], [48, 52, 55], [48, 52, 55],
]
const hz = (n) => 440 * Math.pow(2, (n - 69) / 12)

function bell(ctx, out, t, freq, dur, gain) {
  const o1 = ctx.createOscillator()
  const o2 = ctx.createOscillator()
  const g = ctx.createGain()
  o1.type = 'sine'
  o2.type = 'sine'
  o1.frequency.value = freq
  o2.frequency.value = freq * 3.01 // brilho metálico de caixinha
  const g2 = ctx.createGain()
  g2.gain.value = 0.18
  g.gain.setValueAtTime(0.0001, t)
  g.gain.exponentialRampToValueAtTime(gain, t + 0.008)
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur)
  o1.connect(g)
  o2.connect(g2).connect(g)
  g.connect(out)
  o1.start(t)
  o2.start(t)
  o1.stop(t + dur + 0.05)
  o2.stop(t + dur + 0.05)
}

async function renderLoop(sampleRate) {
  const beats = MELODY.reduce((s, [, d]) => s + d, 0)
  const len = beats * BEAT
  const off = new OfflineAudioContext(2, Math.ceil((len + 0.01) * sampleRate), sampleRate)
  const master = off.createGain()
  master.gain.value = 0.9
  // eco suave (sala mágica)
  const delay = off.createDelay(1)
  delay.delayTime.value = BEAT * 0.75
  const fb = off.createGain()
  fb.gain.value = 0.28
  master.connect(off.destination)
  master.connect(delay)
  delay.connect(fb).connect(delay)
  fb.connect(off.destination)
  let t = 0
  for (const [n, d] of MELODY) {
    if (n) bell(off, master, t, hz(n), Math.max(1.2, d * BEAT * 1.6), 0.22)
    t += d * BEAT
  }
  CHORDS.forEach((ch, i) => {
    const t0 = i * 3 * BEAT
    bell(off, master, t0, hz(ch[0]), 2.2, 0.12)
    bell(off, master, t0 + BEAT, hz(ch[1] + 12), 1.2, 0.06)
    bell(off, master, t0 + 2 * BEAT, hz(ch[2] + 12), 1.2, 0.06)
  })
  return off.startRendering()
}

export function createMusicBox(volume = 0.5) {
  let ctx = null
  let buffer = null
  let src = null
  let gain = null
  let rendering = null
  const ensure = async () => {
    if (!ctx) {
      const AC = window.AudioContext || window.webkitAudioContext
      ctx = new AC()
      gain = ctx.createGain()
      gain.gain.value = volume
      gain.connect(ctx.destination)
    }
    if (ctx.state === 'suspended') await ctx.resume()
    if (!buffer) buffer = await (rendering ||= renderLoop(ctx.sampleRate))
  }
  return {
    async play() {
      // resume() precisa acontecer dentro do toque: chamado de forma síncrona primeiro
      if (ctx?.state === 'suspended') ctx.resume()
      await ensure()
      if (src) return
      src = ctx.createBufferSource()
      src.buffer = buffer
      src.loop = true
      src.connect(gain)
      gain.gain.cancelScheduledValues(ctx.currentTime)
      gain.gain.setValueAtTime(0.0001, ctx.currentTime)
      gain.gain.exponentialRampToValueAtTime(volume, ctx.currentTime + 1.2)
      src.start()
    },
    pause() {
      if (!src) return
      const s = src
      src = null
      try {
        gain.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.15)
        s.stop(ctx.currentTime + 0.6)
      } catch {
        /* ok */
      }
    },
    get playing() {
      return !!src
    },
  }
}
