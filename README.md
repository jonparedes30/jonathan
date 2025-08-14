# La Ventanita 593 - Metabuscador de Afiliados

Sistema de comparación de precios que redirige a tiendas externas con enlaces de afiliado.

## 🏗️ Arquitectura

```
La Ventanita 593/
├── apps/
│   ├── web/          # Frontend Next.js + Tailwind
│   └── api/          # Backend FastAPI
├── packages/
│   ├── connectors/   # Conectores de tiendas (eBay, Amazon, etc.)
│   └── common/       # Utilidades compartidas
├── infra/
│   └── docker/       # Configuración Docker
└── scripts/          # Scripts de mantenimiento
```

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker y Docker Compose
- Node.js 18+ (para desarrollo local)
- Python 3.11+ (para desarrollo local)

### Configuración

1. **Clonar y configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

2. **Levantar servicios con Docker:**
```bash
cd infra/docker
docker-compose up -d
```

3. **Acceder a las aplicaciones:**
- **Frontend:** http://localhost:3100
- **API:** http://localhost:8090
- **Panel Admin:** http://localhost:3100/admin
- **Docs API:** http://localhost:8090/docs

### Credenciales por defecto
- **Admin Panel:** admin / admin123

## 📊 Panel de Administración

El panel incluye:
- **Métricas en tiempo real:** búsquedas, clicks, CTR
- **Estimación de ganancias** basada en comisiones
- **Gráficos de tendencias** (7 días)
- **Actividad reciente**
- **Autenticación básica**

### Acceso al Panel
1. Ir a http://localhost:3100/admin
2. Usar credenciales: admin / admin123
3. Ver métricas y ganancias estimadas

## 🔧 Desarrollo Local

### Backend (FastAPI)
```bash
cd apps/api
pip install -r requirements.txt
uvicorn main:app --reload --port 8090
```

### Frontend (Next.js)
```bash
cd apps/web
npm install
npm run dev
```

## 📈 Funcionalidades

### Usuario Final
- ✅ Búsqueda unificada de productos
- ✅ Comparación de precios entre tiendas
- ✅ Redirección con enlaces de afiliado
- ✅ Información de políticas de devolución

### Panel de Administración
- ✅ Dashboard con métricas clave
- ✅ Gráficos de búsquedas y clicks
- ✅ Estimación de ganancias por comisiones
- ✅ Actividad reciente
- ✅ Autenticación segura

### Técnicas
- ✅ API REST con FastAPI
- ✅ Base de datos PostgreSQL
- ✅ Cache con Redis
- ✅ Frontend responsive con Tailwind
- ✅ Arquitectura de conectores extensible
- ✅ Docker para desarrollo y producción

## 🔌 Conectores de Tiendas

### Implementados
- **eBay:** Conector base con API mock
- **Amazon:** Preparado para PA-API
- **Agregadores:** Soporte para Skimlinks/Sovrn

### Agregar Nueva Tienda
1. Crear conector en `packages/connectors/`
2. Implementar interfaz `BaseConnector`
3. Registrar en la API principal

## 💰 Modelo de Monetización

- **Sin inventario:** Solo redirección a tiendas
- **Comisiones por afiliación:** 2-5% por venta
- **Costo operativo mínimo:** Sin pagos ni logística
- **Escalable:** Agregar más fuentes fácilmente

## 🛡️ Seguridad y Cumplimiento

- ✅ Aviso de afiliación visible
- ✅ Términos y condiciones claros
- ✅ Hash de IPs para privacidad
- ✅ Autenticación básica para admin
- ✅ Rate limiting en APIs

## 📊 Métricas Clave

- **CTR (Click-Through Rate):** % de clicks vs búsquedas
- **EPC (Earnings Per Click):** Ganancia promedio por click
- **Conversión estimada:** Basada en datos históricos
- **Fuentes más rentables:** Por tienda/categoría

## 🚀 Roadmap

### Fase 1 (Actual - MVP)
- [x] Búsqueda básica y redirección
- [x] Panel de administración
- [x] Métricas básicas

### Fase 2 (Próxima)
- [ ] Integración real con APIs de tiendas
- [ ] SEO avanzado (sitemap, schema.org)
- [ ] Cache inteligente con Redis
- [ ] Alertas y notificaciones

### Fase 3 (Futuro)
- [ ] Machine Learning para ranking
- [ ] App móvil
- [ ] Programa de afiliados propio
- [ ] Análisis predictivo

## 📝 Licencia

Proyecto privado - La Ventanita 593 - Todos los derechos reservados.