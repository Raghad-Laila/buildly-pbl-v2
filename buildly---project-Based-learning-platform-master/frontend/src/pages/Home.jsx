import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Home.css'

const Home = () => {
  const { isAuthenticated } = useAuth()

  const learningSteps = [
    {
      number: 1,
      title: 'إنشاء حسابك',
      description:
        'سجل مجاناً وقم بإعداد ملفك التعليمي. اختر مستواك المهاراتي والتقنيات التي تريد تعلمها.',
      side: 'right',
      tone: 'purple',
    },
    {
      number: 2,
      title: 'أجب على اختبار المهارات',
      description:
        'أجب على بضعة أسئلة سريعة لتحديد مستواك الحالي. سنخصص مسارك التعليمي بناءً على نتائجك.',
      side: 'left',
      tone: 'teal',
    },
    {
      number: 3,
      title: 'ابدأ مشاريع حقيقية',
      description:
        'تعلم من خلال بناء مشاريع واجهة أمامية حقيقية. كل تحدي يساعدك على ممارسة HTML و CSS و JavaScript خطوة بخطوة.',
      side: 'right',
      tone: 'blue',
    },
    {
      number: 4,
      title: 'تتبع تقدمك',
      description:
        'اكسب النقاط، افتح تحديات جديدة، وشاهد كيف تتحسن مهاراتك البرمجية مع مرور الوقت.',
      side: 'left',
      tone: 'indigo',
    },
  ]

  const whyChooseUs = [
    {
      title: 'توجيه ذكي بالذكاء الاصطناعي',
      description:
        'احصل على ملاحظات فورية وتوجيهات مخصصة تساعدك على تجاوز العقبات وتحسين جودة كودك.',
      icon: 'ai',
    },
    {
      title: 'مجتمع تقني حيوي',
      description:
        'انضم إلى مجتمع من المتعلمين والمطورين، شارك تقدمك، وتعلّم من تجارب الآخرين.',
      icon: 'community',
    },
    {
      title: 'مسار تعليمي مخصص',
      description:
        'نظام ذكي يحدد مستواك ويقدم لك المحتوى والمشاريع المناسبة لمرحلتك الحالية.',
      icon: 'path',
    },
    {
      title: 'بيئة تطوير سحابية',
      description:
        'اكتب شغّل واختبر مشاريعك مباشرة من المتصفح دون الحاجة لإعداد بيئة محلية معقدة.',
      icon: 'cloud',
    },
  ]

  const projectExamples = [
    {
      title: 'صفحة هبوط تفاعلية',
      description: 'بناء صفحة هبوط احترافية باستخدام HTML و CSS و JavaScript',
      level: 'مبتدئ',
      time: '5 ساعات',
      tags: ['HTML', 'CSS', 'JavaScript'],
      theme: 'landing',
    },
    {
      title: 'تطبيق قائمة المهام',
      description: 'تطبيق لإدارة المهام مع إمكانية الإضافة والحذف والتعديل',
      level: 'متوسط',
      time: '8 ساعات',
      tags: ['JavaScript', 'DOM', 'LocalStorage'],
      theme: 'todo',
    },
    {
      title: 'لوحة تحكم تفاعلية',
      description: 'بناء لوحة تحكم كاملة مع الرسوم البيانية والإحصائيات',
      level: 'متقدم',
      time: '15 ساعة',
      tags: ['React', 'Charts', 'UI'],
      theme: 'dashboard',
    },
  ]

  const featureIcon = (type) => {
    if (type === 'ai') {
      return (
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M12 3v3M12 18v3M4.9 4.9l2.1 2.1M16.9 16.9l2.1 2.1M3 12h3M18 12h3M4.9 19.1l2.1-2.1M16.9 7.1l2.1-2.1"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
          <circle cx="12" cy="12" r="3.5" stroke="currentColor" strokeWidth="1.8" />
        </svg>
      )
    }
    if (type === 'community') {
      return (
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="9" cy="8" r="3" stroke="currentColor" strokeWidth="1.8" />
          <circle cx="16.5" cy="9.5" r="2.5" stroke="currentColor" strokeWidth="1.8" />
          <path
            d="M3.5 19c.8-3 2.9-4.5 5.5-4.5S13.7 16 14.5 19"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
          <path
            d="M14 14.2c1.5-.7 3.1-.6 4.8.4 1.2.7 2 1.8 2.2 3.4"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
        </svg>
      )
    }
    if (type === 'path') {
      return (
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M7 4h7l3 3v13H7V4z"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinejoin="round"
          />
          <path d="M14 4v3h3" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
          <path d="M9 12h6M9 16h4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      )
    }
    return (
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path
          d="M7 18a4 4 0 010-8 5.5 5.5 0 0110.7-1.5A3.5 3.5 0 0118 18H7z"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinejoin="round"
        />
      </svg>
    )
  }

  const timelineIcon = (tone) => {
    if (tone === 'teal') {
      return (
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <rect x="4" y="5" width="16" height="14" rx="2" stroke="currentColor" strokeWidth="1.8" />
          <path d="M8 9h8M8 12h5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      )
    }
    if (tone === 'blue') {
      return (
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M5 16l5-5 3 3 6-7"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path d="M14 7h5v5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      )
    }
    if (tone === 'indigo') {
      return (
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M4 19V5h6l2 2h8v12H4z"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinejoin="round"
          />
        </svg>
      )
    }
    return (
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path
          d="M12 3l2.2 4.6L19 9l-3.5 3.3.9 5.2L12 15.2 7.6 17.5l.9-5.2L5 9l4.8-1.4L12 3z"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinejoin="round"
        />
      </svg>
    )
  }

  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="container hero-grid">
          <div className="hero-copy">
            <div className="hero-pill">انضم إلى أكثر من 10,000 طالب</div>
            <h1 className="hero-title">
              تعلم البرمجة من خلال بناء{' '}
              <span className="hero-title-accent">مشاريع حقيقية</span>
            </h1>
            <p className="hero-description">
              منصة تعليمية مبتكرة تجمع بين التعلم النظري والتطبيق العملي. تعلّم
              البرمجة خطوة بخطوة عبر مشاريع واقعية تبني بها مهاراتك لتصبح مطوراً
              محترفاً.
            </p>

            <div className="hero-actions">
              <Link to="/register" className="btn hero-cta">
                ابدأ مشروعك الأول
                <span className="hero-cta-arrow" aria-hidden="true">
                  ←
                </span>
              </Link>
              <div className="hero-social-proof">
                <div className="hero-avatars" aria-hidden="true">
                  <span className="hero-avatar a1">أ</span>
                  <span className="hero-avatar a2">س</span>
                  <span className="hero-avatar a3">م</span>
                </div>
                <span className="hero-social-text">+1.2k متعلم نشط</span>
              </div>
            </div>

            <div className="hero-stats">
              <div className="hero-stat">
                <div className="hero-stat-number">+500</div>
                <div className="hero-stat-label">مشروع مكتمل</div>
              </div>
              <div className="hero-stat">
                <div className="hero-stat-number">98%</div>
                <div className="hero-stat-label">نسبة رضا الطلاب</div>
              </div>
              <div className="hero-stat">
                <div className="hero-stat-number">50+</div>
                <div className="hero-stat-label">مشروع تعليمي</div>
              </div>
              <div className="hero-stat">
                <div className="hero-stat-number">24/7</div>
                <div className="hero-stat-label">دعم متواصل</div>
              </div>
            </div>
          </div>

          <div className="hero-visual" aria-hidden="true">
            <div className="hero-visual-glow" />
            <div className="hero-float-card hero-progress-card">
              <div className="hero-progress-top">
                <span className="hero-progress-brand">Buildly</span>
                <span className="hero-progress-pct">45%</span>
              </div>
              <div className="hero-progress-title">ابدأ Buildly</div>
              <div className="hero-progress-bar">
                <span style={{ width: '45%' }} />
              </div>
              <div className="hero-progress-meta">المرحلة التالية: بناء الواجهة</div>
            </div>

            <div className="hero-float-card hero-code-card">
              <div className="hero-code-dots">
                <span />
                <span />
                <span />
              </div>
              <pre className="hero-code-pre">
                <code>
                  <span className="c-pink">const</span> buildly = {'{'}
                  {'\n'}
                  {'  '}learn: <span className="c-green">'projects'</span>,
                  {'\n'}
                  {'  '}ship: <span className="c-blue">true</span>
                  {'\n'}
                  {'}'}
                </code>
              </pre>
            </div>
          </div>
        </div>
      </section>

      <section className="learning-journey-section" id="journey">
        <div className="container">
          <div className="section-heading">
            <h2 className="section-title">رحلة التعلم في Buildly</h2>
            <p className="section-subtitle">
              مسار واضح من أساسيات التقنية حتى إطلاق مشاريعك وتتبع نموك
            </p>
          </div>

          <div className="timeline">
            {learningSteps.map((step) => (
              <div
                key={step.number}
                className={`timeline-item timeline-${step.side} timeline-${step.tone}`}
              >
                <div className="timeline-content">
                  <span className="timeline-step-label">الخطوة {step.number}</span>
                  <h3 className="timeline-title">{step.title}</h3>
                  <p className="timeline-description">{step.description}</p>
                </div>
                <div className="timeline-marker">
                  <span className="timeline-icon">{timelineIcon(step.tone)}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="why-choose-section" id="about">
        <div className="container">
          <div className="section-heading">
            <h2 className="section-title">لماذا تختار منصتنا؟</h2>
            <p className="section-subtitle">
              أدوات وميزات مصممة لتسريع تعلمك عبر مشاريع عملية حقيقية
            </p>
          </div>

          <div className="features-grid">
            {whyChooseUs.map((feature) => (
              <div key={feature.title} className={`feature-card feature-${feature.icon}`}>
                <div className="feature-icon">{featureIcon(feature.icon)}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="project-examples-section" id="projects">
        <div className="container">
          <div className="projects-heading-row">
            <div>
              <h2 className="section-title section-title-start">مشاريع ألهمت الآلاف</h2>
              <p className="section-subtitle section-subtitle-start">
                أمثلة المشاريع التعليمية التي تبني بها مهاراتك خطوة بخطوة
              </p>
            </div>
            <Link to="/projects" className="btn projects-browse-btn">
              تصفح جميع المشاريع
            </Link>
          </div>

          <div className="projects-grid">
            {projectExamples.map((project) => (
              <article
                key={project.title}
                className={`project-example-card project-theme-${project.theme}`}
              >
                <div className="project-thumb">
                  <div className="project-thumb-ui">
                    <span className="project-badge">{project.level}</span>
                    <div className="project-thumb-window">
                      <span />
                      <span />
                      <span />
                    </div>
                    <div className="project-thumb-body">
                      <div className="project-thumb-line w70" />
                      <div className="project-thumb-line w45" />
                      <div className="project-thumb-blocks">
                        <i />
                        <i />
                        <i />
                      </div>
                    </div>
                  </div>
                </div>
                <div className="project-card-body">
                  <h3 className="project-title">{project.title}</h3>
                  <p className="project-description">{project.description}</p>
                  <div className="project-meta-row">
                    <span className="project-time">{project.time}</span>
                  </div>
                  <div className="project-tags">
                    {project.tags.map((tag) => (
                      <span key={tag} className="project-tag">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <footer className="home-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-brand">
              <div className="footer-logo">
                <span className="navbar-brand-mark" aria-hidden="true">
                  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                    <path
                      d="M14 2.5L24.5 8.5V19.5L14 25.5L3.5 19.5V8.5L14 2.5Z"
                      fill="url(#buildlyFooterGrad)"
                    />
                    <path
                      d="M14 8L19 11V17L14 20L9 17V11L14 8Z"
                      fill="white"
                      fillOpacity="0.9"
                    />
                    <defs>
                      <linearGradient
                        id="buildlyFooterGrad"
                        x1="3.5"
                        y1="2.5"
                        x2="24.5"
                        y2="25.5"
                      >
                        <stop stopColor="#6366F1" />
                        <stop offset="1" stopColor="#8B5CF6" />
                      </linearGradient>
                    </defs>
                  </svg>
                </span>
                <h3>Buildly</h3>
              </div>
              <p>
                منصة التعلم القائمة على المشاريع — ابنِ مهاراتك عبر تجارب عملية
                حقيقية.
              </p>
              <div className="footer-social" aria-label="وسائل التواصل">
                <a href="mailto:info@buildly.com" className="footer-social-link" title="Email">
                  ✉
                </a>
                <a
                  href="mailto:support@buildly.com"
                  className="footer-social-link"
                  title="Support"
                >
                  ⌨
                </a>
              </div>
            </div>

            <div className="footer-links">
              <div className="footer-column">
                <h4>المنصة</h4>
                <Link to="/">الرئيسية</Link>
                <Link to="/courses">المسارات</Link>
                <Link to="/projects">المشاريع</Link>
              </div>
              <div className="footer-column">
                <h4>حسابي</h4>
                {isAuthenticated ? (
                  <>
                    <Link to="/dashboard">لوحة التحكم</Link>
                    <Link to="/profile">الملف الشخصي</Link>
                  </>
                ) : (
                  <>
                    <Link to="/login">تسجيل الدخول</Link>
                    <Link to="/register">إنشاء حساب</Link>
                  </>
                )}
              </div>
              <div className="footer-column">
                <h4>تواصل معنا</h4>
                <p>info@buildly.com</p>
                <p>support@buildly.com</p>
                <a href="#about">عن المنصة</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 Buildly للتعليم التقني. جميع الحقوق محفوظة.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home
