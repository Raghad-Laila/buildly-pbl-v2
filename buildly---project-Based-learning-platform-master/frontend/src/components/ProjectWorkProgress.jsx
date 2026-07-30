import React, { useEffect, useState } from 'react'
import './ProjectWorkProgress.css'

const CELEBRATION_RIBBONS = 48

const ProjectWorkProgress = ({
  progress,
  onImproveCode,
  improveCodeLoading = false,
  showImproveCode = false,
}) => {
  const { percentage, passed, total, allPassed, hasTests } = progress
  const [celebrationKey, setCelebrationKey] = useState(0)

  useEffect(() => {
    if (!allPassed) return
    setCelebrationKey((key) => key + 1)
  }, [allPassed])

  if (!hasTests) {
    return null
  }

  return (
    <div className={`project-work-progress${allPassed ? ' is-complete' : ''}`}>
      {allPassed && (
        <div
          key={celebrationKey}
          className="project-progress-celebration"
          aria-hidden="true"
        >
          <span className="project-progress-burst-flash" />
          {Array.from({ length: CELEBRATION_RIBBONS }, (_, index) => {
            const angle = (index / CELEBRATION_RIBBONS) * Math.PI * 2
            const distance = 160 + (index % 6) * 55
            const dx = Math.cos(angle) * distance
            const dy = Math.sin(angle) * distance - 40
            const spin = 180 + (index % 8) * 90

            return (
              <span
                key={index}
                className={`project-progress-ribbon tone-${index % 6}`}
                style={{
                  '--ribbon-i': index,
                  '--dx': `${dx.toFixed(1)}px`,
                  '--dy': `${dy.toFixed(1)}px`,
                  '--spin': `${spin}deg`,
                }}
              />
            )
          })}
        </div>
      )}

      {allPassed && (
        <div className="project-completed-banner" role="status">
          <span className="project-completed-icon" aria-hidden="true">
            🎉
          </span>
          <div className="project-completed-banner-content">
            <strong>All Tests Passed</strong>
            <p>لقد نجحت في جميع الاختبارات! المشروع جاهز للتسليم.</p>
            {showImproveCode && (
              <button
                type="button"
                className="btn fcc-quality-review-btn project-quality-review-btn"
                onClick={onImproveCode}
                disabled={improveCodeLoading}
              >
                {improveCodeLoading ? (
                  <>
                    <span className="execution-spinner" />
                    Analyzing...
                  </>
                ) : (
                  '✨ Improve Code with AI'
                )}
              </button>
            )}
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
