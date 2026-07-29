import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { accountAPI, coursesAPI, projectsAPI } from '../services/api'
import FavoritesDashboardSection from '../components/FavoritesDashboardSection'
import { formatProjectLanguages } from '../utils/projectLanguages'
import './LearnerDashboard.css'

const computeCourseProgress = (courseId, projects, progressMap) => {
  const courseProjects = projects.filter(
    (project) => Number(project.course_id) === Number(courseId)
  )

  if (!courseProjects.length) return 0

  const completedCount = courseProjects.filter((project) => {
    const progress = progressMap[project.project_id] || progressMap[String(project.project_id)]
    return progress?.status === 'completed'
  }).length

  return Math.round((completedCount / courseProjects.length) * 100)
}

const LearnerDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null)
  const [myCourses, setMyCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)

      const [dashboardRes, coursesRes, progressRes, projectsRes] = await Promise.all([
        accountAPI.getLearnerDashboard(),
        coursesAPI.myCourses().catch(() => ({ data: { courses: [] } })),
        projectsAPI.getProgress().catch(() => ({ data: {} })),
        projectsAPI.list().catch(() => ({ data: { projects: [] } })),
      ])

      const courses = coursesRes.data.courses || []
      const progressMap = progressRes.data || {}
      const projects = projectsRes.data.projects || []

      const coursesWithProgress = courses.map((course) => ({
        ...course,
        progress_percentage: computeCourseProgress(course.id, projects, progressMap),
      }))

      const progressEntries = Object.values(progressMap)
      const completedProjects = progressEntries.filter(
        (item) => item?.status === 'completed'
      ).length
      const inProgressProjects = progressEntries.filter(
        (item) => item?.status && item.status !== 'completed' && item.status !== 'not_started'
      ).length

      const overallFromCourses =
        coursesWithProgress.length > 0
          ? Math.round(
              coursesWithProgress.reduce(
                (sum, course) => sum + (course.progress_percentage || 0),
                0
              ) / coursesWithProgress.length
            )
          : 0

      setMyCourses(coursesWithProgress)
      setDashboardData({
        ...dashboardRes.data,
        _overallProgress: overallFromCourses,
        _completedProjects: completedProjects,
        _inProgressProjects: inProgressProjects,
      })
    } catch (err) {
      setError('فشل تحميل بيانات لوحة التحكم')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="learner-dashboard">
        <div className="learner-dashboard-loading">
          <div className="spinner"></div>
          <p>جاري تحميل لوحة التحكم...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="learner-dashboard">
        <div className="container">
          <div className="alert alert-error">{error}</div>
        </div>
      </div>
    )
  }

  if (!dashboardData) {
    return null
  }

  const {
    dashboard_stats,
    learning_progress,
    recent_activity,
    suggested_projects,
  } = dashboardData

  const overallProgress =
    dashboardData._overallProgress ??
    learning_progress?.overall_progress_percentage ??
    0

  const completedCourses = myCourses.filter((course) => course.progress_percentage === 100).length
  const inProgressCourses = myCourses.filter(
    (course) => course.progress_percentage > 0 && course.progress_percentage < 100
  ).length
  const completedProjects =
    dashboardData._completedProjects ?? dashboard_stats?.completed_projects ?? 0
  const inProgressProjects =
    dashboardData._inProgressProjects ?? dashboard_stats?.in_progress_projects ?? 0

  return (
    <div className="learner-dashboard">
      <div className="container learner-dashboard-inner">
        <header className="learner-dashboard-header">
          <div className="learner-dashboard-header-copy">
            <p className="learner-dashboard-eyebrow">Buildly Learner</p>
            <h1>لوحة تحكم المتعلم</h1>
            <p>مرحباً بك في لوحة التحكم الخاصة بك</p>
          </div>
          <div className="learner-dashboard-header-actions">
            <Link to="/my-courses" className="learner-header-btn learner-header-btn-primary">
              مساراتي
            </Link>
            <Link to="/courses" className="learner-header-btn">
              تصفح المسارات
            </Link>
          </div>
        </header>

        {/* الإحصائيات */}
        <section className="learner-stats-grid" aria-label="الإحصائيات">
          <div className="learner-stat-card learner-stat-blue">
            <div className="learner-stat-icon">
              <span>📚</span>
            </div>
            <div className="learner-stat-content">
              <h3>{myCourses.length || dashboard_stats?.total_enrolled_projects || 0}</h3>
              <p>المسارات المنضم إليها</p>
            </div>
          </div>

          <div className="learner-stat-card learner-stat-green">
            <div className="learner-stat-icon">
              <span>✅</span>
            </div>
            <div className="learner-stat-content">
              <h3>{completedProjects}</h3>
              <p>المشاريع المكتملة</p>
            </div>
          </div>

          <div className="learner-stat-card learner-stat-amber">
            <div className="learner-stat-icon">
              <span>⏳</span>
            </div>
            <div className="learner-stat-content">
              <h3>{inProgressProjects}</h3>
              <p>المشاريع قيد التنفيذ</p>
            </div>
          </div>

          <div className="learner-stat-card learner-stat-purple">
            <div className="learner-stat-icon">
              <span>⏰</span>
            </div>
            <div className="learner-stat-content">
              <h3>{dashboard_stats?.total_hours_spent || 0}</h3>
              <p>ساعات التعلم</p>
            </div>
          </div>
        </section>

        {/* التقدم التعليمي — عرض كامل ومضغوط */}
        <section className="dashboard-card learner-panel learner-panel-wide learner-progress-panel">
          <div className="card-header">
            <h2>التقدم التعليمي</h2>
            <span className="learner-progress-trend">
              {learning_progress?.learning_trend || 'مستقر'}
            </span>
          </div>
          <div className="progress-overview">
            <div
              className="progress-circle"
              style={{ '--progress': `${overallProgress}%` }}
              aria-label={`معدل الإتمام ${overallProgress}%`}
            >
              <div className="progress-value">{overallProgress}%</div>
            </div>
            <div className="learner-progress-copy">
              <p className="learner-progress-title">معدل الإتمام الإجمالي</p>
              <p className="learner-progress-desc">
                ملخص تقدمك عبر المسارات المنضم إليها بناءً على إكمال المشاريع الفعلي.
              </p>
              <div className="learner-progress-meta">
                <span>{myCourses.length} مسار</span>
                <span>{completedCourses} مكتمل</span>
                <span>{inProgressCourses} قيد التنفيذ</span>
              </div>
            </div>
          </div>
        </section>

        <div className="learner-dashboard-grid">
          {/* مساراتي — نتائج حقيقية */}
          <section className="dashboard-card learner-panel learner-panel-wide">
            <div className="card-header">
              <h2>مساراتي</h2>
              <Link to="/my-courses" className="btn btn-secondary learner-view-all-btn">
                عرض الكل
              </Link>
            </div>
            <div className="projects-list">
              {myCourses.length > 0 ? (
                myCourses.slice(0, 5).map((course) => (
                  <Link
                    key={course.id}
                    to={`/courses/${course.id}`}
                    className="project-item learner-course-item"
                  >
                    <div className="project-info">
                      <h4>{course.title}</h4>
                      <p>
                        {course.description
                          ? `${course.description.substring(0, 120)}${
                              course.description.length > 120 ? '...' : ''
                            }`
                          : 'لا يوجد وصف'}
                      </p>
                      <div className="project-meta">
                        <span className="badge badge-info">{course.level_display}</span>
                        <span className="badge badge-warning">{course.category_display}</span>
                        <span className="badge">
                          {course.actual_projects_count ?? course.projects_count ?? 0} مشروع
                        </span>
                      </div>
                    </div>
                    <div className="project-progress">
                      <div className="progress-bar">
                        <div
                          className="progress-fill"
                          style={{ width: `${course.progress_percentage || 0}%` }}
                        ></div>
                      </div>
                      <span>{course.progress_percentage || 0}%</span>
                    </div>
                  </Link>
                ))
              ) : (
                <div className="empty-state learner-quiz-empty">
                  <p>لم تنضم لأي مسار بعد</p>
                  <Link to="/courses" className="btn btn-primary">
                    تصفح المسارات المتاحة
                  </Link>
                </div>
              )}
            </div>
          </section>

          {/* النشاطات الحديثة */}
          <section className="dashboard-card learner-panel learner-panel-wide">
            <div className="card-header">
              <h2>النشاطات الحديثة</h2>
            </div>
            <div className="activity-list">
              {recent_activity?.length > 0 ? (
                recent_activity.map((activity) => (
                  <div key={activity.id} className="activity-item">
                    <div className="activity-icon">{activity.icon}</div>
                    <div className="activity-content">
                      <p>{activity.action}</p>
                      <span>{activity.project}</span>
                    </div>
                    <span className="activity-time">
                      {new Date(activity.timestamp).toLocaleString('ar-SY', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                  </div>
                ))
              ) : (
                <p className="empty-state">
                  لا توجد نشاطات مسجلة بعد — ابدأ مشروعاً ليظهر نشاطك هنا
                </p>
              )}
            </div>
          </section>

          <div className="learner-panel-wide">
            <FavoritesDashboardSection />
          </div>

          {/* المشاريع المقترحة */}
          <section className="dashboard-card learner-panel learner-panel-wide">
            <div className="card-header">
              <h2>مشاريع مقترحة</h2>
            </div>

            {!dashboardData?.user_profile?.is_rated ? (
              <div className="empty-state learner-quiz-empty">
                <p>
                  انضم لمسار Frontend Mastery أو Python لإجراء اختبار تحديد المستوى
                  المتكيف والحصول على مشاريع مناسبة لك
                </p>
                <Link to="/courses" className="btn btn-primary">
                  تصفح المسارات
                </Link>
              </div>
            ) : suggested_projects?.length > 0 ? (
              <div className="suggested-projects">
                {suggested_projects.map((project) => {
                  const projectId = project.project_id || project.id
                  const description = project.description || ''
                  const shortDescription =
                    description.length > 80
                      ? `${description.substring(0, 80)}...`
                      : description

                  return (
                    <Link
                      key={projectId}
                      to={`/projects/${projectId}`}
                      className="suggested-project-card"
                    >
                      <div className="suggested-project-image-wrap">
                        {project.image ? (
                          <img
                            src={project.image}
                            alt={project.title}
                            className="suggested-project-image"
                          />
                        ) : (
                          <div className="suggested-project-image-placeholder">
                            <span>{project.title?.charAt(0)}</span>
                          </div>
                        )}
                      </div>

                      <div className="suggested-project-body">
                        <h4>{project.title}</h4>

                        <div className="suggested-project-badges">
                          <span className="badge badge-info">
                            {project.level_display || project.difficulty}
                          </span>
                          <span className="badge badge-warning">
                            {formatProjectLanguages(project) || project.category}
                          </span>
                        </div>

                        {shortDescription ? <p>{shortDescription}</p> : null}

                        <div className="suggested-project-meta">
                          <div className="suggested-meta-item">
                            <span className="suggested-meta-label">المسار</span>
                            <span className="suggested-meta-value">
                              {project.course_title || '—'}
                            </span>
                          </div>
                          <div className="suggested-meta-item">
                            <span className="suggested-meta-label">الوقت</span>
                            <span className="suggested-meta-value">
                              {project.estimated_time
                                ? `${project.estimated_time} ساعة`
                                : '—'}
                            </span>
                          </div>
                        </div>

                        <span className="suggested-project-cta">عرض التفاصيل</span>
                      </div>
                    </Link>
                  )
                })}
              </div>
            ) : (
              <p className="empty-state">لا توجد مشاريع مناسبة حالياً</p>
            )}
          </section>
        </div>
      </div>
    </div>
  )
}

export default LearnerDashboard
