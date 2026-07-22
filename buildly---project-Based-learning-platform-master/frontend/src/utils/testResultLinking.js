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

export function linkResultsByTask(stories, tests, testResults) {
  const results = testResults?.results || []
  const resultsByTestId = new Map()

  for (const result of results) {
    if (result?.id != null) {
      resultsByTestId.set(result.id, result)
    }
  }

  const storyList = stories || []
  const testList = tests || []

  return storyList.map((story) => {
    const linkedTests = testList.filter((test) => test?.task === story.id)

    if (!linkedTests.length) {
      return { ...story, testStatus: null }
    }

    const linkedResults = linkedTests.map((test) => resultsByTestId.get(test.id))

    if (linkedResults.some((result) => result == null)) {
      return { ...story, testStatus: null }
    }

    if (linkedResults.some((result) => !result.passed)) {
      return { ...story, testStatus: 'failed' }
    }

    return { ...story, testStatus: 'passed' }
  })
}
