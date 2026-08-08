from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="")
# Estas variables las recibiremos desde app.py
mysql = None


def init_app(mysql_instance):
    global mysql
    mysql = mysql_instance


@auth_bp.route("/")
def login():
    return render_template("auth/login.html")


@auth_bp.route("/registro")
def registro():
    return render_template("auth/registro.html")


@auth_bp.route("/registrar", methods=["POST"])
def registrar():

    nombre = request.form["nombre"]
    usuario = request.form["usuario"]
    correo = request.form["correo"]
    password = request.form["password"]

    password_encriptada = generate_password_hash(password)

    cursor = mysql.connection.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=%s",
        (usuario,)
    )

    usuario_existente = cursor.fetchone()

    if usuario_existente:

        cursor.close()

        flash("El nombre de usuario ya está registrado.", "error")

        return redirect("/registro")

    cursor.execute("""
        INSERT INTO usuarios(nombre, usuario, correo, contraseña)
        VALUES(%s,%s,%s,%s)
    """, (nombre, usuario, correo, password_encriptada))

    mysql.connection.commit()

    cursor.close()

    flash("Usuario registrado correctamente.", "success")

    return redirect("/")


@auth_bp.route("/validar_login", methods=["POST"])
def validar_login():

    usuario = request.form["usuario"]
    password = request.form["password"]

    cursor = mysql.connection.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=%s",
        (usuario,)
    )

    usuario_encontrado = cursor.fetchone()

    cursor.close()

    if usuario_encontrado and check_password_hash(usuario_encontrado[4], password):

        session["usuario"] = usuario_encontrado[2]
        session["nombre"] = usuario_encontrado[1]
        session["rol"] = usuario_encontrado[5]

        if session["rol"] == "admin":
            return redirect("/admin")

        return redirect("/home")

    flash("Usuario o contraseña incorrectos.", "error")

    return redirect("/")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")