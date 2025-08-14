@echo off
echo 🚀 Desplegando La Ventanita 593 para Skimlinks...

cd apps\web

echo 📦 Instalando dependencias...
call npm install

echo 🔨 Construyendo proyecto...
call npm run build

echo 🌐 Verificando que Vercel CLI esté instalado...
where vercel >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Instalando Vercel CLI...
    call npm install -g vercel
)

echo 🚀 Desplegando a Vercel...
call vercel --prod

echo.
echo ✅ ¡Despliegue completado!
echo.
echo 📋 PRÓXIMOS PASOS:
echo 1. Copia la URL que aparece arriba
echo 2. Ve a https://skimlinks.com/publishers
echo 3. Aplica con tu URL
echo 4. Espera 24-48 horas para aprobación
echo.
echo 📊 Tu sitio cumple TODOS los requisitos de Skimlinks
echo.
pause