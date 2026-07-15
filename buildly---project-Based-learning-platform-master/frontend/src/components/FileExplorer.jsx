import React, { useEffect, useRef, useState } from 'react'

function FileTypeIcon({ fileName }) {
  const ext = fileName.split('.').pop()?.toLowerCase() || ''
  const common = {
    width: 14,
    height: 14,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 1.75,
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
    'aria-hidden': true,
  }

  if (ext === 'html' || ext === 'htm') {
    return (
      <svg {...common} className="file-explorer-icon icon-html">
        <polyline points="16 18 22 12 16 6" />
        <polyline points="8 6 2 12 8 18" />
      </svg>
    )
  }

  if (ext === 'css') {
    return (
      <svg {...common} className="file-explorer-icon icon-css">
        <circle cx="13.5" cy="6.5" r="2.5" />
        <circle cx="6" cy="12" r="2.5" />
        <circle cx="18" cy="12" r="2.5" />
        <circle cx="8.5" cy="18.5" r="2.5" />
        <path d="M12 8.5v7M8 12h8" />
      </svg>
    )
  }

  if (ext === 'js' || ext === 'jsx' || ext === 'mjs' || ext === 'cjs') {
    return (
      <svg {...common} className="file-explorer-icon icon-js">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <path d="M10 13v5a1.5 1.5 0 0 1-3 0" />
        <path d="M14 18c.8.6 2 .6 2.5 0 .4-.5.3-1.2 0-1.5-.8-.7-2.5-.4-2.5-1.5 0-.6.5-1 1.2-1 .7 0 1.2.3 1.5.7" />
      </svg>
    )
  }

  if (ext === 'ts' || ext === 'tsx') {
    return (
      <svg {...common} className="file-explorer-icon icon-ts">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <path d="M9 13h4M11 13v5" />
        <path d="M15 18v-5h2.2a1.4 1.4 0 0 1 0 2.8H15" />
      </svg>
    )
  }

  if (ext === 'py') {
    return (
      <svg {...common} className="file-explorer-icon icon-py">
        <path d="M12 2c-3 0-4 1.5-4 4v2h8V6c0-2.5-1-4-4-4z" />
        <path d="M8 10H6c-2.5 0-4 1.5-4 4s1.5 4 4 4h2v-2H6c-1 0-2-.5-2-2s1-2 2-2h6v-2H8z" />
        <path d="M16 14h2c2.5 0 4-1.5 4-4s-1.5-4-4-4h-2v2h2c1 0 2 .5 2 2s-1 2-2 2h-6v2h6z" />
        <circle cx="10" cy="5" r="0.8" fill="currentColor" stroke="none" />
        <circle cx="14" cy="19" r="0.8" fill="currentColor" stroke="none" />
      </svg>
    )
  }

  if (ext === 'json') {
    return (
      <svg {...common} className="file-explorer-icon icon-json">
        <path d="M8 4c-2 0-3 1.5-3 4v2c0 1.5-1 2.5-2 3 1 .5 2 1.5 2 3v2c0 2.5 1 4 3 4" />
        <path d="M16 4c2 0 3 1.5 3 4v2c0 1.5 1 2.5 2 3-1 .5-2 1.5-2 3v2c0 2.5-1 4-3 4" />
      </svg>
    )
  }

  if (ext === 'md' || ext === 'markdown') {
    return (
      <svg {...common} className="file-explorer-icon icon-md">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <path d="M7 15V9l2.5 3.5L12 9v6" />
        <path d="M15 12v3M15 12l2 3 2-3" />
      </svg>
    )
  }

  if (ext === 'txt' || ext === 'text' || ext === 'log') {
    return (
      <svg {...common} className="file-explorer-icon icon-txt">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="8" y1="13" x2="16" y2="13" />
        <line x1="8" y1="17" x2="14" y2="17" />
      </svg>
    )
  }

  return (
    <svg {...common} className="file-explorer-icon icon-unknown">
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
    </svg>
  )
}

/**
 * Presentation-only file tree for the shared ProjectWork workspace.
 * Owns no workspace state; requests all mutations via callbacks.
 */
