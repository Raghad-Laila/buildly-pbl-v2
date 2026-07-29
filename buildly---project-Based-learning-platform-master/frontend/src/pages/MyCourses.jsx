import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { coursesAPI, accountAPI } from '../services/api'
import LearnerCourseCard from '../components/LearnerCourseCard'
import './Courses.css'

const MyCourses = () => {
  const [courses, setCourses] = useState([])
  const [favoriteCourseIds, setFavoriteCourseIds] = useState(new Set())
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchMyCourses()
  }, [])

  const fetchMyCourses = async () => {
    try {
      setLoading(true)
      const [coursesRes, favoritesRes] = await Promise.all([
        coursesAPI.myCourses(),
        accountAPI.getFavorites().catch(() => ({ data: { favorite_course_ids: [] } })),
      ])
      setCourses(coursesRes.data.courses || [])
      setFavoriteCourseIds(new Set(favoritesRes.data.favorite_course_ids || []))
    } catch (err) {
      setError('فشل تحميل مساراتك')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleFavoriteToggle = (isFavorite, _itemType, objectId) => {
    setFavoriteCourseIds((prev) => {
      const next = new Set(prev)
      if (isFavorite) {
        next.add(objectId)
      } else {
        next.delete(objectId)
      }
      return next
    })
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  if (error) {
    return <div className="alert alert-error">{error}</div>
  }

  return (
    <div className="container learner-courses-page">
      <div className="page-header">
        <h1>مساراتي</h1>
        <Link to="/courses" className="btn btn-secondary">
          استكشف المزيد
        </Link>
      </div>

      {courses.length === 0 ? (
        <div className="empty-state">
          <p>لم تنضم لأي مسار بعد</p>
          <Link to="/courses" className="btn btn-primary">
            تصفح المسارات المتاحة
          </Link>
        </div>
      ) : (
        <div className="learner-courses-grid">
          {courses.map((course) => (
            <LearnerCourseCard
              key={course.id}
              course={course}
              isFavorite={favoriteCourseIds.has(course.id)}
              onFavoriteToggle={handleFavoriteToggle}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default MyCourses
