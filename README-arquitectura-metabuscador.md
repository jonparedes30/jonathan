# Metabuscador/Afiliados (MVP) — Arquitectura + Endpoints + Esquema SQL
> **Objetivo:** Sitio que **solo redirige** a tiendas externas con **enlaces de afiliado** (sin membresías, sin pagos propios, sin devoluciones propias). Coste mínimo; base lista para crecer.
---
## 1) Stack recomendado
- **Frontend:** Next.js (SSR/ISR) + Tailwind (o Django Templates si prefieres Python puro).
- **Backend API:** FastAPI (Python) o Django REST Framework.
- **BD:** PostgreSQL (SQLite para prototipo).
- **Caché:** Redis (resultados y throttling).
- **Jobs:** Celery/Beat o Cron (refrescos y limpieza).
- **Analítica:** Plausible/GA4 (IP anon), Sentry (errores).
- **Infra:** Docker, PaaS económico (Render/Fly/Railway) + CDN + HTTPS Let’s Encrypt.

---
## 2) Estructura de carpetas (sugerencia monorepo)
```
repo/
├─ apps/
│  ├─ web/                 # Next.js (páginas, componentes, SEO)
│  └─ api/                 # FastAPI / DRF (servicios)
├─ packages/
│  ├─ connectors/          # SDKs/fuentes (eBay, Amazon, Agregadores)
│  └─ common/              # tipos, utils, normalizadores
├─ infra/
│  ├─ docker/              # Dockerfiles y compose
│  └─ k8s/                 # (opcional) manifests
├─ scripts/                # jobs (cron), importadores
└─ docs/                   # documentación
```

---
## 3) Variables de entorno (.env ejemplo)
```
# App
APP_ENV=prod
PORT=8080
BASE_URL=https://tusitio.com

# Postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=afiliados
DB_USER=afiliados_user
DB_PASSWORD=superseguro

# Redis
REDIS_URL=redis://localhost:6379/0

# Redes / Fuentes (usa las que vayas a integrar)
AFF_NETWORK=skimlinks   # skimlinks|sovrn|direct
SKIMLINKS_SITE_ID=YOUR_SITE_ID
SOVRN_API_KEY=YOUR_SOVRN_KEY

# eBay
EBAY_APP_ID=YOUR_EBAY_APP_ID

# Amazon PA-API (si te aprueban)
AMAZON_ASSOC_TAG=tu-tag-20
AMAZON_ACCESS_KEY=AKIA...
AMAZON_SECRET_KEY=...

# Walmart / BestBuy (opcional)
WALMART_API_KEY=...
BESTBUY_API_KEY=...
```

---
## 4) Modelo de datos (SQL — PostgreSQL)
> Mínimo para MVP. Mantiene PII fuera (solo sesión/IP hasheada).
```sql
-- merchants: tiendas/fuentes afiliadas
CREATE TABLE merchant (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  network TEXT NOT NULL,              -- 'skimlinks' | 'sovrn' | 'direct'
  program_id TEXT,                    -- id de programa en agregador
  cookie_window_days INT DEFAULT 1,   -- ventana de atribución estimada
  commission_estimated NUMERIC(5,2),  -- % estimado (solo informativo)
  return_policy_url TEXT,
  base_url TEXT,
  active BOOLEAN DEFAULT TRUE
);

-- productos normalizados (snapshots ligeros)
CREATE TABLE product (
  id BIGSERIAL PRIMARY KEY,
  merchant_id INT REFERENCES merchant(id),
  source_sku TEXT,                    -- id/sku en la tienda origen
  title TEXT NOT NULL,
  image_url TEXT,
  category TEXT,
  price NUMERIC(12,2),
  currency CHAR(3),
  shipping_info TEXT,                 -- texto simple (ETA/costo estimado)
  rating NUMERIC(3,2),
  source_url TEXT NOT NULL,           -- enlace original
  affiliate_url_cached TEXT,          -- último deep link afiliado (si aplicó)
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_product_merchant ON product(merchant_id);
CREATE INDEX idx_product_category ON product(category);
CREATE INDEX idx_product_title_trgm ON product USING GIN (title gin_trgm_ops);

-- eventos de salida (clicks a tienda)
CREATE TABLE click_out (
  id BIGSERIAL PRIMARY KEY,
  product_id BIGINT REFERENCES product(id),
  merchant_id INT REFERENCES merchant(id),
  session_id TEXT NOT NULL,
  ip_hash TEXT NOT NULL,
  user_agent TEXT,
  ts TIMESTAMPTZ DEFAULT NOW()
);

-- logs de búsqueda (para ranking/SEO)
CREATE TABLE search_log (
  id BIGSERIAL PRIMARY KEY,
  q TEXT,
  category TEXT,
  results_count INT,
  session_id TEXT,
  ts TIMESTAMPTZ DEFAULT NOW()
);
```

