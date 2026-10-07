export default function SortDropdown({ value, onChange }) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="bg-gray-800 text-white border border-gray-700 rounded px-3 py-1.5 text-sm"
      aria-label="Sort products"
    >
      <option value="price_asc">Price: Low to High</option>
      <option value="price_desc">Price: High to Low</option>
      <option value="rating_desc">Rating: High to Low</option>
    </select>
  )
}
