/**
 * Prêmios sorteados no jogo: vestido (jogando com a Sophie) ou coroa (com a Layla).
 * Desenhos em SVG — cores e enfeites mudam a cada sorteio.
 */
const DRESSES = [
  { name: 'Vestido Arco-íris Encantado', c: ['#F7A8CF', '#C9B5F2', '#A9DCF2', '#FFE58F'], deco: 'star' },
  { name: 'Vestido Princesa das Estrelas', c: ['#B79BEA', '#D9C6F7', '#EFE6FF', '#EBCB85'], deco: 'star' },
  { name: 'Vestido Nuvem de Algodão', c: ['#FFFFFF', '#FBE3EF', '#F7C6DE', '#EBCB85'], deco: 'heart' },
  { name: 'Vestido Jardim Mágico', c: ['#B9EBD2', '#F7A8CF', '#FFE0EE', '#F2A900'], deco: 'flower' },
  { name: 'Vestido Céu de Unicórnio', c: ['#A9DCF2', '#C9B5F2', '#E9F6FD', '#EBCB85'], deco: 'heart' },
  { name: 'Vestido Doce de Morango', c: ['#F48CC0', '#FFC2DD', '#FFE6F1', '#E85FA0'], deco: 'flower' },
  { name: 'Vestido Brilho Dourado', c: ['#FFE58F', '#FFF3C4', '#F7C6DE', '#D99A1E'], deco: 'star' },
]
const CROWNS = [
  { name: 'Coroa de Cristal Rosa', c: ['#F7C9DF', '#E85FA0', '#FFFFFF'] },
  { name: 'Coroa Arco-íris', c: ['#FFE58F', '#C9B5F2', '#A9DCF2'] },
  { name: 'Coroa de Estrelas Douradas', c: ['#FFD36B', '#F2A900', '#FFF3C4'] },
  { name: 'Coroa de Flores Mágicas', c: ['#FFE58F', '#F48CC0', '#B9EBD2'] },
  { name: 'Coroa de Diamante Lilás', c: ['#E2D3F9', '#9B6BDB', '#FFFFFF'] },
  { name: 'Coroa do Céu Azul', c: ['#FFE58F', '#3FA7D6', '#E9F6FD'] },
]

import { DRESSUP } from '../config/event.js'

/** vestido n (0 = principal) da lista do guarda-roupa */
export function dressPrize(n) {
  const list = DRESSUP?.dresses || []
  if (!list.length) return drawPrize('dress')
  const d = list[n % list.length]
  return { kind: 'dress', name: d.name, img: d.src }
}

export function drawPrize(kind, avoid) {
  const list = kind === 'crown' ? CROWNS : DRESSES
  let p
  do p = list[Math.floor(Math.random() * list.length)]
  while (list.length > 1 && avoid && p.name === avoid)
  return { kind, ...p }
}

function Deco({ type, x, y, s, fill }) {
  if (type === 'heart') return <path transform={`translate(${x} ${y}) scale(${s})`} d="M0 3C-2 1 -3.5 -.4 -3.5 -1.8 -3.5 -3 -2.5 -3.8 -1.5 -3.8 -.8 -3.8 -.3 -3.4 0 -2.9 .3 -3.4 .8 -3.8 1.5 -3.8 2.5 -3.8 3.5 -3 3.5 -1.8 3.5 -.4 2 1 0 3Z" fill={fill} />
  if (type === 'flower') return <g transform={`translate(${x} ${y}) scale(${s})`}>{[0, 72, 144, 216, 288].map((a) => <ellipse key={a} cx="0" cy="-2" rx="1.4" ry="2" fill={fill} transform={`rotate(${a})`} />)}<circle r="1.1" fill="#FFE58F" /></g>
  return <path transform={`translate(${x} ${y}) scale(${s})`} d="M0 -4L1.2 -1.2 4 -1.2 1.8 .6 2.6 3.6 0 1.8 -2.6 3.6 -1.8 .6 -4 -1.2 -1.2 -1.2Z" fill={fill} />
}

