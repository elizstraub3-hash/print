import Unicorn from '../components/Unicorn.jsx'
import { Rainbow, Cloud } from '../components/Decor.jsx'
import { PATTERN_URL } from '../components/Pattern.jsx'
import { EVENT } from '../config/event.js'
import { DAY_MONTH, TIME_LABEL, WEEKDAY } from '../lib/event-utils.js'

/** Capa 1200×630 para WhatsApp/Open Graph (gerada por `npm run og`) */
export default function OgCard() {
  return (
    <div style={{ width: 1200, height: 630, position: 'relative', overflow: 'hidden', background: 'linear-gradient(160deg,#CDECF7 0%,#E6E0FA 45%,#F8CDE3 100%)', fontFamily: 'Fredoka' }}>
      <div style={{ position: 'absolute', inset: 0, backgroundImage: PATTERN_URL, backgroundSize: '240px', opacity: 0.25 }} />
      <div style={{ position: 'absolute', left: 40, top: 60, width: 520 }}>
        <Rainbow className="og-w" />
      </div>
      <div style={{ position: 'absolute', left: 110, top: 110, width: 380 }}>
        <Unicorn idPrefix="og" className="og-w" />
      </div>
      <div style={{ position: 'absolute', left: 30, top: 440, width: 540 }}>
        <Cloud className="og-w" />
      </div>
      <div style={{ position: 'absolute', right: -60, bottom: -40, width: 340 }}>
        <Cloud className="og-w" />
      </div>
      <div style={{ position: 'absolute', left: 600, top: 0, bottom: 0, right: 40, display: 'flex', flexDirection: 'column', justifyContent: 'center', textAlign: 'center', color: '#5E4466' }}>
        <div style={{ fontSize: 22, letterSpacing: '0.3em', textTransform: 'uppercase', color: '#7D6585', fontWeight: 500 }}>Você foi convidado para</div>
        <div style={{ fontSize: 40, fontWeight: 500, marginTop: 14 }}>O Mundo Encantado da</div>
        <div className="sophie-og" style={{ fontFamily: '"Dancing Script"', fontWeight: 700, fontSize: 150, lineHeight: 1.05 }}>{EVENT.childFirstName}</div>
        <div style={{ margin: '10px auto 0', background: 'rgba(255,255,255,.85)', borderRadius: 999, padding: '10px 30px', fontSize: 32, fontWeight: 600 }}>
          <span style={{ color: '#A67C2E' }}>{EVENT.age}</span> aninhos · {WEEKDAY}, {DAY_MONTH} · {TIME_LABEL}
        </div>
      </div>
    </div>
  )
}
