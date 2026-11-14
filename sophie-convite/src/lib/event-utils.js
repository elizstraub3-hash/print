import { EVENT, RSVP_PHONE, GIFT_LIST } from '../config/event.js'

export const START = new Date(EVENT.startsAt)
export const END = new Date(START.getTime() + EVENT.durationHours * 3600 * 1000)

export const FULL_ADDRESS = `${EVENT.addressLine}, ${EVENT.neighborhood}, ${EVENT.city} - ${EVENT.state}, ${EVENT.country}`
export const SHORT_ADDRESS = `${EVENT.addressLine}, ${EVENT.neighborhood}, ${EVENT.city}/${EVENT.state}`

const fmt = (opts) => new Intl.DateTimeFormat('pt-BR', { timeZone: EVENT.timeZone, ...opts }).format(START)

/** "domingo, 13 de dezembro de 2026" — calculado, nunca digitado à mão */
export const DATE_LONG = fmt({ weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
export const WEEKDAY = fmt({ weekday: 'long' })
export const DAY_MONTH = fmt({ day: '2-digit', month: '2-digit' })
/** "11h30" */
export const TIME_LABEL = (() => {
  const [h, m] = fmt({ hour: '2-digit', minute: '2-digit', hour12: false }).split(':')
  return m === '00' ? `${Number(h)}h` : `${Number(h)}h${m}`
})()

/** Estado da contagem: before | live | after */
export function getCountdown(now = Date.now()) {
  if (now >= END.getTime()) return { phase: 'after' }
  if (now >= START.getTime()) return { phase: 'live' }
  let s = Math.floor((START.getTime() - now) / 1000)
  const days = Math.floor(s / 86400); s -= days * 86400
  const hours = Math.floor(s / 3600); s -= hours * 3600
  const minutes = Math.floor(s / 60)
  const seconds = s - minutes * 60
  // "É hoje!" no fuso de Brasília
  const day = (d) => new Intl.DateTimeFormat('en-CA', { timeZone: EVENT.timeZone }).format(d)
  return { phase: 'before', days, hours, minutes, seconds, isToday: day(new Date(now)) === day(START) }
}

/* ---------- Links reais ---------- */

export const MAPS_URL = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${EVENT.venueName}, ${FULL_ADDRESS}`)}`
export const MAPS_ADDRESS_URL = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(FULL_ADDRESS)}`

/** Normaliza o telefone; retorna null se não estiver configurado/válido */
export function getRsvpPhone() {
  const digits = String(RSVP_PHONE || '').replace(/\D/g, '')
  // Brasil: 55 + DDD (2) + 8/9 dígitos  → 12 ou 13 dígitos. Outros países: 10–15.
  if (digits.length < 10 || digits.length > 15) return null
  return digits
}

export function buildRsvpMessage({ name = '', adults = 1, kids = 0 } = {}) {
  const lines = [
    `Olá! 🦄✨ Quero confirmar presença no aniversário de ${EVENT.age} anos da ${EVENT.childFirstName}!`,
    `📅 ${DAY_MONTH} às ${TIME_LABEL} · ${EVENT.venueName}`,
    '',
    `Nome: ${name.trim() || '(seu nome)'}`,
    `Adultos: ${adults}`,
    `Crianças: ${kids}`,
  ]
  return lines.join('\n')
}

export function buildWhatsAppUrl(phone, message) {
  return `https://wa.me/${phone}?text=${encodeURIComponent(message)}`
}

const gcalDate = (d) => d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '')
export const CALENDAR_URL =
  'https://calendar.google.com/calendar/render?action=TEMPLATE' +
  `&text=${encodeURIComponent(`Aniversário de ${EVENT.age} anos da ${EVENT.childFirstName} 🦄`)}` +
  `&dates=${gcalDate(START)}/${gcalDate(END)}` +
  `&ctz=${encodeURIComponent(EVENT.timeZone)}` +
  `&location=${encodeURIComponent(`${EVENT.venueName} - ${FULL_ADDRESS}`)}` +
  `&details=${encodeURIComponent(EVENT.message)}`

/** Lista de presentes só aparece com enabled=true e URL https válida */
export function getGiftUrl() {
  if (!GIFT_LIST.enabled) return null
  try {
    const u = new URL(GIFT_LIST.url)
    return u.protocol === 'https:' ? u.href : null
  } catch {
    return null
  }
}
