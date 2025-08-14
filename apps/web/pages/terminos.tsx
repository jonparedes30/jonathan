import Head from 'next/head'

export default function Terminos() {
  return (
    <>
      <Head>
        <title>Términos y Condiciones - La Ventanita 593</title>
      </Head>
      
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-4xl mx-auto px-4 py-6">
            <h1 className="text-3xl font-bold text-gray-900">Términos y Condiciones</h1>
          </div>
        </header>

        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold mb-6">Términos de Uso</h2>
            
            <div className="space-y-6 text-gray-700">
              <section>
                <h3 className="text-xl font-semibold mb-3">Sobre Nuestro Servicio</h3>
                <p>La Ventanita 593 es un servicio de comparación de precios que te redirige a tiendas externas. 
                No vendemos productos directamente ni gestionamos transacciones.</p>
              </section>

              <section>
                <h3 className="text-xl font-semibold mb-3">Compras y Devoluciones</h3>
                <p>Todas las compras se realizan directamente con las tiendas externas. 
                Las políticas de devolución, garantías y servicio al cliente son responsabilidad de cada tienda.</p>
              </section>

              <section>
                <h3 className="text-xl font-semibold mb-3">Enlaces de Afiliados</h3>
                <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
                  <p><strong>TRANSPARENCIA:</strong> Algunos enlaces en nuestro sitio son enlaces de afiliados. 
                  Esto significa que podemos recibir una comisión si realizas una compra, sin costo adicional para ti.</p>
                </div>
              </section>

              <section>
                <h3 className="text-xl font-semibold mb-3">Precios y Disponibilidad</h3>
                <p>Los precios mostrados son informativos y pueden cambiar. 
                El precio final será el mostrado en la tienda de destino al momento de la compra.</p>
              </section>

              <section>
                <h3 className="text-xl font-semibold mb-3">Limitación de Responsabilidad</h3>
                <p>La Ventanita 593 no se hace responsable por problemas con productos, 
                entregas o servicios proporcionados por las tiendas externas.</p>
              </section>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}