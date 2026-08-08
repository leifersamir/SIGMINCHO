from flask import Blueprint, render_template, request, redirect, flash, session, make_response
from werkzeug.utils import secure_filename
import os
import uuid

usuario_bp = Blueprint("usuario", __name__)

mysql = None
app = None


def init_usuario(mysql_instance, flask_app):
    global mysql, app
    mysql = mysql_instance
    app = flask_app


@usuario_bp.route("/home")
def home():

    if "usuario" not in session:
        return redirect("/")

    response = make_response(

        render_template(
            "usuario/index.html",
            nombre=session["nombre"]
        )

    )

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response
@usuario_bp.route("/subir_reporte", methods=["POST"])
def subir_reporte():

    municipio = request.form["municipio"]
    descripcion = request.form["descripcion"]

    archivo = request.files["evidencia"]

    if archivo.filename != "":

        nombre_archivo = str(uuid.uuid4()) + "_" + secure_filename(archivo.filename)

        ruta = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)

        archivo.save(ruta)

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO reportes(municipio, descripcion, evidencia)
            VALUES (%s,%s,%s)
        """, (municipio, descripcion, nombre_archivo))

        mysql.connection.commit()

        cursor.close()

        flash("Reporte enviado correctamente.", "success")

    return redirect("/home")

@usuario_bp.route("/mis_reportes")
def mis_reportes():

    if "usuario" not in session:
        return redirect("/")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.municipio,
            r.descripcion,
            r.evidencia,
            r.fecha,
            r.estado
        FROM reportes r
        ORDER BY r.fecha DESC
    """)

    reportes = cursor.fetchall()

    cursor.close()

    return render_template(
        "usuario/mis_reportes.html",
        reportes=reportes,
        nombre=session["nombre"]
    )