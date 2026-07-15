import React, { useEffect, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { accountAPI } from '../services/api'
import AuthStepIndicator from '../components/AuthStepIndicator'
import './Auth.css'

const OTP_LENGTH = 6
const DEFAULT_RESEND_COOLDOWN = 60
const RESET_STEPS = ['البريد الإلكتروني', 'رمز التحقق', 'كلمة مرور جديدة']

const ResetPasswordVerify = () => {
  const [searchParams] = useSearchParams()
  const emailParam = searchParams.get('email') || ''
  const cooldownParam = Number(searchParams.get('cooldown') || DEFAULT_RESEND_COOLDOWN)

  const [email] = useState(emailParam)
  const [code, setCode] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(cooldownParam)
  const navigate = useNavigate()

  useEffect(() => {
    if (!email) {
      navigate('/forgot-password')
    }
  }, [email, navigate])

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
      setSuccess(response.data.message || 'تم إرسال رمز تحقق جديد إلى بريدك الإلكتروني')
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

  if (!email) {
    return null
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <AuthStepIndicator currentStep={2} labels={RESET_STEPS} />

        <h1 className="auth-title">التحقق من الرمز</h1>
        <p className="auth-subtitle">
          أدخل رمز التحقق المكوّن من 6 أرقام المرسل إلى{' '}
          <strong>{email}</strong>
        </p>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
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
            <Link to="/forgot-password" className="auth-link">
              تغيير البريد الإلكتروني
            </Link>
          </p>
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
