@echo off
echo Iniciando La Ventanita en modo desarrollo...

echo.
echo 1. Levantando servicios de base de datos...
cd infra\docker
docker-compose up -d postgres redis

echo.
echo 2. Esperando que los servicios estén listos...
timeout /t 10

echo.
echo 3. Iniciando API (FastAPI)...
cd ..\..\apps\api
start "API" cmd /k "pip install -r requirements.txt && uvicorn main:app --reload --port 8090"

echo.
echo 4. Iniciando Frontend (Next.js)...
cd ..\web
start "Frontend" cmd /k "npm install && npm run dev"

echo.
echo ========================================
echo La Ventanita está iniciando...
echo.
echo Frontend: http://localhost:3100
echo API: http://localhost:8090
echo Admin Panel: http://localhost:3100/admin
echo API Docs: http://localhost:8090/docs
echo.
echo Red de Afiliados: Skimlinks Network
echo Tiendas: Best Buy, Target, Walmart, Nike...
echo Credenciales Admin: admin / admin123
echo ========================================

pause