// Comportamiento general de todas las páginas.

// Pide confirmación antes de enviar formularios con el atributo data-confirmar (ej.: eliminar).
document.querySelectorAll("form[data-confirmar]").forEach(function (formulario) {
    formulario.addEventListener("submit", function (evento) {
        if (!window.confirm(formulario.dataset.confirmar)) {
            evento.preventDefault();
        }
    });
});
