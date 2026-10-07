import { useState, useEffect, useCallback } from 'react'
import { useSearchParams } from 'react-router-dom'
import { getProducts } from '../services/productApi'

export function useProducts() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [products, setProducts] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const page = parseInt(searchParams.get('page') || '1', 10)
  const limit = 12
  const category = searchParams.get('category') || ''
  const brand = searchParams.get('brand') || ''
  const sort = searchParams.get('sort') || 'price_asc'

  const fetchProducts = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getProducts({ page, limit, category, brand, sort })
      setProducts(data.items || [])
      setTotal(data.total || 0)
    } catch (e) {
      setError(e.message || 'Failed to load products')
    } finally {
      setLoading(false)
    }
  }, [page, limit, category, brand, sort])

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  const updateParams = useCallback((updates) => {
    const params = new URLSearchParams(searchParams)
    Object.entries(updates).forEach(([key, value]) => {
      if (value === '' || value === null || value === undefined) {
        params.delete(key)
      } else {
        params.set(key, value)
      }
    })
    setSearchParams(params)
  }, [searchParams, setSearchParams])

  const totalPages = Math.ceil(total / limit)

  const handleCategoryChange = (newCategory) => {
    updateParams({ category: newCategory, page: '1' })
  }

  const handleBrandChange = (newBrand) => {
    updateParams({ brand: newBrand, page: '1' })
  }

  const handleSortChange = (newSort) => {
    updateParams({ sort: newSort, page: '1' })
  }

  const handlePageChange = (newPage) => {
    updateParams({ page: String(newPage) })
  }

  const resetFilters = () => {
    setSearchParams(new URLSearchParams())
  }

  return {
    products,
    total,
    page,
    limit,
    totalPages,
    category,
    brand,
    sort,
    loading,
    error,
    handleCategoryChange,
    handleBrandChange,
    handleSortChange,
    handlePageChange,
    resetFilters,
    refetch: fetchProducts,
  }
}
