/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        forest: {
          50: '#f1f8f5',
          100: '#ddece3',
          200: '#bddbc9',
          300: '#91c1a8',
          400: '#64a182',
          500: '#418563',
          600: '#316a4f',
          700: '#285541',
          800: '#224436',
          900: '#1b3a2e', // Primary Forest Green
          950: '#0f211a',
        },
        moss: '#52796F',
        gold: '#D4AF37',
        ivory: '#F8F9FA',
        amber: '#FFBF00',
        charcoal: '#2D2D2D',
      },
      fontFamily: {
        serif: ['Fraunces', 'serif'],
        sans: ['Inter', 'sans-serif'],
      },
      borderRadius: {
        'blob-1': '30% 70% 70% 30% / 30% 30% 70% 70%',
        'blob-2': '50% 50% 33% 67% / 55% 27% 73% 45%',
        'ear': '2rem 2rem 0.5rem 0.5rem',
      },
      animation: {
        'gentle-wag': 'wag 2s ease-in-out infinite',
        'soft-pounce': 'pounce 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards',
      },
      keyframes: {
        wag: {
          '0%, 100%': { transform: 'rotate(-2deg)' },
          '50%': { transform: 'rotate(2deg)' },
        },
        pounce: {
          '0%': { transform: 'translateY(0) scale(1)' },
          '100%': { transform: 'translateY(-8px) scale(1.02)' },
        },
      },
    },
  },
  plugins: [],
}
