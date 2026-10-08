const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8100'

export async function getProducts(params = {}) {
  const queryParams = new URLSearchParams()
  if (params.page) queryParams.set('page', params.page)
  if (params.limit) queryParams.set('limit', params.limit)
  if (params.category) queryParams.set('category', params.category)
  if (params.brand) queryParams.set('brand', params.brand)
  if (params.sort) queryParams.set('sort', params.sort)

  const url = `${API_BASE_URL}/api/products?${queryParams.toString()}`
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error(`Failed to fetch products: ${response.status}`)
  }

  return response.json()
}

export async function getProductById(productId) {
  const url = `${API_BASE_URL}/api/products/${productId}`
  const response = await fetch(url)

  if (response.status === 404) {
    throw new Error('Product not found')
  }

  if (!response.ok) {
    throw new Error(`Failed to fetch product: ${response.status}`)
  }

  return response.json()
}
