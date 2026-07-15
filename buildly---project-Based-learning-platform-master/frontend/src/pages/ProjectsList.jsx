import React, { useState, useEffect } from 'react'
import { Link, useSearchParams, useParams } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { projectsAPI, accountAPI } from '../services/api'
import FavoriteButton from '../components/FavoriteButton'
import { formatProjectLanguages } from '../utils/projectLanguages'
import './Projects.css'

const ProjectsList = () => {
  const { isAdmin, isLearner } = useAuth()
  const { courseId: routeCourseId } = useParams()
  const [searchParams] = useSearchParams()
  const courseId = routeCourseId || searchParams.get('course_id')
  const [projects, setProjects] = useState([])
  const [courseInfo, setCourseInfo] = useState(null)
  const [initialLoading, setInitialLoading] = useState(true)
  const [searching, setSearching] = useState(false)
  const [error, setError] = useState('')
  const [progress, setProgress] = useState({})
  const [levelFilter, setLevelFilter] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [favoriteProjectIds, setFavoriteProjectIds] = useState(new Set())

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchQuery.trim())
    }, 350)

    return () => clearTimeout(timer)
  }, [searchQuery])

  useEffect(() => {
    fetchProjects()
  }, [courseId, debouncedSearch])

  const fetchProjects = async () => {
    const isFirstLoad = initialLoading

    try {
      if (isFirstLoad) {
        setInitialLoading(true)
      } else {
        setSearching(true)
      }

      const progressPromise = isAdmin
        ? Promise.resolve({ data: {} })
        : projectsAPI.getProgress()
      const favoritesPromise = accountAPI.getFavorites().catch(() => ({ data: { favorite_project_ids: [] } }))

      let projectsRes

      if (courseId && !debouncedSearch) {
        projectsRes = await projectsAPI.getByCourse(courseId)
        setCourseInfo(projectsRes.data.course_info || null)
        setProjects(projectsRes.data.projects || [])
      } else if (courseId) {
        const [listRes, courseRes] = await Promise.all([
          projectsAPI.list(courseId, debouncedSearch),
          projectsAPI.getByCourse(courseId).catch(() => null),
        ])
        setCourseInfo(courseRes?.data?.course_info || null)
        setProjects(listRes.data.projects || [])
      } else {
        projectsRes = await projectsAPI.list(courseId, debouncedSearch)
        setCourseInfo(null)
        setProjects(projectsRes.data.projects || [])
      }

      const [progressRes, favoritesRes] = await Promise.all([progressPromise, favoritesPromise])

      setProgress(progressRes.data || {})
      setFavoriteProjectIds(new Set(favoritesRes.data.favorite_project_ids || []))
      setError('')
    } catch (err) {
      setError('فشل تحميل المشاريع')
      console.error(err)
    } finally {
      setInitialLoading(false)
      setSearching(false)
    }
  }

  const handleFavoriteToggle = (isFavorite, _itemType, objectId) => {
    setFavoriteProjectIds((prev) => {
      const next = new Set(prev)
      if (isFavorite) {
        next.add(objectId)
      } else {
        next.delete(objectId)
      }
      return next
    })
  }

  const handleDelete = async (id) => {
    if (!window.confirm('هل أنت متأكد من حذف هذا المشروع؟')) {
      return
    }

    try {
      await projectsAPI.delete(id)
      setProjects(projects.filter((project) => project.project_id !== id))
    } catch (err) {
      alert('فشل حذف المشروع')
    }
  }

  const getStatusLabel = (status) => {
    switch (status) {
      case 'completed':
        return 'مكتمل'
      case 'in_progress':
        return 'قيد التنفيذ'
      default:
        return 'لم يبدأ'
    }
  }

  const getStatusClass = (status) => {
    switch (status) {
      case 'completed':
        return 'status-completed'
      case 'in_progress':
        return 'status-progress'
      default:
        return 'status-not-started'
    }
  }

  const getProjectStatus = (projectId) => {
    return progress[projectId]?.status || 'not_started'
  }

  const filteredProjects = projects.filter((project) => {
    if (levelFilter === 'all') return true
    return project.level === levelFilter
  })

  const groupedProjects = {
    not_started: [],
    in_progress: [],
    completed: []
  }

  filteredProjects.forEach((project) => {
    const status = getProjectStatus(project.project_id)
    groupedProjects[status].push(project)
  })

  const totalVisibleProjects = isAdmin
    ? filteredProjects.length
    : groupedProjects.not_started.length +
      groupedProjects.in_progress.length +
      groupedProjects.completed.length

  const ProjectSection = ({ title, projects, isAdmin, handleDelete, showStatus = false }) => {
    if (!projects.length) return null

    return (
      <div className={title ? 'project-section' : 'projects-sections-flat'}>
        {title && <h2 className="section-title">{title}</h2>}

        <div className="projects-grid">
          {projects.map((project) => {
            const status = getProjectStatus(project.project_id)

            return (
            <div key={project.project_id} className="project-card">
              <div className="project-image-container">
                {project.image ? (
                  <img src={project.image} alt={project.title} className="project-image" />
                ) : (
                  <div className="project-image-placeholder">
                    <span>{project.title.charAt(0)}</span>
                  </div>
                )}
                <div className="project-favorite-badge">
                  <FavoriteButton
                    itemType="project"
                    objectId={project.project_id}
                    initialFavorite={favoriteProjectIds.has(project.project_id)}
                    onToggle={handleFavoriteToggle}
                    showLabel={false}
                  />
                </div>
              </div>

              <div className="project-card-content">
                <div className="project-header">
                  <div className="project-header-top">
                    <h3>{project.title}</h3>
                  </div>

                  <div className="project-badges">
                    {showStatus && (
                      <span className={`badge status-badge ${getStatusClass(status)}`}>
                        {getStatusLabel(status)}
                      </span>
                    )}
                    <span className="badge badge-info">{project.level_display}</span>
                    <span className="badge badge-warning">{formatProjectLanguages(project)}</span>
                  </div>
                </div>

                <p className="project-description">
                  {project.description?.substring(0, 100)}...
                </p>

                  <div className="project-meta">
                    <div className="meta-item">
                      <span className="meta-label">المسار</span>
                      <span className="meta-value">{project.course_title}</span>
                    </div>
                    <div className="meta-item">
                      <span className="meta-label">الوقت</span>
                      <span className="meta-value">{project.estimated_time} ساعة</span>
                    </div>
                  </div>

                <div className="project-actions">
                  <Link to={`/projects/${project.project_id}`} className="btn btn-primary btn-view-details">
                    عرض التفاصيل
                  </Link>

                  {isAdmin && (
                    <div className="admin-actions">
                      <Link to={`/projects/${project.project_id}/edit`} className="btn btn-secondary btn-sm">
                        تعديل
                      </Link>
                      <button onClick={() => handleDelete(project.project_id)} className="btn btn-danger btn-sm">
                        حذف
                      </button>
                    </div>
                  )}
                </div>
              </div>

            </div>
            )
          })}
        </div>
      </div>
    )
  }

  const isSearchActive = Boolean(debouncedSearch)

  const levelFilterSelect = (
    <select
      value={levelFilter}
      onChange={(e) => setLevelFilter(e.target.value)}
      className="filter-select projects-level-filter"
      aria-label="تصفية حسب المستوى"
    >
      <option value="all">جميع المستويات</option>
      <option value="beginner">مبتدئ</option>
      <option value="intermediate">متوسط</option>
      <option value="advanced">متقدم</option>
      <option value="expert">خبير</option>
    </select>
  )

  if (initialLoading) {
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

      <div className="container">
        <div className={`page-header projects-page-header ${isAdmin ? 'projects-page-header--admin' : 'projects-page-header--learner'}`}>
          <div className="projects-header-main">
            {courseId && (
              <Link to={`/courses/${courseId}`} className="back-link">
                ← العودة للمسار
              </Link>
            )}
            <h1>
              {courseInfo?.title
                ? `مشاريع المسار: ${courseInfo.title}`
                : 'المشاريع التعليمية'}
            </h1>

            {isLearner && (
              <div className="projects-level-filter-wrap">
                {levelFilterSelect}
              </div>
            )}

            {courseInfo && (
              <p className="projects-search-summary">
                {projects.length > 0
                  ? `${projects.length} مشروع في هذا المسار`
                  : 'لا توجد مشاريع في هذا المسار حالياً'}
              </p>
            )}
            {isLearner && debouncedSearch && (
              <p className="projects-search-summary">
                {searching
                  ? 'جاري البحث...'
                  : totalVisibleProjects > 0
                    ? `تم العثور على ${totalVisibleProjects} مشروع`
                    : 'لا توجد نتائج مطابقة'}
              </p>
            )}
          </div>

          {isLearner && (
            <div className="projects-toolbar">
              <div className="projects-search-box">
                <span className="projects-search-icon" aria-hidden="true">🔍</span>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="projects-search-input"
                  placeholder="ابحث باسم المشروع..."
                  aria-label="بحث باسم المشروع"
                  autoComplete="off"
                />
                {searchQuery && (
                  <button
                    type="button"
                    className="projects-search-clear"
                    onClick={() => setSearchQuery('')}
                    aria-label="مسح البحث"
                  >
                    ×
                  </button>
                )}
              </div>
            </div>
          )}

          {isAdmin && (
            <div className="projects-header-actions">
              {levelFilterSelect}
              <Link
                to="/projects/create"
                state={courseId ? { courseId: Number(courseId) } : undefined}
                className="btn btn-primary"
              >
                إضافة مشروع جديد
              </Link>
            </div>
          )}
        </div>

        {projects.length === 0 ? (
          <div className="empty-state">
            <p>
              {debouncedSearch
                ? `لا توجد مشاريع مطابقة لـ "${debouncedSearch}"`
                : courseId
                  ? 'لا توجد مشاريع في هذا المسار حالياً'
                  : 'لا توجد مشاريع في مساراتك المنضم إليها. انضم لمسار من صفحة المسارات لعرض مشاريعه.'}
            </p>
            {isAdmin && courseId && (
              <Link
                to="/projects/create"
                state={{ courseId: Number(courseId) }}
                className="btn btn-primary"
              >
                إضافة أول مشروع للمسار
              </Link>
            )}
          </div>
        ) : totalVisibleProjects === 0 ? (
          <div className="empty-state">
            <p>لا توجد مشاريع مطابقة للمستوى المحدد</p>
          </div>
        ) : (
          <div className="projects-sections">
            {isAdmin ? (
              <ProjectSection
                projects={filteredProjects}
                isAdmin={isAdmin}
                handleDelete={handleDelete}
              />
            ) : isSearchActive ? (
              <ProjectSection
                title={`🔍 نتائج البحث (${totalVisibleProjects})`}
                projects={filteredProjects}
                isAdmin={isAdmin}
                handleDelete={handleDelete}
                showStatus
              />
            ) : (
              <>
                <ProjectSection
                  title="🆕 لم يبدأ"
                  projects={groupedProjects.not_started}
                  isAdmin={isAdmin}
                  handleDelete={handleDelete}
                />

                <ProjectSection
                  title="🔄 قيد التنفيذ"
                  projects={groupedProjects.in_progress}
                  isAdmin={isAdmin}
                  handleDelete={handleDelete}
                />

                <ProjectSection
                  title="✅ مكتمل"
                  projects={groupedProjects.completed}
                  isAdmin={isAdmin}
                  handleDelete={handleDelete}
                />
              </>
            )}
          </div>
        )}
      </div>

    </div>
  )
}

export default ProjectsList

