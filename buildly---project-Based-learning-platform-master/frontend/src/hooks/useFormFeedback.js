import { useCallback, useState } from 'react'
import {
  clearFieldErrorHighlights,
  focusFirstInvalidField,
  focusFormField,
  resolveFieldKeyFromMessage,
} from '../utils/formFeedback'

/**
 * Shared form feedback: toast + scroll-to-field + highlight.
 */
export default function useFormFeedback() {
  const [error, setErrorState] = useState('')
  const [errorField, setErrorField] = useState(null)

  const clearError = useCallback(() => {
    setErrorState('')
    setErrorField(null)
    clearFieldErrorHighlights()
  }, [])

  const setError = useCallback((message, field = null) => {
    if (!message) {
      setErrorState('')
      setErrorField(null)
      clearFieldErrorHighlights()
      return
    }

    const resolvedField = field || resolveFieldKeyFromMessage(message)
    clearFieldErrorHighlights()
    setErrorState(message)
    setErrorField(resolvedField)

    if (resolvedField) {
      window.requestAnimationFrame(() => focusFormField(resolvedField))
    } else {
      window.requestAnimationFrame(() => {
        document.querySelector('.alert-error')?.scrollIntoView({
          behavior: 'smooth',
          block: 'center',
        })
      })
    }
  }, [])

  const handleInvalid = useCallback((event) => {
    event.preventDefault()

    // Only guide the user to the first invalid field in this submit attempt
    if (document.querySelector('.field-has-error')) return

    const target = event.target
    const field =
      target.closest('[data-field]')?.getAttribute('data-field') ||
      target.getAttribute('data-field') ||
      target.id ||
      target.getAttribute('name')

    const message =
      target.validationMessage ||
      'يرجى تعبئة الحقول المطلوبة بشكل صحيح'

    setError(message, field)
  }, [setError])

  const handleFormInvalidCapture = handleInvalid

  return {
    error,
    errorField,
    setError,
    clearError,
    handleInvalid: handleFormInvalidCapture,
    focusFirstInvalidField,
  }
}
