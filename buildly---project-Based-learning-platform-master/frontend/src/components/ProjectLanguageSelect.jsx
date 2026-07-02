import React from 'react'
import {
  FRONTEND_LANGUAGE_OPTIONS,
  OTHER_LANGUAGE_OPTIONS,
} from '../utils/projectLanguages'
import './ProjectLanguageSelect.css'

const ProjectLanguageSelect = ({ selectedLanguages, onChange, error = '' }) => {
  const toggleLanguage = (value) => {
    if (selectedLanguages.includes(value)) {
      onChange(selectedLanguages.filter((lang) => lang !== value))
      return
    }

    onChange([...selectedLanguages, value])
  }

  const renderGroup = (title, options) => (
    <div className="language-select-group">
      <h4>{title}</h4>
      <div className="language-select-grid">
        {options.map((option) => (
          <label key={option.value} className="language-select-option">
            <input
              type="checkbox"
              checked={selectedLanguages.includes(option.value)}
              onChange={() => toggleLanguage(option.value)}
            />
            <span>{option.label}</span>
          </label>
        ))}
      </div>
    </div>
  )

  return (
    <div className="language-select-section">
      <div className="language-select-header">
        <label>لغات المشروع *</label>
        <span className="language-select-count">
          {selectedLanguages.length} لغة محددة
        </span>
      </div>

      {renderGroup('لغات الفرونت إند', FRONTEND_LANGUAGE_OPTIONS)}
      {renderGroup('لغات أخرى', OTHER_LANGUAGE_OPTIONS)}

      {selectedLanguages.length > 0 && (
        <p className="language-select-primary">
          اللغة الرئيسية للتنفيذ:{' '}
          <strong>
            {
              [...FRONTEND_LANGUAGE_OPTIONS, ...OTHER_LANGUAGE_OPTIONS].find(
                (option) => option.value === selectedLanguages[0]
              )?.label
            }
          </strong>
        </p>
      )}

      {error && <p className="language-select-error">{error}</p>}
    </div>
  )
}

export default ProjectLanguageSelect
