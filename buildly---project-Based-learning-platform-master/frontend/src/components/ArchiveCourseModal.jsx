import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { coursesAPI } from '../services/api'
import './ArchiveCourseModal.css'

const getArchiveErrorMessage = (err) => {
  if (!err.response) {
    return 'تعذر الاتصال بالخادم. تأكد أن الخادم يعمل ثم حاول مجدداً.'
  }

  const data = err.response.data
  if (typeof data === 'string') {
    if (data.includes('<!DOCTYPE html>') || data.includes('<html')) {
      if (err.response.status === 404) {
        return 'مسار الأرشفة غير متوفر على الخادم. أوقف الخادم ثم شغّله من جديد: python manage.py runserver'
      }
      return 'حدث خطأ في الخادم. أعد تشغيل الخادم ثم حاول مجدداً.'
    }
    return data
  }

  return (
    data?.message ||
    data?.error ||
    data?.detail ||
    'فشل أرشفة المسار'
  )
}

const ArchiveCourseModal = ({ course, onClose, onSuccess }) => {
  const navigate = useNavigate()
  const [archiving, setArchiving] = useState(false)
  const [error, setError] = useState('')

  const handleCancel = () => {
    onClose?.()
  }

  const handleConfirm = async () => {
    setArchiving(true)
    setError('')

    try {
      const response = await coursesAPI.archive(course.id)
      alert(response.data.message || 'تمت أرشفة المسار بنجاح')
      onClose?.()
      if (onSuccess) {
        onSuccess()
      } else {
        navigate('/courses')
      }
    } catch (err) {
      setError(getArchiveErrorMessage(err))
    } finally {
      setArchiving(false)
    }
  }

  return (
    <div className="archive-modal-overlay" onClick={handleCancel}>
      <div
        className="archive-modal"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="archive-modal-title"
      >
        <h2 id="archive-modal-title">تأكيد أرشفة المسار</h2>
        <p className="archive-modal-message">
          هل أنت متأكد من أرشفة المسار <strong>{course.title}</strong>؟
        </p>
        <p className="archive-modal-warning">
          سيتم تغيير حالة المسار إلى <strong>مؤرشف</strong>، ونقل بياناته إلى سجل
          الأرشيف، ثم إخفاؤه من الواجهة النشطة.
        </p>

        {error && <div className="alert alert-error">{error}</div>}

        <div className="archive-modal-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleCancel}
            disabled={archiving}
          >
            لا، إلغاء
          </button>
          <button
            type="button"
            className="btn btn-warning"
            onClick={handleConfirm}
            disabled={archiving}
          >
            {archiving ? 'جاري الأرشفة...' : 'نعم، أرشفة المسار'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ArchiveCourseModal
