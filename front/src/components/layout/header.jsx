import Link from "next/link"
import { TrendingUp } from "lucide-react"

export default function Header() {
  return (
    <header className="bg-black border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <TrendingUp className="h-8 w-8 text-blue-500" />
            <span className="text-2xl font-bold text-white">SalesVision AI</span>
          </Link>

          <nav className="hidden md:flex items-center gap-8">
            <Link href="/" className="text-gray-300 hover:text-white">
              Inicio
            </Link>
            <Link href="/upload" className="text-gray-300 hover:text-white">
              Subir Datos
            </Link>
          </nav>

          <Link href="/upload" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium">
            Empezar
          </Link>
        </div>
      </div>
    </header>
  )
}
