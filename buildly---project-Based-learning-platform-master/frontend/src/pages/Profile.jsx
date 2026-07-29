import React, { useState, useEffect, useRef } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { accountAPI } from '../services/api'
import './Profile.css'

const getDisplayName = (profile) => {
  if (!profile) return ''
  if (profile.full_name) return profile.full_name
  const combined = `${profile.first_name || ''} ${profile.last_name || ''}`.trim()
  return combined || profile.email || ''
}

const getInitials = (profile) => {
  if (!profile) return '?'
  if (profile.first_name) return profile.first_name.charAt(0).toUpperCase()
  if (profile.email) return profile.email.charAt(0).toUpperCase()
  return '?'
}

const Profile = () => {
  const { user, updateUser, isAdmin } = useAuth()
  const fileInputRef = useRef(null)

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
  })

  const [profileData, setProfileData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [uploadingAvatar, setUploadingAvatar] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      setLoading(true)
      const response = await accountAPI.getProfile()
      const userData = response.data.user
      setProfileData(userData)
      setFormData({
        first_name: userData.first_name || '',
        last_name: userData.last_name || '',
        email: userData.email || '',
      })
    } catch (err) {
      setError('فشل تحميل بيانات الملف الشخصي')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const syncUser = (updatedUser) => {
    updateUser(updatedUser)
    setProfileData(updatedUser)
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setError('')
    setSuccess('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setSaving(true)

    try {
      const response = await accountAPI.updateProfile(formData)
      syncUser(response.data.user)
      setSuccess('تم تحديث الملف الشخصي بنجاح')
    } catch (err) {
      const errorData = err.response?.data
      if (errorData?.email) {
        setError(Array.isArray(errorData.email) ? errorData.email[0] : errorData.email)
      } else if (errorData?.first_name) {
        setError(Array.isArray(errorData.first_name) ? errorData.first_name[0] : errorData.first_name)
      } else if (errorData?.message) {
        setError(errorData.message)
      } else {
        setError('حدث خطأ أثناء تحديث الملف الشخصي')
      }
    } finally {
      setSaving(false)
    }
  }

  const handleAvatarSelect = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (!file.type.startsWith('image/')) {
      setError('يرجى اختيار ملف صورة صالح')
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('حجم الصورة يجب أن لا يتجاوز 5 ميغابايت')
      return
    }

    setUploadingAvatar(true)
    setError('')
    setSuccess('')

    try {
      const response = await accountAPI.uploadAvatar(file)
      syncUser(response.data.user)
      setSuccess('تم تحديث الصورة الشخصية بنجاح')
    } catch (err) {
      const errorData = err.response?.data
      setError(
        errorData?.profile_picture?.[0] ||
          errorData?.message ||
          'فشل رفع الصورة الشخصية'
      )
    } finally {
      setUploadingAvatar(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleDeleteAvatar = async () => {
    if (!profileData?.profile_picture_url) return

    const confirmed = window.confirm('هل تريد حذف الصورة الشخصية؟')
    if (!confirmed) return

    setUploadingAvatar(true)
    setError('')
    setSuccess('')

    try {
      const response = await accountAPI.deleteAvatar()
      syncUser(response.data.user)
      setSuccess('تم حذف الصورة الشخصية بنجاح')
    } catch (err) {
      setError('فشل حذف الصورة الشخصية')
    } finally {
      setUploadingAvatar(false)
    }
  }

  if (loading) {
    return (
      <div className={`profile-page ${isAdmin ? 'profile-page-admin' : 'profile-page-learner'}`}>
        <div className="profile-page-loading">
          <div className="spinner"></div>
          <p>جاري تحميل الملف الشخصي...</p>
        </div>
      </div>
    )
  }

  const displayName = getDisplayName(profileData || user)
  const avatarUrl = profileData?.profile_picture_url

  return (
    <div className={`profile-page ${isAdmin ? 'profile-page-admin' : 'profile-page-learner'}`}>
      <div className="container profile-page-inner">
        <header className="profile-page-header">
          <div className="profile-page-header-copy">
            <p className="profile-page-eyebrow">
              {isAdmin ? 'Buildly Admin Profile' : 'Buildly Profile'}
            </p>
            <h1>الملف الشخصي</h1>
            <p>
              {isAdmin
                ? 'إدارة بيانات حساب المشرف وإعدادات الملف الشخصي'
                : 'إدارة معلوماتك الشخصية وإعدادات الحساب'}
            </p>
          </div>
        </header>

        <div className="profile-container">
          <aside className="profile-sidebar">
            <div className="profile-panel profile-identity-card">
              <div className="profile-avatar">
                {avatarUrl ? (
                  <img
                    src={avatarUrl}
                    alt={displayName}
                    className="avatar-image"
                  />
                ) : (
                  <div className="avatar-circle">
                    {getInitials(profileData || user)}
                  </div>
                )}
              </div>

              <h2>{displayName}</h2>
              <p className="user-email-text">{profileData?.email || user?.email}</p>
              <p className="user-type">{profileData?.user_type || user?.user_type}</p>

              <div className="avatar-actions">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/png,image/webp,image/gif"
                  className="avatar-file-input"
                  onChange={handleAvatarSelect}
                />
                <button
                  type="button"
                  className="btn btn-primary btn-sm profile-avatar-btn"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={uploadingAvatar}
                >
                  {uploadingAvatar ? 'جاري الرفع...' : 'رفع صورة'}
                </button>
                {avatarUrl && (
                  <button
                    type="button"
                    className="btn btn-secondary btn-sm profile-avatar-btn-secondary"
                    onClick={handleDeleteAvatar}
                    disabled={uploadingAvatar}
                  >
                    حذف الصورة
                  </button>
                )}
              </div>
            </div>

            {profileData?.enrollment_info && (
              <div className="profile-panel">
                <div className="profile-panel-header">
                  <h3>معلومات الانضمام</h3>
                </div>
                <div className="info-list">
                  <div className="info-item">
                    <span className="info-label">عدد المسارات:</span>
                    <span className="info-value">
                      {profileData.enrollment_info.enrolled_courses_count || 0}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </aside>

          <div className="profile-main">
            <div className="profile-panel">
              <div className="profile-panel-header">
                <h2>تعديل المعلومات الشخصية</h2>
                <p>حدّث اسمك وبريدك الإلكتروني الظاهر في المنصة</p>
              </div>

              {error && <div className="alert alert-error">{error}</div>}
              {success && <div className="alert alert-success">{success}</div>}

              <form onSubmit={handleSubmit} className="profile-form">
                <div className="profile-form-grid">
                  <div className="input-group">
                    <label htmlFor="first_name">الاسم الأول</label>
                    <input
                      type="text"
                      id="first_name"
                      name="first_name"
                      value={formData.first_name}
                      onChange={handleChange}
                      placeholder="أدخل اسمك الأول"
                    />
                  </div>

                  <div className="input-group">
                    <label htmlFor="last_name">اسم العائلة</label>
                    <input
                      type="text"
                      id="last_name"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleChange}
                      placeholder="أدخل اسم العائلة"
                    />
                  </div>
                </div>

                <div className="input-group">
                  <label htmlFor="email">البريد الإلكتروني *</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="أدخل بريدك الإلكتروني"
                  />
                </div>

                <div className="form-actions">
                  <button type="submit" className="btn btn-primary" disabled={saving}>
                    {saving ? 'جاري الحفظ...' : 'حفظ التغييرات'}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <div className="profile-panel profile-panel-full">
            <div className="profile-panel-header">
              <h2>معلومات الحساب</h2>
              <p>بيانات الحساب الأساسية من النظام</p>
            </div>
            <div className="info-list info-list-grid">
              <div className="info-item">
                <span className="info-label">نوع المستخدم:</span>
                <span className="info-value">{profileData?.user_type}</span>
              </div>
              <div className="info-item">
                <span className="info-label">تاريخ الانضمام:</span>
                <span className="info-value">
                  {profileData?.date_joined
                    ? new Date(profileData.date_joined).toLocaleDateString('ar-SA')
                    : '-'}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">آخر تسجيل دخول:</span>
                <span className="info-value">
                  {profileData?.last_login
                    ? new Date(profileData.last_login).toLocaleDateString('ar-SA')
                    : '-'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile
