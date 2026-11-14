import { useId, useState } from 'react'
import { EVENT, GIFT_LIST, RSVP_DEADLINE, MUSIC } from '../config/event.js'
import { buildRsvpMessage, buildWhatsAppUrl, getRsvpPhone, getGiftUrl, MAPS_URL, CALENDAR_URL } from '../lib/event-utils.js'
import { WhatsIcon, PinIcon, GiftIcon, MusicIcon, MuteIcon, AgendaIcon } from './Icons.jsx'
import Reveal from './Reveal.jsx'
import Pattern from './Pattern.jsx'

function Stepper({ label, value, setValue, min = 0, max = 10 }) {
  const id = useId()
  return (
    <div className="flex items-center justify-between gap-3 rounded-2xl bg-white/80 px-4 py-2 ring-1 ring-rosa/60">
      <span id={id} className="font-sans text-base font-medium text-ameixa">{label}</span>
      <div className="flex items-center gap-2" role="group" aria-labelledby={id}>
        <button type="button" className="stepper-btn" onClick={() => setValue(Math.max(min, value - 1))} disabled={value <= min} aria-label={`Diminuir ${label.toLowerCase()}`}>−</button>
        <output className="w-7 text-center font-sans text-lg font-semibold tabular-nums text-ameixa" aria-live="polite">{value}</output>
        <button type="button" className="stepper-btn" onClick={() => setValue(Math.min(max, value + 1))} disabled={value >= max} aria-label={`Aumentar ${label.toLowerCase()}`}>+</button>
      </div>
    </div>
  )
}

function Rsvp() {
  const phone = getRsvpPhone()
  const [name, setName] = useState('')
  const [adults, setAdults] = useState(1)
  const [kids, setKids] = useState(0)
  const nameId = useId()
  const href = phone ? buildWhatsAppUrl(phone, buildRsvpMessage({ name, adults, kids })) : null

  return (
    <div className="rounded-[2rem] bg-white/90 p-5 text-left shadow-soft ring-1 ring-white">
      <h3 className="text-center font-script text-3xl font-bold text-rosaForte">Confirme sua presença</h3>
      {RSVP_DEADLINE && <p className="mt-1 text-center font-sans text-sm text-ameixaSoft">Por favor, confirme até {RSVP_DEADLINE}</p>}

      <div className="mt-4 grid gap-2.5">
        <label htmlFor={nameId} className="sr-only">Seu nome</label>
        <input
          id={nameId}
          type="text"
          autoComplete="name"
          placeholder="Seu nome (ou da família)"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="min-h-[52px] w-full rounded-2xl border-0 bg-white px-4 font-sans text-base text-ameixa placeholder:text-ameixaSoft/70 ring-1 ring-rosa focus:outline-none focus:ring-2 focus:ring-rosaForte"
        />
        <Stepper label="Adultos" value={adults} setValue={setAdults} min={0} max={15} />
        <Stepper label="Crianças" value={kids} setValue={setKids} min={0} max={15} />
      </div>

      {href ? (
        <a href={href} target="_blank" rel="noopener noreferrer" className="btn-whats mt-4 w-full">
          <WhatsIcon className="h-6 w-6" /> Confirmar presença
        </a>
      ) : (
        <div className="mt-4" role="note">
          <button type="button" disabled className="btn-disabled w-full" aria-describedby="rsvp-config">
            <WhatsIcon className="h-6 w-6" /> Confirmação em breve
          </button>
          <p id="rsvp-config" className="mt-2 text-center font-sans text-sm text-ameixaSoft">
            O número para confirmação ainda está sendo configurado.
            {import.meta.env.DEV && (
              <span className="mt-1 block rounded-lg bg-amarelo/70 px-2 py-1 text-xs text-ameixa">
                Dev: defina <code>RSVP_PHONE</code> em <code>src/config/event.js</code>
              </span>
            )}
          </p>
        </div>
      )}
      {href && <p className="mt-3 text-center font-sans text-xs text-ameixaSoft">Abre o WhatsApp com a mensagem pronta — é só enviar 💌</p>}
    </div>
  )
}

export default function Actions({ music }) {
  const giftUrl = getGiftUrl()
  const playing = music.status === 'playing' || music.status === 'loading'
  const musicLabel =
    music.status === 'unavailable'
      ? 'Música indisponível'
      : music.status === 'error'
      ? 'Não foi possível tocar'
      : playing
      ? 'Desligar música'
      : 'Ligar música'

  return (
    <section id="confirmar" aria-labelledby="acoes-titulo" className="relative overflow-hidden bg-gradient-to-b from-azul/70 via-menta/60 to-amarelo/60 px-5 py-16">
      <Pattern opacity={0.18} />
      <div className="relative mx-auto max-w-md">
        <Reveal className="text-center">
          <p className="font-sans text-xs font-semibold uppercase tracking-[0.3em] text-ameixaSoft">Com muito carinho</p>
          <h2 id="acoes-titulo" className="mt-2 font-sans text-[clamp(1.5rem,6.4vw,2rem)] font-semibold text-ameixa">
            Vem celebrar com a gente?
          </h2>
        </Reveal>

        <Reveal delay={0.1} className="mt-6">
          <Rsvp />
        </Reveal>

        <Reveal delay={0.15} className="mt-4 grid gap-3">
          <a href={MAPS_URL} target="_blank" rel="noopener noreferrer" className="btn-soft">
            <PinIcon className="h-6 w-6" /> Ver localização
          </a>
          <a href={CALENDAR_URL} target="_blank" rel="noopener noreferrer" className="btn-soft">
            <AgendaIcon className="h-6 w-6" /> Salvar na agenda
          </a>
          <button
            type="button"
            onClick={music.toggle}
            disabled={!music.available}
            aria-pressed={playing}
            className={music.available ? 'btn-soft' : 'btn-disabled'}
            title={music.status === 'unavailable' ? 'Nenhuma música configurada' : undefined}
          >
            {playing ? <MusicIcon className="h-6 w-6" /> : <MuteIcon className="h-6 w-6" />} {musicLabel}
            {playing && <span className="eq" aria-hidden="true"><i /><i /><i /></span>}
          </button>
          {music.status === 'unavailable' && import.meta.env.DEV && (
            <p className="text-center font-sans text-xs text-ameixaSoft">
              Dev: adicione um MP3 em <code>public/audio/</code> e configure <code>MUSIC.src</code> ({MUSIC.title}).
            </p>
          )}
        </Reveal>

        {giftUrl && (
          <Reveal delay={0.2} className="mt-6">
            <div className="rounded-[2rem] bg-white/85 p-5 text-center shadow-soft ring-1 ring-white">
              <GiftIcon className="mx-auto h-8 w-8 text-rosaForte" />
              <p className="mt-2 font-sans text-base text-ameixa">{GIFT_LIST.note}</p>
              <a href={giftUrl} target="_blank" rel="noopener noreferrer" className="btn-soft mt-4">
                <GiftIcon className="h-6 w-6" /> {GIFT_LIST.label}
              </a>
            </div>
          </Reveal>
        )}
      </div>
    </section>
  )
}
