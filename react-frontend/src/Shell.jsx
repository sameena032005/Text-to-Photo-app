import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import Home from './pages/Home'

export default function Shell() {
  return (
    <div className="flex h-screen flex-col overflow-hidden bg-ai-black">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto">
          <Home />
        </main>
      </div>
    </div>
  )
}
