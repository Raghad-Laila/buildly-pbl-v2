import React, { useRef } from 'react'
import './CustomFilePicker.css'

const ProjectImageInput = ({
  id = 'project_image',
  label = 'صورة المشروع',
  selectedFile = null,
  preview = null,
  onChange,
  hint = 'قم برفع صورة تعبيرية للمشروع (يفضل مقاس 16:9)',
}) => {
  const inputRef = useRef(null)

  const statusText = selectedFile?.name
    || (preview ? 'صورة محددة' : 'لم يتم اختيار أي صورة')
  const isSelected = Boolean(selectedFile || preview)

  const handleChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onloadend = () => {
      onChange({ file, preview: reader.result })
    }
    reader.readAsDataURL(file)
    event.target.value = ''
  }

  return (
    <div className="input-group">
      <label htmlFor={id}>{label}</label>

      <div className="custom-file-picker">
        <div className="custom-file-picker-actions">
          <input
            ref={inputRef}
            type="file"
            id={id}
            className="custom-file-picker-input"
            accept="image/*"
            onChange={handleChange}
          />
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={() => inputRef.current?.click()}
          >
            اختيار صورة
          </button>
        </div>

        <span
          className={`custom-file-picker-status ${isSelected ? 'is-selected' : ''}`}
        >
          {statusText}
        </span>
      </div>

      {preview && (
        <div className="image-preview-container">
          <img src={preview} alt={label} className="image-preview" />
        </div>
      )}

      <small className="input-hint">{hint}</small>
    </div>
  )
}

export default ProjectImageInput
