const encode = (value) => encodeURIComponent(value || '')

export const buildAchievementShareContent = ({
  projectTitle,
  courseTitle,
  languageDisplay,
  levelDisplay,
  completedAt,
  learnerName,
  projectUrl,
}) => {
  const completionDate = completedAt
    ? new Date(completedAt).toLocaleDateString('ar-SY', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : null

  const learnerLine = learnerName ? `أنا ${learnerName} ` : 'لقد '

  const details = [
    courseTitle ? `ضمن مسار «${courseTitle}»` : null,
    languageDisplay ? `بلغة ${languageDisplay}` : null,
    levelDisplay ? `مستوى ${levelDisplay}` : null,
    completionDate ? `بتاريخ ${completionDate}` : null,
  ]
    .filter(Boolean)
    .join(' • ')

  const message = `${learnerLine}أنجزت مشروع «${projectTitle}» على منصة Buildly! 🎉\n${details}\n\n#Buildly #تعلم_برمجة #إنجاز`

  return {
    message,
    url: projectUrl,
    title: `إنجاز مشروع ${projectTitle}`,
    hashtags: 'Buildly,تعلم_برمجة,إنجاز',
  }
}

export const getAchievementShareLinks = (shareContent) => {
  const { message, url, title } = shareContent
  const fullText = `${message}\n${url}`

  return {
    whatsapp: `https://wa.me/?text=${encode(fullText)}`,
    twitter: `https://twitter.com/intent/tweet?text=${encode(message)}&url=${encode(url)}`,
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encode(url)}&quote=${encode(message)}`,
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encode(url)}`,
    telegram: `https://t.me/share/url?url=${encode(url)}&text=${encode(message)}`,
    email: `mailto:?subject=${encode(title)}&body=${encode(fullText)}`,
  }
}

export const canUseNativeShare = () =>
  typeof navigator !== 'undefined' && typeof navigator.share === 'function'

export const shareAchievementNatively = async (shareContent) => {
  if (!canUseNativeShare()) {
    return false
  }

  await navigator.share({
    title: shareContent.title,
    text: shareContent.message,
    url: shareContent.url,
  })

  return true
}

export const copyAchievementText = async (shareContent) => {
  const fullText = `${shareContent.message}\n${shareContent.url}`

  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(fullText)
    return true
  }

  const textarea = document.createElement('textarea')
  textarea.value = fullText
  textarea.setAttribute('readonly', '')
  textarea.style.position = 'absolute'
  textarea.style.left = '-9999px'
  document.body.appendChild(textarea)
  textarea.select()
  const copied = document.execCommand('copy')
  document.body.removeChild(textarea)
  return copied
}
