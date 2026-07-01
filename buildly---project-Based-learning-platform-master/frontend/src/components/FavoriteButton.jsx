import React, { useState } from 'react'
import { accountAPI } from '../services/api'
import './FavoriteButton.css'

const FavoriteButton = ({
  itemType,
  objectId,
  initialFavorite = false,
  onToggle,
  label = 'مفضلة',
}) => {
  const [isFavorite, setIsFavorite] = useState(initialFavorite)
  const [loading, setLoading] = useState(false)

  const handleToggle = async (event) => {
    event.preventDefault()
    event.stopPropagation()

    if (loading) return

    try {
      setLoading(true)
      const response = await accountAPI.toggleFavorite({
        item_type: itemType,
        object_id: objectId,
      })
      const nextValue = Boolean(response.data.is_favorite)
      setIsFavorite(nextValue)
      onToggle?.(nextValue, itemType, objectId)
    } catch (err) {
      const message =
        err.response?.data?.message || 'تعذر تحديث المفضلة'
      alert(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <button
      type="button"
      className={`favorite-btn ${isFavorite ? 'is-favorite' : ''}`}
      onClick={handleToggle}
      disabled={loading}
      aria-pressed={isFavorite}
      title={isFavorite ? 'إزالة من المفضلة' : 'إضافة إلى المفضلة'}
    >
      <span className="favorite-icon">{isFavorite ? '★' : '☆'}</span>
      <span className="favorite-label">{label}</span>
    </button>
  )
}

export default FavoriteButton
