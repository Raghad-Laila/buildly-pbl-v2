import {
  detectLanguageFromFile,
  getMainExecutableFile,
} from './codeWorkspace'
import {
  isFrontendLanguage,
  resolveExecutionLanguage,
  runFrontendCode,
  runWorkspace,
} from './frontendCodeRunner'
import { runJsKernel } from './jsKernel'
import { getLanguageMismatchResult } from './languageMismatch'

function runPythonOnDocker(workspace, pythonEntryFile, runServerPython, onStream) {
  const entryName = pythonEntryFile?.name || 'main.py'
  const entryContent = pythonEntryFile?.content || ''

  if (!runServerPython) {
    return {
      stdout: '',
      stderr: 'تنفيذ Python يتطلب خادم Docker.',
      returnValue: '',
      status: 'error',
      previewHtml: null,
      hasPreview: false,
      kernelMessage: 'Docker Python',
    }
  }

  onStream?.('status', 'Running on Docker Python...')
  return runServerPython({
    files: workspace?.files || [],
    entryFileName: entryName,
    code: entryContent,
  })
}

/**
 * Detect execution strategy from file extensions (+ project language hint).
 * Never uses file count alone.
 *
 * @returns {'python' | 'web' | 'javascript' | 'unknown'}
 */
export function detectWorkspaceType(workspace, projectLanguage = null) {
  const files = workspace?.files || []
  const names = files.map((file) => (file.name || '').toLowerCase())

  const hasPy = names.some((name) => name.endsWith('.py'))
  const hasHtml = names.some((name) => /\.html?$/.test(name))
  const hasCss = names.some((name) => name.endsWith('.css'))
  const hasJsLike = names.some((name) =>
    /\.(js|jsx|mjs|cjs|ts|tsx)$/.test(name)
  )
  const hasJsx = names.some((name) => /\.(jsx|tsx)$/.test(name))

  // Project language is an explicit product signal.
  if (projectLanguage === 'python') {
    return 'python'
  }

  // HTML (or React JSX bundle) → browser preview path.
  if (hasHtml) {
    return 'web'
  }

  // Python sources without HTML → Docker Python.
  if (hasPy) {
    return 'python'
  }

  if (
    projectLanguage === 'html' ||
    projectLanguage === 'css' ||
    projectLanguage === 'typescript' ||
    projectLanguage === 'react'
  ) {
    return 'web'
  }

  if (hasJsx) {
    return 'web'
  }

  // Common frontend lab layout without renaming project language.
  if (hasCss && hasJsLike) {
    return 'web'
  }

  if (hasCss) {
    return 'web'
  }

  if (projectLanguage === 'javascript' || hasJsLike) {
    return 'javascript'
  }

  return 'unknown'
}

function findWorkspaceFileByName(workspace, fileName) {
  if (!fileName) return null
  const target = String(fileName).toLowerCase()
  return (
    (workspace?.files || []).find(
      (file) => (file.name || '').toLowerCase() === target
    ) || null
  )
}

export async function executeWorkspace(workspace, projectLanguage, options = {}) {
  const { onStream, runServerPython, entryFileName } = options

  const mismatch = getLanguageMismatchResult(workspace, projectLanguage)
  if (mismatch) {
    return mismatch
  }

  const workspaceType = detectWorkspaceType(workspace, projectLanguage)
  const projectEntryFile = getMainExecutableFile(workspace, projectLanguage)
  // Optional Run Code override; missing/unknown name → project entry (getMainExecutableFile).
  const pythonEntryFile =
    findWorkspaceFileByName(workspace, entryFileName) || projectEntryFile
  const mainContent = projectEntryFile?.content || ''

  onStream?.('status', 'Executing workspace...')

  if (workspaceType === 'python') {
    return runPythonOnDocker(
      workspace,
      pythonEntryFile,
      runServerPython,
      onStream
    )
  }

  if (workspaceType === 'web') {
    const result = await runWorkspace(workspace, projectLanguage)
    return {
      ...result,
      kernelMessage: 'Web Preview Runner',
    }
  }

  if (workspaceType === 'javascript') {
    return runJsKernel(mainContent, onStream)
  }

  // Unknown: preserve previous single-file fallbacks without using file count.
  const executionLanguage = resolveExecutionLanguage(mainContent, projectLanguage)

  if (isFrontendLanguage(executionLanguage)) {
    if (executionLanguage === 'javascript') {
      return runJsKernel(mainContent, onStream)
    }

    const result = await runFrontendCode(mainContent, executionLanguage)
    return {
      ...result,
      kernelMessage: 'Web Preview Runner',
    }
  }

  if (projectLanguage === 'python' || executionLanguage === 'python') {
    return runPythonOnDocker(
      workspace,
      pythonEntryFile,
      runServerPython,
      onStream
    )
  }

  if (runServerPython) {
    return runServerPython({
      files: workspace.files || [],
      entryFileName: projectEntryFile?.name || 'main.py',
      code: mainContent,
    })
  }

  return {
    stdout: '',
    stderr: 'نوع التنفيذ غير مدعوم لهذه اللغة.',
    returnValue: '',
    status: 'error',
    previewHtml: null,
    hasPreview: false,
    kernelMessage: 'Code Runner',
  }
}

export function getKernelLabel(projectLanguage, workspace) {
  const workspaceType = detectWorkspaceType(workspace, projectLanguage)

  if (workspaceType === 'python') {
    return 'Docker Python'
  }

  if (workspaceType === 'web') {
    return 'Web Preview Runner'
  }

  if (workspaceType === 'javascript') {
    return 'JavaScript Kernel'
  }

  const mainFile = getMainExecutableFile(workspace, projectLanguage)
  const language = detectLanguageFromFile(mainFile, projectLanguage)

  if (language === 'python' || projectLanguage === 'python') {
    return 'Docker Python'
  }

  if (isFrontendLanguage(language)) {
    return 'Web Preview Runner'
  }

  return 'Code Runner'
}
