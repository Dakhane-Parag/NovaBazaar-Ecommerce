export default function ProductFilters({ category, brand, onCategoryChange, onBrandChange }) {
  const categories = [
    { value: '', label: 'All Categories' },
    { value: 'electronics', label: 'Electronics' },
    { value: 'fashion', label: 'Fashion' },
    { value: 'home-kitchen', label: 'Home & Kitchen' },
    { value: 'beauty', label: 'Beauty' },
    { value: 'fitness', label: 'Fitness' },
  ]

  const brands = [
    { value: '', label: 'All Brands' },
    { value: 'Apple', label: 'Apple' },
    { value: 'Samsung', label: 'Samsung' },
    { value: 'Sony', label: 'Sony' },
    { value: 'Nike', label: 'Nike' },
    { value: 'Adidas', label: 'Adidas' },
    { value: 'Dell', label: 'Dell' },
    { value: 'HP', label: 'HP' },
    { value: 'Lenovo', label: 'Lenovo' },
    { value: 'ASUS', label: 'ASUS' },
    { value: 'JBL', label: 'JBL' },
    { value: 'Logitech', label: 'Logitech' },
    { value: 'Anker', label: 'Anker' },
    { value: 'GoPro', label: 'GoPro' },
    { value: 'Bose', label: 'Bose' },
    { value: 'Prestige', label: 'Prestige' },
    { value: 'Wakefit', label: 'Wakefit' },
    { value: 'Borosil', label: 'Borosil' },
    { value: 'Milton', label: 'Milton' },
    { value: 'IKEA', label: 'IKEA' },
    { value: 'Calvin Klein', label: 'Calvin Klein' },
    { value: 'Lakme', label: 'Lakme' },
    { value: 'Minimalist', label: 'Minimalist' },
    { value: 'Philips', label: 'Philips' },
  ]

  return (
    <div className="flex items-center gap-3">
      <select
        value={category}
        onChange={(e) => onCategoryChange(e.target.value)}
        className="bg-gray-800 text-white border border-gray-700 rounded px-3 py-1.5 text-sm"
        aria-label="Filter by category"
      >
        {categories.map((c) => (
          <option key={c.value} value={c.value}>{c.label}</option>
        ))}
      </select>
      <select
        value={brand}
        onChange={(e) => onBrandChange(e.target.value)}
        className="bg-gray-800 text-white border border-gray-700 rounded px-3 py-1.5 text-sm"
        aria-label="Filter by brand"
      >
        {brands.map((b) => (
          <option key={b.value} value={b.value}>{b.label}</option>
        ))}
      </select>
    </div>
  )
}
