import Header from "../../components/layout/header"
import Footer from "../..//components/layout/footer"
import { Upload, FileText, ArrowRight } from "lucide-react"

export default function UploadPage() {
  return (
    <div className="min-h-screen bg-black text-white">
      <Header />
      <main className="py-20">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-white mb-4">Sube tus datos de ventas</h1>
            <p className="text-xl text-gray-400">Carga tu archivo CSV y comienza a generar predicciones precisas</p>
          </div>

          <div className="bg-gray-900 border-2 border-dashed border-gray-600 hover:border-blue-500 rounded-xl p-12 text-center space-y-6 transition-colors">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-blue-600 text-white">
              <Upload className="h-10 w-10" />
            </div>

            <div>
              <h3 className="text-xl font-bold text-white mb-2">Arrastra tu archivo CSV aquí</h3>
              <p className="text-gray-400">o haz clic para seleccionar desde tu computadora</p>
            </div>

            <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-bold flex items-center gap-2 mx-auto">
              <FileText className="h-5 w-5" />
              Seleccionar archivo
            </button>

            <div className="text-gray-500">Formatos soportados: CSV, Excel (.xlsx)</div>
          </div>

          <div className="mt-8 text-center">
            <button className="border border-gray-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-gray-800 flex items-center gap-2 mx-auto">
              Ver ejemplo de formato
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
