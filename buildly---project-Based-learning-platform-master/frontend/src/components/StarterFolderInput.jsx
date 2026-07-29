import React, { useEffect, useRef, useState } from 'react'
import { getStarterFolderLabel } from '../utils/starterFolder'
import './CustomFilePicker.css'

const StarterFolderInput = ({
  id = 'starter_folder',
  selection,
  onChange,
  existingFile = null,
}) => {
  const folderInputRef = useRef(null)
  const zipInputRef = useRef(null)
  const menuWrapperRef = useRef(null)
  const [menuOpen, setMenuOpen] = useState(false)

  const selectedLabel = getStarterFolderLabel(selection)
  const statusText = selectedLabel || 'لم يتم اختيار أي مجلد'
  const isSelected = Boolean(selectedLabel)

  useEffect(() => {
    if (!menuOpen) return undefined

    const handleClickOutside = (event) => {
      if (menuWrapperRef.current?.contains(event.target)) return
      setMenuOpen(false)
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [menuOpen])

  const handleFolderChange = (event) => {
    const files = event.target.files
    if (!files?.length) return

    onChange({
      mode: 'folder',
      folderFiles: files,
      zipFile: null,
    })
    event.target.value = ''
  }

  const handleZipChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    onChange({
      mode: 'zip',
      zipFile: file,
      folderFiles: null,
    })
    event.target.value = ''
  }

  const openFolderPicker = () => {
    setMenuOpen(false)
    folderInputRef.current?.click()
  }

  const openZipPicker = () => {
    setMenuOpen(false)
    zipInputRef.current?.click()
  }

  return (
    <div className="input-group" data-field="starter_folder">
      <label htmlFor={id}>مجلد البداية</label>

      <div className="custom-file-picker">
        <div className="custom-file-picker-actions">
          <input
            ref={folderInputRef}
            type="file"
            id={id}
            className="custom-file-picker-input"
            webkitdirectory=""
            directory=""
            multiple
            onChange={handleFolderChange}
          />
          <input
            ref={zipInputRef}
            type="file"
            className="custom-file-picker-input"
            accept=".zip,application/zip,application/x-zip-compressed"
            onChange={handleZipChange}
          />

          <div className="custom-file-picker-menu-wrapper" ref={menuWrapperRef}>
            <button
              type="button"
              className="btn btn-secondary btn-sm custom-file-picker-trigger"
              onClick={() => setMenuOpen((prev) => !prev)}
              aria-expanded={menuOpen}
              aria-haspopup="menu"
            >
              اختيار مجلد
            </button>

            {menuOpen && (
              <div className="custom-file-picker-menu" role="menu">
                <button
                  type="button"
                  role="menuitem"
                  className="custom-file-picker-menu-item"
                  onClick={openFolderPicker}
                >
                  مجلد عادي
                </button>
                <button
                  type="button"
                  role="menuitem"
                  className="custom-file-picker-menu-item"
                  onClick={openZipPicker}
                >
                  ملف ZIP
                </button>
              </div>
            )}
          </div>
        </div>

        <span
          className={`custom-file-picker-status ${isSelected ? 'is-selected' : ''}`}
        >
          {statusText}
        </span>
      </div>

      {existingFile && !isSelected && (
        <p className="existing-file-info">
          المجلد الحالي:{' '}
          <a href={existingFile.file_url} target="_blank" rel="noreferrer">
            {existingFile.file_name}
          </a>
        </p>
      )}

      <small className="input-hint">
        اضغط «اختيار مجلد» ثم اختر مجلداً عادياً أو ملف zip. سيتم حفظه كملف مضغوط للتحميل.
      </small>
    </div>
  )
}

export default StarterFolderInput
