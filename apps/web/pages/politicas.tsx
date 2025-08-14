import Head from 'next/head'

export default function Politicas() {
  return (
    <>
      <Head>
        <title>Políticas de Privacidad - La Ventanita 593</title>
      </Head>
      
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-4xl mx-auto px-4 py-6">
            <h1 className="text-3xl font-bold text-gray-900">Políticas de Privacidad</h1>
          </div>
        </header>

        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold mb-6">Política de Privacidad</h2>
            
            <div className="space-y-6 text-gray-700">
              <section>
                <h3 className="text-xl font-semibold mb-3">Información que Recopilamos</h3>
                <p>La Ventanita 593 recopila información mínima necesaria para proporcionar nuestro servicio de comparación de precios.</p>
              </section>

              <section>
                <h3 className="text-xl font-semibold mb-3">Enlaces de Afiliados</h3>
                <p className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
                  <strong>AVISO IMPORTANTE:</strong> La Ventanita 593 participa en programas de afiliados. 
                  Podemos ganar una comisión cuando realizas una compra a través de nuestros enlaces, 
                  sin costo adicional para ti.
                </p>
              </section>

              <section>
                <h3 className="text-xl font-semibold mb-3">Socios de Afiliación</h3>
                <p>Trabajamos con redes de afiliados como Skimlinks para monetizar nuestro servicio. 
                Puedes consultar la <a href="https://skimlinks.com/privacy-policy" className="text-blue-600 underline">
                política de privacidad de Skimlinks</a>.</p>
              </section>

              <section>
                <h3 className="text-xl font-semibold mb-3">Cookies</h3>
                <p>Utilizamos cookies para mejorar tu experiencia y para el funcionamiento de los enlaces de afiliados.</p>
              </section>

              <section>
                <h3 className="text-xl font-semibold mb-3">Contacto</h3>
                <p>Para consultas sobre privacidad: contacto@laventanita593.com</p>
              </section>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}