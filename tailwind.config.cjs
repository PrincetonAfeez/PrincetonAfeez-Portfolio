/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/templates/**/*.html", "./portfolio/templates/**/*.html"],
  theme: {
    extend: {
      spacing: {
        18: "4.5rem",
      },
    },
  },
  plugins: [],
};
