/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",  
    "./a_chat/templates/**/*.html",
    "./a_home/templates/**/*.html",
    "./a_users/templates/**/*.html",
    "./a_notifications/templates/**/*.html",
    "./website/templates/**/*.html",
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
