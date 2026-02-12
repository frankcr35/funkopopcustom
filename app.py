import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from flask import Flask, render_template, request, url_for, redirect, session, flash

try:
    import stripe
except ImportError:
    stripe = None

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambiar-en-produccion-clave-secreta")


@app.route("/health")
def health():
    """Ruta para comprobar que la app está viva (Render, etc.)."""
    return "ok", 200


EMAIL_TO = "frankcr35@gmail.com"

LOGO_IMAGE = "imagen principal.jpeg"
HERO_IMAGE = "imagen principal.jpeg"
HERO_VIDEO = "WhatsApp Video 2026-01-21 at 15.54.33.mp4"

# Precios: bodas 160€, cantantes 80€, otras individuales 80€, figura con mascota 100€
GRUPOS = [
    {
        "id": "bodas",
        "nombre": "Bodas",
        "precio": 160,
        "descripcion": "Figuras de novios para el día de tu boda. Detalles únicos y vestuario a medida.",
        "imagen_principal": {"archivo": "boda.jpeg", "titulo": "Bodas"},
        "resto": [
            {"archivo": "boda 2.jpeg", "titulo": "Pareja de novios"},
            {"archivo": "boda 3.jpeg", "titulo": "Detalle boda"},
            {"archivo": "boda 4.jpeg", "titulo": "Funko boda"},
        ],
    },
    {
        "id": "cantantes",
        "nombre": "Cantantes",
        "precio": 80,
        "descripcion": "Tu artista favorito o tú como estrella del escenario. Poses y estilos de música.",
        "imagen_principal": {"archivo": "cantante 2.jpeg", "titulo": "Cantantes"},
        "resto": [
            {"archivo": "cantante 4.jpeg", "titulo": "Edición música"},
            {"archivo": "cantante 7.jpeg", "titulo": "Personalizado"},
            {"archivo": "cantante 8 .jpeg", "titulo": "Cantante exclusivo"},
            {"archivo": "cantante 9.jpeg", "titulo": "Figura escenario"},
            {"archivo": "cantante 12.jpeg", "titulo": "Colección música"},
        ],
    },
    {
        "id": "cantantes-red",
        "nombre": "Cantantes alfombra roja",
        "precio": 80,
        "descripcion": "Edición gala y premios. Looks de alfombra roja y eventos especiales.",
        "imagen_principal": {"archivo": "cantante red.jpeg", "titulo": "Alfombra roja"},
        "resto": [
            {"archivo": "cantante red 2.jpeg", "titulo": "Estrella"},
            {"archivo": "cantante red 3.jpeg", "titulo": "Gala"},
            {"archivo": "cantante red 5.jpeg", "titulo": "Premios"},
            {"archivo": "cantante red 6.jpeg", "titulo": "Exclusivo"},
            {"archivo": "cantante red 7.jpeg", "titulo": "Edición limitada"},
        ],
    },
    {
        "id": "custom",
        "nombre": "Custom a tu medida",
        "precio": 80,
        "descripcion": "Diseños únicos a tu medida: temática personal o lo que imagines.",
        "imagen_principal": {"archivo": "custom.jpeg", "titulo": "Custom único"},
        "resto": [
            {"archivo": "custom 2.jpeg", "titulo": "A tu medida"},
            {"archivo": "custom 3.jpeg", "titulo": "Personalizado"},
            {"archivo": "custom 10 .jpeg", "titulo": "Artesanal"},
        ],
    },
    {
        "id": "custom-mascota",
        "nombre": "Custom con mascota",
        "precio": 100,
        "descripcion": "Figura personalizada que incluye tu mascota. Incluye persona + mascota.",
        "imagen_principal": {"archivo": "custom con mascota.jpeg", "titulo": "Con mascota"},
        "resto": [],
    },
    {
        "id": "custom-cine",
        "nombre": "Custom cine",
        "precio": 80,
        "descripcion": "Inspirados en películas y personajes. Tu escena favorita en figura.",
        "imagen_principal": {"archivo": "custom movie.jpeg", "titulo": "Inspiración cine"},
        "resto": [{"archivo": "custom movie 2.jpeg", "titulo": "Película"}],
    },
    {
        "id": "películas",
        "nombre": "Películas",
        "precio": 80,
        "descripcion": "Edición cine. Personajes y momentos icónicos hechos a mano.",
        "imagen_principal": {"archivo": "movie 8.jpeg", "titulo": "Edición cine"},
        "resto": [],
    },
]


