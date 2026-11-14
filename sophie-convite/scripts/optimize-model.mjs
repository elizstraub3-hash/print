/**
 * Uso: npm run model -- caminho/do/modelo.glb
 * Gera public/models/unicornio.glb otimizado (requer Playwright + Chromium).
 */
import { createServer } from 'vite'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import { copyFileSync, writeFileSync, mkdirSync } from 'node:fs'
import path from 'node:path'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const input = path.resolve(process.argv[2] || path.join(root, 'tools/source/unicornio-original.glb'))
mkdirSync(path.join(root, 'tools/source'), { recursive: true })
const staged = path.join(root, 'tools/source/unicornio-original.glb')
if (input !== staged) copyFileSync(input, staged)

const { chromium } = createRequire(root + '/')('playwright')
const server = await createServer({ root, logLevel: 'error', server: { port: 5198 } })
await server.listen()
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] })
const page = await browser.newPage()
page.on('pageerror', (e) => console.error(e))
await page.goto('http://localhost:5198/tools/optimize-model.html?src=/tools/source/unicornio-original.glb')
await page.waitForFunction(() => window.result, null, { timeout: 60000 })
const { b64, calls, verts, mats } = await page.evaluate(() => window.result)
await browser.close(); await server.close()
const out = path.join(root, 'public/models/unicornio.glb')
writeFileSync(out, Buffer.from(b64, 'base64'))
console.log(`✓ ${out} — ${calls} draw calls, ${verts} vértices, ${(Buffer.from(b64, 'base64').length / 1024).toFixed(0)} KB`)
console.log(mats.map((m) => m.join(' ')).join('\n'))
