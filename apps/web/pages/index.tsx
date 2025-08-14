import { useState } from 'react'
import Head from 'next/head'

interface Product {
  id: number
  title: string
  image: string
  price: { amount: number; currency: string }
  merchant: { name: string }
  rating: number
  shipping: string
  affiliate_preview: boolean
}

export default function Home() {
  const [query, setQuery] = useState('')
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    try {
      const response = await fetch(`http://localhost:8090/api/search?q=${encodeURIComponent(query)}`)
      const data = await response.json()
      setProducts(data.items)
    } catch (error) {
      console.error('Error searching:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleProductClick = async (productId: number) => {
    try {
      const response = await fetch('http://localhost:8090/api/click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: productId,
          session_id: 'session_' + Date.now()
        })
      })
      const data = await response.json()
      window.open(data.redirect_url, '_blank')
    } catch (error) {
      console.error('Error clicking product:', error)
    }
  }

  return (
    <>
      <Head>
        <title>La Ventanita 593 - Comparador de Precios</title>
        <meta name="description" content="Encuentra los mejores precios en múltiples tiendas" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">LV</span>
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">La Ventanita 593</h1>
                  <p className="text-sm text-gray-600">Tu comparador de confianza</p>
                </div>
              </div>
              <div className="hidden md:flex items-center space-x-6 text-sm">
                <a href="/como-funciona" className="text-gray-600 hover:text-gray-900 font-medium">Cómo Funciona</a>
                <span className="flex items-center text-gray-600"><span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>8+ Tiendas</span>
                <span className="flex items-center text-gray-600"><span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>Mejores Precios</span>
              </div>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 text-white py-16">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <h2 className="text-4xl md:text-6xl font-bold mb-6">
              Encuentra los <span className="text-yellow-300">Mejores Precios</span>
            </h2>
            <p className="text-xl md:text-2xl mb-8 text-blue-100">
              Comparamos precios en tiempo real de las tiendas más populares
            </p>
            <div className="flex flex-wrap justify-center gap-4 mb-8">
              {['Best Buy', 'Target', 'Walmart', 'Nike', 'Samsung', 'Adidas'].map((store) => (
                <span key={store} className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-medium">
                  {store}
                </span>
              ))}
            </div>
          </div>
        </section>

        <div className="max-w-7xl mx-auto px-4 py-12">
          {/* Search Section */}
          <div className="-mt-8 relative z-10 mb-16">
            <div className="bg-white rounded-2xl shadow-xl p-8 max-w-4xl mx-auto">
              <form onSubmit={handleSearch}>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                  <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Busca iPhone, laptop, zapatos deportivos..."
                    className="w-full pl-12 pr-32 py-4 text-lg border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="absolute right-2 top-2 px-8 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 font-medium disabled:opacity-50 transition-all"
                  >
                    {loading ? '🔍 Buscando...' : '🔍 Buscar'}
                  </button>
                </div>
              </form>
              
              {/* Popular Searches */}
              <div className="mt-6">
                <p className="text-sm text-gray-600 mb-3">Búsquedas populares:</p>
                <div className="flex flex-wrap gap-2">
                  {['iPhone 15', 'MacBook Air', 'Nike Air Max', 'Samsung TV', 'AirPods Pro'].map((term) => (
                    <button
                      key={term}
                      onClick={() => {setQuery(term); handleSearch({preventDefault: () => {}} as any)}}
                      className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors"
                    >
                      {term}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {products.length > 0 && (
            <>
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  Encontramos {products.length} productos para "{query}"
                </h2>
                <p className="text-gray-600">Comparando precios en múltiples tiendas</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {products.map((product) => (
                  <div key={product.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                    <div className="relative">
                      <div className="aspect-square bg-gradient-to-br from-gray-100 to-gray-200">
                        <img 
                          src={product.image} 
                          alt={product.title}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.currentTarget.src = 'https://via.placeholder.com/400x400/f3f4f6/6b7280?text=' + encodeURIComponent(product.title.split(' ')[0])
                          }}
                        />
                      </div>
                      <div className="absolute top-3 right-3">
                        <span className="bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full text-xs font-medium text-gray-700">
                          {product.merchant.name}
                        </span>
                      </div>
                      {product.shipping?.includes('Free') && (
                        <div className="absolute top-3 left-3">
                          <span className="bg-green-500 text-white px-2 py-1 rounded-full text-xs font-medium">
                            🚚 Envío Gratis
                          </span>
                        </div>
                      )}
                    </div>
                    
                    <div className="p-5">
                      <h3 className="font-bold text-gray-900 mb-3 line-clamp-2 h-12 text-lg leading-tight">{product.title}</h3>
                      
                      <div className="flex items-center justify-between mb-3">
                        {product.rating && (
                          <div className="flex items-center">
                            <div className="flex text-yellow-400 text-sm">
                              {[...Array(5)].map((_, i) => (
                                <span key={i}>{i < Math.floor(product.rating!) ? '⭐' : '☆'}</span>
                              ))}
                            </div>
                            <span className="text-sm text-gray-600 ml-2">({product.rating})</span>
                          </div>
                        )}
                      </div>
                      
                      <div className="mb-4">
                        <div className="flex items-baseline justify-between">
                          <span className="text-3xl font-bold text-green-600">
                            ${product.price.amount}
                          </span>
                          <span className="text-sm text-gray-500 line-through">
                            ${(product.price.amount * 1.2).toFixed(2)}
                          </span>
                        </div>
                        <p className="text-sm text-green-600 font-medium mt-1">
                          Ahorras ${((product.price.amount * 1.2) - product.price.amount).toFixed(2)}
                        </p>
                      </div>
                      
                      {product.shipping && (
                        <div className="flex items-center mb-4 text-sm text-gray-600">
                          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                          </svg>
                          {product.shipping}
                        </div>
                      )}
                      
                      <button
                        onClick={() => handleProductClick(product.id)}
                        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-4 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-semibold text-sm flex items-center justify-center space-x-2"
                      >
                        <span>Ver en {product.merchant.name}</span>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>

        <footer className="bg-gray-800 text-white py-8 mt-16">
          <div className="max-w-7xl mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-6">
              <div>
                <h3 className="font-semibold mb-3">La Ventanita 593</h3>
                <p className="text-sm text-gray-300">
                  Comparamos precios de múltiples tiendas para que encuentres las mejores ofertas.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-3">Tiendas Afiliadas</h3>
                <p className="text-sm text-gray-300">
                  Best Buy, Target, Walmart, Nike, Adidas, Samsung y más.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-3">Enlaces Legales</h3>
                <div className="space-y-2">
                  <a href="/como-funciona" className="block text-sm text-gray-300 hover:text-white">Cómo Funciona</a>
                  <a href="/politicas" className="block text-sm text-gray-300 hover:text-white">Políticas de Privacidad</a>
                  <a href="/terminos" className="block text-sm text-gray-300 hover:text-white">Términos y Condiciones</a>
                  <a href="/contacto" className="block text-sm text-gray-300 hover:text-white">Contacto</a>
                </div>
              </div>
              <div>
                <h3 className="font-semibold mb-3">Información</h3>
                <div className="bg-yellow-900/30 border border-yellow-700 rounded p-3">
                  <p className="text-xs text-yellow-200">
                    ⚠️ AVISO: Podemos ganar una comisión por compras realizadas a través de nuestros enlaces.
                  </p>
                </div>
              </div>
            </div>
            <div className="border-t border-gray-700 pt-6 text-center">
              <p className="text-sm text-gray-400">
                © 2024 La Ventanita 593. Compras en la tienda original; aplican sus términos y devoluciones.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}