import { useState } from 'react'

export default function JobsPage() {
  const [search, setSearch] = useState('')

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Jobs</h1>
        <button className="px-4 py-2 bg-brand-600 text-white rounded hover:bg-brand-700">
          Post New Job
        </button>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <input
          type="text"
          placeholder="Search jobs by title, location, or skills..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg"
        />
      </div>

      <div className="space-y-4">
        <p className="text-gray-500 text-center py-8">No jobs found</p>
      </div>
    </div>
  )
}
