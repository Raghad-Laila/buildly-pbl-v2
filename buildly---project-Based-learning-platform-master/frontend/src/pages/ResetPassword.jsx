import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { accountAPI } from '../services/api'
import AuthStepIndicator from '../components/AuthStepIndicator'
import './Auth.css'

const RESET_STEPS = ['البريد الإلكتروني', 'رمز التحقق', 'كلمة مرور جديدة']

const ResetPassword = () => {
  const [formData, setFormData] = useState({
    new_password: '',
    new_password2: '',
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showPassword2, setShowPassword2] = useState(false)
  const [resetToken, setResetToken] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const token = sessionStorage.getItem('password_reset_token')
    if (!token) {
      navigate('/forgot-password')
      return
    }
    setResetToken(token)
  }, [navigate])

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (formData.new_password !== formData.new_password2) {
      setError('كلمات المرور غير متطابقة')
      return
    }

    if (formData.new_password.length < 8) {
      setError('كلمة المرور يجب أن تكون 8 أحرف على الأقل')
      return
    }

    setLoading(true)

    try {
      const response = await accountAPI.confirmPasswordReset({
        reset_token: resetToken,
        new_password: formData.new_password,
        new_password2: formData.new_password2,
      })

      sessionStorage.removeItem('password_reset_token')

      setSuccess(response.data.message || 'تمت إعادة تعيين كلمة المرور بنجاح')
      setTimeout(() => {
        navigate('/login')
      }, 1200)
    } catch (err) {
      setError(
        err.response?.data?.message ||
        err.response?.data?.new_password?.[0] ||
        'تعذر إعادة تعيين كلمة المرور'
      )
    } finally {
      setLoading(false)
    }
  }

  if (!resetToken) {
    return null
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <AuthStepIndicator currentStep={3} labels={RESET_STEPS} />

        <h1 className="auth-title">كلمة مرور جديدة</h1>
        <p className="auth-subtitle">
          أدخل كلمة المرور الجديدة وتأكيدها
        </p>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <label htmlFor="new_password">كلمة المرور الجديدة</label>
            <div className="password-input-wrapper">
              <input
                type={showPassword ? 'text' : 'password'}
                id="new_password"
                name="new_password"
                value={formData.new_password}
                onChange={handleChange}
                required
                minLength={8}
                placeholder="كلمة المرور (8 أحرف على الأقل)"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? 'إخفاء كلمة المرور' : 'إظهار كلمة المرور'}
              >
                {showPassword ? 'إخفاء' : 'إظهار'}
              </button>
            </div>
          </div>

          <div className="input-group">
            <label htmlFor="new_password2">تأكيد كلمة المرور</label>
            <div className="password-input-wrapper">
              <input
                type={showPassword2 ? 'text' : 'password'}
                id="new_password2"
                name="new_password2"
                value={formData.new_password2}
                onChange={handleChange}
                required
                minLength={8}
                placeholder="أعد إدخال كلمة المرور"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword2(!showPassword2)}
                aria-label={showPassword2 ? 'إخفاء كلمة المرور' : 'إظهار كلمة المرور'}
              >
                {showPassword2 ? 'إخفاء' : 'إظهار'}
              </button>
            </div>
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'جاري الحفظ...' : 'حفظ كلمة المرور'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            <Link to="/login" className="auth-link">
              العودة لتسجيل الدخول
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default ResetPassword
