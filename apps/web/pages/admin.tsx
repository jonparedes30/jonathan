import { useState, useEffect } from 'react'
import Head from 'next/head'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

interface Stats {
  total_searches: number
  total_clicks: number
  total_products: number
  ctr: number
  estimated_earnings: number
}

interface DailyStats {
  date: string
  searches: number
  clicks: number
  estimated_earnings: number
}

export default function AdminPanel() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [dailyStats, setDailyStats] = useState<DailyStats[]>([])
  const [authenticated, setAuthenticated] = useState(false)
  const [credentials, setCredentials] = useState({ username: '', password: '' })
  const [loading, setLoading] = useState(false)

  const authenticate = async (username: string, password: string) => {
    const auth = btoa(`${username}:${password}`)
    try {
      const response = await fetch('http://localhost:8090/api/admin/stats', {
        headers: { 'Authorization': `Basic ${auth}` }
      })
      if (response.ok) {
        setAuthenticated(true)
        localStorage.setItem('admin_auth', auth)
        return true
      }
    } catch (error) {
      console.error('Auth error:', error)
    }
    return false
  }

  const fetchData = async () => {
    const auth = localStorage.getItem('admin_auth')
    if (!auth) return

    setLoading(true)
    try {
      const [statsRes, dailyRes] = await Promise.all([
        fetch('http://localhost:8090/api/admin/stats', {
          headers: { 'Authorization': `Basic ${auth}` }
        }),
        fetch('http://localhost:8090/api/admin/daily-stats', {
          headers: { 'Authorization': `Basic ${auth}` }
        })
      ])

      if (statsRes.ok && dailyRes.ok) {
        const statsData = await statsRes.json()
        const dailyData = await dailyRes.json()
        setStats(statsData)
        setDailyStats(dailyData.daily_stats)
      }
    } catch (error) {
      console.error('Fetch error:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const auth = localStorage.getItem('admin_auth')
    if (auth) {
      setAuthenticated(true)
      fetchData()
    }
  }, [])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    const success = await authenticate(credentials.username, credentials.password)
    if (success) {
      fetchData()
    } else {
      alert('Credenciales incorrectas')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('admin_auth')
    setAuthenticated(false)
    setStats(null)
    setDailyStats([])
  }

  if (!authenticated) {
    return (
      <>
        <Head>
          <title>Admin Panel - La Ventanita 593</title>
        </Head>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="bg-white p-8 rounded-lg shadow-md w-96">
            <h1 className="text-2xl font-bold mb-6 text-center">Panel de Administración</h1>
            <form onSubmit={handleLogin}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Usuario</label>
                <input
                  type="text"
                  value={credentials.username}
                  onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Contraseña</label>
                <input
                  type="password"
                  value={credentials.password}
                  onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
              >
                Iniciar Sesión
              </button>
            </form>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <Head>
        <title>Admin Panel - La Ventanita</title>
      </Head>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Panel de Administración</h1>
            <button
              onClick={handleLogout}
              className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
            >
              Cerrar Sesión
            </button>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 py-8">
          {loading ? (
            <div className="text-center">Cargando...</div>
          ) : (
            <>
              {/* Stats Cards */}
              {stats && (
                <>
                  <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 mb-8 text-white">
                    <div className="flex items-center justify-between">
                      <div>
                        <h2 className="text-2xl font-bold mb-2">La Ventanita 593 - Panel de Control</h2>
                        <p className="text-blue-100">Monitoreo en tiempo real de tu metabuscador de afiliados</p>
                      </div>
                      <div className="text-right">
                        <p className="text-3xl font-bold">${stats.estimated_earnings}</p>
                        <p className="text-blue-100">Ganancias Estimadas</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
                      <h3 className="text-sm font-medium text-gray-500 mb-1">Total Búsquedas</h3>
                      <p className="text-3xl font-bold text-blue-600">{stats.total_searches}</p>
                      <p className="text-xs text-gray-400 mt-1">Consultas realizadas</p>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
                      <h3 className="text-sm font-medium text-gray-500 mb-1">Clicks a Tiendas</h3>
                      <p className="text-3xl font-bold text-green-600">{stats.total_clicks}</p>
                      <p className="text-xs text-gray-400 mt-1">Redirecciones exitosas</p>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-purple-500">
                      <h3 className="text-sm font-medium text-gray-500 mb-1">CTR</h3>
                      <p className="text-3xl font-bold text-purple-600">{stats.ctr}%</p>
                      <p className="text-xs text-gray-400 mt-1">Tasa de conversión</p>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-orange-500">
                      <h3 className="text-sm font-medium text-gray-500 mb-1">Productos Mostrados</h3>
                      <p className="text-3xl font-bold text-orange-600">{stats.total_products}</p>
                      <p className="text-xs text-gray-400 mt-1">Resultados generados</p>
                    </div>
                  </div>
                </>
              )}

              {/* Charts */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-lg font-semibold mb-4">Búsquedas y Clicks (7 días)</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={dailyStats}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="searches" stroke="#3B82F6" name="Búsquedas" />
                      <Line type="monotone" dataKey="clicks" stroke="#10B981" name="Clicks" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-lg font-semibold mb-4">Ganancias Estimadas (7 días)</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={dailyStats}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`$${value}`, 'Ganancias']} />
                      <Bar dataKey="estimated_earnings" fill="#10B981" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Additional Info */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-lg font-semibold mb-4 text-gray-900">Información del Sistema</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Red de Afiliados:</span>
                      <span className="font-medium text-blue-600">Skimlinks Network</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Tiendas Conectadas:</span>
                      <span className="font-medium">8+ tiendas principales</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Comisión Promedio:</span>
                      <span className="font-medium text-green-600">5.0%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Conversión Estimada:</span>
                      <span className="font-medium">15%</span>
                    </div>
                  </div>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-lg font-semibold mb-4 text-gray-900">Tiendas Principales</h3>
                  <div className="space-y-2">
                    {['Best Buy', 'Target', 'Walmart', 'Nike', 'Adidas', 'Samsung'].map((store) => (
                      <div key={store} className="flex items-center justify-between py-1">
                        <span className="text-gray-700">{store}</span>
                        <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Activo</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              
              <div className="mt-8 text-center">
                <button
                  onClick={fetchData}
                  className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 font-medium"
                >
                  🔄 Actualizar Datos
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  )
}