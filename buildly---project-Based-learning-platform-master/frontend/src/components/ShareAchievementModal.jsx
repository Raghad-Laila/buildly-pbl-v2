import React, { useMemo, useState } from 'react'
import {
  buildAchievementShareContent,
  canUseNativeShare,
  copyAchievementText,
  getAchievementShareLinks,
  shareAchievementNatively,
} from '../utils/shareAchievement'
import './ShareAchievementModal.css'

const SHARE_OPTIONS = [
  { id: 'whatsapp', label: 'واتساب', icon: '💬', color: '#22c55e' },
  { id: 'twitter', label: 'X', icon: '𝕏', color: '#111827' },
  { id: 'facebook', label: 'فيسبوك', icon: 'f', color: '#1877f2' },
  { id: 'linkedin', label: 'لينكدإن', icon: 'in', color: '#0a66c2' },
  { id: 'telegram', label: 'تيليغرام', icon: '✈️', color: '#229ed9' },
  { id: 'email', label: 'بريد', icon: '✉️', color: '#64748b' },
]

const ShareAchievementModal = ({
  project,
  progress,
  learnerName,
  onClose,
}) => {
  const [copyMessage, setCopyMessage] = useState('')
  const [sharingNative, setSharingNative] = useState(false)

  const shareContent = useMemo(() => {
    const projectUrl = `${window.location.origin}/projects/${project.project_id || project.id}`

    return buildAchievementShareContent({
      projectTitle: project.title,
      courseTitle: project.course_title,
      languageDisplay: project.language_display,
      levelDisplay: project.level_display,
      completedAt: progress?.completed_at,
      learnerName,
      projectUrl,
    })
  }, [project, progress, learnerName])

  const shareLinks = useMemo(
    () => getAchievementShareLinks(shareContent),
    [shareContent]
  )

  const openShareLink = (platformId) => {
    const url = shareLinks[platformId]
    if (!url) return
    window.open(url, '_blank', 'noopener,noreferrer,width=640,height=720')
  }

  const handleNativeShare = async () => {
    try {
      setSharingNative(true)
      await shareAchievementNatively(shareContent)
      onClose?.()
    } catch (err) {
      if (err?.name !== 'AbortError') {
        setCopyMessage('تعذر فتح مشاركة الجهاز')
      }
    } finally {
      setSharingNative(false)
    }
  }

  const handleCopy = async () => {
    try {
      const copied = await copyAchievementText(shareContent)
      setCopyMessage(copied ? 'تم نسخ نص الإنجاز' : 'تعذر النسخ')
    } catch (err) {
      setCopyMessage('تعذر النسخ')
    }
  }

  return (
    <div className="share-modal-overlay" onClick={onClose}>
      <div
        className="share-modal"
        onClick={(event) => event.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="share-modal-title"
      >
        <div className="share-modal-header">
          <div>
            <h2 id="share-modal-title">مشاركة الإنجاز</h2>
            <p>شارك إتمام مشروع «{project.title}» على منصات التواصل</p>
          </div>
          <button type="button" className="share-modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="share-preview-card">
          <span className="share-preview-badge">مشروع مكتمل</span>
          <h3>{project.title}</h3>
          <p>{shareContent.message}</p>
        </div>

        <div className="share-platforms-grid">
          {SHARE_OPTIONS.map((option) => (
            <button
              key={option.id}
              type="button"
              className="share-platform-btn"
              style={{ '--platform-color': option.color }}
              onClick={() => openShareLink(option.id)}
            >
              <span className="share-platform-icon">{option.icon}</span>
              <span>{option.label}</span>
            </button>
          ))}
        </div>

        <div className="share-modal-actions">
          {canUseNativeShare() && (
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleNativeShare}
              disabled={sharingNative}
            >
              {sharingNative ? 'جاري المشاركة...' : 'مشاركة عبر الجهاز'}
            </button>
          )}
          <button type="button" className="btn btn-secondary" onClick={handleCopy}>
            نسخ النص
          </button>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            إغلاق
          </button>
        </div>

        {copyMessage && <div className="share-copy-message">{copyMessage}</div>}
      </div>
    </div>
  )
}

export default ShareAchievementModal
