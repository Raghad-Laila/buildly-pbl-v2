import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { accountAPI } from '../services/api'
import './Auth.css'

const ForgotPassword = () => {
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      const response = await accountAPI.requestPasswordReset(email.trim())
      const cooldown = response.data.resend_available_in || 60

      if (response.data.dev_otp) {
        sessionStorage.setItem('dev_password_reset_otp', response.data.dev_otp)
      }

      setSuccess(response.data.message)
      setTimeout(() => {
        navigate(
          `/reset-password/verify?email=${encodeURIComponent(email.trim())}&cooldown=${cooldown}`
        )
      }, 900)
    } catch (err) {
      const cooldown = err.response?.data?.resend_available_in
      if (cooldown) {
        navigate(
          `/reset-password/verify?email=${encodeURIComponent(email.trim())}&cooldown=${cooldown}`
        )
        return
      }

      setError(
        err.response?.data?.message ||
        err.response?.data?.email?.[0] ||
        'تعذر إرسال رمز التحقق'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="auth-title">نسيت كلمة المرور؟</h1>
        <p className="auth-subtitle">
          أدخل بريدك الإلكتروني وسنرسل لك رمز تحقق لإعادة تعيين كلمة المرور
        </p>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <label htmlFor="email">البريد الإلكتروني</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="أدخل بريدك الإلكتروني"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'جاري الإرسال...' : 'إرسال رمز التحقق'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            تذكرت كلمة المرور؟{' '}
            <Link to="/login" className="auth-link">
              تسجيل الدخول
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default ForgotPassword