def url_imagen(archivo):
    return url_for("static", filename="images/" + archivo)


def preparar_grupo(g):
    principal = g["imagen_principal"]
    return {
        "id": g["id"],
        "nombre": g["nombre"],
        "precio": g["precio"],
        "descripcion": g["descripcion"],
        "imagen_principal": {
            "titulo": principal["titulo"],
            "url": url_imagen(principal["archivo"]),
        },
        "resto": [
            {"titulo": it["titulo"], "url": url_imagen(it["archivo"])}
            for it in g["resto"]
        ],
    }


@app.route("/")
def home():
    if "carrito" not in session:
        session["carrito"] = []
    hero_img_url = url_imagen(HERO_IMAGE)
    hero_video_url = url_imagen(HERO_VIDEO)
    logo_url = url_imagen(LOGO_IMAGE)
    grupos = [preparar_grupo(g) for g in GRUPOS]
    todas_imagenes = []
    for g in grupos:
        todas_imagenes.append({"titulo": g["imagen_principal"]["titulo"], "url": g["imagen_principal"]["url"]})
        for it in g["resto"]:
            todas_imagenes.append(it)
    return render_template(
        "index.html",
        hero_image=hero_img_url,
        hero_video=hero_video_url,
        logo_url=logo_url,
        grupos=grupos,
        todas_imagenes=todas_imagenes,
        cart_count=len(session.get("carrito", [])),
    )


@app.route("/carrito/add", methods=["POST"])
def carrito_add():
    session.permanent = True
    if "carrito" not in session:
        session["carrito"] = []
    session["carrito"].append(
        {
            "tipo": "personalizado",
            "nombre": request.form.get("name", ""),
            "diseño": request.form.get("diseño_elegido", ""),
            "descripcion": request.form.get("details", ""),
            "ref_imagenes": request.form.get("ref_imagenes", ""),
            "direccion": request.form.get("direccion", ""),
            "ciudad": request.form.get("ciudad", ""),
            "cp": request.form.get("cp", ""),
            "pais": request.form.get("pais", ""),
            "precio": 80,
        }
    )
    return redirect(url_for("carrito"))


@app.route("/carrito/add-product", methods=["POST"])
def carrito_add_product():
    session.permanent = True
    if "carrito" not in session:
        session["carrito"] = []
    grupo_id = request.form.get("grupo_id")
    for g in GRUPOS:
        if g["id"] == grupo_id:
            session["carrito"].append(
                {
                    "tipo": "producto",
                    "grupo_id": g["id"],
                    "nombre": g["nombre"],
                    "precio": g["precio"],
                }
            )
            break
    return redirect(url_for("carrito"))


def cart_total(items):
    return sum(it.get("precio", 0) for it in items)


@app.route("/carrito")
def carrito():
    items = session.get("carrito", [])
    total = cart_total(items)
    stripe_ok = stripe is not None and os.environ.get("STRIPE_SECRET_KEY")
    return render_template(
        "carrito.html",
        items=items,
        total=total,
        logo_url=url_imagen(LOGO_IMAGE),
        stripe_ok=stripe_ok,
    )


@app.route("/carrito/vaciar", methods=["POST"])
def carrito_vaciar():
    session["carrito"] = []
    return redirect(url_for("carrito"))


@app.route("/carrito/quitar/<int:index>", methods=["POST"])
def carrito_quitar(index):
    items = session.get("carrito", [])
    if 0 <= index < len(items):
        session["carrito"] = items[:index] + items[index + 1 :]
    return redirect(url_for("carrito"))