const FileExplorer = ({
  workspace,
  onSelectFile,
  onAddFile,
  onRenameFile,
  onDeleteFile,
  readOnly = false,
}) => {
  const [renamingFileId, setRenamingFileId] = useState(null)
  const [renameValue, setRenameValue] = useState('')
  const [menuFileId, setMenuFileId] = useState(null)
  const menuRef = useRef(null)

  const files = workspace?.files || []
  const activeFileId = workspace?.activeFileId

  useEffect(() => {
    if (!renamingFileId) return

    const stillExists = files.some((file) => file.id === renamingFileId)
    if (!stillExists) {
      setRenamingFileId(null)
      setRenameValue('')
    }
  }, [files, renamingFileId])

  useEffect(() => {
    if (!menuFileId) return undefined

    const handlePointerDown = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuFileId(null)
      }
    }

    const handleEscape = (event) => {
      if (event.key === 'Escape') setMenuFileId(null)
    }

    document.addEventListener('mousedown', handlePointerDown)
    document.addEventListener('keydown', handleEscape)
    return () => {
      document.removeEventListener('mousedown', handlePointerDown)
      document.removeEventListener('keydown', handleEscape)
    }
  }, [menuFileId])

  const handleSelect = (fileId) => {
    if (renamingFileId) return
    setMenuFileId(null)
    onSelectFile?.(fileId)
  }

  const handleAddFile = () => {
    if (readOnly) return

    const name = window.prompt('New file name:', 'untitled.js')
    if (!name) return

    const trimmed = name.trim()
    if (!trimmed) return

    const exists = files.some(
      (file) => file.name.toLowerCase() === trimmed.toLowerCase()
    )
    if (exists) {
      window.alert('A file with this name already exists')
      return
    }

    onAddFile?.(trimmed)
  }

  const startRename = (file) => {
    if (readOnly) return
    setMenuFileId(null)
    setRenamingFileId(file.id)
    setRenameValue(file.name)
  }

  const commitRename = () => {
    if (!renamingFileId) return

    const trimmed = renameValue.trim()
    if (!trimmed) {
      setRenamingFileId(null)
      setRenameValue('')
      return
    }

    const exists = files.some(
      (file) =>
        file.id !== renamingFileId &&
        file.name.toLowerCase() === trimmed.toLowerCase()
    )
    if (exists) {
      window.alert('A file with this name already exists')
      return
    }

    onRenameFile?.(renamingFileId, trimmed)
    setRenamingFileId(null)
    setRenameValue('')
  }

  const cancelRename = () => {
    setRenamingFileId(null)
    setRenameValue('')
  }

  const handleDeleteFile = (fileId) => {
    if (readOnly || files.length <= 1) return

    const file = files.find((item) => item.id === fileId)
    const confirmed = window.confirm(`Delete "${file?.name}"?`)
    if (!confirmed) return

    setMenuFileId(null)
    onDeleteFile?.(fileId)
  }

  if (!workspace) return null

  return (
    <aside className="file-explorer" aria-label="File explorer">
      <div className="file-explorer-header">
        <span className="file-explorer-title">Workspace</span>
        {!readOnly && (
          <button
            type="button"
            className="file-explorer-add"
            onClick={handleAddFile}
            title="New File"
          >
            <span className="file-explorer-add-plus" aria-hidden="true">
              +
            </span>
            <span>New File</span>
          </button>
        )}
      </div>

      {files.length === 0 ? (
        <div className="file-explorer-empty">
          <p className="file-explorer-empty-text">No files yet</p>
          {!readOnly && (
            <button
              type="button"
              className="file-explorer-empty-btn"
              onClick={handleAddFile}
            >
              Create File
            </button>
          )}
        </div>
      ) : (
        <ul className="file-explorer-list">
          {files.map((file) => {
            const isActive = file.id === activeFileId
            const isRenaming = renamingFileId === file.id
            const isMenuOpen = menuFileId === file.id

            return (
              <li key={file.id} className="file-explorer-row">
                <div
                  className={`file-explorer-item ${isActive ? 'active' : ''}`}
                  onClick={() => handleSelect(file.id)}
                >
                  <span className="file-explorer-icon-wrap">
                    <FileTypeIcon fileName={file.name} />
                  </span>

                  {isRenaming ? (
                    <input
                      className="file-explorer-rename-input"
                      value={renameValue}
                      autoFocus
                      onChange={(e) => setRenameValue(e.target.value)}
                      onBlur={commitRename}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') commitRename()
                        if (e.key === 'Escape') cancelRename()
                      }}
                      onClick={(e) => e.stopPropagation()}
                    />
                  ) : (
                    <>
                      <span className="file-explorer-name" title={file.name}>
                        {file.name}
                      </span>

                      {!readOnly && (
                        <div
                          className="file-explorer-menu-wrap"
                          ref={isMenuOpen ? menuRef : null}
                        >
                          <button
                            type="button"
                            className={`file-explorer-menu-btn ${isMenuOpen ? 'open' : ''}`}
                            title="File actions"
                            aria-haspopup="menu"
                            aria-expanded={isMenuOpen}
                            onClick={(e) => {
                              e.stopPropagation()
                              setMenuFileId(isMenuOpen ? null : file.id)
                            }}
                          >
                            ⋮
                          </button>

                          {isMenuOpen && (
                            <div className="file-explorer-menu" role="menu">
                              <button
                                type="button"
                                role="menuitem"
                                className="file-explorer-menu-item"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  startRename(file)
                                }}
                              >
                                Rename
                              </button>
                              <button
                                type="button"
                                role="menuitem"
                                className="file-explorer-menu-item danger"
                                disabled={files.length <= 1}
                                onClick={(e) => {
                                  e.stopPropagation()
                                  handleDeleteFile(file.id)
                                }}
                              >
                                Delete
                              </button>
                            </div>
                          )}
                        </div>
                      )}
                    </>
                  )}
                </div>
              </li>
            )
          })}
        </ul>
      )}
    </aside>
  )
}

export default FileExplorer
