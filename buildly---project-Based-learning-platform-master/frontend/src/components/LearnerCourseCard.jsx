import React from 'react'
import { Link } from 'react-router-dom'
import FavoriteButton from './FavoriteButton'

const LearnerCourseCard = ({
  course,
  isFavorite = false,
  onFavoriteToggle,
  showFavorite = true,
  actions = null,
}) => {
  const projectsCount =
    course.actual_projects_count ?? course.projects_count ?? 0
  const learnersCount = course.enrolled_students_count ?? 0
  const description = course.description || ''
  const shortDescription =
    description.length > 140
      ? `${description.substring(0, 140)}...`
      : description

  return (
    <article className="learner-course-card">
      <div className="learner-course-card-media">
        {course.image ? (
          <img
            src={course.image}
            alt={course.title}
            className="learner-course-card-image"
          />
        ) : (
          <div className="learner-course-card-image-placeholder">
            <span>{course.title?.charAt(0) || 'م'}</span>
          </div>
        )}

        {showFavorite && (
          <div className="learner-course-card-favorite">
            <FavoriteButton
              itemType="course"
              objectId={course.id}
              initialFavorite={isFavorite}
              onToggle={onFavoriteToggle}
              label="مفضلة"
            />
          </div>
        )}

        <span className="learner-course-card-chip">
          {course.level_display}
          {course.category_display ? `: ${course.category_display}` : ''}
        </span>
      </div>

      <div className="learner-course-card-body">
        <h3>{course.title}</h3>
        {shortDescription ? <p>{shortDescription}</p> : null}

        <div className="learner-course-card-stats">
          <div className="learner-course-stat">
            <span className="learner-course-stat-icon" aria-hidden="true">
              ⏱
            </span>
            <strong>{course.estimated_duration || 0} ساعة</strong>
            <span>مدة المسار</span>
          </div>
          <div className="learner-course-stat">
            <span className="learner-course-stat-icon" aria-hidden="true">
              ▣
            </span>
            <strong>{projectsCount} مشروعاً</strong>
            <span>تطبيقات عملية</span>
          </div>
          <div className="learner-course-stat">
            <span className="learner-course-stat-icon" aria-hidden="true">
              👥
            </span>
            <strong>{learnersCount} طالباً</strong>
            <span>في الرحلة</span>
          </div>
        </div>

        <div className={`learner-course-card-actions${actions ? ' learner-course-card-actions--admin' : ''}`}>
          {actions || (
            <Link
              to={`/courses/${course.id}`}
              className="learner-course-card-cta"
            >
              عرض التفاصيل
            </Link>
          )}
        </div>
      </div>
    </article>
  )
}

export default LearnerCourseCard
