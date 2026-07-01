import React, { useEffect, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { accountAPI } from '../services/api'
import './Auth.css'

const OTP_LENGTH = 6
const DEFAULT_RESEND_COOLDOWN = 60

const ResetPasswordVerify = () => {
  const [searchParams] = useSearchParams()
  const emailParam = searchParams.get('email') || ''
  const cooldownParam = Number(searchParams.get('cooldown') || DEFAULT_RESEND_COOLDOWN)

  const [email, setEmail] = useState(emailParam)
  const [code, setCode] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(cooldownParam)
  const [devOtp, setDevOtp] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const storedOtp = sessionStorage.getItem('dev_password_reset_otp')
    if (storedOtp) {
      setDevOtp(storedOtp)
    }
  }, [])

  useEffect(() => {
    if (resendCooldown <= 0) return undefined

    const timer = setInterval(() => {
      setResendCooldown((prev) => Math.max(0, prev - 1))
    }, 1000)

    return () => clearInterval(timer)
  }, [resendCooldown])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (code.length !== OTP_LENGTH) {
      setError('يرجى إدخال رمز التحقق المكون من 6 أرقام')
      return
    }

    setLoading(true)

    try {
      const response = await accountAPI.verifyPasswordResetOTP(email.trim(), code.trim())
      sessionStorage.setItem('password_reset_token', response.data.reset_token)
      sessionStorage.removeItem('dev_password_reset_otp')

      setSuccess(response.data.message || 'تم التحقق بنجاح')
      setTimeout(() => {
        navigate('/reset-password')
      }, 700)
    } catch (err) {
      setError(
        err.response?.data?.message ||
        err.response?.data?.code?.[0] ||
        'رمز التحقق غير صحيح'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleResend = async () => {
    if (resendCooldown > 0) return

    setError('')
    setSuccess('')

    try {
      const response = await accountAPI.resendPasswordResetOTP(email.trim())
      setResendCooldown(response.data.resend_available_in || DEFAULT_RESEND_COOLDOWN)

      if (response.data.dev_otp) {
        setDevOtp(response.data.dev_otp)
        sessionStorage.setItem('dev_password_reset_otp', response.data.dev_otp)
      }

      setSuccess(response.data.message || 'تم إنشاء رمز تحقق جديد')
    } catch (err) {
      const cooldown = err.response?.data?.resend_available_in
      if (cooldown) {
        setResendCooldown(cooldown)
      }

      setError(
        err.response?.data?.message ||
        'تعذر إعادة إرسال الرمز'
      )
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="auth-title">التحقق من الرمز</h1>
        <p className="auth-subtitle">
          أدخل رمز التحقق لإعادة تعيين كلمة المرور
        </p>

        {devOtp && (
          <div className="dev-otp-panel" role="note">
            <strong>وضع التطوير</strong>
            <p>رمز إعادة تعيين كلمة المرور للاختبار:</p>
            <code className="dev-otp-code">{devOtp}</code>
          </div>
        )}

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

          <div className="input-group">
            <label htmlFor="code">رمز التحقق</label>
            <input
              type="text"
              id="code"
              name="code"
              value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, OTP_LENGTH))}
              required
              inputMode="numeric"
              autoComplete="one-time-code"
              placeholder="000000"
              className="otp-input"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'جاري التحقق...' : 'متابعة'}
          </button>
        </form>

        <div className="auth-footer">
          <button
            type="button"
            className="auth-link-button"
            onClick={handleResend}
            disabled={resendCooldown > 0}
          >
            {resendCooldown > 0
              ? `إعادة إرسال الرمز خلال ${resendCooldown} ثانية`
              : 'إعادة إرسال رمز التحقق'}
          </button>
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

export default ResetPasswordVerify
