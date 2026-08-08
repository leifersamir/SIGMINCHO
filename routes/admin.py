from flask import Blueprint, render_template, redirect, session, flash, request

admin_bp = Blueprint("admin", __name__)

mysql = None


def init_admin(mysql_instance):
    global mysql
    mysql = mysql_instance


# ==========================
# DASHBOARD
# ==========================

@admin_bp.route("/admin")
def admin():

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

    # Usuarios
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    # Reportes
    cursor.execute("SELECT COUNT(*) FROM reportes")
    total_reportes = cursor.fetchone()[0]

    # Municipios
    cursor.execute("SELECT COUNT(DISTINCT municipio) FROM reportes")
    total_municipios = cursor.fetchone()[0]

    # Evidencias
    cursor.execute("SELECT COUNT(*) FROM reportes")
    total_evidencias = cursor.fetchone()[0]

    # Últimos reportes
    cursor.execute("""
        SELECT
            id,
            municipio,
            descripcion,
            evidencia,
            fecha,
            estado
        FROM reportes
        ORDER BY fecha DESC
        LIMIT 5
    """)

    reportes = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin/dashboard.html",
        total_usuarios=total_usuarios,
        total_reportes=total_reportes,
        total_municipios=total_municipios,
        total_evidencias=total_evidencias,
        reportes=reportes
    )


# ==========================
# USUARIOS
# ==========================

@admin_bp.route("/usuarios")
def usuarios():

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            id,
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


# ==========================
# EDITAR USUARIO
# ==========================

@admin_bp.route("/editar/<int:id>")
def editar(id):

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE id=%s",
        (id,)
    )

    usuario = cursor.fetchone()

    cursor.close()

    return render_template("admin/editar.html", usuario=usuario)


# ==========================
# ACTUALIZAR
# ==========================

@admin_bp.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    nombre = request.form["nombre"]
    usuario = request.form["usuario"]
    correo = request.form["correo"]
    rol = request.form["rol"]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nombre=%s,
            usuario=%s,
            correo=%s,
            rol=%s
        WHERE id=%s
    """, (nombre, usuario, correo, rol, id))

    mysql.connection.commit()

    cursor.close()

    flash("Usuario actualizado correctamente.", "success")

    return redirect("/usuarios")

# ==========================
# ELIMINAR
# ==========================

@admin_bp.route("/eliminar/<int:id>")
def eliminar(id):

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM usuarios WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cursor.close()

    flash("Usuario eliminado.", "success")

    return redirect("/usuarios")


# ==========================
# REPORTES
# ==========================

@admin_bp.route("/reportes")
def reportes():

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            id,
            municipio,
            descripcion,
            evidencia,
            fecha,
            estado
        FROM reportes
        ORDER BY fecha DESC
    """)

    reportes = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM reportes")
    total_reportes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT municipio) FROM reportes")
    total_municipios = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    cursor.close()

    return render_template(
    "admin/reportes.html",
    reportes=reportes,
    total_reportes=total_reportes,
    total_municipios=total_municipios,
    total_usuarios=total_usuarios
)
@admin_bp.route("/evidencias")
def evidencias():

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

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

    evidencias = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM reportes")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM reportes
        WHERE estado='Pendiente'
    """)
    pendientes = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM reportes
        WHERE estado='Aprobado'
    """)
    aprobados = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM reportes
        WHERE estado='Rechazado'
    """)
    rechazados = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "admin/evidencias.html",
        evidencias=evidencias,
        total=total,
        pendientes=pendientes,
        aprobados=aprobados,
        rechazados=rechazados
    )
@admin_bp.route("/cambiar_estado/<int:id>", methods=["POST"])
def cambiar_estado(id):

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    estado = request.form.get("estado")

    estados_validos = [
        "Pendiente",
        "Aprobado",
        "Rechazado"
    ]

    if estado not in estados_validos:
        flash("Estado no válido.", "error")
        return redirect("/evidencias")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE reportes
        SET estado = %s
        WHERE id = %s
    """, (estado, id))

    mysql.connection.commit()

    cursor.close()

    flash(
        "El estado del reporte fue actualizado correctamente.",
        "success"
    )

    return redirect("/evidencias")
@admin_bp.route("/estadisticas")
def estadisticas():

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

    # Reportes por estado
    cursor.execute("""
        SELECT estado, COUNT(*)
        FROM reportes
        GROUP BY estado
    """)
    estados = cursor.fetchall()

    # Reportes por municipio
    cursor.execute("""
        SELECT municipio, COUNT(*)
        FROM reportes
        GROUP BY municipio
        ORDER BY COUNT(*) DESC
    """)
    municipios = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin/estadisticas.html",
        total_usuarios=total_usuarios,
        total_reportes=total_reportes,
        estados=estados,
        municipios=municipios
    )


# ==========================
# APROBAR
# ==========================

@admin_bp.route("/aprobar/<int:id>")
def aprobar(id):

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE reportes
        SET estado='Aprobado'
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()

    cursor.close()

    flash("Reporte aprobado.", "success")

    return redirect("/reportes")


# ==========================
# RECHAZAR
# ==========================

@admin_bp.route("/rechazar/<int:id>")
def rechazar(id):

    if "usuario" not in session:
        return redirect("/")

    if session.get("rol") != "admin":
        return redirect("/home")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE reportes
        SET estado='Rechazado'
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()

    cursor.close()

    flash("Reporte rechazado.", "success")

    return redirect("/reportes")


#