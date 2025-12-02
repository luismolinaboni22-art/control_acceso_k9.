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
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")
@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        nombre = request.form["nombre"]
        cedula = request.form["cedula"]
        empresa = request.form["empresa"]
        placa = request.form["placa"]
        persona_visita = request.form["persona_visita"]
        proposito = request.form["proposito"]

        # Aquí luego guardaremos en base de datos
        print("Visitante registrado:", nombre, cedula, empresa, placa, persona_visita, proposito)

        return render_template("registrar.html", success=True)

    return render_template("registrar.html")


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

LOGGI

<!DOCTYPE html>
<html>
<head>
    <title>Acceso – Sistema K9</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body class="login-ultra-bg">

<!-- Fondo animado -->
<canvas id="particles"></canvas>

<div class="login-ultra-wrapper">

    <div class="login-ultra-card">

        <!-- LOGO K9 -->
        <div class="logo-box">
            <img src="https://i.imgur.com/IlLxK0b.png" class="login-ultra-logo" alt="K9 Logo">
        </div>

        <h1 class="login-ultra-title">Sistema K-9</h1>
        <p class="login-ultra-subtitle">Control Corporativo de Acceso</p>

        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}

        <form method="POST" onsubmit="return startLogin()">

            <!-- Email -->
            <input 
                type="email" 
                name="email" 
                id="email"
                class="input-ultra"
                placeholder="Correo corporativo"
                required
            >

            <!-- Password con icono -->
            <div class="input-ultra-group">
                <input 
                    type="password" 
                    name="password" 
                    id="password"
                    class="input-ultra"
                    placeholder="Contraseña"
                    required
                >
                <span class="toggle-icon" onclick="togglePassword()">👁</span>
            </div>

            <!-- Recordar usuario -->
            <div class="remember-row">
                <input type="checkbox" id="remember">
                <label for="remember">Recordar usuario</label>
            </div>

            <!-- Botón premium -->
            <button type="submit" class="ultra-btn" id="loginBtn">
                <span id="btnText">Ingresar</span>
                <div class="spinner" id="spinner"></div>
            </button>

        </form>

    </div>

</div>


<!-- Scripts -->
<script>
/* RECORDAR USUARIO */
window.onload = function() {
    if (localStorage.getItem("k9_user")) {
        document.getElementById("email").value = localStorage.getItem("k9_user");
        document.getElementById("remember").checked = true;
    }
}

/* ANIMACIÓN DEL BOTÓN */
function startLogin() {
    const email = document.getElementById("email").value;
    const remember = document.getElementById("remember").checked;

    if (remember) { localStorage.setItem("k9_user", email); }
    else { localStorage.removeItem("k9_user"); }

    document.getElementById("btnText").style.display = "none";
    document.getElementById("spinner").style.display = "block";
    return true;
}

/* VER / OCULTAR CONTRASEÑA */
function togglePassword() {
    let pass = document.getElementById("password");
    pass.type = pass.type === "password" ? "text" : "password";
}

/* FONDO DE PARTÍCULAS */
const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

class Particle {
    constructor() {
        this.x = Math.random()*canvas.width;
        this.y = Math.random()*canvas.height;
        this.size = Math.random()*2 + 1;
        this.speedX = (Math.random() - 0.5) * 0.4;
        this.speedY = (Math.random() - 0.5) * 0.4;
    }
    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
        if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
    }
    draw() {
        ctx.beginPath();
        ctx.fillStyle = "rgba(255,255,255,0.45)";
        ctx.arc(this.x, this.y, this.size, 0, Math.PI*2);
        ctx.fill();
    }
}

function init() {
    particles = [];
    for (let i = 0; i < 120; i++) particles.push(new Particle());
}

function animate() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    requestAnimationFrame(animate);
}

init();
animate();
</script>

</body>
</html>


