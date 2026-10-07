import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getProductById } from '../services/productApi'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

export default function ProductDetailsPage() {
  const { productId } = useParams()
  const navigate = useNavigate()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchProduct()
  }, [productId])

  async function fetchProduct() {
    setLoading(true)
    setError(null)
    try {
      const data = await getProductById(productId)
      setProduct(data)
    } catch (e) {
      setError(e.message || 'Failed to load product')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100">
        <header className="bg-gray-900 text-white px-4 py-3 flex items-center justify-between sticky top-0 z-10">
          <h1 className="text-xl font-bold text-orange-400">NovaBazaar</h1>
          <button onClick={() => navigate(-1)} className="text-sm text-gray-300 hover:text-white flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
            Back
          </button>
        </header>
        <LoadingSpinner />
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100">
        <header className="bg-gray-900 text-white px-4 py-3 flex items-center justify-between sticky top-0 z-10">
          <h1 className="text-xl font-bold text-orange-400">NovaBazaar</h1>
          <button onClick={() => navigate(-1)} className="text-sm text-gray-300 hover:text-white flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
            Back
          </button>
        </header>
        <ErrorMessage message={error} onRetry={fetchProduct} />
      </div>
    )
  }

  if (!product) return null

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gray-900 text-white px-4 py-3 flex items-center justify-between sticky top-0 z-10">
        <h1 className="text-xl font-bold text-orange-400">NovaBazaar</h1>
        <button onClick={() => navigate(-1)} className="text-sm text-gray-300 hover:text-white flex items-center gap-1">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
          Back
        </button>
      </header>

      <main className="max-w-6xl mx-auto p-4">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="aspect-square bg-gray-50 rounded-lg overflow-hidden border">
              <img
                src={product.images?.[0] || 'https://via.placeholder.com/400'}
                alt={product.title}
                className="w-full h-full object-cover"
                onError={(e) => { e.target.src = 'https://via.placeholder.com/400?text=No+Image' }}
              />
            </div>

            <div className="flex flex-col">
              <h1 className="text-2xl font-bold text-gray-900 mb-1">{product.title}</h1>
              <p className="text-sm text-blue-600 hover:text-blue-800 cursor-pointer mb-3">{product.brand}</p>

              <div className="flex items-center gap-2 mb-4">
                <div className="flex">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <span key={star} className={`text-lg ${star <= Math.round(product.rating || 0) ? 'text-yellow-500' : 'text-gray-300'}`}>★</span>
                  ))}
                </div>
                <span className="text-sm text-blue-600">{product.rating} out of 5</span>
              </div>

              <hr className="my-4" />

              <div className="mb-4">
                <span className="text-3xl font-bold text-gray-900">₹{product.price?.toLocaleString()}</span>
                <span className="text-sm text-gray-500 ml-2">Inclusive of all taxes</span>
              </div>

              <p className="text-gray-700 mb-4 leading-relaxed">{product.description}</p>

              {product.attributes && Object.keys(product.attributes).length > 0 && (
                <div className="mb-4">
                  <h3 className="text-sm font-semibold text-gray-900 mb-2">Specifications</h3>
                  <div className="bg-gray-50 rounded p-3">
                    {Object.entries(product.attributes).map(([key, value]) => (
                      <div key={key} className="flex text-sm py-1">
                        <span className="text-gray-500 w-32 capitalize">{key}:</span>
                        <span className="text-gray-900 font-medium">{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {product.tags && product.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-6">
                  {product.tags.map((tag) => (
                    <span key={tag} className="px-3 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">{tag}</span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
