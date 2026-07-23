import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#172033",
        moss: "#45644c",
        coral: "#d8694f",
        skyglass: "#d7edf2"
      },
      boxShadow: {
        soft: "0 20px 60px rgba(23, 32, 51, 0.12)"
      }
    }
  },
  plugins: [require("@tailwindcss/typography")]
} satisfies Config;
