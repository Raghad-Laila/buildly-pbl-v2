import React from 'react'
import './AiReviewDrawer.css'

const SEVERITY_LABELS = {
  High: 'مرتفع',
  Medium: 'متوسط',
  Low: 'منخفض',
}

const CATEGORY_LABELS = {
  Logic: 'المنطق',
  Security: 'الأمان',
  Performance: 'الأداء',
  Maintainability: 'قابلية الصيانة',
  Readability: 'قابلية القراءة',
}

const normalizeSeverity = (severity) => {
  const value = String(severity || '').trim()
  const key = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase()
  if (key === 'High' || key === 'Medium' || key === 'Low') return key
  return value || 'Medium'
}

const severityClass = (severity) => {
  const key = normalizeSeverity(severity).toLowerCase()
  if (key === 'high') return 'is-high'
  if (key === 'low') return 'is-low'
  return 'is-medium'
}

const AiReviewDrawer = ({
  open = false,
  loading = false,
  error = '',
  review = null,
  failedTestsCount = 0,
  onClose,
}) => {
  if (!open) return null

  const score = Number(review?.overall_score)
  const hasScore = Number.isFinite(score)
  const clampedScore = hasScore ? Math.max(0, Math.min(100, score)) : 0
  const strengths = Array.isArray(review?.strengths) ? review.strengths : []
  const issues = Array.isArray(review?.issues) ? review.issues : []
  const hasFailedTests = Number(failedTestsCount) > 0
  const showSuccessEmpty =
    Boolean(review) &&
    !loading &&
    !error &&
    issues.length === 0 &&
    !hasFailedTests
  const showFailedTestsGuard =
    Boolean(review) &&
    !loading &&
    !error &&
    issues.length === 0 &&
    hasFailedTests

  return (
    <aside
      className="ai-review-drawer"
      dir="rtl"
      role="complementary"
      aria-label="مساعد التعلم الذكي"
    >
      <header className="ai-review-drawer-header">
        <div className="ai-review-drawer-title-wrap">
          <h2 className="ai-review-drawer-title">🤖 مساعد التعلم الذكي</h2>
          <p className="ai-review-drawer-subtitle">مراجعة تعليمية لكودك</p>
        </div>
        <button
          type="button"
          className="ai-review-drawer-close"
          onClick={onClose}
          aria-label="إغلاق"
        >
          ×
        </button>
      </header>

      <div className="ai-review-drawer-body">
        {loading && (
          <div className="ai-review-loading">
            <span className="execution-spinner" />
            <span>جاري تحليل الكود...</span>
          </div>
        )}

        {!loading && error && (
          <div className="ai-review-error" role="alert">
            {error}
          </div>
        )}

        {!loading && !error && review && (
          <>
            <section className="ai-review-score-section">
              <h3 className="ai-review-section-label">جودة الكود الإجمالية</h3>
              <div
                className="ai-review-score-ring"
                style={{
                  background: `conic-gradient(#38bdf8 ${clampedScore * 3.6}deg, #2a2a40 0deg)`,
                }}
                aria-label={`الدرجة ${clampedScore} بالمئة`}
              >
                <div className="ai-review-score-inner">
                  <span className="ai-review-score-value">{clampedScore}%</span>
                </div>
              </div>
            </section>

            {review.summary && (
              <section className="ai-review-section">
                <h3 className="ai-review-section-label">الملخص</h3>
                <p className="ai-review-summary">{review.summary}</p>
              </section>
            )}

            <section className="ai-review-section">
              <h3 className="ai-review-section-label">✨ نقاط القوة</h3>
              {strengths.length > 0 ? (
                <ul className="ai-review-strengths">
                  {strengths.map((item, index) => (
                    <li key={`strength-${index}`}>{item}</li>
                  ))}
                </ul>
              ) : (
                <p className="ai-review-empty-note">لم تُذكر نقاط قوة إضافية.</p>
              )}
            </section>

            <section className="ai-review-section">
              <h3 className="ai-review-section-label">⚠ المشكلات</h3>

              {showSuccessEmpty ? (
                <div className="ai-review-success-state">
                  <span className="ai-review-success-icon" aria-hidden="true">
                    🎉
                  </span>
                  <p className="ai-review-success-title">عمل ممتاز!</p>
                  <p className="ai-review-success-text">
                    لم يتم العثور على مشكلات مهمة.
                  </p>
                </div>
              ) : showFailedTestsGuard ? (
                <div className="ai-review-failed-tests-state">
                  <p className="ai-review-success-title">ما زالت هناك اختبارات فاشلة</p>
                  <p className="ai-review-success-text">
                    لا يمكن اعتبار الحل مكتملاً بينما تفشل متطلبات Check Code.
                    راجع رسائل الاختبارات والمتطلبات الفاشلة ثم أعد المحاولة.
                  </p>
                </div>
              ) : (
                <div className="ai-review-issues">
                  {issues.map((issue, index) => {
                    const severity = normalizeSeverity(issue.severity)
                    return (
                      <article
                        key={issue.id ?? `issue-${index}`}
                        className={`ai-review-issue-card ${severityClass(severity)}`}
                      >
                        <div className="ai-review-issue-meta">
                          <span className="ai-review-issue-category">
                            {CATEGORY_LABELS[issue.category] || issue.category || 'عام'}
                          </span>
                          <span className={`ai-review-issue-severity ${severityClass(severity)}`}>
                            {SEVERITY_LABELS[severity] || severity}
                          </span>
                        </div>

                        <h4 className="ai-review-issue-title">
                          {issue.title || 'مشكلة'}
                        </h4>

                        <div className="ai-review-issue-location">
                          <span>{issue.file || 'ملف غير محدد'}</span>
                          {issue.line != null && (
                            <span>السطر {issue.line}</span>
                          )}
                        </div>

                        {issue.explanation && (
                          <div className="ai-review-issue-block">
                            <span className="ai-review-issue-block-label">الشرح</span>
                            <p>{issue.explanation}</p>
                          </div>
                        )}

                        {issue.hint && (
                          <div className="ai-review-issue-block is-hint">
                            <span className="ai-review-issue-block-label">تلميح</span>
                            <p>{issue.hint}</p>
                          </div>
                        )}
                      </article>
                    )
                  })}
                </div>
              )}
            </section>
          </>
        )}
      </div>
    </aside>
  )
}

export default AiReviewDrawer
