# 🚀 Guía de Despliegue para Skimlinks

## ✅ **Checklist Skimlinks (LISTO)**

- [x] **Aviso de afiliados visible** (footer + páginas legales)
- [x] **Políticas de privacidad** (/politicas)
- [x] **Términos y condiciones** (/terminos)
- [x] **Página de contacto** (/contacto)
- [x] **Contenido real** (productos de ejemplo funcionando)
- [x] **Navegación clara** (header + footer con enlaces)

## 🌐 **Opciones de Despliegue GRATIS**

### **Opción 1: Vercel (Recomendado)**
```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Desde apps/web/
cd apps/web
vercel

# 3. Seguir pasos:
# - Link to existing project? No
# - Project name: la-ventanita-593
# - Directory: ./
# - Override settings? No

# Resultado: https://la-ventanita-593.vercel.app
```

### **Opción 2: Netlify**
```bash
# 1. Build del proyecto
cd apps/web
npm run build

# 2. Subir carpeta 'out' a netlify.com
# Resultado: https://la-ventanita-593.netlify.app
```

### **Opción 3: GitHub Pages**
```bash
# 1. Subir código a GitHub
# 2. Settings > Pages > Deploy from branch
# 3. Configurar Next.js para static export
```

## 📋 **Aplicar a Skimlinks**

1. **Ir a:** https://skimlinks.com/publishers
2. **Completar formulario:**
   - Website URL: `https://tu-dominio.vercel.app`
   - Category: Price Comparison
   - Traffic: 1000+ monthly visitors (estimado)
   - Content: Product comparison and affiliate links

3. **Información adicional:**
   - "Somos un comparador de precios que redirige a tiendas como Best Buy, Target, Walmart"
   - "Tenemos políticas de privacidad y avisos de afiliados visibles"

## ⚡ **Despliegue EXPRESS (15 minutos)**

```bash
# 1. Preparar build
cd apps/web
npm install
npm run build

# 2. Desplegar
vercel --prod

# 3. Aplicar a Skimlinks con la URL generada
```

## 🔧 **Configuración Next.js para Producción**

Agregar a `next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
```

## 📞 **Después de la Aprobación**

1. **Instalar script Skimlinks** en `_app.tsx`
2. **Actualizar connector** con credenciales reales
3. **Configurar dominio personalizado** (opcional)

**Tiempo estimado de aprobación:** 24-48 horas

Tu sitio ya cumple TODOS los requisitos de Skimlinks. Solo necesitas desplegarlo y aplicar.