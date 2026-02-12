# Enviar la ficha por correo en Render (Resend)

En Render el puerto SMTP (Gmail) suele estar bloqueado, por eso sale "Network is unreachable". La app usa **Resend** cuando está configurado: es una API por HTTPS que sí funciona en Render.

## Pasos

1. **Cuenta en Resend**  
   Entra en [resend.com](https://resend.com), regístrate (puedes usar tu Gmail frankcr35@gmail.com).

2. **API Key**  
   En el dashboard: **API Keys** → **Create API Key** → copia la clave (empieza por `re_`).

3. **Variable en Render**  
   En tu servicio **funkopopcustom** → **Environment** → Add:
   - **Key:** `RESEND_API_KEY`
   - **Value:** tu clave (ej. `re_xxxxxxxx`)

4. **Guardar y redesplegar**  
   Tras guardar, Render redespliega solo. Vuelve a probar "Enviar datos y continuar al pago".

Los correos llegarán a **frankcr35@gmail.com** (definido en `EMAIL_TO` en el código). En el plan gratuito de Resend solo puedes enviar al email con el que te registraste; si usas ese, no hace falta verificar dominio.
