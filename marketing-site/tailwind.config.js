/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        marketing: {
          bg: "#FAFAF8",
          surface: "#FFFFFF",
          text: "#1A1F36",
          muted: "#5C6370",
          accent: "#2563EB",
          gold: "#C4A962",
          border: "#E8E6E1",
          dark: "#1A1F36",
        },
      },
      fontFamily: {
        serif: ['"DM Serif Display"', "Georgia", "serif"],
        sans: ['"Plus Jakarta Sans"', "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
