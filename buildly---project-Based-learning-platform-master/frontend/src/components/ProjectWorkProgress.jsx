import React from 'react'
import './ProjectWorkProgress.css'

const ProjectWorkProgress = ({ progress }) => {
  const { percentage, passed, total, allPassed, hasTests } = progress

  if (!hasTests) {
    return null
  }

  return (
    <div className="project-work-progress">
      {allPassed && (
        <div className="project-completed-banner" role="status">
          <span className="project-completed-icon" aria-hidden="true">
            🎉
          </span>
          <div>
            <strong>Project Completed</strong>
            <p>لقد نجحت في جميع الاختبارات! يمكنك الآن تسليم المشروع.</p>
          </div>
        </div>
      )}

      <div className="project-progress-card">
        <div className="project-progress-header">
          <span className="project-progress-label">نسبة الإنجاز</span>
          <span className="project-progress-value">{percentage}%</span>
        </div>

        <div className="project-progress-bar-bg" aria-hidden="true">
          <div
            className={`project-progress-bar-fill ${allPassed ? 'is-complete' : ''}`}
            style={{ width: `${percentage}%` }}
          />
        </div>

        <p className="project-progress-meta">
          {passed} من {total} اختبار ناجح
        </p>
      </div>
    </div>
  )
}

export default ProjectWorkProgress
