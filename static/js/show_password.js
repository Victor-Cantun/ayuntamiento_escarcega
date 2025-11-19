document.addEventListener("DOMContentLoaded", function () {
    const passwordFields = document.querySelectorAll('input[type="password"]');

    passwordFields.forEach((input) => {
        // Crear el botón
        const toggle = document.createElement("button");
        toggle.type = "button";
        //toggle.textContent = "👁️";
        toggle.innerHTML = '<i class="fa fa-eye"></i>';
        toggle.style.position = "absolute";
        toggle.style.right = "10px";
        toggle.style.top = "50%";
        toggle.style.transform = "translateY(-50%)";
        toggle.style.background = "none";
        toggle.style.border = "none";
        toggle.style.cursor = "pointer";

        // Crear contenedor relativo si no existe
        const wrapper = document.createElement("div");
        wrapper.style.position = "relative";
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);
        wrapper.appendChild(toggle);

        toggle.addEventListener("click", () => {
        const type = input.getAttribute("type") === "password" ? "text" : "password";
        input.setAttribute("type", type);
        toggle.innerHTML= type === "password" ? '<i class="fa fa-eye"></i>' : '<i class="fa fa-eye-slash"></i>';
        });
    });
});
