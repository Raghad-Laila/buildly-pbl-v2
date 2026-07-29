import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { coursesAPI, accountAPI } from '../services/api'
import ArchiveCourseModal from '../components/ArchiveCourseModal'
import LearnerCourseCard from '../components/LearnerCourseCard'
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
    <div className={`container ${!isAdmin ? 'learner-courses-page' : ''}`}>
      {archiveCourse && (
        <ArchiveCourseModal
          course={archiveCourse}
          onClose={handleArchiveClose}
          onSuccess={fetchCourses}
        />
      )}

      {isAdmin ? (
        <div className="page-header">
          <h1>المسارات التعليمية</h1>
          <Link to="/courses/create" className="btn btn-primary">
            إضافة مسار جديد
          </Link>
        </div>
      ) : (
        <header className="learner-courses-header">
          <div className="learner-courses-header-copy">
            <p className="learner-courses-eyebrow">Buildly Learner</p>
            <h1>المسارات التعليمية</h1>
            <p>
              اكتشف رحلة تعلم متكاملة مصممة لنقلك من الصفر إلى الاحتراف في مجالات
              التكنولوجيا الأكثر طلباً.
            </p>
          </div>
          <div className="learner-courses-header-actions">
            <Link to="/my-courses" className="learner-courses-btn learner-courses-btn-primary">
              مساراتي
            </Link>
            <Link to="/dashboard" className="learner-courses-btn">
              لوحة التحكم
            </Link>
          </div>
        </header>
      )}

      {courses.length === 0 ? (
        <div className="empty-state">
          <p>لا توجد مسارات متاحة</p>
          {isAdmin && (
            <Link to="/courses/create" className="btn btn-primary">
              إنشاء أول مسار
            </Link>
          )}
        </div>
      ) : isAdmin ? (
        <div className="learner-courses-grid">
          {courses.map((course) => (
            <LearnerCourseCard
              key={course.id}
              course={course}
              isFavorite={favoriteCourseIds.has(course.id)}
              onFavoriteToggle={handleFavoriteToggle}
              actions={
                <>
                  <Link to={`/courses/${course.id}`} className="learner-course-card-cta">
                    عرض التفاصيل
                  </Link>
                  <Link
                    to={`/courses/${course.id}/edit`}
                    className="learner-course-card-btn learner-course-card-btn-secondary"
                  >
                    تعديل
                  </Link>
                  <button
                    type="button"
                    onClick={() => setArchiveCourse(course)}
                    className="learner-course-card-btn learner-course-card-btn-warning"
                  >
                    أرشفة
                  </button>
                  <button
                    type="button"
                    onClick={() => handleDelete(course.id)}
                    className="learner-course-card-btn learner-course-card-btn-danger"
                  >
                    حذف
                  </button>
                </>
              }
            />
          ))}
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

export default CoursesList

