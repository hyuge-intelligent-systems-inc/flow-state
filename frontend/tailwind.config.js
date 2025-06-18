/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'flow-blue': '#3B82F6',
        'flow-green': '#10B981',
        'flow-purple': '#8B5CF6',
        'flow-gray': '#6B7280',
        'flow-light': '#F9FAFB',
        'flow-dark': '#1F2937'
      },
      fontFamily: {
        'sans': ['Inter', 'ui-sans-serif', 'system-ui'],
      }
    },
  },
  plugins: [],
}