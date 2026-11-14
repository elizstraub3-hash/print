/**
 * Pattern repetível (tile SVG 240×240) com mini estrelas, corações,
 * nuvens e pequenos unicórnios. Gerado em código: zero requisições.
 */
const star = (x, y, s, c) =>
  `<path transform="translate(${x} ${y})" d="M0 -${s} C${s * 0.15} -${s * 0.15} ${s * 0.15} -${s * 0.15} ${s} 0 C${s * 0.15} ${s * 0.15} ${s * 0.15} ${s * 0.15} 0 ${s} C-${s * 0.15} ${s * 0.15} -${s * 0.15} ${s * 0.15} -${s} 0 C-${s * 0.15} -${s * 0.15} -${s * 0.15} -${s * 0.15} 0 -${s}Z" fill="${c}"/>`
const heart = (x, y, k, c) =>
  `<path transform="translate(${x} ${y}) scale(${k})" d="M12 21C5 15 1 11.5 1 7C1 3.5 3.7 1 7 1C9.2 1 11 2.2 12 4C13 2.2 14.8 1 17 1C20.3 1 23 3.5 23 7C23 11.5 19 15 12 21Z" fill="${c}"/>`
const cloud = (x, y, k, c) =>
  `<path transform="translate(${x} ${y}) scale(${k})" d="M38 90C14 90 6 70 18 56C10 36 34 22 52 32C58 12 92 4 108 24C122 8 158 14 158 40C182 38 196 58 186 76C182 86 172 90 160 90Z" fill="${c}"/>`
// mini unicórnio (silhueta de perfil)
const uni = (x, y, k, c) =>
  `<g transform="translate(${x} ${y}) scale(${k})"><path d="M14 2 L18 14 L14 13Z" fill="#EBCB85"/><path d="M10 14C10 9 16 8 19 12C22 14 26 18 25 21C24 23 21 23 19 21C18 24 17 28 18 32L8 32C7 26 8 20 10 14Z" fill="${c}"/><path d="M10 14C5 16 4 22 6 28C2 24 2 16 10 12Z" fill="#DCCCF7"/></g>`

const TILE = `<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">
${star(20, 24, 6, '#EBCB85')}${star(150, 40, 4, '#E8B3CF')}${star(96, 120, 5, '#B9A4E6')}${star(212, 150, 6, '#EBCB85')}${star(44, 200, 4, '#9FD3E6')}${star(170, 222, 3, '#EBCB85')}
${heart(70, 30, 0.55, '#F2B6D2')}${heart(190, 96, 0.5, '#CDB8F0')}${heart(116, 196, 0.45, '#F2B6D2')}
${cloud(170, 6, 0.22, '#C9E7F3')}${cloud(18, 120, 0.2, '#E7DCF9')}
${uni(110, 46, 0.9, '#F5D3E4')}${uni(200, 186, 0.75, '#D9CDF5')}
</svg>`

export const PATTERN_URL = `url("data:image/svg+xml,${encodeURIComponent(TILE)}")`

export default function Pattern({ opacity = 0.32, className = '' }) {
  return (
    <div
      aria-hidden="true"
      className={`pointer-events-none absolute inset-0 ${className}`}
      style={{ backgroundImage: PATTERN_URL, backgroundSize: '240px 240px', opacity }}
    />
  )
}
