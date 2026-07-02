import React from 'react'
import './ProjectContentSections.css'

const ProjectContentSections = ({
  objectiveItems,
  onObjectiveItemsChange,
  userStories,
  onUserStoriesChange,
  hintItems,
  onHintItemsChange,
}) => {
  const updateObjective = (index, value) => {
    const next = [...objectiveItems]
    next[index] = value
    onObjectiveItemsChange(next)
  }

  const addObjective = () => {
    onObjectiveItemsChange([...objectiveItems, ''])
  }

  const removeObjective = (index) => {
    if (objectiveItems.length === 1) {
      onObjectiveItemsChange([''])
      return
    }
    onObjectiveItemsChange(objectiveItems.filter((_, i) => i !== index))
  }

  const updateStory = (index, field, value) => {
    const next = userStories.map((story, i) =>
      i === index ? { ...story, [field]: value } : story
    )
    onUserStoriesChange(next)
  }

  const addStory = () => {
    onUserStoriesChange([
      ...userStories,
      { id: null, title: '', description: '' },
    ])
    onHintItemsChange([...hintItems, ''])
  }

  const removeStory = (index) => {
    if (userStories.length === 1) {
      onUserStoriesChange([{ id: null, title: '', description: '' }])
      onHintItemsChange([''])
      return
    }
    onUserStoriesChange(userStories.filter((_, i) => i !== index))
    onHintItemsChange(hintItems.filter((_, i) => i !== index))
  }

  const updateHint = (index, value) => {
    const next = [...hintItems]
    next[index] = value
    onHintItemsChange(next)
  }

  const addHint = () => {
    onHintItemsChange([...hintItems, ''])
  }

  const removeHint = (index) => {
    if (hintItems.length === 1) {
      onHintItemsChange([''])
      return
    }
    onHintItemsChange(hintItems.filter((_, i) => i !== index))
  }

  return (
    <div className="project-content-sections">
      <section className="content-section-card">
        <div className="content-section-header">
          <div>
            <h3>Objectives</h3>
            <p>أهداف تعليمية واضحة يحققها المتعلم بعد إكمال المشروع</p>
          </div>
          <button type="button" className="btn btn-secondary btn-sm" onClick={addObjective}>
            + إضافة هدف
          </button>
        </div>

        <div className="content-items-list">
          {objectiveItems.map((item, index) => (
            <div key={`objective-${index}`} className="content-item-row">
              <span className="content-item-index">{index + 1}</span>
              <input
                type="text"
                value={item}
                onChange={(e) => updateObjective(index, e.target.value)}
                placeholder="مثال: فهم أساسيات HTML و CSS"
              />
              <button
                type="button"
                className="btn btn-danger btn-sm"
                onClick={() => removeObjective(index)}
                aria-label="حذف الهدف"
              >
                حذف
              </button>
            </div>
          ))}
        </div>
      </section>

      <section className="content-section-card">
        <div className="content-section-header">
          <div>
            <h3>User Stories</h3>
            <p>قصص المستخدم التي يجب أن ينجزها المتعلم ضمن المشروع</p>
          </div>
          <button type="button" className="btn btn-secondary btn-sm" onClick={addStory}>
            + إضافة قصة
          </button>
        </div>

        <div className="content-items-list">
          {userStories.map((story, index) => (
            <div key={story.id || `story-${index}`} className="content-story-card">
              <div className="content-story-header">
                <span className="content-item-index">{index + 1}</span>
                <button
                  type="button"
                  className="btn btn-danger btn-sm"
                  onClick={() => removeStory(index)}
                >
                  حذف
                </button>
              </div>
              <input
                type="text"
                value={story.title}
                onChange={(e) => updateStory(index, 'title', e.target.value)}
                placeholder="عنوان قصة المستخدم"
              />
              <textarea
                value={story.description}
                onChange={(e) => updateStory(index, 'description', e.target.value)}
                placeholder="صياغة قصة المستخدم أو المتطلب المطلوب"
                rows={3}
              />
            </div>
          ))}
        </div>
      </section>

      <section className="content-section-card">
        <div className="content-section-header">
          <div>
            <h3>Hints</h3>
            <p>تلميحات اختيارية تظهر للمتعلم (تُربط بالترتيب مع قصص المستخدم)</p>
          </div>
          <button type="button" className="btn btn-secondary btn-sm" onClick={addHint}>
            + إضافة تلميح
          </button>
        </div>

        <div className="content-items-list">
          {hintItems.map((hint, index) => (
            <div key={`hint-${index}`} className="content-item-row content-hint-row">
              <span className="content-item-index">{index + 1}</span>
              <textarea
                value={hint}
                onChange={(e) => updateHint(index, e.target.value)}
                placeholder="اكتب تلميحاً يساعد المتعلم دون حل المشكلة كاملة"
                rows={2}
              />
              <button
                type="button"
                className="btn btn-danger btn-sm"
                onClick={() => removeHint(index)}
                aria-label="حذف التلميح"
              >
                حذف
              </button>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default ProjectContentSections
