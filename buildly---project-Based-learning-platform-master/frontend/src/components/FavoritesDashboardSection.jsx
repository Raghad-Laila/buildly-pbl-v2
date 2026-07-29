import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { accountAPI } from '../services/api'
import './FavoriteButton.css'

const FavoritesDashboardSection = () => {
  const [favorites, setFavorites] = useState({ courses: [], projects: [] })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchFavorites()
  }, [])

  const fetchFavorites = async () => {
    try {
      setLoading(true)
      const response = await accountAPI.getFavorites()
      setFavorites({
        courses: response.data.courses || [],
        projects: response.data.projects || [],
      })
    } catch (err) {
      console.error('Error fetching favorites:', err)
    } finally {
      setLoading(false)
    }
  }

  const totalCount = favorites.courses.length + favorites.projects.length

  const formatDate = (value) => {
    if (!value) return '—'
    return new Date(value).toLocaleString('ar-SY', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  if (loading) {
    return (
      <div className="dashboard-card favorites-card">
        <div className="card-header">
          <h2>المفضلة</h2>
        </div>
        <p className="empty-state">جاري تحميل المفضلة...</p>
      </div>
    )
  }

  return (
    <div className="dashboard-card favorites-card">
      <div className="card-header">
        <h2>المفضلة</h2>
        <span className="favorites-count-badge">{totalCount}</span>
      </div>

      <p className="favorites-section-note">
        المسارات والمشاريع التي حددتها كمفضلة — تُحدَّث تلقائياً من قاعدة البيانات.
      </p>

      {totalCount === 0 ? (
        <p className="empty-state">لم تضف أي مسار أو مشروع للمفضلة بعد</p>
      ) : (
        <div className="items-list">
          {favorites.courses.map((course) => (
            <Link
              key={`course-${course.id}`}
              to={`/courses/${course.id}`}
              className="list-item"
            >
              <div className="item-info">
                <h4>{course.title}</h4>
                <p>{course.description?.substring(0, 80)}...</p>
                <div className="item-meta">
                  <span className="badge badge-favorite">مسار مفضل</span>
                  <span className="badge">{course.category_display}</span>
                </div>
              </div>
              <div className="item-stats">
                <span>{course.projects_count || 0} مشروع</span>
                <span className="archived-date">{formatDate(course.favorited_at)}</span>
              </div>
            </Link>
          ))}

          {favorites.projects.map((project) => (
            <Link
              key={`project-${project.project_id}`}
              to={`/projects/${project.project_id}`}
              className="list-item"
            >
              <div className="item-info">
                <h4>{project.title}</h4>
                <p>{project.description?.substring(0, 80)}...</p>
                <div className="item-meta">
                  <span className="badge badge-favorite">مشروع مفضل</span>
                  <span className="badge">{project.level_display}</span>
                  <span className="badge">{project.language_display}</span>
                </div>
              </div>
              <div className="item-stats">
                <span>{project.course_title}</span>
                <span className="archived-date">{formatDate(project.favorited_at)}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default FavoritesDashboardSection
