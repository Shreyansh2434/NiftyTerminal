/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#e8edf5",
        panel: "#111822",
        edge: "#263345",
        cyan: "#45d6d2",
        amber: "#f2b84b",
      },
    },
  },
  plugins: [],
};
