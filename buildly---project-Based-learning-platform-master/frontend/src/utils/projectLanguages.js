export const FRONTEND_LANGUAGE_OPTIONS = [
  { value: 'html', label: 'HTML' },
  { value: 'css', label: 'CSS' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'json', label: 'JSON' },
  { value: 'react', label: 'React' },
  { value: 'vue', label: 'Vue.js' },
  { value: 'angular', label: 'Angular' },
  { value: 'svelte', label: 'Svelte' },
  { value: 'nextjs', label: 'Next.js' },
  { value: 'nuxt', label: 'Nuxt.js' },
  { value: 'sass', label: 'Sass' },
  { value: 'scss', label: 'SCSS' },
  { value: 'less', label: 'Less' },
  { value: 'tailwind', label: 'Tailwind CSS' },
  { value: 'bootstrap', label: 'Bootstrap' },
  { value: 'jquery', label: 'jQuery' },
]

export const OTHER_LANGUAGE_OPTIONS = [
  { value: 'python', label: 'Python' },
  { value: 'java', label: 'Java' },
  { value: 'csharp', label: 'C#' },
  { value: 'cpp', label: 'C++' },
  { value: 'php', label: 'PHP' },
  { value: 'ruby', label: 'Ruby' },
  { value: 'go', label: 'Go' },
  { value: 'swift', label: 'Swift' },
  { value: 'kotlin', label: 'Kotlin' },
  { value: 'dart', label: 'Dart' },
  { value: 'rust', label: 'Rust' },
  { value: 'other', label: 'أخرى' },
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
