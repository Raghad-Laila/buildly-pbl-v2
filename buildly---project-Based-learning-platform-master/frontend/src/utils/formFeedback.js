/**
 * Focus a form field / section and scroll it into view.
 * Looks up by [data-field], #id, or [name].
 */
export function focusFormField(fieldKey, { behavior = 'smooth' } = {}) {
  if (!fieldKey || typeof document === 'undefined') return null

  const target =
    document.querySelector(`[data-field="${fieldKey}"]`) ||
    document.getElementById(fieldKey) ||
    document.querySelector(`[name="${fieldKey}"]`)

  if (!target) return null

  const group =
    target.closest('[data-field]') ||
    target.closest('.input-group') ||
    target.closest('.content-section-card') ||
    target.closest('.language-select-section') ||
    target

  group.classList.add('field-has-error')
  group.scrollIntoView({ behavior, block: 'center' })

  const focusable = group.querySelector(
    'input:not([type="hidden"]):not([type="file"]), select, textarea, button'
  )
  if (focusable && typeof focusable.focus === 'function') {
    try {
      focusable.focus({ preventScroll: true })
    } catch {
      focusable.focus()
    }
  }

  window.setTimeout(() => {
    group.classList.remove('field-shake')
    // force reflow so animation can replay
    void group.offsetWidth
    group.classList.add('field-shake')
  }, 0)

  return group
}

export function clearFieldErrorHighlights(root = document) {
  if (!root?.querySelectorAll) return
  root.querySelectorAll('.field-has-error').forEach((el) => {
    el.classList.remove('field-has-error', 'field-shake')
  })
}

/**
 * Map known Arabic/English validation messages to field keys.
 */
export function resolveFieldKeyFromMessage(message = '') {
  const text = String(message).toLowerCase()

  if (text.includes('مجلد البداية') || text.includes('starter')) return 'starter_folder'
  if (text.includes('قصة مستخدم') || text.includes('user stor')) return 'user_stories'
  if (text.includes('لغة') || text.includes('language')) return 'languages'
  if (text.includes('عنوان') || text.includes('title')) return 'title'
  if (text.includes('وصف') || text.includes('description')) return 'description'
  if (text.includes('المسار') || text.includes('course')) return 'course_id'
  if (text.includes('وقت') || text.includes('مدة') || text.includes('duration') || text.includes('estimated')) {
    if (text.includes('مدة')) return 'estimated_duration'
    return 'estimated_time'
  }
  if (text.includes('مستوى') || text.includes('level')) return 'level'
  if (text.includes('فئة') || text.includes('category')) return 'category'
  if (text.includes('هدف') || text.includes('objective')) return 'objective'

  return null
}

export function focusFirstInvalidField(form) {
  if (!form) return null
  const invalid = form.querySelector(':invalid')
  if (!invalid) return null

  const key =
    invalid.getAttribute('data-field') ||
    invalid.id ||
    invalid.getAttribute('name')

  return focusFormField(key || invalid.id)
}
