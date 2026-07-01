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
  const { user, updateUser } = useAuth()
  const fileInputRef = useRef(null)

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
  })
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    new_password2: '',
  })

  const [profileData, setProfileData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [uploadingAvatar, setUploadingAvatar] = useState(false)
  const [changingPassword, setChangingPassword] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [passwordSuccess, setPasswordSuccess] = useState('')

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

  const handlePasswordChange = (e) => {
    const { name, value } = e.target
    setPasswordData((prev) => ({ ...prev, [name]: value }))
    setPasswordError('')
    setPasswordSuccess('')
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

  const handlePasswordSubmit = async (e) => {
    e.preventDefault()
    setPasswordError('')
    setPasswordSuccess('')
    setChangingPassword(true)

    try {
      const response = await accountAPI.changePassword(passwordData)
      setPasswordSuccess(response.data.message || 'تم تغيير كلمة المرور بنجاح')
      setPasswordData({
        current_password: '',
        new_password: '',
        new_password2: '',
      })
    } catch (err) {
      const errorData = err.response?.data
      if (errorData?.current_password) {
        setPasswordError(
          Array.isArray(errorData.current_password)
            ? errorData.current_password[0]
            : errorData.current_password
        )
      } else if (errorData?.new_password) {
        setPasswordError(
          Array.isArray(errorData.new_password)
            ? errorData.new_password[0]
            : errorData.new_password
        )
      } else if (errorData?.message) {
        setPasswordError(errorData.message)
      } else {
        setPasswordError('حدث خطأ أثناء تغيير كلمة المرور')
      }
    } finally {
      setChangingPassword(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  const displayName = getDisplayName(profileData || user)
  const avatarUrl = profileData?.profile_picture_url

  return (
    <div className="container">
      <div className="page-header">
        <h1>الملف الشخصي</h1>
      </div>

      <div className="profile-container">
        <div className="profile-sidebar">
          <div className="card">
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
                className="btn btn-primary btn-sm"
                onClick={() => fileInputRef.current?.click()}
                disabled={uploadingAvatar}
              >
                {uploadingAvatar ? 'جاري الرفع...' : 'رفع صورة'}
              </button>
              {avatarUrl && (
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={handleDeleteAvatar}
                  disabled={uploadingAvatar}
                >
                  حذف الصورة
                </button>
              )}
            </div>
          </div>

          {profileData?.enrollment_info && (
            <div className="card">
              <h3>معلومات الانضمام</h3>
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
        </div>

        <div className="profile-main">
          <div className="card">
            <h2>تعديل المعلومات الشخصية</h2>

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

          <div className="card">
            <h2>تغيير كلمة المرور</h2>

            {passwordError && <div className="alert alert-error">{passwordError}</div>}
            {passwordSuccess && <div className="alert alert-success">{passwordSuccess}</div>}

            <form onSubmit={handlePasswordSubmit} className="profile-form">
              <div className="input-group">
                <label htmlFor="current_password">كلمة المرور الحالية *</label>
                <input
                  type="password"
                  id="current_password"
                  name="current_password"
                  value={passwordData.current_password}
                  onChange={handlePasswordChange}
                  required
                  placeholder="أدخل كلمة المرور الحالية"
                />
              </div>

              <div className="profile-form-grid">
                <div className="input-group">
                  <label htmlFor="new_password">كلمة المرور الجديدة *</label>
                  <input
                    type="password"
                    id="new_password"
                    name="new_password"
                    value={passwordData.new_password}
                    onChange={handlePasswordChange}
                    required
                    minLength={8}
                    placeholder="8 أحرف على الأقل"
                  />
                </div>

                <div className="input-group">
                  <label htmlFor="new_password2">تأكيد كلمة المرور *</label>
                  <input
                    type="password"
                    id="new_password2"
                    name="new_password2"
                    value={passwordData.new_password2}
                    onChange={handlePasswordChange}
                    required
                    minLength={8}
                    placeholder="أعد إدخال كلمة المرور"
                  />
                </div>
              </div>

              <div className="form-actions">
                <button
                  type="submit"
                  className="btn btn-secondary"
                  disabled={changingPassword}
                >
                  {changingPassword ? 'جاري التحديث...' : 'تغيير كلمة المرور'}
                </button>
              </div>
            </form>
          </div>

          <div className="card">
            <h2>معلومات الحساب</h2>
            <div className="info-list">
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
