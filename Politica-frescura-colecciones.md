# Política de Frescura de Datos y Colecciones Dinámicas

> **Contexto:** Metabuscador de afiliados que **solo redirige** a tiendas externas (sin pagos propios). Este documento define cómo mantener precios/listados frescos y cómo automatizar secciones de la Home con productos en tendencia, novedades y descuentos.

---
## 1) Objetivos
- Evitar mantenimiento manual de precios/listados.
- Mostrar **lo más nuevo y popular** sin intervención diaria.
- Mantener una **UI viva** (Home/Categorías) con datos actualizados y slots dinámicos.

---
## 2) Fuentes y niveles de frescura (TTL por proveedor)
Configurar **TTL (Time To Live)** específicos por fuente para balancear costo y frescura:

| Fuente | TTL listado | TTL ficha | Notas |
|---|---|---|---|
| eBay Browse API | 10–30 min | 5–15 min | Precio y stock suelen ser frecuentes; usar caché corto |
| Amazon PA-API | 30–60 min | 10–30 min | PA-API permite detalles al abrir ficha |
| Best Buy API | 10–30 min | 5–15 min | Útil para tech/outlet |
| Walmart API | 15–45 min | 10–30 min | |
| Agregadores (Skimlinks/Sovrn) | 60–180 min | 30–60 min | A veces sin precio fiable → mostrar "ver precio" |

> Regla general: **Listado** usa TTL más largo; **Ficha** refresca agresivo al abrir si está vencido.

---
## 3) Flujos de actualización
### 3.1 Búsqueda/Listado
1. Consultar caché por `q, cat, page`.
2. Si **vencido/ausente**, consultar API → **normalizar** → **guardar** (DB) → **cachear**.
3. Renderizar tarjetas con: tienda, precio (o "ver precio"), envío, rating, link a devoluciones.

### 3.2 Ficha de producto
1. Cargar de DB. Si `updated_at` > TTL_ficha → **refrescar** desde API.
2. Si API falla: mostrar datos previos **+ botón de salida activo**.
3. Mostrar "**Última actualización**: hh:mm".

### 3.3 Click de salida
1. Registrar evento `click_out` (session, ip_hash, UA, product_id, merchant_id).
2. Generar **deep link afiliado** al vuelo (conector) y redirigir.

---
## 4) Jobs programados (cron)
Se recomiendan tres tipos de jobs:
- **Hot cache** (cada 15–30 min): refrescar top por **clics/impresiones** del día.
- **Colecciones** (cada 1–12 h): recalcular tendencias, descuentos, novedades.
- **Higiene** (cada 24 h): limpiar productos obsoletos y recalcular métricas lentas.

### 4.1 Ejemplo `cron.yml` (pseudoconfiguración)
```yaml
version: '1'
schedules:
  hot-cache:
    cron: '*/20 * * * *'   # cada 20 minutos
    task: python scripts/refresh_hot_cache.py
  collections-fast:
    cron: '*/60 * * * *'   # cada 60 minutos
    task: python scripts/rebuild_collections.py --fast
  collections-daily:
    cron: '0 */6 * * *'    # cada 6 horas
    task: python scripts/rebuild_collections.py --full
  hygiene:
    cron: '15 3 * * *'     # diario 03:15
    task: python scripts/cleanup_obsolete.py
```

---
## 5) Colecciones automáticas (Home/Categorías)
### 5.1 Tipos sugeridos
- **Hot today**: más clicados en 24 h.
- **Trending week**: tendencia 7 días (crecimiento + popularidad + rating).
- **New arrivals**: `release_date` ≤ 30 días.
- **Big deals**: `discount_pct` ≥ 20%.
- **Top rated**: `rating` y `review_count` altos.
- **Por categoría**: top N por `trend_score` en cada categoría.

### 5.2 Señales y fórmula de tendencia (ejemplo)
```
trend_score =
  0.40 * zscore(clicks_24h) +
  0.25 * zscore(clicks_7d_growth) +
  0.15 * norm(discount_pct) +
  0.10 * norm(review_count) +
  0.10 * norm(rating)
```

> "Big deals" se ordena por `discount_pct`; "Top rated" por `rating` y `review_count`.

