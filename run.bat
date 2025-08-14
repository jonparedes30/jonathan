@echo off
echo 🚀 Iniciando La Ventanita 593...

REM Crear .env si no existe
if not exist .env (
    echo Copiando variables de entorno...
    copy .env.example .env
)

REM Levantar base de datos
echo 📊 Iniciando PostgreSQL y Redis...
cd infra\docker
docker-compose up -d postgres redis
cd ..\..

REM Esperar servicios
echo ⏳ Esperando servicios...
timeout /t 5 /nobreak >nul

REM Instalar dependencias API
echo 🐍 Instalando dependencias Python...
cd apps\api
pip install -r requirements.txt >nul 2>&1

REM Iniciar API
echo 🔧 Iniciando API en puerto 8090...
start "La Ventanita 593 API" cmd /k "uvicorn main:app --reload --port 8090"
cd ..\..

REM Instalar dependencias Frontend
echo ⚛️ Instalando dependencias Node.js...
cd apps\web
call npm install >nul 2>&1

REM Iniciar Frontend
echo 🌐 Iniciando Frontend en puerto 3100...
start "La Ventanita 593 Web" cmd /k "npm run dev -- -p 3100"
cd ..\..

echo.
echo ✅ La Ventanita 593 está iniciando...
echo.
echo 🌐 Frontend: http://localhost:3100
echo 🔧 API: http://localhost:8090
echo 👤 Admin: http://localhost:3100/admin
echo 📚 Docs: http://localhost:8090/docs
echo.
echo 🔑 Admin: admin / admin123
echo 🛍️ Red: Skimlinks Network
echo.
pause