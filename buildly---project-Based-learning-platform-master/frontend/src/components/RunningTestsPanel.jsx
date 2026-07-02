import React from 'react'
import './RunningTestsPanel.css'

export const normalizeTestResult = (result) => {
  const error = (result.error || result.stderr || '').trim()
  const message = (result.message || '').trim()

  return {
    ...result,
    icon: result.passed ? '✔' : '✘',
    statusLabel: result.passed ? 'نجح' : 'فشل',
    displayMessage: result.passed
      ? message || 'نجح الاختبار'
      : message || 'فشل الاختبار',
    errorMessage: !result.passed && error && error !== message ? error : null,
  }
}

const RunningTestsPanel = ({
  running = false,
  testError = '',
  testResults = null,
  testsCount = 0,
}) => {
  const hasRun = Boolean(testResults)
  const results = (testResults?.results || []).map(normalizeTestResult)
  const summary = testResults?.summary

  return (
    <section className="fcc-section fcc-tests-section">
      <h2 className="fcc-section-title">Running Tests</h2>
      <div className="fcc-section-body">
        {running && (
          <div className="running-tests-loading">
            <span className="execution-spinner" />
            <span>جاري تشغيل الاختبارات...</span>
          </div>
        )}

        {testError && !running && (
          <div className="running-tests-global-error">{testError}</div>
        )}

        {!running && !hasRun && !testError && (
          <div className="running-tests-empty">
            <span className="running-tests-empty-icon" aria-hidden="true">
              ◎
            </span>
            <p>
              {testsCount > 0
                ? 'اضغط Check Code لتشغيل الاختبارات وعرض النتائج.'
                : 'لا توجد اختبارات مُعرَّفة لهذا المشروع بعد.'}
            </p>
          </div>
        )}

        {hasRun && !running && (
          <div className="running-tests-results">
            {summary && (
              <div className="running-tests-summary">
                <span className="running-tests-summary-total">
                  {summary.total} اختبار
                </span>
                <span className="running-tests-summary-passed">
                  {summary.passed} نجح
                </span>
                <span className="running-tests-summary-failed">
                  {summary.failed} فشل
                </span>
              </div>
            )}

            {results.length === 0 ? (
              <p className="running-tests-no-items">لا توجد اختبارات لعرض نتائجها.</p>
            ) : (
              <ul className="running-tests-list">
                {results.map((result, index) => (
                  <li
                    key={result.id ?? `test-${index}`}
                    className={`running-tests-item ${result.passed ? 'is-passed' : 'is-failed'}`}
                  >
                    <div className="running-tests-item-header">
                      <span
                        className="running-tests-item-icon"
                        aria-label={result.statusLabel}
                        title={result.statusLabel}
                      >
                        {result.icon}
                      </span>
                      <span className="running-tests-item-name">{result.name}</span>
                    </div>

                    {result.displayMessage && (
                      <p className="running-tests-item-message">{result.displayMessage}</p>
                    )}

                    {result.errorMessage && (
                      <pre className="running-tests-item-error">{result.errorMessage}</pre>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </section>
  )
}

export default RunningTestsPanel
