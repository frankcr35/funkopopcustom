# Desplegar la tienda en Render y conectar funkopopcustom.com

## 1. Subir el proyecto a GitHub

1. Crea una cuenta en [GitHub](https://github.com) si no tienes.
2. Crea un **nuevo repositorio** (por ejemplo `funkopopcustom`). No inicialices con README si ya tienes archivos.
3. En la carpeta del proyecto (`tienda`), abre una terminal y ejecuta:

```bash
cd /home/frankdcr/tienda
git init
git add .
git commit -m "Tienda Funko Pops lista para Render"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

(Sustituye `TU_USUARIO` y `TU_REPO` por tu usuario de GitHub y el nombre del repositorio.)

---

## 2. Crear el Web Service en Render

1. Entra en [Render](https://render.com) y regístrate o inicia sesión (puedes usar “Sign in with GitHub”).
2. En el **Dashboard**, pulsa **New** → **Web Service**.
3. Conecta tu cuenta de GitHub si aún no está conectada y **selecciona el repositorio** de la tienda.
4. Configura el servicio:
   - **Name:** `funkopopcustom` (o el que quieras).
   - **Region:** el más cercano a tu público (por ejemplo Frankfurt).
   - **Branch:** `main`.
   - **Runtime:** `Python 3`.
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. En **Advanced** (opcional) puedes fijar **Python Version** a `3.12.0`.
6. Pulsa **Create Web Service**. Render construirá y desplegará la app. Al terminar tendrás una URL tipo:  
   `https://funkopopcustom-xxxx.onrender.com`

---

## 3. Variables de entorno en Render

En el servicio que acabas de crear, ve a **Environment** y añade:

| Key | Value |
|-----|--------|
| `SECRET_KEY` | Una cadena aleatoria larga (para la sesión de Flask). Puedes generar una con: `"` |
| `STRIPE_SECRET_KEY` |python3 -c "import secrets; print(secrets.token_hex(32)) Tu clave secreta de Stripe (`sk_test_...` o `sk_live_...`) para que funcione el pago. |
| `MAIL_USERNAME` | El email desde el que se envían las fichas (ej. Gmail). |
| `MAIL_PASSWORD` | Contraseña de aplicación del email (en Gmail: Cuenta → Seguridad → Contraseñas de aplicación). |

Después de guardar, Render hará un **redeploy** automático.

---

## 4. Conectar el dominio funkopopcustom.com

1. En el **Dashboard de Render**, abre tu **Web Service** (funkopopcustom).
2. Ve a **Settings** y baja hasta **Custom Domains**.
3. Pulsa **Add Custom Domain**.
4. Añade:
   - `funkopopcustom.com`
   - `www.funkopopcustom.com`
5. Render te mostrará qué registros DNS usar. Normalmente será algo así:
   - Para **funkopopcustom.com** (raíz): un **CNAME** que apunte a `funkopopcustom-xxxx.onrender.com`, o las **A records** que indique Render.
   - Para **www**: un **CNAME** con valor `funkopopcustom-xxxx.onrender.com`.

---

## 5. Configurar DNS en Namecheap

1. Entra en [Namecheap](https://www.namecheap.com) → **Domain List** → **Manage** en **funkopopcustom.com**.
2. Abre la pestaña **Advanced DNS**.
3. **Elimina** los registros que ya no quieras:
   - El **URL Redirect** de `@`.
   - El **CNAME** de `www` que apunta a `parkingpage.namecheap.com`.
4. **Añade** los registros que Render te haya indicado. Ejemplo típico:

   | Type | Host | Value | TTL |
   |------|------|--------|-----|
   | **CNAME** | `www` | `funkopopcustom-xxxx.onrender.com` | Automatic |
   | **CNAME** | `@`  | `funkopopcustom-xxxx.onrender.com` | Automatic |

   En Namecheap, a veces la raíz `@` no admite CNAME y piden usar **URL Redirect** o **A record**. Si Render te da **A records** (IPs), úsalos para `@` y deja **CNAME** solo para `www`. **Sigue siempre lo que diga la pantalla de Custom Domains de Render.**

5. Guarda los cambios. La propagación puede tardar unos minutos u horas.

---

## 6. HTTPS en Render

Render asigna un **certificado SSL** a tu dominio personalizado cuando está bien configurado. No hace falta que hagas nada más; en unos minutos `https://funkopopcustom.com` debería estar activo.

---

## Resumen

- **Código:** en GitHub (repositorio de la tienda).
- **Hosting:** Render (Web Service con `gunicorn app:app`).
- **Dominio:** funkopopcustom.com y www → apuntando en Namecheap a lo que indique Render en Custom Domains.
- **Variables:** `SECRET_KEY`, `STRIPE_SECRET_KEY`, `MAIL_USERNAME`, `MAIL_PASSWORD` en Environment del servicio en Render.

Si algo falla, revisa los **Logs** del servicio en Render y que los registros DNS en Namecheap coincidan exactamente con lo que muestra Render en **Custom Domains**.

---

## Si la página no carga y no salen logs

1. **Estado del despliegue**
   - En Render, entra a tu servicio **funkopopcustom**.
   - Arriba verás pestañas: **Logs**, **Events**, **Settings**, etc.
   - Abre **Events** (o la lista de **Deploys**). Mira el **último despliegue**: ¿pone **"Live"** (verde) o **"Failed"** (rojo)?
   - Si pone **Failed**, haz clic en ese despliegue y abre **Build Logs**. Ahí sale el error (por ejemplo fallo al instalar paquetes o al arrancar).

2. **Directorio raíz (Root Directory)**
   - Si en GitHub tu `app.py` está **dentro de una carpeta** (por ejemplo `tienda/app.py`), Render ejecuta desde la raíz del repo y no encuentra `app`.
   - En **Settings** del servicio, busca **Root Directory**. Si tu app está en la carpeta `tienda`, escribe: `tienda` y guarda. Luego haz **Manual Deploy** → **Deploy latest commit**.

3. **Comando de arranque**
   - En **Settings** → **Build & Deploy** → **Start Command** debe ser exactamente:
     ```bash
     gunicorn app:app --bind 0.0.0.0:$PORT
     ```
   - Si está vacío, Render puede usar el **Procfile** del repo (ya incluye ese comando). Si lo cambiaste, vuelve a poner el de arriba y guarda.

4. **Probar que la app responde**
   - Después de un despliegue correcto, abre:  
     `https://funkopopcustom.onrender.com/health`  
   - Si responde con `ok`, la app está viva. Si no carga, el servicio no está arrancando (revisa Build Logs del último deploy).