> **Extensiones útiles:** `pg_trgm` para búsquedas por similitud del `title`.

---
## 5) Endpoints (contratos y ejemplos)
### 5.1 `GET /api/health`
**200 OK** → `{ "status": "ok", "uptime": 12345 }`

---
### 5.2 `GET /api/search`
**Query params:**  
- `q` (string, opcional) — término de búsqueda  
- `cat` (string, opcional) — categoría  
- `sort` (enum: `price_asc|price_desc|relevance`)  
- `price_min`, `price_max` (número)  
- `page` (int, default 1), `page_size` (int, default 24)

**Respuesta 200** (ejemplo):
```json
{
  "page": 1,
  "page_size": 24,
  "total": 128,
  "items": [
    {
      "id": 987654,
      "title": "Auriculares Bluetooth XYZ",
      "image": "https://cdn.../xyz.jpg",
      "merchant": { "id": 3, "name": "eBay" },
      "price": { "amount": 24.99, "currency": "USD" },
      "shipping": "Entrega estimada 7–12 días",
      "rating": 4.5,
      "return_policy_url": "https://.../returns",
      "source_url": "https://ebay.com/itm/....",
      "affiliate_preview": true
    }
  ]
}
```

> `affiliate_preview: true` indica que este ítem soporta deep link afiliado (se genera en el click).

---
### 5.3 `GET /api/product/:id`
Devuelve ficha extendida (mismos campos + alternativas y “ver también”).

**Respuesta 200** (ejemplo parcial):
```json
{
  "id": 987654,
  "title": "Auriculares Bluetooth XYZ",
  "merchant": { "id": 3, "name": "eBay" },
  "price": { "amount": 24.99, "currency": "USD" },
  "source_url": "https://ebay.com/itm/...",
  "return_policy_url": "https://.../returns",
  "also_available_at": [
    { "merchant": "Amazon", "price": 26.50, "source_url": "https://amazon.com/dp/..." }
  ]
}
```

---
### 5.4 `POST /api/click`
Registra el evento y devuelve la **URL de salida** final (afiliada).

**Body:**
```json
{ "product_id": 987654, "session_id": "abc123" }
```

**Respuesta 200:**
```json
{ "redirect_url": "https://redir.skimlinks.com/?id=...&to=https%3A%2F%2Febay.com%2Fitm%2F..." }
```

> El frontend hace `window.location = redirect_url` y listo.

**Errores comunes:**
- **404** si `product_id` no existe
- **429** si se detecta abuso/click-spam (rate limit por IP/sesión)

---
## 6) Lógica de ranking (simple)

**Score** = `w1*precio_norm` + `w2*reputacion_merchant` + `w3*velocidad_envio` + `w4*popularidad`  
- `precio_norm`: escala 0–1 dentro del conjunto (menor precio, mejor).  
- `reputacion_merchant`: valor fijo por tienda (ej.: 0.6–0.95).  
- `velocidad_envio`: mapear a 0–1 (rápido = 1).  
- `popularidad`: clics e impresiones previas (suavizado).

Empates: prioriza **política de devoluciones más favorable** y, si sigue igual, **mejor comisión esperada** (no visible al usuario).

---
## 7) Capa de conectores (patrón)

Interfaz común (`packages/connectors/base.py`):
```python
class SearchResult(NamedTuple):
    title: str
    image: str
    price_amount: float
    currency: str
    source_url: str
    shipping_text: str | None
    rating: float | None
    merchant_name: str
    return_policy_url: str | None
    source_sku: str | None

class Connector(Protocol):
    def search(self, q: str, cat: str | None, page: int, page_size: int) -> list[SearchResult]: ...
    def product(self, source_id: str) -> SearchResult: ...
    def to_affiliate(self, source_url: str) -> str: ...   # deep link afiliado
```

