"use client"
import { useRouter } from "next/navigation"
import Header from "../../components/layout/header"
import Footer from "../../components/layout/footer"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import { TrendingUp, BarChart3, Info } from "lucide-react"

// Datos de ejemplo para la gráfica
const predictionData = [
  { fecha: "2023-10-01", True: 4800, "Quantile LSTM": 4750, Ensemble: 4820, yhat_lower: 4200, yhat_upper: 5400 },
  { fecha: "2023-11-01", True: 5200, "Quantile LSTM": 5150, Ensemble: 5180, yhat_lower: 4600, yhat_upper: 5800 },
  { fecha: "2023-12-01", True: 5800, "Quantile LSTM": 5750, Ensemble: 5820, yhat_lower: 5200, yhat_upper: 6400 },
  { fecha: "2024-01-01", True: null, "Quantile LSTM": 6200, Ensemble: 6180, yhat_lower: 5600, yhat_upper: 6800 },
  { fecha: "2024-02-01", True: null, "Quantile LSTM": 6500, Ensemble: 6480, yhat_lower: 5900, yhat_upper: 7100 },
  { fecha: "2024-03-01", True: null, "Quantile LSTM": 6800, Ensemble: 6750, yhat_lower: 6200, yhat_upper: 7400 },
]

// Datos para la tabla
const tableData = [
  { fecha: "2024-01-01", lstm: 6200.12, ensemble: 6180.88, yhat_lower: 5600.15, yhat_upper: 6800.54 },
  { fecha: "2024-02-01", lstm: 6500.45, ensemble: 6480.22, yhat_lower: 5900.33, yhat_upper: 7100.67 },
  { fecha: "2024-03-01", lstm: 6800.78, ensemble: 6750.55, yhat_lower: 6200.44, yhat_upper: 7400.89 },
  { fecha: "2024-04-01", lstm: 7100.23, ensemble: 7080.11, yhat_lower: 6500.77, yhat_upper: 7700.45 },
  { fecha: "2024-05-01", lstm: 7400.56, ensemble: 7380.33, yhat_lower: 6800.88, yhat_upper: 8000.22 },
  { fecha: "2024-06-01", lstm: 7700.89, ensemble: 7680.66, yhat_lower: 7100.99, yhat_upper: 8300.55 },
]

export default function ResultsPage() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-black text-white">
      <Header />
      <main className="py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-white mb-4">Resultados de Predicción</h1>
            <p className="text-xl text-gray-400">Análisis completo de tus predicciones de ventas</p>
          </div>

          {/* Gráfica de líneas */}
          <div className="bg-gray-900 rounded-xl p-8 border border-gray-800 mb-8">
            <div className="flex items-center gap-2 mb-6">
              <TrendingUp className="h-6 w-6 text-blue-500" />
              <h2 className="text-2xl font-bold text-white">Gráfica de Predicciones</h2>
            </div>

            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={predictionData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="fecha" stroke="#9CA3AF" tick={{ fill: "#9CA3AF" }} />
                  <YAxis stroke="#9CA3AF" tick={{ fill: "#9CA3AF" }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1F2937",
                      border: "1px solid #374151",
                      borderRadius: "8px",
                      color: "#FFFFFF",
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="True"
                    stroke="#10B981"
                    strokeWidth={3}
                    name="Datos Reales"
                    connectNulls={false}
                  />
                  <Line type="monotone" dataKey="Quantile LSTM" stroke="#3B82F6" strokeWidth={2} name="Quantile LSTM" />
                  <Line type="monotone" dataKey="Ensemble" stroke="#F59E0B" strokeWidth={2} name="Ensemble" />
                  <Line
                    type="monotone"
                    dataKey="yhat_lower"
                    stroke="#6B7280"
                    strokeWidth={1}
                    strokeDasharray="5 5"
                    name="Límite Inferior"
                  />
                  <Line
                    type="monotone"
                    dataKey="yhat_upper"
                    stroke="#6B7280"
                    strokeWidth={1}
                    strokeDasharray="5 5"
                    name="Límite Superior"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Explicación de métricas */}
          <div className="bg-gray-900 rounded-xl p-8 border border-gray-800 mb-8">
            <div className="flex items-center gap-2 mb-6">
              <Info className="h-6 w-6 text-blue-500" />
              <h2 className="text-2xl font-bold text-white">¿Qué significan estas métricas?</h2>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-bold text-green-400 mb-2">Datos Reales (True)</h3>
                  <p className="text-gray-300">
                    Valores históricos reales de tus ventas. Se usan como referencia para validar la precisión del
                    modelo.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-blue-400 mb-2">Quantile LSTM</h3>
                  <p className="text-gray-300">
                    Predicciones generadas por un modelo de red neuronal LSTM que considera múltiples cuantiles para
                    mayor precisión.
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-bold text-yellow-400 mb-2">Ensemble</h3>
                  <p className="text-gray-300">
                    Combinación de múltiples modelos de IA que promedia sus predicciones para obtener resultados más
                    robustos.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-gray-400 mb-2">Intervalos de Confianza</h3>
                  <p className="text-gray-300">
                    Límites superior e inferior que indican el rango probable donde se encontrarán las ventas reales.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Tabla de predicciones */}
          <div className="bg-gray-900 rounded-xl p-8 border border-gray-800 mb-8">
            <div className="flex items-center gap-2 mb-6">
              <BarChart3 className="h-6 w-6 text-blue-500" />
              <h2 className="text-2xl font-bold text-white">Tabla de Predicciones</h2>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="pb-3 text-gray-300 font-bold">Fecha</th>
                    <th className="pb-3 text-blue-400 font-bold">LSTM</th>
                    <th className="pb-3 text-yellow-400 font-bold">Ensemble</th>
                    <th className="pb-3 text-gray-400 font-bold">Límite Inferior</th>
                    <th className="pb-3 text-gray-400 font-bold">Límite Superior</th>
                  </tr>
                </thead>
                <tbody>
                  {tableData.map((row, index) => (
                    <tr key={index} className="border-b border-gray-800">
                      <td className="py-3 text-white font-mono">{row.fecha}</td>
                      <td className="py-3 text-blue-300 font-mono">{row.lstm.toFixed(2)}</td>
                      <td className="py-3 text-yellow-300 font-mono">{row.ensemble.toFixed(2)}</td>
                      <td className="py-3 text-gray-300 font-mono">{row.yhat_lower.toFixed(2)}</td>
                      <td className="py-3 text-gray-300 font-mono">{row.yhat_upper.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Botón para métricas */}
          <div className="text-center">
            <button
              onClick={() => router.push("/metrics")}
              className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-4 rounded-lg font-bold text-lg flex items-center gap-2 mx-auto"
            >
              <BarChart3 className="h-5 w-5" />
              Ver métricas comparativas
            </button>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