### 5.3 Publicación en frontend
- La **Home** tiene *slots* (hero + carruseles + rejillas) que leen de `collection_items`.
- **ISR/SSR** (Next.js): reconstruye bloques cada X minutos.
- Mostrar badge dinámico: "-35%", "Nuevo", "Trending" y pie: "Última actualización hh:mm".

---
## 6) Esquema de datos (extensiones)
### 6.1 Campos extra en `product`
```sql
ALTER TABLE product ADD COLUMN IF NOT EXISTS old_price NUMERIC(12,2);
ALTER TABLE product ADD COLUMN IF NOT EXISTS review_count INT;
ALTER TABLE product ADD COLUMN IF NOT EXISTS release_date DATE;
ALTER TABLE product ADD COLUMN IF NOT EXISTS discount_pct NUMERIC(5,2);
```

### 6.2 Métricas internas y colecciones
```sql
-- métricas por producto (puede ser tabla o materialized view)
CREATE TABLE IF NOT EXISTS product_metrics (
  product_id BIGINT PRIMARY KEY REFERENCES product(id),
  clicks_24h INT DEFAULT 0,
  clicks_7d INT DEFAULT 0,
  clicks_7d_growth NUMERIC(6,3) DEFAULT 0,
  trend_score NUMERIC(6,3) DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- items publicados en colecciones
CREATE TABLE IF NOT EXISTS collection_items (
  id BIGSERIAL PRIMARY KEY,
  collection TEXT NOT NULL,           -- trending_week, hot_today, etc.
  product_id BIGINT REFERENCES product(id),
  score NUMERIC(6,3) DEFAULT 0,
  generated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_collection_name ON collection_items(collection);
```

---
## 7) Configuración por JSON (pesos y límites)
```json
{
  "collections": {
    "trending_week": { "size": 12, "min_rating": 3.8, "min_reviews": 25 },
    "hot_today":     { "size": 12 },
    "new_arrivals":  { "size": 12, "max_age_days": 30 },
    "big_deals":     { "size": 12, "min_discount_pct": 20 }
  },
  "weights": {
    "trend": { "clicks_24h": 0.40, "clicks_7d_growth": 0.25, "discount_pct": 0.15, "review_count": 0.10, "rating": 0.10 }
  },
  "ttl": {
    "ebay": { "list": 1800, "detail": 900 },        
    "amazon": { "list": 3600, "detail": 1800 },
    "bestbuy": { "list": 1800, "detail": 900 },
    "walmart": { "list": 2700, "detail": 1200 },
    "aggregator": { "list": 7200, "detail": 3600 }
  }
}
```

---
## 8) Endpoints/servicios de soporte
- `GET /api/collections/:name` → devuelve items ya generados (no recalcula).
- `POST /internal/rebuild-collections?mode=fast|full` → job manual (protección por token).
- `POST /internal/refresh/product/:id` → refresco bajo demanda al abrir ficha.

---
## 9) Observabilidad y KPIs
- **CTR** por bloque/categoría.
- **EPC** (earning per click) por tienda/categoría.
- **Freshness lag**: % de vistas con datos fuera de TTL.
- **Error rate** por conector (timeout, 4xx/5xx).
- **Tiempo de reconstrucción** de colecciones.

---
## 10) UX/Copy dinámico
- Hero: 1–3 productos del **Top semanal** (imágenes grandes).
- Carruseles: **Tendencias**, **Novedades**, **Descuentos**, **Mejor valorados**.
- Badges: "-35%", "Nuevo", "Trending".
- Pie: "**Última actualización**: hh:mm" en cada bloque.

---
## 11) Fallbacks y privacidad
- Si una API falla, **no bloquees**: muestra el botón "Ver en la tienda".
- No guardes PII. Usa `session_id` y `ip_hash` para métricas.
- Aviso de afiliados visible: "Podemos ganar una comisión por compras desde nuestros enlaces (sin costo extra para ti)".

---
## 12) Checklist de implementación
- [ ] TTL por fuente configurado y testeado.
- [ ] Jobs (hot-cache, collections, hygiene) desplegados.
- [ ] Campos extra en `product` migrados.
- [ ] `product_metrics` y `collection_items` creadas.
- [ ] Home/Categorías leyendo de colecciones (ISR/SSR activado).
- [ ] Monitoreo: Sentry/logs + panel de KPIs.
