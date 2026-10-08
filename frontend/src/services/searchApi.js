const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8100'

export async function searchProducts(params = {}) {
  const queryParams = new URLSearchParams()
  if (params.q) queryParams.set('q', params.q)
  if (params.category) queryParams.set('category', params.category)
  if (params.brand) queryParams.set('brand', params.brand)
  if (params.minPrice) queryParams.set('minPrice', params.minPrice)
  if (params.maxPrice) queryParams.set('maxPrice', params.maxPrice)
  if (params.minRating) queryParams.set('minRating', params.minRating)
  if (params.page) queryParams.set('page', params.page)
  if (params.limit) queryParams.set('limit', params.limit)
  if (params.sort) queryParams.set('sort', params.sort)

  const url = `${API_BASE_URL}/api/search?${queryParams.toString()}`
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error(`Search failed: ${response.status}`)
  }

  return response.json()
}

export async function getSuggestions(q) {
  const url = `${API_BASE_URL}/api/search/suggestions?q=${encodeURIComponent(q)}`
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error(`Suggestions failed: ${response.status}`)
  }

  return response.json()
}
