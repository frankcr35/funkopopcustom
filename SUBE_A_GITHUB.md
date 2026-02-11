# Subir la tienda a GitHub (repositorio frankcr35/funkopopcustom)

Abre una **terminal** en la carpeta del proyecto (`/home/frankdcr/tienda`) y ejecuta estos comandos **uno por uno**:

```bash
cd /home/frankdcr/tienda

git init
git add .
git status
git commit -m "Tienda Funko Pops - primer commit"
git branch -M main
git remote add origin https://github.com/frankcr35/funkopopcustom.git
git push -u origin main
```

- Si te pide **usuario y contraseña** al hacer `git push`, en GitHub ya no se usa la contraseña normal. Debes usar un **Personal Access Token**:
  1. GitHub → Settings → Developer settings → Personal access tokens → Generate new token.
  2. Marca al menos el permiso **repo**.
  3. Usa ese token como contraseña cuando `git push` lo pida (el usuario es tu usuario de GitHub).

- Si el repo en GitHub ya tiene algo (por ejemplo un README creado al crear el repo), puede que tengas que hacer antes:
  ```bash
  git pull origin main --allow-unrelated-histories
  ```
  y luego otra vez `git push -u origin main`.

Después del `git push` correcto, en Render haz **Manual Deploy** → **Deploy latest commit**. En unos minutos la página debería desplegarse.
