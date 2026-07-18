import React from 'react'
import './CodeQualityDrawer.css'

const asList = (value) => (Array.isArray(value) ? value.filter(Boolean) : [])

const CodeQualityDrawer = ({
  open = false,
  loading = false,
  error = '',
  review = null,
  onClose,
}) => {
  if (!open) return null

  const score = Number(review?.score)
  const hasScore = Number.isFinite(score)
  const clampedScore = hasScore ? Math.max(0, Math.min(100, score)) : 0
  const strengths = asList(review?.strengths)
  const cleanCodeTips = asList(review?.clean_code_tips)
  const performanceTips = asList(review?.performance_tips)
  const complexity = review?.complexity || {}
  const timeComplexity = complexity.time || ''
  const spaceComplexity = complexity.space || ''

  return (
    <aside
      className="code-quality-drawer"
      dir="rtl"
      role="complementary"
      aria-label="تحسين الكود بالذكاء الاصطناعي"
    >
      <header className="code-quality-drawer-header">
        <div className="code-quality-drawer-title-wrap">
          <h2 className="code-quality-drawer-title">✨ تحسين الكود بالذكاء الاصطناعي</h2>
          <p className="code-quality-drawer-subtitle">
            تقرير جودة بعد نجاح الاختبارات
          </p>
        </div>
        <button
          type="button"
          className="code-quality-drawer-close"
          onClick={onClose}
          aria-label="إغلاق"
        >
          ×
        </button>
      </header>

      <div className="code-quality-drawer-body">
        {loading && (
          <div className="code-quality-loading">
            <span className="execution-spinner" />
            <span>جاري تحليل جودة الكود...</span>
          </div>
        )}

        {!loading && error && (
          <div className="code-quality-error" role="alert">
            {error}
          </div>
        )}

        {!loading && !error && review && (
          <>
            <section className="code-quality-score-section">
              <h3 className="code-quality-section-label">درجة جودة الكود</h3>
              <div
                className="code-quality-score-ring"
                style={{
                  background: `conic-gradient(#34d399 ${clampedScore * 3.6}deg, #1f3a2e 0deg)`,
                }}
                aria-label={`الدرجة ${clampedScore} بالمئة`}
              >
                <div className="code-quality-score-inner">
                  <span className="code-quality-score-value">{clampedScore}%</span>
                </div>
              </div>
            </section>

            {review.summary && (
              <section className="code-quality-section">
                <h3 className="code-quality-section-label">الملخص</h3>
                <p className="code-quality-summary">{review.summary}</p>
              </section>
            )}

            <section className="code-quality-section">
              <h3 className="code-quality-section-label">التعقيد (Complexity)</h3>
              <div className="code-quality-complexity-grid">
                <article className="code-quality-complexity-card">
                  <h4>Time Complexity</h4>
                  <p>{timeComplexity || 'غير متوفر'}</p>
                </article>
                <article className="code-quality-complexity-card">
                  <h4>Space Complexity</h4>
                  <p>{spaceComplexity || 'غير متوفر'}</p>
                </article>
              </div>
            </section>

            <section className="code-quality-section">
              <h3 className="code-quality-section-label">نقاط القوة</h3>
              {strengths.length > 0 ? (
                <ul className="code-quality-list">
                  {strengths.map((item, index) => (
                    <li key={`quality-strength-${index}`}>{item}</li>
                  ))}
                </ul>
              ) : (
                <p className="code-quality-empty-note">لم تُذكر نقاط قوة إضافية.</p>
              )}
            </section>

            <section className="code-quality-section">
              <h3 className="code-quality-section-label">نصائح الكود النظيف</h3>
              {cleanCodeTips.length > 0 ? (
                <ul className="code-quality-list is-tips">
                  {cleanCodeTips.map((item, index) => (
                    <li key={`clean-tip-${index}`}>{item}</li>
                  ))}
                </ul>
              ) : (
                <p className="code-quality-empty-note">لا توجد نصائح إضافية حالياً.</p>
              )}
            </section>

            <section className="code-quality-section">
              <h3 className="code-quality-section-label">تحسينات الأداء</h3>
              {performanceTips.length > 0 ? (
                <ul className="code-quality-list is-performance">
                  {performanceTips.map((item, index) => (
                    <li key={`perf-tip-${index}`}>{item}</li>
                  ))}
                </ul>
              ) : (
                <p className="code-quality-empty-note">لا توجد اقتراحات أداء إضافية حالياً.</p>
              )}
            </section>
          </>
        )}
      </div>
    </aside>
  )
}

export default CodeQualityDrawer
