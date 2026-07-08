export const FRONTEND_LANGUAGE_OPTIONS = [
  { value: 'html', label: 'HTML' },
  { value: 'css', label: 'CSS' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'react', label: 'React' },
]

export const OTHER_LANGUAGE_OPTIONS = [
  { value: 'python', label: 'Python' },
]

export const ALL_LANGUAGE_OPTIONS = [
  ...FRONTEND_LANGUAGE_OPTIONS,
  ...OTHER_LANGUAGE_OPTIONS,
]

const LANGUAGE_LABELS = Object.fromEntries(
  ALL_LANGUAGE_OPTIONS.map((option) => [option.value, option.label])
)

export function getProjectLanguages(project) {
  if (project?.languages?.length) {
    return project.languages
  }
  if (project?.language) {
    return [project.language]
  }
  return ['python']
}

export function getPrimaryProjectLanguage(project) {
  return getProjectLanguages(project)[0] || 'python'
}

export function getProjectLanguagesDisplay(project) {
  if (project?.languages_display?.length) {
    return project.languages_display
  }

  return getProjectLanguages(project).map(
    (code) => LANGUAGE_LABELS[code] || code
  )
}

export function formatProjectLanguages(project) {
  return getProjectLanguagesDisplay(project).join(' · ')
}
