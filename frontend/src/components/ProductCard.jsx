import { Link } from 'react-router-dom'

export default function ProductCard({ product }) {
  return (
    <Link
      to={`/products/${product.id}`}
      className="bg-white rounded-lg shadow-sm hover:shadow-lg transition-all p-3 flex flex-col group block"
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
      <p className="text-xs text-gray-400 mb-1">{product.category}</p>
      <div className="flex items-center gap-1 mb-2">
        <span className="text-yellow-500 text-sm">{'★'.repeat(Math.round(product.rating || 0))}</span>
        <span className="text-xs text-gray-400">({product.rating})</span>
      </div>
      <div className="mt-auto">
        <span className="text-lg font-bold text-gray-900">₹{product.price?.toLocaleString()}</span>
      </div>
    </Link>
  )
}
