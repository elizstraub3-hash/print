/**
 * Renderiza o unicórnio 3D em imagem (poster/fallback): public/img/unicornio-3d.png
 * Depois converta para WebP (ex.: squoosh.app ou `cwebp -q 82`). Uso: npm run poster
 */
import { createServer } from 'vite'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const { chromium } = createRequire(root + '/')('playwright')
const server = await createServer({ root, logLevel: 'error', server: { port: 5197 } })
await server.listen()
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] })
const page = await browser.newPage({ viewport: { width: 900, height: 900 } })
page.on('pageerror', (e) => console.error(e))
await page.goto('http://localhost:5197/tools/poster.html?yaw=-0.5')
await page.waitForFunction(() => window.ready, null, { timeout: 60000 })
await page.waitForTimeout(300)
const out = path.join(root, 'public/img/unicornio-3d.png')
await page.locator('#c').screenshot({ path: out, omitBackground: true })
await browser.close()
await server.close()
console.log('✓', out)
