import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { coursesAPI, accountAPI } from '../services/api'
import ArchiveCourseModal from '../components/ArchiveCourseModal'
import FavoriteButton from '../components/FavoriteButton'
import './Courses.css'

const CoursesList = () => {
  const { isAdmin } = useAuth()
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [archiveCourse, setArchiveCourse] = useState(null)
  const [favoriteCourseIds, setFavoriteCourseIds] = useState(new Set())

  useEffect(() => {
    fetchCourses()
  }, [])

  const fetchCourses = async () => {
    try {
      setLoading(true)
      const [coursesRes, favoritesRes] = await Promise.all([
        coursesAPI.list(),
        accountAPI.getFavorites().catch(() => ({ data: { favorite_course_ids: [] } })),
      ])

      const courses = coursesRes.data.courses || []
      setCourses(courses)
      setFavoriteCourseIds(new Set(favoritesRes.data.favorite_course_ids || []))
    } catch (err) {
      setError('فشل تحميل المسارات')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('هل أنت متأكد من حذف هذا المسار؟')) {
      return
    }

    try {
      await coursesAPI.delete(id)
      setCourses(courses.filter((course) => course.id !== id))
    } catch (err) {
      alert('فشل حذف المسار')
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

  const handleArchiveClose = () => {
    setArchiveCourse(null)
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
    <div className="container">
      {archiveCourse && (
        <ArchiveCourseModal
          course={archiveCourse}
          onClose={handleArchiveClose}
          onSuccess={fetchCourses}
        />
      )}

      <div className="page-header">
        <h1>المسارات التعليمية</h1>
        {isAdmin && (
          <Link to="/courses/create" className="btn btn-primary">
            إضافة مسار جديد
          </Link>
        )}
      </div>

      {courses.length === 0 ? (
        <div className="empty-state">
          <p>لا توجد مسارات متاحة</p>
          {isAdmin && (
            <Link to="/courses/create" className="btn btn-primary">
              إنشاء أول مسار
            </Link>
          )}
        </div>
      ) : (
        <div className="courses-grid">
          {courses.map((course) => (
            <div key={course.id} className="course-card">
              <div className="course-header">
                <div className="course-header-top">
                  <h3>{course.title}</h3>
                  <FavoriteButton
                    itemType="course"
                    objectId={course.id}
                    initialFavorite={favoriteCourseIds.has(course.id)}
                    onToggle={handleFavoriteToggle}
                    label="مفضلة"
                  />
                </div>
                <div className="course-badges">
                  <span className="badge badge-info">{course.level_display}</span>
                  <span className="badge badge-warning">{course.category_display}</span>
                </div>
              </div>
              <p className="course-description">
                {course.description?.substring(0, 150)}...
              </p>
              <div className="course-meta">
                <div className="meta-item">
                  <span className="meta-label">المدة:</span>
                  <span className="meta-value">{course.estimated_duration} ساعة</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">المشاريع:</span>
                  <span className="meta-value">{course.projects_count || 0}</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">المتعلمين:</span>
                  <span className="meta-value">{course.enrolled_students_count || 0}</span>
                </div>
              </div>
              <div className="course-actions">
                <Link to={`/courses/${course.id}`} className="btn btn-primary">
                  عرض التفاصيل
                </Link>
                {isAdmin && (
                  <>
                    <Link
                      to={`/courses/${course.id}/edit`}
                      className="btn btn-secondary"
                    >
                      تعديل
                    </Link>
                    <button
                      onClick={() => setArchiveCourse(course)}
                      className="btn btn-warning"
                    >
                      أرشفة
                    </button>
                    <button
                      onClick={() => handleDelete(course.id)}
                      className="btn btn-danger"
                    >
                      حذف
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default CoursesList

