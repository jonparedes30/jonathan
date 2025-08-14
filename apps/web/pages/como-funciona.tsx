import Head from 'next/head'

export default function ComoFunciona() {
  return (
    <>
      <Head>
        <title>Cómo Funciona - La Ventanita 593</title>
      </Head>
      
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-4xl mx-auto px-4 py-6">
            <h1 className="text-3xl font-bold text-gray-900">Cómo Funciona</h1>
          </div>
        </header>

        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold mb-8 text-center">Encuentra los Mejores Precios en 3 Pasos</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white text-2xl font-bold">1</span>
                </div>
                <h3 className="text-xl font-semibold mb-3">Busca</h3>
                <p className="text-gray-600">Escribe el producto que buscas: iPhone, laptop, zapatos, etc.</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white text-2xl font-bold">2</span>
                </div>
                <h3 className="text-xl font-semibold mb-3">Compara</h3>
                <p className="text-gray-600">Ve precios de múltiples tiendas: Best Buy, Target, Walmart y más.</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white text-2xl font-bold">3</span>
                </div>
                <h3 className="text-xl font-semibold mb-3">Compra</h3>
                <p className="text-gray-600">Haz clic y compra directamente en la tienda con el mejor precio.</p>
              </div>
            </div>

            <div className="bg-blue-50 border-l-4 border-blue-400 p-6 mb-8">
              <h3 className="text-lg font-semibold mb-3">¿Por qué usar La Ventanita 593?</h3>
              <ul className="space-y-2 text-gray-700">
                <li>✅ <strong>Ahorra tiempo:</strong> No busques en cada tienda por separado</li>
                <li>✅ <strong>Mejores precios:</strong> Comparamos automáticamente</li>
                <li>✅ <strong>Tiendas confiables:</strong> Solo trabajamos con retailers reconocidos</li>
                <li>✅ <strong>Gratis:</strong> Nuestro servicio es completamente gratuito</li>
              </ul>
            </div>

            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6">
              <h3 className="text-lg font-semibold mb-3">Transparencia Total</h3>
              <p className="text-gray-700">
                Somos transparentes: ganamos una pequeña comisión cuando compras a través de nuestros enlaces, 
                pero esto NO afecta el precio que pagas. Es así como mantenemos nuestro servicio gratuito.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}