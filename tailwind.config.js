/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  safelist: [
    'w-72', 'md:ml-72', '-translate-x-full', 'md:translate-x-0',
    'z-[100]', 'z-[999]', 'z-[1000]', 'z-[9999]',
    // Badge colors for gravity / status
    'bg-red-100', 'text-red-700', 'bg-red-50', 'bg-red-500',
    'bg-green-100', 'text-green-700', 'bg-green-50', 'bg-green-500',
    'bg-yellow-100', 'text-yellow-700', 'bg-yellow-50', 'bg-yellow-500',
    'bg-blue-100', 'text-blue-700', 'bg-blue-50', 'bg-blue-500',
    'bg-orange-100', 'text-orange-700', 'bg-orange-50',
    'bg-purple-100', 'text-purple-700', 'bg-purple-50',
    'bg-gray-100', 'text-gray-700', 'bg-gray-50',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50:  '#f0f4ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
          950: '#1e1b4b',
        },
        success: { DEFAULT: '#10b981', light: '#d1fae5', dark: '#047857' },
        error:   { DEFAULT: '#ef4444', light: '#fee2e2', dark: '#b91c1c' },
        warning: { DEFAULT: '#f59e0b', light: '#fef3c7', dark: '#d97706' },
        info:    { DEFAULT: '#06b6d4', light: '#cffafe', dark: '#0891b2' },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      animation: {
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'fade-in': 'fadeIn 0.3s ease-out',
        'float': 'float 20s infinite',
        'rotate': 'rotate 30s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0) rotate(0deg)' },
          '50%':      { transform: 'translateY(-30px) rotate(180deg)' },
        },
        rotate: {
          'from': { transform: 'rotate(0deg)' },
          'to':   { transform: 'rotate(360deg)' },
        },
        slideInRight: {
          '0%':   { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)',    opacity: '1' },
        },
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'glow':  '0 0 20px rgba(99, 102, 241, 0.3)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
