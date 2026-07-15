import React, { useState } from 'react'

const DOCK_TABS = [
  { id: 'output', label: 'Output' },
  { id: 'tests', label: 'Tests' },
  { id: 'terminal', label: 'Terminal' },
]

/**
 * Presentation-only dock. Owns no execution/test/workspace state.
 * Optionally controlled via activeTab + onActiveTabChange.
 */
const BottomDock = ({
  output,
  tests,
  executionBlocks = [],
  activeTab: controlledTab,
  onActiveTabChange,
}) => {
  const [internalTab, setInternalTab] = useState('output')
  const isControlled =
    controlledTab !== undefined && typeof onActiveTabChange === 'function'
  const activeTab = isControlled ? controlledTab : internalTab

  const setActiveTab = (tabId) => {
    if (isControlled) {
      onActiveTabChange(tabId)
      return
    }
    setInternalTab(tabId)
  }

  const streamBlocks = executionBlocks.filter(
    (block) => block.type === 'stdout' || block.type === 'stderr'
  )

  return (
    <div className="bottom-dock">
      <div className="bottom-dock-tabs" role="tablist" aria-label="Workspace dock">
        {DOCK_TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            role="tab"
            aria-selected={activeTab === tab.id}
            className={`bottom-dock-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="bottom-dock-body">
        <div
          className="bottom-dock-panel"
          role="tabpanel"
          hidden={activeTab !== 'output'}
        >
          {output}
        </div>

        <div
          className="bottom-dock-panel"
          role="tabpanel"
          hidden={activeTab !== 'tests'}
        >
          {tests}
        </div>

        <div
          className="bottom-dock-panel bottom-dock-terminal"
          role="tabpanel"
          hidden={activeTab !== 'terminal'}
        >
          {!streamBlocks.length ? (
            <div className="bottom-dock-terminal-empty">
              لا توجد مخرجات stdout/stderr بعد. شغّل الكود لعرضها هنا.
            </div>
          ) : (
            streamBlocks.map((block) => (
              <div
                key={block.id}
                className={`bottom-dock-terminal-block block-${block.type}`}
              >
                <div className="bottom-dock-terminal-label">{block.type}</div>
                <pre className="bottom-dock-terminal-content">{block.content}</pre>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default BottomDock
