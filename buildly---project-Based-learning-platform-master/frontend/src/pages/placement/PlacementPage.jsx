import React, { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { placementAPI } from '../../services/api'
import './Placement.css'

const FRONTEND_COURSE_TITLE = 'Frontend Mastery'

const TOPIC_LABELS = {
  html: 'HTML',
  css: 'CSS',
  javascript: 'JavaScript',
}

const formatDuration = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

const PlacementPage = () => {
  const { courseId } = useParams()
  const navigate = useNavigate()
  const [step, setStep] = useState('intro')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const [attemptId, setAttemptId] = useState(null)
  const [totalQuestions, setTotalQuestions] = useState(12)
  const [currentQuestionNumber, setCurrentQuestionNumber] = useState(1)
  const [question, setQuestion] = useState(null)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [explanation, setExplanation] = useState('')
  const [answerFeedback, setAnswerFeedback] = useState(null)
  const [abilityScore, setAbilityScore] = useState(0)
  const [result, setResult] = useState(null)
  const [elapsedSeconds, setElapsedSeconds] = useState(0)

  useEffect(() => {
    const bootstrap = async () => {
      try {
        setLoading(true)
        const statusRes = await placementAPI.getStatus(courseId)
        const status = statusRes.data

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
          })
          setStep('result')
        } else if (status.has_in_progress) {
          const startRes = await placementAPI.start(courseId)
          hydrateAttempt(startRes.data)
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
    if (step !== 'test' || answerFeedback) {
      return undefined
    }

    const timer = window.setInterval(() => {
      setElapsedSeconds((prev) => prev + 1)
    }, 1000)

    return () => window.clearInterval(timer)
  }, [step, question?.id, answerFeedback])

  const progressPercent = useMemo(() => {
    if (!totalQuestions) return 0
    const answered = Math.max(0, currentQuestionNumber - 1)
    return Math.round((answered / totalQuestions) * 100)
  }, [currentQuestionNumber, totalQuestions])

  const hydrateAttempt = (payload) => {
    if (payload.completed) {
      setResult(payload)
      setStep('result')
      return
    }

    setAttemptId(payload.attempt_id)
    setTotalQuestions(payload.total_questions || 12)
    setCurrentQuestionNumber(payload.current_question_number || 1)
    setQuestion(payload.question)
    setAbilityScore(payload.ability_score || 0)
    setSelectedAnswer(null)
    setExplanation('')
    setAnswerFeedback(null)
    setElapsedSeconds(0)
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
      const response = await placementAPI.submitAnswer({
        attempt_id: attemptId,
        question_id: question.id,
        selected_answer: selectedAnswer,
        time_ms: elapsedSeconds * 1000,
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

      setTimeout(() => {
        setQuestion(payload.question)
        setCurrentQuestionNumber(payload.current_question_number)
        setSelectedAnswer(null)
        setExplanation('')
        setAnswerFeedback(null)
        setElapsedSeconds(0)
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
            <h1>Frontend Placement Test</h1>
            <p>
              اختبار متكيف لتحديد مستواك في أساسيات Frontend (HTML, CSS, JavaScript).
              سيختار النظام أسئلة تناسب أداءك، ثم يعرض لك المشاريع المناسبة لمستواك في مسار
              {' '}
              {FRONTEND_COURSE_TITLE}.
            </p>
          </section>

          <div className="placement-card">
            <div className="placement-meta">
              <span className="placement-badge">12 سؤالاً</span>
              <span className="placement-badge">اختبار متكيف</span>
              <span className="placement-badge">HTML · CSS · JavaScript</span>
            </div>
            <p>
              يبدأ الجميع من نفس النقطة، وتتغير صعوبة الأسئلة حسب إجاباتك.
              لا يمكن العودة للسؤال السابق بعد الانتقال.
            </p>
            <div className="placement-actions">
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleStart}
                disabled={submitting}
              >
                {submitting ? 'جاري التحضير...' : 'Start Assessment'}
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
              {TOPIC_LABELS[question.topic] || question.topic}
            </span>
            <span className="placement-timer">⏱ {formatDuration(elapsedSeconds)}</span>
          </div>

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
              {submitting ? 'جاري الإرسال...' : 'Next'}
            </button>
          </div>
        </div>
      )}

      {step === 'result' && result && (
        <div className="placement-card placement-result">
          <h2>تم إكمال اختبار تحديد المستوى</h2>
          <p>تم حفظ نتيجتك وانضمامك لمسار {FRONTEND_COURSE_TITLE}.</p>
          <div className="placement-result-level">
            المستوى النهائي: {result.final_level_display || result.final_level}
          </div>
          <p>Ability Score: {result.ability_score}</p>
          <div className="placement-topics">
            <span className="placement-topic-tag html">HTML</span>
            <span className="placement-topic-tag css">CSS</span>
            <span className="placement-topic-tag javascript">JavaScript</span>
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