def enviar_ficha_por_email(nombre, descripcion, direccion, ciudad, cp, pais, archivos=None):
    """Envía los datos de la ficha al correo configurado. Requiere MAIL_USERNAME y MAIL_PASSWORD en el entorno."""
    mail_user = os.environ.get("MAIL_USERNAME")
    mail_pass = os.environ.get("MAIL_PASSWORD")
    if not mail_user or not mail_pass:
        return False, "Correo no configurado (MAIL_USERNAME/MAIL_PASSWORD)"
    msg = MIMEMultipart()
    msg["Subject"] = "Nuevo encargo Funko Pops - {}".format(nombre or "Sin nombre")
    msg["From"] = mail_user
    msg["To"] = EMAIL_TO
    cuerpo = (
        "Datos del encargo:\n\n"
        "Nombre: {}\n"
        "Descripción / referencia:\n{}\n\n"
        "Dirección: {}, {} {}, {}\n"
    ).format(
        nombre or "-",
        descripcion or "-",
        direccion or "-",
        cp or "-",
        ciudad or "-",
        pais or "-",
    )
    msg.attach(MIMEText(cuerpo, "plain", "utf-8"))
    if archivos:
        for f in archivos:
            if f and getattr(f, "filename", None):
                try:
                    data = f.read()
                    if not data:
                        continue
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(data)
                    encoders.encode_base64(part)
                    safe_name = (f.filename or "adjunto").encode("ascii", "ignore").decode("ascii") or "adjunto"
                    part.add_header("Content-Disposition", "attachment", filename=safe_name)
                    msg.attach(part)
                except Exception:
                    pass
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(mail_user, mail_pass)
            s.sendmail(mail_user, EMAIL_TO, msg.as_string())
        return True, None
    except Exception as e:
        return False, str(e)


@app.route("/carrito/enviar-datos", methods=["POST"])
def carrito_enviar_datos():
    try:
        nombre = request.form.get("name", "") or ""
        descripcion = request.form.get("details", "") or ""
        direccion = request.form.get("direccion", "") or ""
        ciudad = request.form.get("ciudad", "") or ""
        cp = request.form.get("cp", "") or ""
        pais = request.form.get("pais", "") or ""
        archivos = request.files.getlist("imagenes") or []
        ok, err = enviar_ficha_por_email(
            nombre, descripcion, direccion, ciudad, cp, pais, archivos
        )
        if ok:
            flash("Datos enviados correctamente. Redirigiendo al pago.")
        else:
            flash("No se pudo enviar el correo: {}.".format(err), "error")
    except Exception as e:
        flash("Error al enviar los datos: {}.".format(str(e)), "error")
    return redirect(url_for("checkout"))


@app.route("/checkout")
def checkout():
    items = session.get("carrito", [])
    if not items:
        return redirect(url_for("home"))
    total = cart_total(items)
    stripe_ok = stripe is not None and os.environ.get("STRIPE_SECRET_KEY")
    return render_template(
        "checkout.html",
        items=items,
        total=total,
        logo_url=url_imagen(LOGO_IMAGE),
        stripe_ok=stripe_ok,
    )


@app.route("/crear-pago", methods=["POST"])
def crear_pago():
    """Crea una sesión de Stripe Checkout y redirige a la pasarela de pago."""
    if not stripe:
        flash("Pasarela de pago no disponible. Instala: pip install stripe", "error")
        return redirect(url_for("checkout"))
    key = os.environ.get("STRIPE_SECRET_KEY")
    if not key:
        flash("Configura STRIPE_SECRET_KEY en el entorno para activar los pagos.", "error")
        return redirect(url_for("checkout"))
    items = session.get("carrito", [])
    if not items:
        return redirect(url_for("home"))
    total = cart_total(items)
    total_centimos = int(round(total * 100))
    if total_centimos < 50:
        total_centimos = 50
    stripe.api_key = key
    try:
        checkout_session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "quantity": 1,
                    "price_data": {
                        "currency": "eur",
                        "unit_amount": total_centimos,
                        "product_data": {
                            "name": "Funko Pops personalizados",
                            "description": "{} artículo(s) – Total {} €".format(len(items), total),
                        },
                    },
                }
            ],
            success_url=url_for("gracias", _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=url_for("carrito", _external=True),
        )
        return redirect(checkout_session.url)
    except Exception as e:
        flash("Error al crear el pago: {}.".format(str(e)), "error")
        return redirect(url_for("checkout"))


@app.route("/gracias")
def gracias():
    session_id = request.args.get("session_id")
    if session_id:
        session["carrito"] = []
    return render_template(
        "gracias.html",
        logo_url=url_imagen(LOGO_IMAGE),
        session_id=session_id,
    )


if __name__ == "__main__":
    app.run(debug=True)
