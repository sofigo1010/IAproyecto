"use client";

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import Header from "../../components/layout/header"
import Footer from "../../components/layout/footer"
import { Upload, FileText, ChevronDown, Loader2 } from "lucide-react"


export default function UploadPage() {
  const [selectedMonths, setSelectedMonths] = useState(6)
  const [file, setFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const router = useRouter()

  const monthOptions = [1, 6, 12, 24]

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.type === "text/csv" || droppedFile.name.endsWith(".csv")) {
        setFile(droppedFile)
      }
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async () => {
    if (!file) return

    setIsLoading(true)

    // Simular procesamiento
    await new Promise((resolve) => setTimeout(resolve, 3000))

    // Redirigir a resultados
    router.push("/results")
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <Header />
      <main className="py-20">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-white mb-4">Configurar Predicción</h1>
            <p className="text-xl text-gray-400">Configura los parámetros y sube tus datos de ventas</p>
          </div>

          {/* Selector de meses */}
          <div className="mb-8">
            <label className="block text-lg font-bold text-white mb-4">¿Cuántos meses deseas predecir?</label>
            <div className="relative">
              <select
                value={selectedMonths}
                onChange={(e) => setSelectedMonths(Number(e.target.value))}
                className="w-full bg-gray-900 border border-gray-600 text-white px-4 py-3 rounded-lg appearance-none cursor-pointer focus:border-blue-500 focus:outline-none"
              >
                {monthOptions.map((months) => (
                  <option key={months} value={months}>
                    {months} {months === 1 ? "mes" : "meses"}
                  </option>
                ))}
              </select>
              <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none" />
            </div>
          </div>

          {/* Área de carga de archivo */}
          <div className="mb-8">
            <div
              className={`bg-gray-900 border-2 border-dashed rounded-xl p-12 text-center space-y-6 transition-colors ${
                dragActive
                  ? "border-blue-500 bg-blue-500/10"
                  : file
                    ? "border-green-500 bg-green-500/10"
                    : "border-gray-600 hover:border-blue-500"
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-blue-600 text-white">
                <Upload className="h-10 w-10" />
              </div>

              <div>
                <h3 className="text-xl font-bold text-white mb-2">
                  {file ? file.name : "Arrastra tu archivo CSV aquí"}
                </h3>
                <p className="text-gray-400">o haz clic para seleccionar desde tu computadora</p>
              </div>

              <input type="file" accept=".csv" onChange={handleFileChange} className="hidden" id="file-upload" />
              <label
                htmlFor="file-upload"
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-bold flex items-center gap-2 mx-auto cursor-pointer"
              >
                <FileText className="h-5 w-5" />
                Cargar archivo CSV
              </label>

              <div className="text-gray-500">Formatos soportados: CSV</div>
            </div>
          </div>

          {/* Instrucciones */}
          <div className="mb-8 bg-gray-900 border border-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-bold text-white mb-3">Formato requerido del CSV:</h3>
            <p className="text-gray-300 mb-4">
              Sube un CSV con columnas:{" "}
              <span className="text-blue-400 font-mono">fecha, ventas_previas, otras_vars</span>
            </p>
            <div className="bg-black rounded-lg p-4 font-mono text-sm">
              <div className="text-gray-400">Ejemplo:</div>
              <div className="text-green-400">fecha,ventas_previas,otras_vars</div>
              <div className="text-white">2023-01-01,5000,variable1</div>
              <div className="text-white">2023-01-02,5200,variable2</div>
            </div>
          </div>

          {/* Preview del archivo */}
          {file && (
            <div className="mb-8 bg-gray-900 border border-gray-700 rounded-lg p-6">
              <h3 className="text-lg font-bold text-white mb-3">Archivo seleccionado:</h3>
              <div className="flex items-center gap-3 text-gray-300">
                <FileText className="h-5 w-5 text-blue-400" />
                <span>{file.name}</span>
                <span className="text-gray-500">({(file.size / 1024).toFixed(1)} KB)</span>
              </div>
            </div>
          )}

          {/* Botón de envío */}
          <div className="text-center">
            <button
              onClick={handleSubmit}
              disabled={!file || isLoading}
              className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white px-8 py-4 rounded-lg font-bold text-lg flex items-center gap-2 mx-auto"
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Procesando predicción...
                </>
              ) : (
                "Enviar a predicción"
              )}
            </button>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
