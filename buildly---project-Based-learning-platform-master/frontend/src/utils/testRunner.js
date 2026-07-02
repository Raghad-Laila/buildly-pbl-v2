import { FRONTEND_LANGUAGE_OPTIONS } from './projectLanguages'
import { getWorkspaceFileContent } from './codeWorkspace'

const CLIENT_TEST_LANGUAGES = new Set(
  FRONTEND_LANGUAGE_OPTIONS.map((option) => option.value)
)

export function usesWorkspaceFileTests(projectLanguage) {
  return projectLanguage === 'html' || projectLanguage === 'css'
}

function testCodeUsesWorkspaceVariables(testCode = '') {
  return /\b(html|css)\b/.test(testCode)
}

export function shouldUseWorkspaceFileTests(projectLanguage, tests = []) {
  if (usesWorkspaceFileTests(projectLanguage)) {
    return true
  }

  return tests.some((test) => testCodeUsesWorkspaceVariables(test.test_code))
}

export function canRunTestsOnClient(language) {
  return CLIENT_TEST_LANGUAGES.has(language)
}

export function runClientTests(code, tests = [], options = {}) {
  const { workspace, projectLanguage } = options
  const useWorkspace =
    Boolean(workspace) && shouldUseWorkspaceFileTests(projectLanguage, tests)

  const html = useWorkspace ? getWorkspaceFileContent(workspace, 'index.html') : ''
  const css = useWorkspace ? getWorkspaceFileContent(workspace, 'style.css') : ''

  const results = tests.map((test) => {
    try {
      if (useWorkspace) {
        const runner = new Function('html', 'css', test.test_code || '')
        runner(html, css)
      } else {
        const combinedCode = `${code}\n\n${test.test_code || ''}`.trim()
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
