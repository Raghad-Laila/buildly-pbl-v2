import React, { useEffect, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { accountAPI } from '../services/api'
import './Auth.css'

const OTP_LENGTH = 6
const DEFAULT_RESEND_COOLDOWN = 60

const VerifyEmail = () => {
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
  const { loginWithTokens } = useAuth()

  useEffect(() => {
    const storedOtp = sessionStorage.getItem('dev_otp')
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
      const response = await accountAPI.verifyEmail(email.trim(), code.trim())
      const { user: userData, tokens } = response.data

      loginWithTokens(userData, tokens)
      sessionStorage.removeItem('dev_otp')

      setSuccess(response.data.message || 'تم تفعيل الحساب بنجاح')

      const userType = userData.user_type
      setTimeout(() => {
        if (userType === 'مشرف' || userType === 'admin') {
          navigate('/admin/dashboard')
        } else {
          navigate('/dashboard')
        }
      }, 800)
    } catch (err) {
      const message =
        err.response?.data?.message ||
        err.response?.data?.code?.[0] ||
        err.response?.data?.email?.[0] ||
        'فشل التحقق من الرمز'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const handleResend = async () => {
    if (resendCooldown > 0) return

    setError('')
    setSuccess('')

    try {
      const response = await accountAPI.resendOTP(email.trim())
      setResendCooldown(response.data.resend_available_in || DEFAULT_RESEND_COOLDOWN)

      if (response.data.dev_otp) {
        setDevOtp(response.data.dev_otp)
        sessionStorage.setItem('dev_otp', response.data.dev_otp)
      }

      setSuccess(response.data.message || 'تم إنشاء رمز تحقق جديد')
    } catch (err) {
      const cooldown = err.response?.data?.resend_available_in
      if (cooldown) {
        setResendCooldown(cooldown)
      }

      setError(
        err.response?.data?.message ||
        err.response?.data?.email?.[0] ||
        'تعذر إعادة إرسال الرمز'
      )
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="auth-title">تفعيل الحساب</h1>
        <p className="auth-subtitle">
          أدخل رمز التحقق المكون من 6 أرقام لتفعيل حسابك
        </p>

        {devOtp && (
          <div className="dev-otp-panel" role="note">
            <strong>وضع التطوير</strong>
            <p>رمز التحقق للاختبار (لا يُرسل عبر البريد):</p>
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
            {loading ? 'جاري التحقق...' : 'تفعيل الحساب'}
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
            لديك حساب مفعّل؟{' '}
            <Link to="/login" className="auth-link">
              تسجيل الدخول
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default VerifyEmail
