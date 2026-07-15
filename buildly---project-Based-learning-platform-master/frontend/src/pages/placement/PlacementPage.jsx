import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { placementAPI } from '../../services/api'
import './Placement.css'

const DEFAULT_QUESTION_TIME_LIMIT = 20

const DEFAULT_TOPIC_LABELS = {
  html: 'HTML',
  css: 'CSS',
  javascript: 'JavaScript',
  basics: 'أساسيات Python',
  data_structures: 'هياكل البيانات',
  oop: 'OOP',
}

const formatDuration = (seconds) => {
  const safeSeconds = Math.max(0, seconds)
  const mins = Math.floor(safeSeconds / 60)
  const secs = safeSeconds % 60
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

const PlacementPage = () => {
  const { courseId } = useParams()
  const navigate = useNavigate()
  const [step, setStep] = useState('intro')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [timeoutNotice, setTimeoutNotice] = useState('')

  const [trackMeta, setTrackMeta] = useState(null)
  const [attemptId, setAttemptId] = useState(null)
  const [totalQuestions, setTotalQuestions] = useState(12)
  const [currentQuestionNumber, setCurrentQuestionNumber] = useState(1)
  const [question, setQuestion] = useState(null)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [explanation, setExplanation] = useState('')
  const [answerFeedback, setAnswerFeedback] = useState(null)
  const [abilityScore, setAbilityScore] = useState(0)
  const [result, setResult] = useState(null)
  const [questionTimeLimit, setQuestionTimeLimit] = useState(DEFAULT_QUESTION_TIME_LIMIT)
  const [remainingSeconds, setRemainingSeconds] = useState(DEFAULT_QUESTION_TIME_LIMIT)

  const swappingRef = useRef(false)

  const topicLabels = trackMeta?.topic_labels || DEFAULT_TOPIC_LABELS
  const courseTitle = trackMeta?.course_title || 'المسار'
  const trackDisplayName = trackMeta?.track_display_name || 'المسار'
  const skillsDescription = trackMeta?.skills_description || ''
  const topics = trackMeta?.topics || []

  const resetQuestionTimer = useCallback((limit = questionTimeLimit) => {
    setRemainingSeconds(limit)
  }, [questionTimeLimit])

  const handleQuestionTimeout = useCallback(async () => {
    if (swappingRef.current || !question || !attemptId || submitting || answerFeedback) {
      return
    }

    swappingRef.current = true
    setSubmitting(true)
    setError('')

    try {
      const response = await placementAPI.replaceQuestion({
        attempt_id: attemptId,
        question_id: question.id,
      })

      const payload = response.data
      setQuestion(payload.question)
      setAbilityScore(payload.ability_score ?? abilityScore)
      setSelectedAnswer(null)
      setExplanation('')
      setAnswerFeedback(null)
      setTimeoutNotice(payload.message || 'انتهى الوقت — تم استبدال السؤال')
      resetQuestionTimer(payload.question_time_limit_seconds || questionTimeLimit)
    } catch (err) {
      setError(err.response?.data?.error || 'تعذر استبدال السؤال بعد انتهاء الوقت')
      resetQuestionTimer()
    } finally {
      setSubmitting(false)
      swappingRef.current = false
    }
  }, [
    question,
    attemptId,
    submitting,
    answerFeedback,
    abilityScore,
    questionTimeLimit,
    resetQuestionTimer,
  ])

  useEffect(() => {
    const bootstrap = async () => {
      try {
        setLoading(true)
        const statusRes = await placementAPI.getStatus(courseId)
        const status = statusRes.data

        setTrackMeta(status)

        if (!status.requires_placement) {
          navigate(`/courses/${courseId}`)
          return
        }

        if (status.has_completed) {
          setResult({
            ability_score: status.ability_score,
            final_level: status.final_level,
            final_level_display: status.final_level_display,
            completed_at: status.completed_at,
            course_title: status.course_title,
            track_display_name: status.track_display_name,
          })
          setStep('result')
        } else if (status.has_in_progress) {
          const startRes = await placementAPI.start(courseId)
          hydrateAttempt(startRes.data, status)
          setStep('test')
        }
      } catch (err) {
        setError(err.response?.data?.error || 'تعذر تحميل اختبار تحديد المستوى')
      } finally {
        setLoading(false)
      }
    }

    bootstrap()
  }, [courseId, navigate])

  useEffect(() => {
    if (step !== 'test' || answerFeedback || submitting) {
      return undefined
    }

    const timer = window.setInterval(() => {
      setRemainingSeconds((prev) => (prev <= 0 ? 0 : prev - 1))
    }, 1000)

    return () => window.clearInterval(timer)
  }, [step, question?.id, answerFeedback, submitting])

  useEffect(() => {
    if (step !== 'test' || answerFeedback || submitting || remainingSeconds > 0) {
      return
    }

    handleQuestionTimeout()
  }, [remainingSeconds, step, answerFeedback, submitting, handleQuestionTimeout])

  useEffect(() => {
    if (!timeoutNotice) {
      return undefined
    }

    const timer = window.setTimeout(() => setTimeoutNotice(''), 2500)
    return () => window.clearTimeout(timer)
  }, [timeoutNotice])

  const progressPercent = useMemo(() => {
    if (!totalQuestions) return 0
    const answered = Math.max(0, currentQuestionNumber - 1)
    return Math.round((answered / totalQuestions) * 100)
  }, [currentQuestionNumber, totalQuestions])

  const hydrateAttempt = (payload, statusOverride = null) => {
    if (payload.completed) {
      setResult(payload)
      setStep('result')
      return
    }

    const timeLimit = payload.question_time_limit_seconds || DEFAULT_QUESTION_TIME_LIMIT
    setQuestionTimeLimit(timeLimit)

    if (statusOverride) {
      setTrackMeta((prev) => ({ ...prev, ...statusOverride }))
    } else if (payload.course_title || payload.track_display_name) {
      setTrackMeta((prev) => ({
        ...prev,
        course_title: payload.course_title || prev?.course_title,
        track_display_name: payload.track_display_name || prev?.track_display_name,
        track_slug: payload.track_slug || prev?.track_slug,
      }))
    }

    setAttemptId(payload.attempt_id)
    setTotalQuestions(payload.total_questions || 12)
    setCurrentQuestionNumber(payload.current_question_number || 1)
    setQuestion(payload.question)
    setAbilityScore(payload.ability_score || 0)
    setSelectedAnswer(null)
    setExplanation('')
    setAnswerFeedback(null)
    setTimeoutNotice('')
    setRemainingSeconds(timeLimit)
  }

  const handleStart = async () => {
    try {
      setError('')
      setSubmitting(true)
      const response = await placementAPI.start(courseId)
      hydrateAttempt(response.data)
      setStep('test')
    } catch (err) {
      setError(err.response?.data?.error || 'تعذر بدء الاختبار')
    } finally {
      setSubmitting(false)
    }
  }

  const handleSubmitAnswer = async () => {
    if (selectedAnswer === null || !question || submitting) return

    try {
      setSubmitting(true)
      const elapsedMs = Math.max(0, (questionTimeLimit - remainingSeconds) * 1000)
      const response = await placementAPI.submitAnswer({
        attempt_id: attemptId,
        question_id: question.id,
        selected_answer: selectedAnswer,
        time_ms: elapsedMs,
      })

      const payload = response.data
      setAnswerFeedback(payload.is_correct ? 'correct' : 'incorrect')
      setExplanation(payload.explanation || '')
      setAbilityScore(payload.ability_score ?? abilityScore)

      if (payload.completed) {
        setResult(payload)
        setStep('result')
        return
      }

      const nextTimeLimit = payload.question_time_limit_seconds || questionTimeLimit
      setTimeout(() => {
        setQuestion(payload.question)
        setCurrentQuestionNumber(payload.current_question_number)
        setSelectedAnswer(null)
        setExplanation('')
        setAnswerFeedback(null)
        setTimeoutNotice('')
        setQuestionTimeLimit(nextTimeLimit)
        setRemainingSeconds(nextTimeLimit)
      }, 1200)
    } catch (err) {
      setError(err.response?.data?.error || 'تعذر إرسال الإجابة')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="placement-page">
        <div className="loading">
          <div className="spinner" />
        </div>
      </div>
    )
  }

  return (
    <div className="placement-page">
      <Link to={`/courses/${courseId}`} className="back-link">
        ← العودة لتفاصيل المسار
      </Link>

      {error && <div className="alert alert-error">{error}</div>}

      {step === 'intro' && (
        <>
          <section className="placement-hero">
            <h1>{trackDisplayName} Placement Test</h1>
            <p>
              اختبار متكيف لتحديد مستواك في {skillsDescription || trackDisplayName}.
              يولّد النظام أسئلة فريدة لكل طالب باستخدام الذكاء الاصطناعي، وتتغير صعوبتها
              حسب أدائك، ثم يعرض لك المشاريع المناسبة لمستواك في مسار {courseTitle}.
            </p>
          </section>

          <div className="placement-card">
            <div className="placement-meta">
              <span className="placement-badge">12 سؤالاً</span>
              <span className="placement-badge">20 ثانية لكل سؤال</span>
              <span className="placement-badge">اختبار متكيف + AI</span>
              {skillsDescription && (
                <span className="placement-badge">{skillsDescription}</span>
              )}
            </div>
            <p>
              لديك {questionTimeLimit} ثانية فقط لكل سؤال. إذا انتهى الوقت يُستبدل السؤال
              بسؤال جديد مباشرة دون الانتقال للسؤال التالي — لمنع البحث عن الإجابة.
              لا يمكن العودة للسؤال السابق بعد الإجابة.
            </p>
            <div className="placement-actions">
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleStart}
                disabled={submitting}
              >
                {submitting ? 'جاري توليد الأسئلة...' : 'Start Assessment'}
              </button>
            </div>
          </div>
        </>
      )}

      {step === 'test' && question && (
        <div className="placement-card">
          <div className="placement-meta">
            <span className="placement-badge">
              السؤال {currentQuestionNumber} من {totalQuestions}
            </span>
            <span className={`placement-topic-tag ${question.topic}`}>
              {topicLabels[question.topic] || question.topic}
            </span>
            <span
              className={`placement-timer ${
                remainingSeconds <= 5 ? 'placement-timer-warning' : ''
              }`}
            >
              ⏱ {formatDuration(remainingSeconds)}
            </span>
          </div>

          {timeoutNotice && (
            <div className="placement-timeout-notice">{timeoutNotice}</div>
          )}

          <div className="placement-progress-wrap">
            <div className="placement-progress-label">
              <span>التقدم</span>
              <span>{progressPercent}%</span>
            </div>
            <div className="placement-progress-bar">
              <div
                className="placement-progress-fill"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>

          <div className="placement-question">
            <h2>{question.question}</h2>
            <div className="placement-options">
              {question.options.map((option, index) => {
                let className = 'placement-option'
                if (selectedAnswer === index) className += ' selected'
                if (answerFeedback && selectedAnswer === index) {
                  className += answerFeedback === 'correct' ? ' correct' : ' incorrect'
                }

                return (
                  <button
                    key={`${question.id}-${index}`}
                    type="button"
                    className={className}
                    onClick={() => !answerFeedback && setSelectedAnswer(index)}
                    disabled={Boolean(answerFeedback) || submitting}
                  >
                    {option}
                  </button>
                )
              })}
            </div>
          </div>

          {explanation && (
            <div className="placement-explanation">
              <strong>الشرح:</strong> {explanation}
            </div>
          )}

          <div className="placement-actions">
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleSubmitAnswer}
              disabled={selectedAnswer === null || Boolean(answerFeedback) || submitting}
            >
              {submitting ? 'جاري المعالجة...' : 'Next'}
            </button>
          </div>
        </div>
      )}

      {step === 'result' && result && (
        <div className="placement-card placement-result">
          <h2>تم إكمال اختبار تحديد المستوى</h2>
          <p>
            تم حفظ نتيجتك وانضمامك لمسار {result.course_title || courseTitle}.
          </p>
          <div className="placement-result-level">
            المستوى النهائي: {result.final_level_display || result.final_level}
          </div>
          <p>Ability Score: {result.ability_score}</p>
          <div className="placement-topics">
            {(topics.length ? topics : Object.keys(topicLabels)).map((topic) => (
              <span key={topic} className={`placement-topic-tag ${topic}`}>
                {topicLabels[topic] || topic}
              </span>
            ))}
          </div>
          <div className="placement-actions" style={{ justifyContent: 'center' }}>
            <button
              type="button"
              className="btn btn-primary"
              onClick={() =>
                navigate(`/courses/${courseId}`, { state: { refreshPlacement: true } })
              }
            >
              عرض المشاريع المناسبة لمستواك
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default PlacementPage
