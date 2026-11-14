import { useId, useState } from 'react'
import { GIFT_LIST, RSVP_DEADLINE } from '../config/event.js'
import { buildRsvpMessage, buildWhatsAppUrl, getRsvpPhone, getGiftUrl, getGiftStores, MAPS_URL, CALENDAR_URL } from '../lib/event-utils.js'
import { AgendaIcon, InstagramIcon } from './Icons.jsx'
import Reveal from './Reveal.jsx'
import ArtButton from './ArtButton.jsx'
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

      <ArtButton
        art="confirmar"
        className="mx-auto mt-4 w-[min(100%,20rem)]"
        label={href ? 'Confirmar presença pelo WhatsApp (abre o WhatsApp)' : 'Confirmar presença — em breve'}
        href={href || undefined}
        disabled={!href}
        note={href ? null : 'A confirmação pelo WhatsApp será liberada em breve.'}
      />
      {!href && import.meta.env.DEV && (
        <p className="mt-1 rounded-lg bg-amarelo/70 px-2 py-1 text-center text-xs text-ameixa">
          Dev: defina <code>RSVP_PHONE</code> em <code>src/config/event.js</code>
        </p>
      )}
      {href && <p className="mt-3 text-center font-sans text-xs text-ameixaSoft">Abre o WhatsApp com a mensagem pronta — é só enviar 💌</p>}
    </div>
  )
}

export default function Actions() {
  const giftUrl = getGiftUrl()
  const stores = getGiftStores()
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

        <Reveal delay={0.15} className="mt-6 grid justify-items-center gap-3">
          <ArtButton art="localizacao" className="w-[min(100%,20rem)]" label="Ver localização no Google Maps (abre em nova aba)" href={MAPS_URL} />
          <a href={CALENDAR_URL} target="_blank" rel="noopener noreferrer" className="btn-soft max-w-[20rem]">
            <AgendaIcon className="h-6 w-6" /> Salvar na agenda
          </a>
        </Reveal>

        {(giftUrl || stores.length > 0) && (
          <Reveal delay={0.2} className="mt-8">
            <div id="presentes" className="scroll-mt-4 rounded-[2rem] bg-white/85 p-5 text-center shadow-soft ring-1 ring-white">
              <h3 className="font-script text-3xl font-bold text-rosaForte">Lista de presentes</h3>
              <p className="mx-auto mt-2 max-w-[32ch] font-sans text-base text-ameixa">{GIFT_LIST.note}</p>
              {giftUrl && <ArtButton art="presentes" className="mx-auto mt-3 w-[min(100%,18rem)]" label={`${GIFT_LIST.label} (abre em nova aba)`} href={giftUrl} />}
              {stores.length > 0 && (
                <ul className="mt-4 grid gap-2.5">
                  {stores.map((st) => (
                    <li key={st.url}>
                      <a href={st.url} target="_blank" rel="noopener noreferrer" className="btn-soft !min-h-[54px] !text-base" aria-label={`Loja ${st.name} no Instagram (abre em nova aba)`}>
                        <InstagramIcon className="h-6 w-6 shrink-0 text-rosaForte" />
                        <span className="min-w-0 truncate">{st.name}</span>
                      </a>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </Reveal>
        )}
      </div>
    </section>
  )
}
