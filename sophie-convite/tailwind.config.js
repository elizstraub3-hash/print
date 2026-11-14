/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        rosa: '#F8CDE3',
        lilas: '#DCCCF7',
        azul: '#CDECF7',
        amarelo: '#FFF0B9',
        menta: '#D6EEDC',
        dourado: '#EBCB85',
        // tons de apoio (texto com contraste AA sobre fundos pastel)
        ameixa: '#472A52',
        ameixaSoft: '#5E4468',
        douradoEscuro: '#A67C2E',
        rosaForte: '#CF4A92',
      },
      fontFamily: {
        script: ['"Dancing Script"', 'cursive'],
        sans: ['Fredoka', 'ui-rounded', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 10px 30px -12px rgba(150, 100, 160, 0.35)',
        glow: '0 0 0 6px rgba(255,255,255,.55), 0 14px 30px -10px rgba(229,141,184,.65)',
      },
    },
  },
  plugins: [],
}
