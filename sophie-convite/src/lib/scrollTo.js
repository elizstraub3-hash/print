/**
 * Rola até uma seção de forma confiável (inclusive dentro de iframes/prévias):
 * 1) window.scrollTo calculado; 2) se a janela não rolar, scrollIntoView;
 * 3) por fim, âncora (#id). Também move o foco para o título da seção.
 */
export function scrollToSection(id) {
  const el = document.getElementById(id)
  if (!el) return false
  const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
  const behavior = reduce ? 'auto' : 'smooth'
  const top = el.getBoundingClientRect().top + window.scrollY - 8
  const before = window.scrollY
  window.scrollTo({ top, behavior })
  setTimeout(() => {
    const r = el.getBoundingClientRect()
    const arrived = Math.abs(r.top) < 80 || window.scrollY !== before
    if (!arrived) {
      el.scrollIntoView({ block: 'start' })
      if (Math.abs(el.getBoundingClientRect().top) > 80) {
        try {
          history.replaceState(null, '', `#${id}`)
          location.hash = id
        } catch {
          /* ok */
        }
      }
    }
  }, 350)
  const h = el.querySelector('h2, h3')
  if (h) {
    h.setAttribute('tabindex', '-1')
    h.focus({ preventScroll: true })
  }
  return true
}
