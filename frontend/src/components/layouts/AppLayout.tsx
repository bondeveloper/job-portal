import { Outlet, Link, useNavigate } from 'react-router-dom'

export default function AppLayout() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold text-brand-600">Job Portal</Link>
          <nav className="flex gap-6 items-center">
            <Link to="/jobs" className="text-gray-600 hover:text-brand-600">Jobs</Link>
            <Link to="/candidates" className="text-gray-600 hover:text-brand-600">Candidates</Link>
            <Link to="/dashboard" className="text-gray-600 hover:text-brand-600">Dashboard</Link>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-brand-600 text-white rounded hover:bg-brand-700"
            >
              Logout
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  )
}
