import React from 'react'
import './TestLinkStatus.css'

const TestLinkStatus = ({ status }) => {
  if (!status) return null

  const isPassed = status === 'passed'

  return (
    <span
      className={`test-link-status ${isPassed ? 'is-passed' : 'is-failed'}`}
      aria-label={isPassed ? 'نجح الاختبار المرتبط' : 'فشل الاختبار المرتبط'}
      title={isPassed ? 'نجح الاختبار المرتبط' : 'فشل الاختبار المرتبط'}
    >
      {isPassed ? '✔' : '✘'}
    </span>
  )
}

export default TestLinkStatus