export function PrizeArt({ prize, className = '' }) {
  if (!prize) return null
  if (prize.img) return <img src={prize.img} alt={prize.name} className={`object-contain ${className}`} draggable="false" />
  if (prize.kind === 'crown') {
    const [base, gem, shine] = prize.c
    return (
      <svg viewBox="0 0 120 100" className={className} role="img" aria-label={prize.name}>
        <defs>
          <linearGradient id="cr-b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#fff" stopOpacity=".7" /><stop offset=".35" stopColor={base} /><stop offset="1" stopColor={base} /></linearGradient>
        </defs>
        <path d="M14 78 L10 30 L36 52 L60 16 L84 52 L110 30 L106 78 Z" fill="url(#cr-b)" stroke="#fff" strokeWidth="4" strokeLinejoin="round" />
        <path d="M14 78 L10 30 L36 52 L60 16 L84 52 L110 30 L106 78 Z" fill="none" stroke="#B88832" strokeOpacity=".5" strokeWidth="1.5" strokeLinejoin="round" />
        <rect x="12" y="72" width="96" height="16" rx="8" fill={base} stroke="#fff" strokeWidth="3" />
        {[24, 42, 60, 78, 96].map((x, i) => <circle key={x} cx={x} cy="80" r={i === 2 ? 5 : 3.6} fill={i % 2 ? shine : gem} stroke="#fff" strokeWidth="1.2" />)}
        {[[10, 30], [60, 16], [110, 30]].map(([x, y]) => <circle key={x} cx={x} cy={y} r="6" fill={gem} stroke="#fff" strokeWidth="2" />)}
        <path d="M60 46 L63 54 L71 54 L65 59 L67 67 L60 62 L53 67 L55 59 L49 54 L57 54Z" fill={gem} stroke="#fff" strokeWidth="1.5" />
        <path d="M24 40 L28 66" stroke="#fff" strokeWidth="3" strokeLinecap="round" opacity=".7" />
      </svg>
    )
  }
  const [a, b, c, gold] = prize.c
  return (
    <svg viewBox="0 0 120 140" className={className} role="img" aria-label={prize.name}>
      <path d="M48 12 Q60 20 72 12 L78 44 Q60 52 42 44 Z" fill={b} stroke="#fff" strokeWidth="3" strokeLinejoin="round" />
      <ellipse cx="40" cy="22" rx="10" ry="8" fill={c} stroke="#fff" strokeWidth="2.5" />
      <ellipse cx="80" cy="22" rx="10" ry="8" fill={c} stroke="#fff" strokeWidth="2.5" />
      <path d="M40 46 Q60 54 80 46 L96 84 Q60 96 24 84 Z" fill={a} stroke="#fff" strokeWidth="3" strokeLinejoin="round" />
      <path d="M26 80 Q60 92 94 80 L108 118 Q60 134 12 118 Z" fill={b} stroke="#fff" strokeWidth="3" strokeLinejoin="round" />
      <path d="M12 116 Q24 126 36 118 Q48 128 60 120 Q72 128 84 118 Q96 126 108 116" fill="none" stroke={gold} strokeWidth="2.5" strokeLinecap="round" />
      <path d="M50 44 Q60 50 70 44 L66 52 Q60 56 54 52 Z" fill={gold} />
      <path d="M52 46 C46 40 40 42 42 48 C44 52 50 50 56 48 Z M68 46 C74 40 80 42 78 48 C76 52 70 50 64 48 Z" fill={c} stroke="#fff" strokeWidth="1.5" />
      <circle cx="60" cy="48" r="3.4" fill={gold} stroke="#fff" strokeWidth="1.2" />
      {[[36, 70, 1.2], [60, 72, 1.4], [84, 70, 1.2], [26, 104, 1.3], [48, 108, 1.5], [72, 108, 1.5], [94, 104, 1.3], [60, 30, 1.1]].map(([x, y, s], i) => (
        <Deco key={i} type={prize.deco} x={x} y={y} s={s} fill={i % 2 ? gold : '#fff'} />
      ))}
    </svg>
  )
}
