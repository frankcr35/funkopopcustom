#!/bin/bash
# Script para subir la tienda a GitHub (luego conectar el repo en Render)
# Sustituye TU_USUARIO y TU_REPO antes de ejecutar

cd "$(dirname "$0")"

# Si ya tienes git init y remote, solo haz commit y push:
# git add .
# git commit -m "Mejoras móvil: secciones horizontales y header"
# git push

# Primera vez (repo nuevo):
git init
git add .
git status
echo "---"
echo "Revisa los archivos arriba. Luego ejecuta:"
echo "  git commit -m \"Tienda Funko Pops lista para Render\""
echo "  git branch -M main"
echo "  git remote add origin https://github.com/TU_USUARIO/TU_REPO.git"
echo "  git push -u origin main"
echo "(Sustituye TU_USUARIO y TU_REPO por tu usuario y nombre del repo.)"
