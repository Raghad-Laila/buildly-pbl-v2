export function linkResultsByIndex(items, testResults) {
  const results = testResults?.results || []

  if (!results.length) {
    return items.map((item) => ({ ...item, testStatus: null }))
  }

  return items.map((item, index) => {
    const linkedIndex = item.index ?? index
    const result = results[linkedIndex]

    if (!result) {
      return { ...item, testStatus: null }
    }

    return {
      ...item,
      testStatus: result.passed ? 'passed' : 'failed',
    }
  })
}
