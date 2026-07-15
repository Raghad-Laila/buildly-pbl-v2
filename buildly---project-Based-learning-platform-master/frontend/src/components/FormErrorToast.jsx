import React, { useEffect } from 'react'
import { focusFormField } from '../utils/formFeedback'
import './FormErrorToast.css'

const FormErrorToast = ({ message, field = null, onDismiss }) => {
  useEffect(() => {
    if (!message) return undefined

    const timer = window.setTimeout(() => {
      focusFormField(field)
    }, 40)

    return () => window.clearTimeout(timer)
  }, [message, field])

  if (!message) return null

  return (
    <div className="form-error-toast" role="alert" aria-live="assertive">
      <div className="form-error-toast-body">
        <span className="form-error-toast-icon" aria-hidden="true">
          !
        </span>
        <div className="form-error-toast-content">
          <strong>تحقق من الحقول</strong>
          <p>{message}</p>
        </div>
        {onDismiss && (
          <button
            type="button"
            className="form-error-toast-close"
            onClick={onDismiss}
            aria-label="إغلاق"
          >
            ×
          </button>
        )}
      </div>
    </div>
  )
}

export default FormErrorToast
