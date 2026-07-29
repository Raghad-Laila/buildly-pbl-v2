import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { coursesAPI, projectsAPI, accountAPI } from '../services/api'
import FavoritesDashboardSection from '../components/FavoritesDashboardSection'
import './AdminDashboard.css'

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
      <div className="admin-dashboard">
        <div className="admin-dashboard-loading">
          <div className="spinner"></div>
          <p>جاري تحميل لوحة التحكم...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="admin-dashboard">
      <div className="container admin-dashboard-inner">
        <header className="admin-dashboard-header">
          <div className="admin-dashboard-header-copy">
            <p className="admin-dashboard-eyebrow">Buildly Admin</p>
            <h1>لوحة تحكم المشرف</h1>
            <p>إدارة المسارات والمشاريع التعليمية</p>
          </div>
          <div className="admin-dashboard-header-actions">
            <Link to="/courses/create" className="admin-header-btn admin-header-btn-primary">
              إضافة مسار
            </Link>
            <Link to="/projects/create" className="admin-header-btn">
              إضافة مشروع
            </Link>
          </div>
        </header>

        {/* الإحصائيات */}
        <section className="admin-stats-grid" aria-label="الإحصائيات">
          <div className="admin-stat-card admin-stat-blue">
            <div className="admin-stat-icon">
              <span>📚</span>
            </div>
            <div className="admin-stat-content">
              <h3>{stats.totalCourses}</h3>
              <p>إجمالي المسارات</p>
            </div>
          </div>

          <div className="admin-stat-card admin-stat-green">
            <div className="admin-stat-icon">
              <span>✅</span>
            </div>
            <div className="admin-stat-content">
              <h3>{stats.activeCourses}</h3>
              <p>المسارات النشطة</p>
            </div>
          </div>

          <div className="admin-stat-card admin-stat-amber">
            <div className="admin-stat-icon">
              <span>📋</span>
            </div>
            <div className="admin-stat-content">
              <h3>{stats.totalProjects}</h3>
              <p>إجمالي المشاريع</p>
            </div>
          </div>

          <div className="admin-stat-card admin-stat-purple">
            <div className="admin-stat-icon">
              <span>👥</span>
            </div>
            <div className="admin-stat-content">
              <h3>{stats.totalLearners}</h3>
              <p>إجمالي المتعلمين</p>
            </div>
          </div>

          <div className="admin-stat-card admin-stat-orange">
            <div className="admin-stat-icon">
              <span>🗄️</span>
            </div>
            <div className="admin-stat-content">
              <h3>{archivedCourses.length}</h3>
              <p>المسارات المؤرشفة</p>
            </div>
          </div>

          <div className="admin-stat-card admin-stat-gold">
            <div className="admin-stat-icon">
              <span>★</span>
            </div>
            <div className="admin-stat-content">
              <h3>{favoritesCount}</h3>
              <p>المفضلة</p>
            </div>
          </div>
        </section>

        <div className="admin-dashboard-grid">
          {/* الإجراءات السريعة */}
          <section className="dashboard-card admin-panel admin-panel-actions">
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
          </section>

          {/* المسارات الحديثة */}
          <section className="dashboard-card admin-panel">
            <div className="card-header">
              <h2>المسارات الحديثة</h2>
              <Link to="/courses" className="btn btn-secondary admin-view-all-btn">
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
          </section>

          {/* المشاريع الحديثة */}
          <section className="dashboard-card admin-panel">
            <div className="card-header">
              <h2>المشاريع الحديثة</h2>
              <Link to="/projects" className="btn btn-secondary admin-view-all-btn">
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
          </section>

          {/* المسارات المؤرشفة */}
          <section className="dashboard-card archived-courses-card admin-panel admin-panel-wide">
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
          </section>

          <div className="admin-panel-wide">
            <FavoritesDashboardSection />
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
