-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;

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
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
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

-- Índices para optimización
CREATE INDEX idx_product_merchant ON product(merchant_id);
CREATE INDEX idx_product_category ON product(category);
CREATE INDEX idx_product_title_trgm ON product USING GIN (title gin_trgm_ops);
CREATE INDEX idx_click_out_product ON click_out(product_id);
CREATE INDEX idx_click_out_merchant ON click_out(merchant_id);
CREATE INDEX idx_click_out_ts ON click_out(ts);
CREATE INDEX idx_search_log_q_trgm ON search_log USING GIN (q gin_trgm_ops);
CREATE INDEX idx_search_log_ts ON search_log(ts);

-- Datos iniciales
INSERT INTO merchant (name, network, commission_estimated, return_policy_url, base_url) VALUES
('eBay', 'direct', 3.00, 'https://ebay.com/help/policies/returns', 'https://ebay.com'),
('Amazon', 'direct', 4.00, 'https://amazon.com/returns', 'https://amazon.com'),
('Walmart', 'skimlinks', 2.50, 'https://walmart.com/returns', 'https://walmart.com');

INSERT INTO product (merchant_id, source_sku, title, price, currency, source_url) VALUES
(1, 'ebay-123', 'iPhone 15 Pro Max 256GB', 999.99, 'USD', 'https://ebay.com/itm/123'),
(2, 'amz-456', 'Samsung Galaxy S24 Ultra', 899.99, 'USD', 'https://amazon.com/dp/456'),
(1, 'ebay-789', 'MacBook Air M2', 1199.99, 'USD', 'https://ebay.com/itm/789');