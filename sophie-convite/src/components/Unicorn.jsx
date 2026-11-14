/**
 * Unicórnio autoral em SVG (sem imagens externas).
 * Cabeça frontal estilo "kawaii": olhos fechados, crina pastel,
 * chifre dourado espiralado, coroa de flores e laço.
 */
export default function Unicorn({ className = '', title = 'Unicórnio branco de olhos fechados com crina pastel e chifre dourado', idPrefix = 'u' }) {
  const g = (n) => `${idPrefix}-${n}`
  return (
    <svg viewBox="0 0 320 340" className={className} role="img" aria-label={title} xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id={g('horn')} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#FFF4D2" />
          <stop offset=".55" stopColor="#EBCB85" />
          <stop offset="1" stopColor="#D9AE5C" />
        </linearGradient>
        <radialGradient id={g('face')} cx=".45" cy=".35" r=".75">
          <stop offset="0" stopColor="#FFFFFF" />
          <stop offset=".75" stopColor="#FFFBFD" />
          <stop offset="1" stopColor="#F6EAF3" />
        </radialGradient>
        <linearGradient id={g('snout')} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#FFF6FA" />
          <stop offset="1" stopColor="#FCE3EF" />
        </linearGradient>
        <linearGradient id={g('ribbon')} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#FBDDEB" />
          <stop offset="1" stopColor="#F2B6D2" />
        </linearGradient>
      </defs>

      {/* crina de trás (lado esquerdo e direito) */}
      <g>
        <path d="M92 118 C52 132 40 178 52 214 C60 240 46 262 30 274 C64 280 92 262 100 236 C108 212 104 186 112 160 Z" fill="#DCCCF7" />
        <path d="M96 150 C70 170 70 206 78 232 C84 254 72 276 58 292 C92 290 112 266 114 240 C116 214 112 190 118 170 Z" fill="#F8CDE3" />
        <path d="M226 116 C262 128 278 168 270 204 C264 230 276 250 290 262 C258 270 232 254 222 230 C214 210 216 184 208 160 Z" fill="#CDECF7" />
        <path d="M222 150 C246 168 248 200 242 224 C238 244 248 262 260 276 C230 276 212 256 210 234 C208 212 210 190 206 172 Z" fill="#D6EEDC" />
      </g>

      {/* pescoço + peito */}
      <path d="M118 236 C116 270 110 300 100 330 L222 330 C212 300 206 270 204 236 Z" fill={`url(#${g('face')})`} />

      {/* laço no pescoço */}
      <g transform="translate(161 292)">
        <path d="M-4 0 C-26 -20 -52 -18 -54 2 C-56 22 -28 24 -4 6 Z" fill={`url(#${g('ribbon')})`} />
        <path d="M4 0 C26 -20 52 -18 54 2 C56 22 28 24 4 6 Z" fill={`url(#${g('ribbon')})`} />
        <path d="M-8 6 L-22 36 L-12 33 L-6 42 L0 10 Z" fill="#F2B6D2" />
        <path d="M8 6 L22 36 L12 33 L6 42 L0 10 Z" fill="#F2B6D2" />
        <path d="M-40 -2 C-34 -8 -24 -8 -16 0" stroke="#fff" strokeOpacity=".7" strokeWidth="3" fill="none" strokeLinecap="round" />
        <path d="M40 -2 C34 -8 24 -8 16 0" stroke="#fff" strokeOpacity=".7" strokeWidth="3" fill="none" strokeLinecap="round" />
        <rect x="-10" y="-9" width="20" height="18" rx="8" fill="#F5C2DA" />
      </g>

      {/* orelhas */}
      <g>
        <path d="M104 96 C92 62 100 40 114 30 C126 48 136 72 134 96 Z" fill="#FFFFFF" stroke="#F0E2EC" strokeWidth="2" />
        <path d="M110 90 C104 68 108 54 115 46 C122 60 126 76 126 92 Z" fill="#F8CDE3" />
        <path d="M216 96 C228 62 220 40 206 30 C194 48 184 72 186 96 Z" fill="#FFFFFF" stroke="#F0E2EC" strokeWidth="2" />
        <path d="M210 90 C216 68 212 54 205 46 C198 60 194 76 194 92 Z" fill="#F8CDE3" />
      </g>

      {/* cabeça */}
      <path d="M160 74 C222 74 246 120 244 160 C242 196 230 214 222 226 C210 246 190 258 160 258 C130 258 110 246 98 226 C90 214 78 196 76 160 C74 120 98 74 160 74 Z" fill={`url(#${g('face')})`} stroke="#F0E2EC" strokeWidth="2" />

      {/* focinho */}
      <ellipse cx="160" cy="214" rx="56" ry="40" fill={`url(#${g('snout')})`} />
      <ellipse cx="141" cy="214" rx="6" ry="4.2" fill="#E9A9C6" />
      <ellipse cx="179" cy="214" rx="6" ry="4.2" fill="#E9A9C6" />
      <path d="M150 234 Q160 241 170 234" stroke="#D48FB0" strokeWidth="3" fill="none" strokeLinecap="round" />

      {/* bochechas */}
      <ellipse cx="108" cy="184" rx="15" ry="9" fill="#F8B9D4" opacity=".55" />
      <ellipse cx="212" cy="184" rx="15" ry="9" fill="#F8B9D4" opacity=".55" />

      {/* olhos fechados + cílios */}
      <g stroke="#6B4E71" strokeWidth="4" fill="none" strokeLinecap="round">
        <path d="M112 162 Q128 176 144 162" />
        <path d="M176 162 Q192 176 208 162" />
        <path d="M113 163 L105 157" strokeWidth="3" />
        <path d="M117 168 L109 168" strokeWidth="3" />
        <path d="M207 163 L215 157" strokeWidth="3" />
        <path d="M203 168 L211 168" strokeWidth="3" />
      </g>

      {/* chifre espiralado */}
      <g>
        <path d="M160 6 L178 84 C168 90 152 90 142 84 Z" fill={`url(#${g('horn')})`} />
        <g stroke="#C9994A" strokeOpacity=".55" strokeWidth="2.5" fill="none" strokeLinecap="round">
          <path d="M152 30 Q160 36 166 28" />
          <path d="M148 46 Q160 54 170 44" />
          <path d="M145 62 Q160 72 174 60" />
          <path d="M143 76 Q160 86 177 74" />
        </g>
        <path d="M157 18 L150 70" stroke="#FFFBEA" strokeOpacity=".8" strokeWidth="3" strokeLinecap="round" />
      </g>

      {/* topete (franja) */}
      <g>
        <path d="M120 96 C126 76 150 70 160 88 C150 92 142 106 140 122 C130 112 122 106 120 96 Z" fill="#F8CDE3" />
        <path d="M200 96 C194 76 170 70 160 88 C170 92 178 106 180 122 C190 112 198 106 200 96 Z" fill="#DCCCF7" />
        <path d="M132 100 C138 90 148 88 154 96 C146 100 142 108 140 116 C136 110 132 106 132 100 Z" fill="#FBE3EF" />
      </g>

      {/* coroa de flores */}
      <Flower x={112} y={100} r={13} petal="#FFF0B9" center="#EBCB85" />
      <Flower x={92} y={124} r={10} petal="#F8CDE3" center="#EBCB85" />
      <Flower x={208} y={100} r={13} petal="#CDECF7" center="#EBCB85" />
      <Flower x={228} y={124} r={10} petal="#F8CDE3" center="#EBCB85" />
      <Leaf x={100} y={108} rot={-40} />
      <Leaf x={222} y={110} rot={220} />

      {/* brilhos */}
      <Sparkle x={262} y={56} s={12} />
      <Sparkle x={56} y={70} s={9} />
      <Sparkle x={282} y={150} s={7} />
    </svg>
  )
}

