document.addEventListener("DOMContentLoaded", function(){

    const buscador = document.getElementById("buscarUsuario");

    if(!buscador) return;

    buscador.addEventListener("keyup", function(){

        let texto = this.value.toLowerCase();

        let filas = document.querySelectorAll("#tablaUsuarios tbody tr");

        filas.forEach(fila=>{

            let contenido = fila.textContent.toLowerCase();

            fila.style.display = contenido.includes(texto) ? "" : "none";

        });

    });

});
/*=========================================
    ELIMINAR USUARIO
=========================================*/

document.querySelectorAll(".btn-eliminar").forEach(function(boton){

    boton.addEventListener("click", function(e){

        e.preventDefault();

        const url = this.dataset.url;

        const nombre = this.dataset.nombre;

        Swal.fire({

            title: "¿Eliminar usuario?",

            html: "Se eliminará el usuario <b>" + nombre + "</b>.<br>Esta acción no podrá deshacerse.",

            icon: "warning",

            showCancelButton: true,

            confirmButtonColor: "#145A32",

            cancelButtonColor: "#d33",

            confirmButtonText: "Sí, eliminar",

            cancelButtonText: "Cancelar"

        }).then((result)=>{

            if(result.isConfirmed){

                window.location.href = url;

            }

        });

    });

});