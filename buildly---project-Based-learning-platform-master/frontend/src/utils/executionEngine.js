import {
  bundleWorkspaceFiles,
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
import { runPythonKernel } from './pythonKernel'

function workspaceHasWebBundle(workspace) {
  return Boolean(bundleWorkspaceFiles(workspace.files))
}

export async function executeWorkspace(workspace, projectLanguage, options = {}) {
  const { onStream, runServerPython } = options
  const mainFile = getMainExecutableFile(workspace, projectLanguage)
  const mainContent = mainFile?.content || ''
  const executionLanguage = resolveExecutionLanguage(mainContent, projectLanguage)

  onStream?.('status', 'جاري التنفيذ...')

  if (workspaceHasWebBundle(workspace) || workspace.files.length > 1) {
    const result = await runWorkspace(workspace, projectLanguage)
    return {
      ...result,
      kernelMessage: 'Web preview engine',
    }
  }

  if (isFrontendLanguage(executionLanguage)) {
    if (executionLanguage === 'javascript') {
      return runJsKernel(mainContent, onStream)
    }

    const result = await runFrontendCode(mainContent, executionLanguage)
    return {
      ...result,
      kernelMessage: 'Frontend runtime',
    }
  }

  if (projectLanguage === 'python' || executionLanguage === 'python') {
    try {
      return await runPythonKernel(mainContent, onStream)
    } catch (kernelError) {
      if (runServerPython) {
        onStream?.('status', 'التحويل إلى تنفيذ السيرفر...')
        return runServerPython(mainContent)
      }

      throw kernelError
    }
  }

  if (runServerPython) {
    return runServerPython(mainContent)
  }

  return {
    stdout: '',
    stderr: 'نوع التنفيذ غير مدعوم لهذه اللغة.',
    returnValue: '',
    status: 'error',
    previewHtml: null,
    hasPreview: false,
  }
}

export function getKernelLabel(projectLanguage, workspace) {
  const mainFile = getMainExecutableFile(workspace, projectLanguage)
  const language = detectLanguageFromFile(mainFile, projectLanguage)

  if (workspaceHasWebBundle(workspace) || workspace.files.length > 1) {
    return 'Web Preview'
  }

  if (language === 'python' || projectLanguage === 'python') {
    return 'Python Kernel'
  }

  if (isFrontendLanguage(language)) {
    return 'Browser Runtime'
  }

  return 'Code Runner'
}
