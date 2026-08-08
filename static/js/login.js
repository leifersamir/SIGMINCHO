document.addEventListener("DOMContentLoaded", function () {

    const usuario = document.getElementById("usuario");
    const password = document.getElementById("password");
    const boton = document.getElementById("btnIngresar");

    function validarCampos() {

        if (usuario.value.trim() !== "" && password.value.trim() !== "") {
            boton.disabled = false;
        } else {
            boton.disabled = true;
        }

    }

    usuario.addEventListener("input", validarCampos);
    password.addEventListener("input", validarCampos);

});