function Flower({ x, y, r, petal, center }) {
  const petals = [0, 72, 144, 216, 288]
  return (
    <g transform={`translate(${x} ${y})`}>
      {petals.map((a) => (
        <ellipse key={a} cx="0" cy={-r * 0.62} rx={r * 0.48} ry={r * 0.62} fill={petal} stroke="#fff" strokeWidth="1.5" transform={`rotate(${a})`} />
      ))}
      <circle r={r * 0.36} fill={center} />
    </g>
  )
}

function Leaf({ x, y, rot }) {
  return <path d="M0 0 C6 -8 16 -8 20 0 C16 8 6 8 0 0 Z" fill="#BFE3C8" transform={`translate(${x} ${y}) rotate(${rot})`} />
}

export function Sparkle({ x, y, s, fill = '#EBCB85' }) {
  return (
    <path
      transform={`translate(${x} ${y})`}
      d={`M0 ${-s} C${s * 0.15} ${-s * 0.15} ${s * 0.15} ${-s * 0.15} ${s} 0 C${s * 0.15} ${s * 0.15} ${s * 0.15} ${s * 0.15} 0 ${s} C${-s * 0.15} ${s * 0.15} ${-s * 0.15} ${s * 0.15} ${-s} 0 C${-s * 0.15} ${-s * 0.15} ${-s * 0.15} ${-s * 0.15} 0 ${-s} Z`}
      fill={fill}
    />
  )
}
