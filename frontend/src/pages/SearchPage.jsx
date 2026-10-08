import { useState, useEffect, useCallback } from 'react'
import { useSearchParams } from 'react-router-dom'
import { searchProducts } from '../services/searchApi'
import ProductGrid from '../components/ProductGrid'
import Pagination from '../components/Pagination'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

export default function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [results, setResults] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const q = searchParams.get('q') || ''
  const category = searchParams.get('category') || ''
  const brand = searchParams.get('brand') || ''
  const minPrice = searchParams.get('minPrice') || ''
  const maxPrice = searchParams.get('maxPrice') || ''
  const minRating = searchParams.get('minRating') || ''
  const page = parseInt(searchParams.get('page') || '1', 10)
  const limit = 12
  const sort = searchParams.get('sort') || 'price_asc'

  const totalPages = Math.ceil(total / limit)

  const fetchResults = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await searchProducts({
        q, category, brand, minPrice, maxPrice, minRating, page, limit, sort,
      })
      setResults(data.items || [])
      setTotal(data.total || 0)
    } catch (e) {
      setError(e.message || 'Search failed')
    } finally {
      setLoading(false)
    }
  }, [q, category, brand, minPrice, maxPrice, minRating, page, limit, sort])

  useEffect(() => {
    fetchResults()
  }, [fetchResults])

  function updateParams(updates) {
    const params = new URLSearchParams(searchParams)
    Object.entries(updates).forEach(([key, value]) => {
      if (value === '' || value === null || value === undefined) {
        params.delete(key)
      } else {
        params.set(key, value)
      }
    })
    setSearchParams(params)
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gray-900 text-white px-4 py-3 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold text-orange-400">NovaBazaar</h1>
          <span className="text-sm text-gray-300">Search Results for: {q}</span>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-4">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-4 flex flex-wrap items-center gap-3">
          <select
            value={category}
            onChange={(e) => updateParams({ category: e.target.value, page: '1' })}
            className="border border-gray-300 rounded px-3 py-1.5 text-sm"
          >
            <option value="">All Categories</option>
            <option value="electronics">Electronics</option>
            <option value="fashion">Fashion</option>
            <option value="home-kitchen">Home & Kitchen</option>
            <option value="beauty">Beauty</option>
            <option value="fitness">Fitness</option>
          </select>

          <select
            value={brand}
            onChange={(e) => updateParams({ brand: e.target.value, page: '1' })}
            className="border border-gray-300 rounded px-3 py-1.5 text-sm"
          >
            <option value="">All Brands</option>
            <option value="Apple">Apple</option>
            <option value="Samsung">Samsung</option>
            <option value="Sony">Sony</option>
            <option value="Nike">Nike</option>
            <option value="Adidas">Adidas</option>
          </select>

          <input
            type="number"
            placeholder="Min Price"
            value={minPrice}
            onChange={(e) => updateParams({ minPrice: e.target.value, page: '1' })}
            className="border border-gray-300 rounded px-3 py-1.5 text-sm w-28"
          />
          <input
            type="number"
            placeholder="Max Price"
            value={maxPrice}
            onChange={(e) => updateParams({ maxPrice: e.target.value, page: '1' })}
            className="border border-gray-300 rounded px-3 py-1.5 text-sm w-28"
          />

          <select
            value={sort}
            onChange={(e) => updateParams({ sort: e.target.value, page: '1' })}
            className="border border-gray-300 rounded px-3 py-1.5 text-sm"
          >
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="rating_desc">Rating</option>
          </select>
        </div>

        {loading && <LoadingSpinner />}
        {error && <ErrorMessage message={error} onRetry={fetchResults} />}

        {!loading && !error && results.length === 0 && (
          <div className="flex flex-col items-center justify-center py-20">
            <p className="text-gray-500 text-lg">No results found for "{q}"</p>
          </div>
        )}

        {!loading && !error && results.length > 0 && (
          <>
            <p className="text-sm text-gray-500 mb-4">{total} results found</p>
            <ProductGrid products={results} />
            <Pagination page={page} totalPages={totalPages} onPageChange={(p) => updateParams({ page: String(p) })} />
          </>
        )}
      </main>
    </div>
  )
}
