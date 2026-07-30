import { isFrontendLanguage } from './frontendCodeRunner'

function collectWorkspaceText(workspace) {
  return (workspace?.files || [])
    .map((file) => String(file?.content || ''))
    .join('\n')
    .trim()
}

export function looksLikePythonSource(text) {
  const t = String(text || '')
  if (!t.trim()) return false

  const hits = [
    /(?:^|\n)\s*def\s+\w+\s*\(/m,
    /(?:^|\n)\s*class\s+\w+\s*:/m,
    /(?:^|\n)\s*print\s*\(/m,
    /(?:^|\n)\s*from\s+\w[\w.]*\s+import\s+/m,
    /(?:^|\n)\s*import\s+\w+/m,
    /if\s+__name__\s*==\s*['"]__main__['"]/,
  ].filter((pattern) => pattern.test(t)).length

  return hits >= 1
}

export function looksLikeFrontendSource(text) {
  const t = String(text || '')
  if (!t.trim()) return false

  return (
    /<!DOCTYPE\s+html/i.test(t) ||
    /<html[\s>]/i.test(t) ||
    /<\/?(div|body|head|script|style|form|input|button|h[1-6]|p|span|section|main|nav)\b/i.test(
      t
    ) ||
    /(?:^|\n)\s*(const|let|var|function)\s+/m.test(t) ||
    /console\.log\s*\(/.test(t) ||
    /document\.(getElementById|querySelector|addEventListener)/.test(t) ||
    /(?:^|\n)\s*[.#]?[\w-]+\s*\{[^}]*:[^}]*\}/m.test(t)
  )
}

/** Java / C# / C++ style that students often paste into Python labs. */
export function looksLikeJavaOrCStyle(text) {
  const t = String(text || '')
  if (!t.trim()) return false

  return (
    /(?:^|\n)\s*(?:public\s+|private\s+|protected\s+)?(?:class|interface|enum)\s+\w+\s*\{/m.test(
      t
    ) ||
    /public\s+static\s+void\s+main\s*\(/.test(t) ||
    /System\.out\./.test(t) ||
    /import\s+java\./.test(t) ||
    /#include\s*[<"]/.test(t) ||
    /Console\.Write(?:Line)?\s*\(/.test(t) ||
    /std::\w+/.test(t)
  )
}

function mismatchResult(message) {
  return {
    stdout: '',
    stderr: '',
    error: message,
    returnValue: '',
    status: 'error',
    previewHtml: null,
    hasPreview: false,
    kernelMessage: 'Language Check',
  }
}

/**
 * Returns a polite execution error result when workspace content clearly
 * does not match the project language family. Returns null when OK to run.
 */
export function getLanguageMismatchResult(workspace, projectLanguage) {
  const sample = collectWorkspaceText(workspace)
  if (!sample) return null

  const lang = projectLanguage || 'python'

  if (lang === 'python') {
    if (looksLikeJavaOrCStyle(sample) && !looksLikePythonSource(sample)) {
      return mismatchResult(
        'لغة غير مدعومة في هذا المشروع.\nيقتصر التنفيذ هنا على Python فقط. يُرجى كتابة كود Python صالح ثم إعادة التشغيل.'
      )
    }

    // Strong frontend dump into a Python lab (no Python signals).
    if (looksLikeFrontendSource(sample) && !looksLikePythonSource(sample)) {
      return mismatchResult(
        'لغة غير مدعومة في هذا المشروع.\nيقتصر التنفيذ هنا على Python فقط. يُرجى كتابة كود Python صالح ثم إعادة التشغيل.'
      )
    }

    return null
  }

  if (isFrontendLanguage(lang)) {
    // Python (or other backend) pasted into a frontend path project.
    if (looksLikePythonSource(sample) && !looksLikeFrontendSource(sample)) {
      return mismatchResult(
        'لغة غير مدعومة في هذا المشروع.\nيقتصر التنفيذ هنا على تقنيات الواجهة الأمامية (HTML و CSS و JavaScript). يُرجى إدخال كود متوافق مع متطلبات المشروع ثم إعادة التشغيل.'
      )
    }

    if (looksLikeJavaOrCStyle(sample) && !looksLikeFrontendSource(sample)) {
      return mismatchResult(
        'لغة غير مدعومة في هذا المشروع.\nيقتصر التنفيذ هنا على تقنيات الواجهة الأمامية (HTML و CSS و JavaScript). يُرجى إدخال كود متوافق مع متطلبات المشروع ثم إعادة التشغيل.'
      )
    }

    return null
  }

  return null
}
