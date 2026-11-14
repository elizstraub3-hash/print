import { useId, useState } from 'react'
import { GIFT_LIST, RSVP_DEADLINE, RSVP_CONTACT } from '../config/event.js'
import { buildRsvpMessage, buildWhatsAppUrl, getRsvpPhone, getGiftUrl, getGiftStores, MAPS_URL, CALENDAR_URL } from '../lib/event-utils.js'
import { AgendaIcon, InstagramIcon, WhatsIcon, PhoneIcon, PinIcon } from './Icons.jsx'
import { EVENT } from '../config/event.js'
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
        label={href ? `Confirmar presença pelo WhatsApp${RSVP_CONTACT ? ` com ${RSVP_CONTACT}` : ''} (abre o WhatsApp)` : 'Confirmar presença — em breve'}
        href={href || undefined}
        disabled={!href}
        note={href ? null : 'A confirmação pelo WhatsApp será liberada em breve.'}
      />
      {!href && import.meta.env.DEV && (
        <p className="mt-1 rounded-lg bg-amarelo/70 px-2 py-1 text-center text-xs text-ameixa">
          Dev: defina <code>RSVP_PHONE</code> em <code>src/config/event.js</code>
        </p>
      )}
      {href && (
        <p className="mt-3 text-center font-sans text-sm text-ameixaSoft">
          Abre o WhatsApp{RSVP_CONTACT ? <> da <strong className="font-semibold text-ameixa">{RSVP_CONTACT}</strong></> : null} com a mensagem pronta — é só enviar 💌
        </p>
      )}
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
          <Reveal delay={0.1} className="mt-8">
            <div id="presentes" className="scroll-mt-4 rounded-[2rem] bg-white/90 p-5 text-center shadow-soft ring-1 ring-white">
              <h3 className="font-script text-[2.2rem] font-bold leading-tight text-rosaForte">Lista de presentes</h3>
              <p className="mx-auto mt-1 max-w-[32ch] font-sans text-base font-medium text-ameixa">{GIFT_LIST.note.replaceAll('{nome}', EVENT.childFirstName)}</p>

              {/* tamanhos */}
              {GIFT_LIST.sizes?.length > 0 && (
                <dl className="mt-4 grid grid-cols-2 gap-2.5">
                  {GIFT_LIST.sizes.map((z) => (
                    <div key={z.label} className="rounded-2xl bg-gradient-to-b from-rosa/60 to-lilas/50 px-3 py-3 ring-1 ring-white">
                      <dt className="font-sans text-xs font-semibold uppercase tracking-[0.15em] text-ameixaSoft">
                        <span aria-hidden="true">{z.icon} </span>
                        {z.label}
                      </dt>
                      <dd className="mt-0.5 font-sans text-lg font-semibold leading-tight text-ameixa">{z.value}</dd>
                    </div>
                  ))}
                </dl>
              )}

              {/* gostos */}
              {GIFT_LIST.likes?.length > 0 && (
                <div className="mt-4">
                  <p className="font-sans text-sm font-semibold text-ameixa">A {EVENT.childFirstName} adora:</p>
                  <ul className="mt-2 flex flex-wrap justify-center gap-1.5">
                    {GIFT_LIST.likes.map((l) => (
                      <li key={l} className="rounded-full bg-amarelo/80 px-3 py-1 font-sans text-sm font-semibold text-ameixa ring-1 ring-dourado/50">
                        {l}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {giftUrl && <ArtButton art="presentes" className="mx-auto mt-4 w-[min(100%,18rem)]" label={`${GIFT_LIST.label} (abre em nova aba)`} href={giftUrl} />}

              {/* lojas */}
              {stores.length > 0 && (
                <>
                  <p className="mt-5 font-sans text-sm font-semibold uppercase tracking-[0.18em] text-ameixaSoft">Lojas que ela ama</p>
                  <ul className="mt-2 grid gap-3 text-left">
                    {stores.map((st) => (
                      <li key={st.name} className="rounded-3xl bg-white p-4 shadow-soft ring-1 ring-rosa/50">
                        <p className="font-sans text-lg font-semibold leading-tight text-ameixa">{st.name}</p>
                        {st.place && <p className="font-sans text-sm text-ameixaSoft">{st.place}</p>}
                        <div className="mt-3 grid grid-cols-2 gap-2">
                          {st.whatsappUrl && (
                            <a href={st.whatsappUrl} target="_blank" rel="noopener noreferrer" className="store-btn col-span-2 bg-[#25A35F] text-white" aria-label={`Chamar a loja ${st.name} no WhatsApp (abre o WhatsApp)`}>
                              <WhatsIcon className="h-5 w-5" /> Chamar no WhatsApp
                            </a>
                          )}
                          {st.phoneUrl && (
                            <a href={st.phoneUrl} className="store-btn col-span-2 bg-rosaForte text-white" aria-label={`Ligar para a loja ${st.name}: ${st.phoneLabel}`}>
                              <PhoneIcon className="h-5 w-5" /> Ligar · {st.phoneLabel}
                            </a>
                          )}
                          {st.instagramUrl && (
                            <a href={st.instagramUrl} target="_blank" rel="noopener noreferrer" className="store-btn bg-lilas/70 text-ameixa" aria-label={`Instagram da loja ${st.name} (abre em nova aba)`}>
                              <InstagramIcon className="h-5 w-5" /> Instagram
                            </a>
                          )}
                          {st.mapsUrl && (
                            <a href={st.mapsUrl} target="_blank" rel="noopener noreferrer" className="store-btn bg-menta text-ameixa" aria-label={`Ver a loja ${st.name} no mapa (abre em nova aba)`}>
                              <PinIcon className="h-5 w-5" /> Mapa
                            </a>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                  <p className="mt-3 font-sans text-xs text-ameixaSoft">O WhatsApp já abre com os tamanhos e os gostos da {EVENT.childFirstName} 💌</p>
                </>
              )}
            </div>
          </Reveal>
        )}
      </div>
    </section>
  )
}
