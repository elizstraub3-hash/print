/**
 * Renderiza as 9 cenas 3D em MP4 vertical (H.264) + poster de cada cena.
 * Uso: npm run historia [-- --cenas=1,2 --fps=30 --w=720 --h=1280 --amostra]
 * Requer Playwright (Chromium) e ffmpeg.
 */
import { createRequire } from 'node:module'; import { createServer } from 'vite'
import { mkdirSync, rmSync, writeFileSync } from 'node:fs'; import { execFileSync } from 'node:child_process'; import path from 'node:path'
const { chromium } = createRequire(process.cwd() + '/')('playwright')
const arg = (k, d) => (process.argv.find((a) => a.startsWith(`--${k}=`)) || '').split('=')[1] || d
const FPS = Number(arg('fps', 30)), W = Number(arg('w', 720)), H = Number(arg('h', 1280))
const sample = process.argv.includes('--amostra')
const OUT = path.resolve('public/video/historia'); mkdirSync(OUT, { recursive: true })
const TMP = path.resolve('node_modules/.cache/historia-frames')
const server = await createServer({ root: process.cwd(), logLevel: 'error', server: { port: 5193, hmr: false, watch: null } }); await server.listen()
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] })
const p = await b.newPage({ viewport: { width: W, height: H } }); p.on('pageerror', (e) => console.error('ERR', e.message))
await p.goto(`http://localhost:5193/tools/historia3d/render.html?w=${W}&h=${H}`); await p.waitForFunction(() => window.ready, null, { timeout: 120000 })
const durs = await p.evaluate(() => window.SCENES)
const list = arg('cenas', '') ? arg('cenas').split(',').map((n) => Number(n) - 1) : durs.map((_, i) => i)
for (const i of list) {
  const dir = path.join(TMP, `c${i + 1}`); rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true })
  const N = sample ? 1 : Math.round(durs[i] * FPS)
  const t0 = Date.now()
  for (let f = 0; f < N; f++) {
    const t = sample ? durs[i] * 0.55 : f / FPS
    const data = await p.evaluate(([i, t]) => { window.renderFrame(i, t); return window.frameJPEG(0.92) }, [i, t])
    writeFileSync(path.join(dir, `f${String(f).padStart(4, '0')}.jpg`), Buffer.from(data.split(',')[1], 'base64'))
  }
  if (sample) { execFileSync('cp', [path.join(dir, 'f0000.jpg'), path.join(OUT, `amostra-${i + 1}.jpg`)]); console.log('amostra', i + 1); continue }
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(dir, 'f%04d.jpg'), '-c:v', 'libx264', '-profile:v', 'main', '-pix_fmt', 'yuv420p', '-crf', '24', '-preset', 'slow', '-movflags', '+faststart', path.join(OUT, `cena-${i + 1}.mp4`)])
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', path.join(dir, `f${String(Math.round(N * 0.6)).padStart(4, '0')}.jpg`), '-vf', 'scale=540:-1', '-q:v', '4', path.join(OUT, `cena-${i + 1}.jpg`)])
  console.log(`cena ${i + 1}: ${N} quadros em ${((Date.now() - t0) / 1000).toFixed(0)}s`)
}
await b.close(); await server.close()
