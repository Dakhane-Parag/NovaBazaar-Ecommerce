import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { getSuggestions } from '../services/searchApi'

export default function SearchBar() {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const debounceRef = useRef(null)

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    if (query.length < 2) {
      setSuggestions([])
      setShowSuggestions(false)
      return
    }
    debounceRef.current = setTimeout(async () => {
      setLoading(true)
      try {
        const data = await getSuggestions(query)
        setSuggestions(data.suggestions || [])
        setShowSuggestions(true)
      } catch (e) {
        setSuggestions([])
      } finally {
        setLoading(false)
      }
    }, 300)
    return () => clearTimeout(debounceRef.current)
  }, [query])

  function handleSearch(e) {
    e.preventDefault()
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`)
      setShowSuggestions(false)
    }
  }

  function handleSuggestionClick(suggestion) {
    setQuery(suggestion)
    navigate(`/search?q=${encodeURIComponent(suggestion)}`)
    setShowSuggestions(false)
  }

  return (
    <div className="relative flex-1 max-w-xl">
      <form onSubmit={handleSearch}>
        <div className="flex">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => query.length >= 2 && setShowSuggestions(true)}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
            placeholder="Search products..."
            className="flex-1 px-4 py-2 rounded-l-lg border border-gray-300 bg-white text-gray-900 placeholder-gray-500 focus:outline-none focus:border-orange-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-orange-500 text-white rounded-r-lg hover:bg-orange-600 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>
      </form>

      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-b-lg shadow-lg z-20">
          {suggestions.map((s, i) => (
            <button
              key={i}
              onMouseDown={() => handleSuggestionClick(s)}
              className="w-full text-left px-4 py-2 hover:bg-gray-50 text-sm text-gray-700"
            >
              {s}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
