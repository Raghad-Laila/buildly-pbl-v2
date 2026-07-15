import React, { useState } from 'react'
import TestLinkStatus from './TestLinkStatus'
import './ProjectWorkSidebar.css'

const ProjectWorkSidebar = ({
  project,
  objective,
  userStoriesWithStatus,
  availableHints,
}) => {
  const [hintsOpen, setHintsOpen] = useState(false)

  return (
    <aside className="project-work-sidebar" aria-label="تعليمات المشروع">
      <div className="project-work-sidebar-inner">
        <header className="project-work-sidebar-header">
          <h2 className="project-work-sidebar-title">{project.title}</h2>
        </header>

        <section className="project-work-sidebar-section">
          <p className="project-work-sidebar-description">{project.description}</p>
        </section>

        <section className="project-work-sidebar-section">
          <h3 className="project-work-sidebar-heading">Objective:</h3>
          <p className="project-work-sidebar-note">
            حقّق قصص المستخدم أدناه واجتز جميع الاختبارات لإكمال المشروع.
          </p>
          {objective ? (
            <p className="project-work-sidebar-objective">{objective}</p>
          ) : (
            <p className="project-work-sidebar-empty">لا يوجد هدف محدد لهذا المشروع.</p>
          )}
        </section>

        <section className="project-work-sidebar-section">
          <h3 className="project-work-sidebar-heading">User Stories:</h3>
          {userStoriesWithStatus.length > 0 ? (
            <ol className="project-work-sidebar-stories">
              {userStoriesWithStatus.map((story) => (
                <li key={story.id} className="project-work-sidebar-story">
                  <div className="project-work-sidebar-story-content">
                    <div className="project-work-sidebar-story-row">
                      <span className="project-work-sidebar-story-text">
                        {story.title && (
                          <strong className="project-work-sidebar-story-title">
                            {story.title}
                            {story.text && story.text !== story.title ? ': ' : ''}
                          </strong>
                        )}
                        {story.text && story.text !== story.title ? (
                          <span>{story.text}</span>
                        ) : null}
                      </span>
                      <TestLinkStatus status={story.testStatus} />
                    </div>
                  </div>
                </li>
              ))}
            </ol>
          ) : (
            <p className="project-work-sidebar-empty">لا توجد قصص مستخدم لهذا المشروع.</p>
          )}
        </section>

        <section className="project-work-sidebar-section project-work-sidebar-hints">
          <button
            type="button"
            className="project-work-sidebar-hints-toggle"
            onClick={() => setHintsOpen((prev) => !prev)}
            aria-expanded={hintsOpen}
          >
            <span>Hints</span>
            <span className="project-work-sidebar-hints-icon">{hintsOpen ? '−' : '+'}</span>
          </button>

          {hintsOpen && (
            <div className="project-work-sidebar-hints-panel">
              {availableHints.length > 0 ? (
                availableHints.map((item) => (
                  <div key={item.id} className="project-work-sidebar-hint-card">
                    <h4>{item.title}</h4>
                    <p>{item.hint}</p>
                  </div>
                ))
              ) : (
                <p className="project-work-sidebar-empty">لا توجد تلميحات متاحة حالياً.</p>
              )}
            </div>
          )}
        </section>
      </div>
    </aside>
  )
}

export default ProjectWorkSidebar