Ejemplo de **adapter** (eBay) *pseudo-código*:
```python
class EbayConnector(Connector):
    def __init__(self, app_id: str, affiliate_tag: str | None):
        ...

    def search(self, q, cat, page, page_size):
        # 1) llamar Browse API
        # 2) mapear campos al modelo SearchResult
        return results

    def to_affiliate(self, source_url: str) -> str:
        # si usas agregador, devolver redirección del agregador
        # si es directo, firmar el deep link con tu tag
        return build_affiliate_url(source_url)
```

Agregador (Skimlinks/Sovrn): `to_affiliate()` envuelve la URL original con el **wrapper** del agregador. Si una tienda no soporta afiliado, devuelves la `source_url` directa (pero marcas `affiliate_preview = false`).

---
## 8) Flujo de redirección (pasos)

1) El usuario hace clic → **POST /api/click** con `product_id` y `session_id`.
2) API registra `click_out` (hash IP, UA).
3) API genera `redirect_url` (afiliada) usando el **conector** adecuado.
4) API responde; el frontend redirige con `window.location`.
5) El evento queda trazado (para EPC y CTR).

---
## 9) SEO y contenido

- **Páginas SSG/ISR** para categorías/colecciones: títulos, descripciones y `schema.org/Product` + `AggregateOffer`.
- Sitemap dinámico, canonical, OpenGraph.
- Rutas legibles: `/categoria/tecnologia/auriculares-inalambricos`.
- Snippets de “Política de Devoluciones” por tienda (links oficiales).

---
## 10) Analítica mínima (eventos)

- `search_performed` (q, cat, results_count)
- `product_viewed` (product_id, merchant_id)
- `click_out` (product_id, merchant_id)
- KPI: **CTR**, **EPC (earning per click)** por tienda/categoría, tasa de “0 resultados”.

---
## 11) Seguridad y cumplimiento (light)

- Sin pagos propios → sin PCI.
- **Aviso de afiliados** visible (“podemos ganar comisión por estos enlaces”). 
- **Términos**: aclarar que no vendes ni gestionas devoluciones.
- **Privacidad (LOPDP):** cookies mínimas; si registras cuentas, incluye mecanismos de derechos (acceso/borrado).

---
## 12) Roadmap de 4 semanas (costo bajo)

- **S1:** Home + búsqueda + conector agregador (Skimlinks/Sovrn) + políticas.
- **S2:** Conector eBay Browse API + caché Redis + ranking básico.
- **S3:** Dedupe/“ver también”, métricas de clics/impresiones, SEO (schema/sitemap).
- **S4:** Conector Amazon PA-API (si aprobado), optimización performance, despliegue productivo.

---
## 13) Esqueleto API (FastAPI — ejemplo mínimo)

```python
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import hashlib, time

app = FastAPI()

class ClickIn(BaseModel):
    product_id: int
    session_id: str

@app.get("/api/health")
def health():
    return {"status": "ok", "uptime": int(time.time())}

@app.get("/api/search")
def search(q: str = "", cat: str | None = None, page: int = 1, page_size: int = 24):
    # 1) caché -> 2) conectores -> 3) normalizar -> 4) rankear
    return {"page": page, "page_size": page_size, "total": 0, "items": []}

@app.get("/api/product/{pid}")
def product(pid: int):
    # recuperar de BD y/o fuente
    return {"id": pid}

@app.post("/api/click")
def click(c: ClickIn, request: Request):
    ip = request.client.host or "0.0.0.0"
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()
    # 1) guardar click_out
    # 2) construir redirect_url afiliada
    redirect_url = "https://redir.example.com/?to=..."  # stub
    return {"redirect_url": redirect_url}
```

---
## 14) SQL de índices recomendados

```sql
CREATE INDEX idx_click_out_product ON click_out(product_id);
CREATE INDEX idx_click_out_merchant ON click_out(merchant_id);
CREATE INDEX idx_search_log_q_trgm ON search_log USING GIN (q gin_trgm_ops);
```

---
## 15) Mensajes/UX claves (copy)

- “**Comparamos ofertas** de múltiples tiendas.”
- “**Compras en la tienda original**; aplican sus **tiempos y devoluciones**.”
- “**Podemos ganar una comisión** si compras desde nuestros enlaces (sin costo extra para ti).”

---
## 16) Checklist para release

- [ ] Aviso de afiliados visible.
- [ ] Términos y Privacidad publicados.
- [ ] Sitemap + schema + canonical listos.
- [ ] Logs de búsqueda y clics operativos.
- [ ] Monitoreo (Sentry) y alertas básicas.
- [ ] Políticas de robots/velocidad (respetar rate limits de APIs).
