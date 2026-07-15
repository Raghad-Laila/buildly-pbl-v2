import React from 'react'

const AuthStepIndicator = ({ currentStep, labels }) => (
  <div className="auth-steps" aria-label="خطوات إعادة تعيين كلمة المرور">
    {labels.map((label, index) => {
      const stepNumber = index + 1
      const isActive = stepNumber === currentStep
      const isCompleted = stepNumber < currentStep

      return (
        <div
          key={label}
          className={`auth-step ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
        >
          <span className="auth-step-number">{stepNumber}</span>
          <span className="auth-step-label">{label}</span>
        </div>
      )
    })}
  </div>
)

export default AuthStepIndicator
