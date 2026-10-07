import { useState, useEffect, useCallback } from 'react'

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8502'

function App() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [category, setCategory] = useState('')
  const [sort, setSort] = useState('price_asc')
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [currentView, setCurrentView] = useState(window.location.pathname)

  const limit = 12
  const totalPages = Math.ceil(total / limit)

  const categories = [
    { value: '', label: 'All' },
    { value: 'electronics', label: 'Electronics' },
    { value: 'fashion', label: 'Fashion' },
    { value: 'home-kitchen', label: 'Home & Kitchen' },
    { value: 'beauty', label: 'Beauty' },
    { value: 'fitness', label: 'Fitness' },
  ]

  useEffect(() => {
    fetchProducts()
  }, [category, sort, page])

  useEffect(() => {
    setPage(1)
  }, [category, sort])

  useEffect(() => {
    const handlePopState = () => {
      setCurrentView(window.location.pathname)
      setSelectedProduct(null)
    }
    window.addEventListener('popstate', handlePopState)
    return () => window.removeEventListener('popstate', handlePopState)
  }, [])

  useEffect(() => {
    const path = window.location.pathname
    const match = path.match(/^\/product\/(.+)$/)
    if (match) {
      fetchProduct(match[1])
    } else {
      setSelectedProduct(null)
    }
  }, [currentView])

  async function fetchProducts() {
    setLoading(true)
    try {
      const params = new URLSearchParams({ page, limit, sort })
      if (category) params.set('category', category)
      const res = await fetch(`${API_URL}/products?${params}`)
      const data = await res.json()
      setProducts(data.items || [])
      setTotal(data.total || 0)
      setError(null)
    } catch (e) {
      setError('Failed to load products')
    } finally {
      setLoading(false)
    }
  }

  const fetchProduct = useCallback(async (id) => {
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/products/${id}`)
      if (res.ok) {
        const data = await res.json()
        setSelectedProduct(data)
      }
    } catch (e) {
      setError('Failed to load product')
    } finally {
      setLoading(false)
    }
  }, [])

  function handleProductClick(product) {
    window.history.pushState({}, '', `/product/${product.id}`)
    setCurrentView(window.location.pathname)
  }

  function handleBack() {
    window.history.pushState({}, '', '/')
    setCurrentView('/')
  }

  if (selectedProduct) {
    return (
      <div className="min-h-screen bg-gray-100">
        <header className="bg-gray-900 text-white px-4 py-3 flex items-center justify-between sticky top-0 z-10">
          <h1 className="text-xl font-bold text-orange-400">NovaBazaar</h1>
          <button onClick={handleBack} className="text-sm text-gray-300 hover:text-white flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
            Back
          </button>
        </header>

        <main className="max-w-6xl mx-auto p-4">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="aspect-square bg-gray-50 rounded-lg overflow-hidden border">
                <img
                  src={selectedProduct.images?.[0] || 'https://via.placeholder.com/400'}
                  alt={selectedProduct.title}
                  className="w-full h-full object-cover"
                  onError={(e) => { e.target.src = 'https://via.placeholder.com/400?text=No+Image' }}
                />
              </div>

              <div className="flex flex-col">
                <h1 className="text-2xl font-bold text-gray-900 mb-1">{selectedProduct.title}</h1>
                <p className="text-sm text-blue-600 hover:text-blue-800 cursor-pointer mb-3">{selectedProduct.brand}</p>

                <div className="flex items-center gap-2 mb-4">
                  <div className="flex">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <span key={star} className={`text-lg ${star <= Math.round(selectedProduct.rating || 0) ? 'text-yellow-500' : 'text-gray-300'}`}>★</span>
                    ))}
                  </div>
                  <span className="text-sm text-blue-600">{selectedProduct.rating} out of 5</span>
                </div>

                <hr className="my-4" />

                <div className="mb-4">
                  <span className="text-3xl font-bold text-gray-900">₹{selectedProduct.price?.toLocaleString()}</span>
                  <span className="text-sm text-gray-500 ml-2">Inclusive of all taxes</span>
                </div>

                <p className="text-gray-700 mb-4 leading-relaxed">{selectedProduct.description}</p>

                {selectedProduct.attributes && Object.keys(selectedProduct.attributes).length > 0 && (
                  <div className="mb-4">
                    <h3 className="text-sm font-semibold text-gray-900 mb-2">Specifications</h3>
                    <div className="bg-gray-50 rounded p-3">
                      {Object.entries(selectedProduct.attributes).map(([key, value]) => (
                        <div key={key} className="flex text-sm py-1">
                          <span className="text-gray-500 w-32 capitalize">{key}:</span>
                          <span className="text-gray-900 font-medium">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {selectedProduct.tags && selectedProduct.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-6">
                    {selectedProduct.tags.map((tag) => (
                      <span key={tag} className="px-3 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">{tag}</span>
                    ))}
                  </div>
                )}

                <div className="flex gap-3 mt-auto">
                  <button className="flex-1 bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-semibold py-3 px-6 rounded-full transition-colors">
                    Add to Cart
                  </button>
                  <button className="flex-1 bg-orange-500 hover:bg-orange-600 text-white font-semibold py-3 px-6 rounded-full transition-colors">
                    Buy Now
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gray-900 text-white px-4 py-3 flex items-center justify-between sticky top-0 z-10">
        <h1 className="text-xl font-bold text-orange-400">NovaBazaar</h1>
        <div className="flex items-center gap-3">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="bg-gray-800 text-white border border-gray-700 rounded px-3 py-1.5 text-sm"
          >
            {categories.map((c) => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            className="bg-gray-800 text-white border border-gray-700 rounded px-3 py-1.5 text-sm"
          >
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="rating_desc">Rating</option>
          </select>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-4">
        {loading && (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-orange-500"></div>
          </div>
        )}
        {error && <p className="text-center text-red-500 py-20">{error}</p>}

        {!loading && !error && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
              {products.map((product) => (
                <div
                  key={product.id}
                  onClick={() => handleProductClick(product)}
                  className="bg-white rounded-lg shadow-sm hover:shadow-lg transition-all p-3 flex flex-col cursor-pointer group"
                >
                  <div className="aspect-square bg-gray-50 rounded mb-3 overflow-hidden">
                    <img
                      src={product.images?.[0] || 'https://via.placeholder.com/300'}
                      alt={product.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                      onError={(e) => { e.target.src = 'https://via.placeholder.com/300?text=No+Image' }}
                    />
                  </div>
                  <h3 className="text-sm font-medium text-gray-900 line-clamp-2 mb-1 group-hover:text-blue-600">
                    {product.title}
                  </h3>
                  <p className="text-xs text-gray-500 mb-1">{product.brand}</p>
                  <div className="flex items-center gap-1 mb-2">
                    <span className="text-yellow-500 text-sm">{'★'.repeat(Math.round(product.rating || 0))}</span>
                    <span className="text-xs text-gray-400">({product.rating})</span>
                  </div>
                  <div className="mt-auto">
                    <span className="text-lg font-bold text-gray-900">₹{product.price?.toLocaleString()}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-center gap-4 mt-8 pb-8">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-5 py-2 bg-gray-900 text-white rounded-full disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-700 transition-colors"
              >
                Previous
              </button>
              <span className="text-gray-600 font-medium">
                Page {page} of {totalPages || 1}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages || totalPages === 0}
                className="px-5 py-2 bg-gray-900 text-white rounded-full disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-700 transition-colors"
              >
                Next
              </button>
            </div>
          </>
        )}

        {!loading && !error && products.length === 0 && (
          <p className="text-center text-gray-500 py-20">No products found</p>
        )}
      </main>
    </div>
  )
}

export default App
