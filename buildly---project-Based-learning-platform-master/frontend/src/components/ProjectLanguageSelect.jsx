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

  const renderOptions = (options) => (
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
  )

  return (
    <div className="language-select-section" data-field="languages">
      <div className="language-select-header">
        <label>لغات المشروع *</label>
        <span className="language-select-count">
          {selectedLanguages.length} لغة محددة
        </span>
      </div>

      {renderOptions([...FRONTEND_LANGUAGE_OPTIONS, ...OTHER_LANGUAGE_OPTIONS])}

      {error && <p className="language-select-error">{error}</p>}
    </div>
  )
}

export default ProjectLanguageSelect
