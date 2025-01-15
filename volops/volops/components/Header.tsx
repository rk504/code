import { Search } from 'lucide-react'
import { Input } from '@/components/ui/input'

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 py-4 px-6 flex items-center justify-between">
      <h1 className="text-2xl font-bold text-blue-600">VolunteerConnect</h1>
      <div className="flex items-center space-x-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <Input
            type="search"
            placeholder="Search opportunities..."
            className="pl-10 pr-4 py-2 w-64 rounded-full border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
          />
        </div>
        <nav>
          <ul className="flex space-x-4">
            <li><a href="#" className="text-gray-600 hover:text-blue-600">Browse</a></li>
            <li><a href="#" className="text-gray-600 hover:text-blue-600">How it works</a></li>
            <li><a href="#" className="text-gray-600 hover:text-blue-600">Sign in</a></li>
          </ul>
        </nav>
      </div>
    </header>
  )
}

