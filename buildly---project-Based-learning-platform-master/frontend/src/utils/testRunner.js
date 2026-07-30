import { FRONTEND_LANGUAGE_OPTIONS } from './projectLanguages'
import {
  detectLanguageFromFile,
  getMainExecutableFile,
  getWorkspaceFileContent,
} from './codeWorkspace'
import { detectWorkspaceType } from './executionEngine'
import { runHtmlWorkspaceTest } from './htmlTestHelpers'

const CLIENT_TEST_LANGUAGES = new Set(
  FRONTEND_LANGUAGE_OPTIONS.map((option) => option.value)
)

const JS_TEST_LANGUAGE_HINTS = ['react', 'javascript', 'typescript']

const HTML_CSS_HELPER_CALL =
  /\b(getEl|getDoc|getText|htmlHasStructure|htmlHasTagContent|htmlHasText|isDescendantOf|getFormInputs|getFormRadios|getFormCheckboxes|cssHasDeclaration|cssHasAttributeSelector|cssAttrRuleHasProperty|cssHasRowAttrSelector|getTableBodyRows|getTableHeadings|hasNumericAttr|submitTypeIsValid|cardHasInlineSize|normalizeCss|cssBlocks)\s*\(/

const HTML_CSS_VAR_USAGE =
  /\bhtml\s*\.|\bcss\s*\.|\bhtml\s*includes|\bcss\s*includes/

function isJsLikeTestFile(file, projectLanguage = 'javascript') {
  if (!file?.name) return false
  const language = detectLanguageFromFile(file, projectLanguage)
  return (
    language === 'javascript' ||
    language === 'typescript' ||
    language === 'react'
  )
}

// CHECK CODE ROUTING — prefer helper calls / html|css variable usage over loose words.
function inferClientTestRunnerHeuristic(testCode = '') {
  const code = String(testCode || '')

  if (HTML_CSS_HELPER_CALL.test(code) || HTML_CSS_VAR_USAGE.test(code)) {
    return 'html-css-workspace'
  }

  return 'javascript-source'
}

// CHECK CODE ROUTING
export function classifyClientTest(test = {}) {
  const explicit =
    test.execution_mode || test.runner_mode || test.client_runner

  if (explicit === 'html-css-workspace' || explicit === 'javascript-source') {
    return explicit
  }

  return inferClientTestRunnerHeuristic(test.test_code)
}

// CHECK CODE ROUTING — language hint only; filenames come from getMainExecutableFile.
export function pickJsTestLanguageHint(languages = []) {
  for (const hint of JS_TEST_LANGUAGE_HINTS) {
    if (languages.includes(hint)) {
      return hint
    }
  }
  return 'javascript'
}

// CHECK CODE ROUTING — reuses codeWorkspace file selection; validates JS-like result.
function pickJsTestSourceFile(workspace, languages = []) {
  const hints = JS_TEST_LANGUAGE_HINTS.filter((hint) => languages.includes(hint))
  if (!hints.length) {
    hints.push('javascript')
  }

  for (const hint of hints) {
    const file = getMainExecutableFile(workspace, hint)
    if (file && isJsLikeTestFile(file, hint)) {
      return file
    }
  }

  for (const file of workspace?.files || []) {
    if (isJsLikeTestFile(file, pickJsTestLanguageHint(languages))) {
      return file
    }
  }

  return null
}

function resolveLanguages(options = {}) {
  const { languages, projectLanguage } = options
  if (Array.isArray(languages) && languages.length) {
    return languages
  }
  if (projectLanguage) {
    return [projectLanguage]
  }
  return ['python']
}

function resolveWorkspaceHtml(workspace) {
  const exact = getWorkspaceFileContent(workspace, 'index.html')
  if (String(exact || '').trim()) return exact

  const file = (workspace?.files || []).find((item) =>
    /\.html?$/i.test(item?.name || '')
  )
  return file?.content || ''
}

function resolveWorkspaceCss(workspace) {
  const exact = getWorkspaceFileContent(workspace, 'style.css')
  if (String(exact || '').trim()) return exact

  const preferred = (workspace?.files || []).find((item) =>
    /(^|\/)styles?\.css$/i.test(item?.name || '')
  )
  if (preferred) return preferred.content || ''

  const cssFiles = (workspace?.files || []).filter((item) =>
    /\.css$/i.test(item?.name || '')
  )
  if (!cssFiles.length) return ''
  if (cssFiles.length === 1) return cssFiles[0].content || ''
  return cssFiles.map((file) => file.content || '').join('\n')
}

/** Prefer main.py with content; otherwise first non-empty .py file. */
export function pickPythonTestEntryFile(workspace) {
  const files = workspace?.files || []
  const main = files.find(
    (file) =>
      String(file?.name || '').toLowerCase() === 'main.py' &&
      String(file?.content || '').trim()
  )
  if (main) return main

  const withContent = files.find(
    (file) =>
      /\.py$/i.test(file?.name || '') && String(file?.content || '').trim()
  )
  if (withContent) return withContent

  return (
    files.find((file) => String(file?.name || '').toLowerCase() === 'main.py') ||
    getMainExecutableFile(workspace, 'python')
  )
}

export function getPythonTestMountFiles(workspace) {
  return (workspace?.files || [])
    .filter((file) => /\.(py|json|txt)$/i.test(file?.name || ''))
    .map((file) => ({
      name: file.name,
      content: file.content || '',
    }))
}

// CHECK CODE ROUTING — project mode via shared detectWorkspaceType; per-test via classifyClientTest.
export function resolveCheckCodePlan({
  languages,
  workspace,
  tests = [],
  projectLanguage,
} = {}) {
  const langs = resolveLanguages({ languages, projectLanguage })
  const hint = langs[0] || 'python'
  const workspaceType = detectWorkspaceType(workspace, hint)

  let mode
  if (workspaceType === 'python') {
    mode = 'server-python'
  } else if (workspaceType === 'web' || workspaceType === 'javascript') {
    mode = 'client'
  } else if (langs.some((language) => CLIENT_TEST_LANGUAGES.has(language))) {
    mode = 'client'
  } else if (langs.includes('python')) {
    mode = 'server-python'
  } else {
    mode = 'unsupported'
  }

  const classifications =
    mode === 'client'
      ? tests.map((test) => ({
          id: test.id,
          runner: classifyClientTest(test),
        }))
      : []

  return {
    mode,
    workspaceType,
    languages: langs,
    classifications,
    needsWorkspaceHtmlCss: classifications.some(
      (item) => item.runner === 'html-css-workspace'
    ),
    needsJsSource: classifications.some(
      (item) => item.runner === 'javascript-source'
    ),
  }
}

export function usesWorkspaceFileTests(projectLanguage) {
  return projectLanguage === 'html' || projectLanguage === 'css'
}

export function shouldUseWorkspaceFileTests(projectLanguage, tests = []) {
  // CHECK CODE ROUTING — suite gate from per-test classification (no primary-language force).
  if (!tests.length && usesWorkspaceFileTests(projectLanguage)) {
    return true
  }

  return tests.some(
    (test) => classifyClientTest(test) === 'html-css-workspace'
  )
}

export function canRunTestsOnClient(language) {
  return CLIENT_TEST_LANGUAGES.has(language)
}

export function runClientTests(code, tests = [], options = {}) {
  const { workspace, projectLanguage, languages } = options
  const langs = resolveLanguages({ languages, projectLanguage })

  const html = workspace ? resolveWorkspaceHtml(workspace) : ''
  const css = workspace ? resolveWorkspaceCss(workspace) : ''

  const results = tests.map((test) => {
    try {
      // CHECK CODE ROUTING
      const runnerKind = classifyClientTest(test)

      if (runnerKind === 'html-css-workspace' && workspace) {
        runHtmlWorkspaceTest(html, css, test.test_code || '')
      } else {
        let source = code || ''
        if (workspace) {
          const sourceFile = pickJsTestSourceFile(workspace, langs)
          if (sourceFile?.content != null && String(sourceFile.content).trim()) {
            source = sourceFile.content
          }
        }

        const combinedCode = `${source}\n\n${test.test_code || ''}`.trim()
        const runner = new Function(combinedCode)
        runner()
      }

      return {
        id: test.id,
        name: test.name,
        passed: true,
        message: test.success_message || 'نجح الاختبار',
        error: '',
        stdout: '',
        stderr: '',
      }
    } catch (error) {
      const errorText = error?.message || 'فشل الاختبار'
      const failureMessage = test.failure_message || errorText

      return {
        id: test.id,
        name: test.name,
        passed: false,
        message: failureMessage,
        error: test.failure_message ? errorText : '',
        stdout: '',
        stderr: errorText,
      }
    }
  })

  const passed = results.filter((item) => item.passed).length

  return {
    results,
    summary: {
      total: results.length,
      passed,
      failed: results.length - passed,
    },
  }
}
