/** UI-only workspace preferences. Never stores code, execution, or test data. */

export const WORKSPACE_UI_VERSION = 1

export const EXPLORER_WIDTH_DEFAULT = 220
export const EXPLORER_WIDTH_MIN = 180
export const EXPLORER_WIDTH_MAX = 450

export const DOCK_HEIGHT_DEFAULT = 260
export const DOCK_HEIGHT_MIN = 180
export const DOCK_HEIGHT_MAX_RATIO = 0.6

export const DOCK_TAB_DEFAULT = 'output'
export const DOCK_TAB_IDS = ['output', 'tests', 'terminal']

export function getWorkspaceUiStorageKey(projectId) {
  return `buildly:workspace-ui:${projectId}`
}

export function getDefaultWorkspaceUiPrefs() {
  return {
    version: WORKSPACE_UI_VERSION,
    explorerWidth: EXPLORER_WIDTH_DEFAULT,
    dockHeight: DOCK_HEIGHT_DEFAULT,
    dockActiveTab: DOCK_TAB_DEFAULT,
    activeFileId: null,
    explorerCollapsed: false,
  }
}

export function clampExplorerWidth(width) {
  if (typeof width !== 'number' || !Number.isFinite(width)) {
    return null
  }

  return Math.min(EXPLORER_WIDTH_MAX, Math.max(EXPLORER_WIDTH_MIN, Math.round(width)))
}

export function clampDockHeight(height, maxHeight = Number.POSITIVE_INFINITY) {
  if (typeof height !== 'number' || !Number.isFinite(height)) {
    return null
  }

  const upper = Number.isFinite(maxHeight) ? maxHeight : Number.POSITIVE_INFINITY
  return Math.min(upper, Math.max(DOCK_HEIGHT_MIN, Math.round(height)))
}

export function normalizeDockActiveTab(tab) {
  return DOCK_TAB_IDS.includes(tab) ? tab : null
}

export function normalizeActiveFileId(fileId) {
  return typeof fileId === 'string' && fileId.trim() ? fileId : null
}

/**
 * Normalize a raw prefs object. Per-field fallbacks keep valid fields
 * when some values are invalid. Does not inspect workspace content.
 */
export function normalizeWorkspaceUiPrefs(raw, options = {}) {
  const defaults = getDefaultWorkspaceUiPrefs()

  if (!raw || typeof raw !== 'object' || raw.version !== WORKSPACE_UI_VERSION) {
    return defaults
  }

  const explorerWidth = clampExplorerWidth(raw.explorerWidth)
  const dockHeight = clampDockHeight(raw.dockHeight, options.maxDockHeight)
  const dockActiveTab = normalizeDockActiveTab(raw.dockActiveTab)
  const activeFileId = normalizeActiveFileId(raw.activeFileId)
  const explorerCollapsed =
    typeof raw.explorerCollapsed === 'boolean'
      ? raw.explorerCollapsed
      : defaults.explorerCollapsed

  return {
    version: WORKSPACE_UI_VERSION,
    explorerWidth: explorerWidth ?? defaults.explorerWidth,
    dockHeight: dockHeight ?? defaults.dockHeight,
    dockActiveTab: dockActiveTab ?? defaults.dockActiveTab,
    activeFileId,
    explorerCollapsed,
  }
}

export function loadWorkspaceUiPrefs(projectId, options = {}) {
  if (projectId == null || projectId === '') {
    return getDefaultWorkspaceUiPrefs()
  }

  try {
    const raw = localStorage.getItem(getWorkspaceUiStorageKey(projectId))
    if (!raw) {
      return getDefaultWorkspaceUiPrefs()
    }

    return normalizeWorkspaceUiPrefs(JSON.parse(raw), options)
  } catch {
    try {
      localStorage.removeItem(getWorkspaceUiStorageKey(projectId))
    } catch {
      // ignore
    }
    return getDefaultWorkspaceUiPrefs()
  }
}

export function saveWorkspaceUiPrefs(projectId, prefs, options = {}) {
  if (projectId == null || projectId === '') return

  try {
    const normalized = normalizeWorkspaceUiPrefs(
      {
        version: WORKSPACE_UI_VERSION,
        ...prefs,
      },
      options
    )

    localStorage.setItem(
      getWorkspaceUiStorageKey(projectId),
      JSON.stringify(normalized)
    )
  } catch {
    // ignore quota / private mode
  }
}
