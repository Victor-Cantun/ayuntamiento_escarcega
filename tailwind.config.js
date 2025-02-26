/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",  
    "./apps/a_chat/templates/**/*.html",
    "./apps/a_home/templates/**/*.html",
    "./apps/a_users/templates/**/*.html",
    "./apps/a_notifications/templates/**/*.html",
    "./apps/website/templates/**/*.html",
    "./apps/a_income/templates/**/*.html",
    "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {
      colors: {
        rojo: "#861F3C",
        verde: "#2A6C62",
        dorado: "#E99B2E",
        gris: "#767676",
      },
    },
  },
  plugins: [require("flowbite/plugin")],
};
