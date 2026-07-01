import React, { useEffect, useState } from 'react'
import Editor from '@monaco-editor/react'
import {
  addFile,
  deleteFile,
  getActiveFile,
  getMonacoLanguageFromFileName,
  renameFile,
  setActiveFile,
  updateFileContent,
} from '../utils/codeWorkspace'

const MultiFileEditor = ({
  workspace,
  onChange,
  onRun,
  readOnly = false,
  defaultMonacoLanguage = 'javascript',
  editorHeight = '400px',
}) => {
  const [renamingFileId, setRenamingFileId] = useState(null)
  const [renameValue, setRenameValue] = useState('')

  const activeFile = getActiveFile(workspace)

  useEffect(() => {
    if (!renamingFileId) return

    const stillExists = workspace.files.some((file) => file.id === renamingFileId)
    if (!stillExists) {
      setRenamingFileId(null)
      setRenameValue('')
    }
  }, [workspace, renamingFileId])

  const emitChange = (nextWorkspace) => {
    onChange(nextWorkspace)
  }

  const handleSelectTab = (fileId) => {
    if (renamingFileId) return
    emitChange(setActiveFile(workspace, fileId))
  }

  const handleContentChange = (value) => {
    if (!activeFile || readOnly) return
    emitChange(updateFileContent(workspace, activeFile.id, value || ''))
  }

  const handleAddFile = () => {
    const name = window.prompt('اسم الملف الجديد:', 'untitled.js')
    if (!name) return

    const trimmed = name.trim()
    if (!trimmed) return

    const exists = workspace.files.some(
      (file) => file.name.toLowerCase() === trimmed.toLowerCase()
    )

    if (exists) {
      window.alert('يوجد ملف بنفس الاسم مسبقاً')
      return
    }

    emitChange(addFile(workspace, trimmed))
  }

  const startRename = (file) => {
    if (readOnly) return
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

    const exists = workspace.files.some(
      (file) =>
        file.id !== renamingFileId &&
        file.name.toLowerCase() === trimmed.toLowerCase()
    )

    if (exists) {
      window.alert('يوجد ملف بنفس الاسم مسبقاً')
      return
    }

    emitChange(renameFile(workspace, renamingFileId, trimmed))
    setRenamingFileId(null)
    setRenameValue('')
  }

  const cancelRename = () => {
    setRenamingFileId(null)
    setRenameValue('')
  }

  const handleDeleteFile = (fileId) => {
    if (readOnly || workspace.files.length <= 1) return

    const file = workspace.files.find((item) => item.id === fileId)
    const confirmed = window.confirm(`هل تريد حذف الملف "${file?.name}"؟`)
    if (!confirmed) return

    emitChange(deleteFile(workspace, fileId))
  }

  const monacoLanguage = activeFile
    ? getMonacoLanguageFromFileName(activeFile.name)
  : defaultMonacoLanguage

  return (
    <div className="multi-file-editor">
      <div className="editor-tabs-bar">
        <div className="editor-tabs-list">
          {workspace.files.map((file) => {
            const isActive = file.id === workspace.activeFileId
            const isRenaming = renamingFileId === file.id

            return (
              <div
                key={file.id}
                className={`editor-tab ${isActive ? 'active' : ''}`}
                onClick={() => handleSelectTab(file.id)}
              >
                {isRenaming ? (
                  <input
                    className="editor-tab-rename-input"
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
                    <span
                      className="editor-tab-name"
                      onDoubleClick={(e) => {
                        e.stopPropagation()
                        startRename(file)
                      }}
                      title="انقر مرتين لإعادة التسمية"
                    >
                      {file.name}
                    </span>

                    {!readOnly && (
                      <div className="editor-tab-actions">
                        <button
                          type="button"
                          className="editor-tab-action"
                          title="إعادة تسمية"
                          onClick={(e) => {
                            e.stopPropagation()
                            startRename(file)
                          }}
                        >
                          ✎
                        </button>
                        {workspace.files.length > 1 && (
                          <button
                            type="button"
                            className="editor-tab-action editor-tab-close"
                            title="حذف الملف"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleDeleteFile(file.id)
                            }}
                          >
                            ×
                          </button>
                        )}
                      </div>
                    )}
                  </>
                )}
              </div>
            )
          })}
        </div>

        {!readOnly && (
          <button
            type="button"
            className="editor-tab-add"
            onClick={handleAddFile}
            title="ملف جديد"
          >
            +
          </button>
        )}
      </div>

      <div className="monaco-wrapper">
        <Editor
          height={editorHeight}
          language={monacoLanguage === 'plaintext' ? defaultMonacoLanguage : monacoLanguage}
          value={activeFile?.content || ''}
          onChange={handleContentChange}
          theme="vs-dark"
          onMount={(editor, monaco) => {
            if (!readOnly && onRun) {
              editor.addCommand(
                monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter,
                () => onRun()
              )
            }
          }}
          options={{
            readOnly,
            minimap: { enabled: false },
            fontSize: 14,
            automaticLayout: true,
            renderWhitespace: 'all',
            colorDecorators: true,
            fixedOverflowWidgets: true,
            suggestWidgetFixed: true,
          }}
        />
      </div>
    </div>
  )
}

export default MultiFileEditor
