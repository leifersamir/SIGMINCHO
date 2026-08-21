
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, flash, session, make_response
from routes.auth import auth_bp, init_app
from routes.usuario import usuario_bp, init_usuario
from routes.admin import admin_bp, init_admin
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import *

import os
import uuid

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mineria_choco_2026")
app.config["MYSQL_HOST"] = MYSQL_HOST
app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config["MYSQL_PORT"] = MYSQL_PORT

mysql = MySQL(app)

init_app(mysql)
init_usuario(mysql, app)
init_admin(mysql)
UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.register_blueprint(auth_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def login():
    return render_template("auth/login.html")

@app.route("/registro")
def registro():
    return render_template("auth/registro.html")

@app.route("/registrar", methods=["POST"])
def registrar():

    nombre = request.form["nombre"]
    usuario = request.form["usuario"]
    correo = request.form["correo"]
    password = request.form["password"]

    password_encriptada = generate_password_hash(password)

    cursor = mysql.connection.cursor()

    # Verificar si el usuario ya existe
    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=%s",
        (usuario,)
    )

    usuario_existente = cursor.fetchone()

    if usuario_existente:

        cursor.close()

        flash("El nombre de usuario ya está registrado.", "error")

        return redirect("/registro")

    # Registrar el nuevo usuario
    cursor.execute("""
        INSERT INTO usuarios(nombre, usuario, correo, contraseña)
        VALUES (%s, %s, %s, %s)
    """, (nombre, usuario, correo, password_encriptada))

    mysql.connection.commit()

    cursor.close()
    
    flash("Usuario registrado correctamente. Ya puedes iniciar sesión.", "success")
    
    return redirect("/")
@app.route("/validar_login", methods=["POST"])
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





@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/probar")
def probar():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM usuarios")

    datos = cursor.fetchall()

    cursor.close()

    return str(datos)

@app.after_request
def add_header(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

@app.route("/admin")
def admin():

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

    # Total de usuarios
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    # Total de reportes
    cursor.execute("SELECT COUNT(*) FROM reportes")
    total_reportes = cursor.fetchone()[0]

    # Municipios diferentes
    cursor.execute("SELECT COUNT(DISTINCT municipio) FROM reportes")
    total_municipios = cursor.fetchone()[0]

    # Reportes recientes
    cursor.execute("""
        SELECT id,
       municipio,
       descripcion,
       evidencia,
       fecha,
       estado
        FROM reportes
        ORDER BY fecha DESC
    """)

    reportes = cursor.fetchall()

    cursor.close()

    return render_template("admin/dashboard.html",
        total_usuarios=total_usuarios,
        total_reportes=total_reportes,
        total_municipios=total_municipios,
        total_evidencias=total_reportes,
        reportes=reportes
    )

@app.route("/usuarios")
def usuarios():

    if "usuario" not in session:
        return redirect("/")

    if session["rol"] != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT id,
               nombre,
               usuario,
               correo,
               contraseña,
               rol
        FROM usuarios
        ORDER BY nombre
    """)

    usuarios = cursor.fetchall()

    cursor.close()


    return render_template(
    "admin/usuarios.html",
    usuarios=usuarios

)








if __name__ == "__main__":
    app.run(debug=True)