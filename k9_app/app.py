from flask import Flask, render_template, redirect, url_for, request, session
import os

app = Flask(__name__)
app.secret_key = "clave_super_secreta_para_sessions"  # Necesario para manejar sesiones

# ----- CREDENCIALES DEL ADMIN -----
ADMIN_USER = "jorgemolinabonilla@gmail.com"
ADMIN_PASSWORD = "123"


# ---------- RUTA LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("email")
        password = request.form.get("password")

        if user == ADMIN_USER and password == ADMIN_PASSWORD:
            session["logged"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")


# ---------- RUTA PRINCIPAL ----------
@app.route("/")
def index():
    if not session.get("logged"):
        return redirect(url_for("login"))

    return render_template("index.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- CONFIG PARA RENDER ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
