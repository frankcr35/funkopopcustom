# Cómo activar Stripe en la tienda

La pasarela de pago **Stripe** ya está integrada en el proyecto. Solo tienes que configurar tu cuenta y la clave secreta.

---

## 1. Crear cuenta en Stripe

1. Entra en [https://stripe.com](https://stripe.com) y pulsa **Registrarse**.
2. Completa el registro (email, contraseña, datos del negocio).
3. En el **Dashboard** puedes usar primero el **modo prueba** (test) para probar sin cobrar de verdad.

---

## 2. Obtener la clave secreta

1. En Stripe: **Developers** (Desarrolladores) → **API keys**.
2. Verás:
   - **Publishable key** (pk_test_... o pk_live_...) — no la necesitas para esta integración.
   - **Secret key** (sk_test_... o sk_live_...) — **esta es la que usa la tienda**.
3. Pulsa **Reveal** en la Secret key y **cópiala**.  
   - Usa **sk_test_...** para pruebas (tarjetas de test).  
   - Usa **sk_live_...** cuando quieras cobrar de verdad.

---

## 3. Configurar la clave en tu entorno

### En tu PC (desarrollo local)

En la terminal, antes de arrancar la app:

```bash
export STRIPE_SECRET_KEY="sk_test_xxxxxxxxxxxxxxxx"
python app.py
```

O crea un archivo `.env` en la carpeta `tienda` (y no lo subas a GitHub) con:

```
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxx
```

Y en `app.py` podrías cargar `.env` con `python-dotenv` si lo instalas; si no, usa `export` como arriba.

### En Render (producción)

1. Dashboard de Render → tu servicio **funkopopcustom**.
2. **Environment** → **Add Environment Variable**.
3. **Key:** `STRIPE_SECRET_KEY`  
   **Value:** tu clave secreta (sk_test_... para pruebas o sk_live_... para producción).
4. Guarda. Render hará un redeploy y los pagos quedarán activos.

---

## 4. Cómo funciona en la tienda

1. El cliente añade productos al carrito y va a **Checkout**.
2. En la página de pago verá el botón **"Ir a pagar con tarjeta (Stripe)"** (si `STRIPE_SECRET_KEY` está configurada).
3. Al pulsar, la app crea una sesión de **Stripe Checkout** y redirige al cliente a la pasarela de Stripe.
4. El cliente paga con tarjeta en Stripe.
5. Stripe redirige a **/gracias** y se vacía el carrito.

Si no configuras `STRIPE_SECRET_KEY`, en checkout se mostrará un mensaje pidiendo que la configures y no aparecerá el botón de pago.

---

## 5. Tarjetas de prueba (modo test)

Con **sk_test_...** puedes usar estas tarjetas en [Stripe Testing](https://stripe.com/docs/testing):

| Número           | Resultado   |
|------------------|------------|
| 4242 4242 4242 4242 | Pago correcto |
| 4000 0000 0000 0002 | Tarjeta rechazada |

- Fecha: cualquier fecha futura (ej. 12/34).  
- CVC: cualquier 3 dígitos (ej. 123).  
- Correo: cualquiera.

---

## Resumen

| Dónde      | Qué hacer |
|-----------|-----------|
| Stripe.com | Crear cuenta y copiar **Secret key** (sk_test_ o sk_live_). |
| Local      | `export STRIPE_SECRET_KEY="sk_test_..."` antes de `python app.py`. |
| Render     | Environment → `STRIPE_SECRET_KEY` = tu clave. |

Con eso la pasarela Stripe queda integrada y activa en tu tienda.
