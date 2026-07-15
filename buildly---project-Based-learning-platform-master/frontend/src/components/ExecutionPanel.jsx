import React, { useEffect, useState } from 'react'

const BLOCK_LABELS = {
  stdout: 'stdout',
  stderr: 'stderr',
  error: 'خطأ',
  result: 'النتيجة',
  info: 'معلومة',
  status: 'حالة',
}

const ExecutionPanel = ({
  execution,
  kernelLabel = 'Kernel',
  onClear,
  onResetKernel,
  showResetKernel = false,
}) => {
  const [activeTab, setActiveTab] = useState(execution?.activeTab || 'console')

  useEffect(() => {
    if (execution?.activeTab) {
      setActiveTab(execution.activeTab)
    }
  }, [execution?.activeTab, execution?.previewHtml])

  const currentTab = execution?.previewHtml ? activeTab : 'console'
  const status = execution?.status || 'idle'

  const statusIcon = {
    idle: '○',
    running: '◌',
    success: '✓',
    error: '✕',
  }[status]

  return (
    <div className="execution-panel">
      <div className="execution-panel-header">
        <div className="execution-panel-tabs">
          <button
            type="button"
            className={`execution-tab ${currentTab === 'console' ? 'active' : ''}`}
            onClick={() => setActiveTab('console')}
          >
            Console
          </button>
          {execution?.previewHtml && (
            <button
              type="button"
              className={`execution-tab ${currentTab === 'preview' ? 'active' : ''}`}
              onClick={() => setActiveTab('preview')}
            >
              Preview
            </button>
          )}
        </div>

        <div className="execution-panel-meta">
          <span className={`execution-kernel-dot status-${status}`} />
          <span className="execution-kernel-label">
            {status === 'running'
              ? execution?.kernelMessage || 'Executing workspace...'
              : kernelLabel}
          </span>
          {execution?.durationMs != null && (
            <span className="execution-duration">{execution.durationMs}ms</span>
          )}
          <span className={`execution-status-badge status-${status}`}>
            {statusIcon}{' '}
            {status === 'running'
              ? 'Running'
              : status === 'success'
                ? 'Success'
                : status === 'error'
                  ? 'Error'
                  : 'Ready'}
          </span>
        </div>
      </div>

      <div className="execution-panel-toolbar">
        <button type="button" className="execution-tool-btn" onClick={onClear}>
          مسح المخرجات
        </button>
        {showResetKernel && (
          <button type="button" className="execution-tool-btn" onClick={onResetKernel}>
            إعادة تشغيل Kernel
          </button>
        )}
      </div>

      <div className="execution-panel-body">
        {status === 'running' && (
          <div className="execution-running-banner">
            <span className="execution-spinner" />
            {execution?.kernelMessage || 'Executing workspace...'}
          </div>
        )}

        {currentTab === 'console' && (
          <div className="execution-blocks">
            {!execution?.blocks?.length && status !== 'running' && (
              <div className="execution-empty">
                شغّل الكود بـ <kbd>Ctrl</kbd> + <kbd>Enter</kbd> أو زر التشغيل لعرض المخرجات هنا.
              </div>
            )}

            {execution?.blocks?.map((block) => (
              <div key={block.id} className={`execution-block block-${block.type}`}>
                <div className="execution-block-label">{BLOCK_LABELS[block.type] || block.type}</div>
                <pre className="execution-block-content">{block.content}</pre>
              </div>
            ))}
          </div>
        )}

        {currentTab === 'preview' && execution?.previewHtml && (
          <iframe
            key={execution.runId ?? execution.previewHtml.length}
            className="execution-preview-frame"
            title="Live preview"
            sandbox="allow-scripts"
            srcDoc={execution.previewHtml}
          />
        )}
      </div>
    </div>
  )
}

export default ExecutionPanel
