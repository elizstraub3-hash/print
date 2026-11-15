import { CREDIT } from '../config/event.js'

/** Rodapé com o crédito da criadora do convite */
export default function Footer() {
  if (!CREDIT?.name) return null
  const digits = String(CREDIT.whatsapp || '').replace(/\D/g, '')
  const wa = digits.length >= 10 ? `https://wa.me/${digits.length <= 11 ? '55' + digits : digits}?text=${encodeURIComponent('Olá, Eliz! Vi o convite digital da Sophie e quero um assim também! ✨🦄')}` : null
  return (
    <footer className="bg-lilas/60 px-5 py-5 text-center font-sans text-sm text-ameixa">
      <p>
        Convite criado com 💖 por <strong className="font-bold">{CREDIT.name}</strong>
      </p>
      {wa && (
        <a href={wa} target="_blank" rel="noopener noreferrer" className="mt-1 inline-flex min-h-[44px] items-center gap-1 font-semibold underline decoration-rosaForte/60 underline-offset-4">
          WhatsApp: {CREDIT.whatsapp}
        </a>
      )}
    </footer>
  )
}
