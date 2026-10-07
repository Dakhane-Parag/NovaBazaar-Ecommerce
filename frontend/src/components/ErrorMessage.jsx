export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <p className="text-red-500 text-lg mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-gray-900 text-white rounded hover:bg-gray-700 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  )
}
