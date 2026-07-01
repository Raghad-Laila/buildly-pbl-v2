import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { coursesAPI, projectsAPI, accountAPI } from '../services/api'
import FavoritesDashboardSection from '../components/FavoritesDashboardSection'
import './Dashboard.css'

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalCourses: 0,
    totalProjects: 0,
    totalLearners: 0,
    activeCourses: 0,
  })
  const [recentCourses, setRecentCourses] = useState([])
  const [recentProjects, setRecentProjects] = useState([])
  const [archivedCourses, setArchivedCourses] = useState([])
  const [favoritesCount, setFavoritesCount] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const [coursesRes, projectsRes, archivedRes, favoritesRes] = await Promise.all([
        coursesAPI.list(),
        projectsAPI.list(),
        coursesAPI.listArchived().catch(() => ({ data: { archived_courses: [] } })),
        accountAPI.getFavorites().catch(() => ({ data: { count: 0 } })),
      ])

      const courses = coursesRes.data.courses || []
      const projects = projectsRes.data.projects || []
      const archived = archivedRes.data.archived_courses || []

      setStats({
        totalCourses: courses.length,
        totalProjects: projects.length,
        totalLearners: courses.reduce((sum, course) => sum + (course.enrolled_students_count || 0), 0),
        activeCourses: courses.filter((c) => c.is_active).length,
      })

      setRecentCourses(courses.slice(0, 5))
      setRecentProjects(projects.slice(0, 5))
      setArchivedCourses(archived)
      setFavoritesCount(favoritesRes.data.count || 0)
    } catch (err) {
      console.error('Error fetching dashboard data:', err)
    } finally {
      setLoading(false)
    }
  }

  const formatArchiveDate = (value) => {
    if (!value) return '—'
    return new Date(value).toLocaleString('ar-SY', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="dashboard-header">
        <h1>لوحة تحكم المشرف</h1>
        <p>إدارة المسارات والمشاريع التعليمية</p>
      </div>

      {/* الإحصائيات */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#dbeafe' }}>
            <span style={{ color: '#3b82f6' }}>📚</span>
          </div>
          <div className="stat-content">
            <h3>{stats.totalCourses}</h3>
            <p>إجمالي المسارات</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#d1fae5' }}>
            <span style={{ color: '#10b981' }}>✅</span>
          </div>
          <div className="stat-content">
            <h3>{stats.activeCourses}</h3>
            <p>المسارات النشطة</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#fef3c7' }}>
            <span style={{ color: '#f59e0b' }}>📋</span>
          </div>
          <div className="stat-content">
            <h3>{stats.totalProjects}</h3>
            <p>إجمالي المشاريع</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#e9d5ff' }}>
            <span style={{ color: '#8b5cf6' }}>👥</span>
          </div>
          <div className="stat-content">
            <h3>{stats.totalLearners}</h3>
            <p>إجمالي المتعلمين</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#ffedd5' }}>
            <span style={{ color: '#ea580c' }}>🗄️</span>
          </div>
          <div className="stat-content">
            <h3>{archivedCourses.length}</h3>
            <p>المسارات المؤرشفة</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#fef3c7' }}>
            <span style={{ color: '#d97706' }}>★</span>
          </div>
          <div className="stat-content">
            <h3>{favoritesCount}</h3>
            <p>المفضلة</p>
          </div>
        </div>
      </div>

      <div className="dashboard-grid">
        {/* الإجراءات السريعة */}
        <div className="dashboard-card">
          <div className="card-header">
            <h2>الإجراءات السريعة</h2>
          </div>
          <div className="quick-actions">
            <Link to="/courses/create" className="action-btn">
              <span className="action-icon">➕</span>
              <span>إضافة مسار جديد</span>
            </Link>
            <Link to="/projects/create" className="action-btn">
              <span className="action-icon">📝</span>
              <span>إضافة مشروع جديد</span>
            </Link>
            <Link to="/courses" className="action-btn">
              <span className="action-icon">📚</span>
              <span>عرض جميع المسارات</span>
            </Link>
            <Link to="/projects" className="action-btn">
              <span className="action-icon">📋</span>
              <span>عرض جميع المشاريع</span>
            </Link>
          </div>
        </div>

        {/* المسارات الحديثة */}
        <div className="dashboard-card">
          <div className="card-header">
            <h2>المسارات الحديثة</h2>
            <Link to="/courses" className="btn btn-secondary">
              عرض الكل
            </Link>
          </div>
          <div className="items-list">
            {recentCourses.length > 0 ? (
              recentCourses.map((course) => (
                <Link
                  key={course.id}
                  to={`/courses/${course.id}`}
                  className="list-item"
                >
                  <div className="item-info">
                    <h4>{course.title}</h4>
                    <p>{course.description?.substring(0, 60)}...</p>
                    <div className="item-meta">
                      <span className="badge">{course.level_display}</span>
                      <span className="badge">{course.category_display}</span>
                    </div>
                  </div>
                  <div className="item-stats">
                    <span>{course.projects_count || 0} مشروع</span>
                    <span>{course.enrolled_students_count || 0} متعلم</span>
                  </div>
                </Link>
              ))
            ) : (
              <p className="empty-state">لا توجد مسارات</p>
            )}
          </div>
        </div>

        {/* المشاريع الحديثة */}
        <div className="dashboard-card">
          <div className="card-header">
            <h2>المشاريع الحديثة</h2>
            <Link to="/projects" className="btn btn-secondary">
              عرض الكل
            </Link>
          </div>
          <div className="items-list">
            {recentProjects.length > 0 ? (
              recentProjects.map((project) => (
                <Link
                  key={project.project_id}
                  to={`/projects/${project.project_id}`}
                  className="list-item"
                >
                  <div className="item-info">
                    <h4>{project.title}</h4>
                    <p>{project.description?.substring(0, 60)}...</p>
                    <div className="item-meta">
                      <span className="badge">{project.level_display}</span>
                      <span className="badge">{project.language_display}</span>
                    </div>
                  </div>
                  <div className="item-stats">
                    <span>{project.estimated_time} ساعة</span>
                  </div>
                </Link>
              ))
            ) : (
              <p className="empty-state">لا توجد مشاريع</p>
            )}
          </div>
        </div>

        {/* المسارات المؤرشفة */}
        <div className="dashboard-card archived-courses-card">
          <div className="card-header">
            <h2>المسارات المؤرشفة</h2>
            <span className="archive-count-badge">{archivedCourses.length}</span>
          </div>
          <p className="archived-section-note">
            قائمة ديناميكية من قاعدة البيانات — تتحدّث تلقائياً بعد كل أرشفة.
          </p>
          <div className="items-list">
            {archivedCourses.length > 0 ? (
              archivedCourses.map((course) => (
                <div key={course.course_id} className="list-item archived-list-item">
                  <div className="item-info">
                    <h4>{course.title}</h4>
                    <p>{course.description?.substring(0, 80)}...</p>
                    <div className="item-meta">
                      <span className="badge">{course.level_display}</span>
                      <span className="badge">{course.category_display}</span>
                      <span className="badge badge-archive">مؤرشف</span>
                    </div>
                  </div>
                  <div className="item-stats archived-item-stats">
                    <span>{course.projects_count || 0} مشروع</span>
                    <span>{course.enrolled_students_count || 0} متعلم</span>
                    <span className="archived-date">
                      أرشفه: {course.archived_by || '—'}
                    </span>
                    <span className="archived-date">
                      {formatArchiveDate(course.archived_at)}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p className="empty-state">لا توجد مسارات مؤرشفة حالياً</p>
            )}
          </div>
        </div>

        <FavoritesDashboardSection />
      </div>
    </div>
  )
}

export default AdminDashboard

