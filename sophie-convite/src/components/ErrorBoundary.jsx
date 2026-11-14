import { Component } from 'react'
import { EVENT } from '../config/event.js'
import { DATE_LONG, TIME_LABEL, SHORT_ADDRESS, MAPS_URL } from '../lib/event-utils.js'

/** Se algo inesperado falhar, o convidado ainda vê as informações essenciais */
export default class ErrorBoundary extends Component {
  state = { error: false }
  static getDerivedStateFromError() {
    return { error: true }
  }
  componentDidCatch(err) {
    if (import.meta.env.DEV) console.error(err)
  }
  render() {
    if (!this.state.error) return this.props.children
    return (
      <section className="bg-[#FFFAFC] px-6 py-16 text-center font-sans text-ameixa">
        <h2 className="font-script text-4xl font-bold text-rosaForte">{EVENT.childFirstName} · {EVENT.age} anos</h2>
        <p className="mt-4 text-lg">{DATE_LONG} · {TIME_LABEL}</p>
        <p className="mt-1">{EVENT.venueName}</p>
        <a className="btn-soft mt-6" href={MAPS_URL} target="_blank" rel="noopener noreferrer">{SHORT_ADDRESS}</a>
        <button type="button" className="btn-ghost mt-4 px-6" onClick={() => location.reload()}>Recarregar o convite</button>
      </section>
    )
  }
}
