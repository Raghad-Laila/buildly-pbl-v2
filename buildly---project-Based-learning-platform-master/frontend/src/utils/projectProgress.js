export function getProjectTestProgress(tests = [], testResults = null) {
  const total = tests.length

  if (!total) {
    return {
      percentage: 0,
      passed: 0,
      total: 0,
      allPassed: false,
      hasTests: false,
    }
  }

  if (!testResults?.summary) {
    return {
      percentage: 0,
      passed: 0,
      total,
      allPassed: false,
      hasTests: true,
    }
  }

  const passed = testResults.summary.passed || 0
  const percentage = Math.round((passed / total) * 100)
  const allPassed = passed === total

  return {
    percentage,
    passed,
    total,
    allPassed,
    hasTests: true,
  }
}
