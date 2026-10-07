import { useProducts } from '../hooks/useProducts'
import ProductGrid from '../components/ProductGrid'
import ProductFilters from '../components/ProductFilters'
import SortDropdown from '../components/SortDropdown'
import Pagination from '../components/Pagination'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

export default function ProductsPage() {
  const {
    products,
    total,
    page,
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
    refetch,
  } = useProducts()

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gray-900 text-white px-4 py-3 flex items-center justify-between sticky top-0 z-10">
        <h1 className="text-xl font-bold text-orange-400">NovaBazaar</h1>
        <div className="flex items-center gap-3">
          <ProductFilters
            category={category}
            brand={brand}
            onCategoryChange={handleCategoryChange}
            onBrandChange={handleBrandChange}
          />
          <SortDropdown value={sort} onChange={handleSortChange} />
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-4">
        {loading && <LoadingSpinner />}
        {error && <ErrorMessage message={error} onRetry={refetch} />}

        {!loading && !error && products.length === 0 && (
          <div className="flex flex-col items-center justify-center py-20">
            <p className="text-gray-500 text-lg mb-4">No products found</p>
            <button
              onClick={resetFilters}
              className="px-4 py-2 bg-gray-900 text-white rounded hover:bg-gray-700 transition-colors"
            >
              Reset Filters
            </button>
          </div>
        )}

        {!loading && !error && products.length > 0 && (
          <>
            <ProductGrid products={products} />
            <Pagination
              page={page}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          </>
        )}
      </main>
    </div>
  )
}
