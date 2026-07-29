import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import NotificationBell from './NotificationBell'
import './Navbar.css'

const BrandMark = () => (
  <span className="navbar-brand-mark" aria-hidden="true">
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
      <path
        d="M14 2.5L24.5 8.5V19.5L14 25.5L3.5 19.5V8.5L14 2.5Z"
        fill="url(#buildlyBrandGrad)"
      />
      <path
        d="M14 8L19 11V17L14 20L9 17V11L14 8Z"
        fill="white"
        fillOpacity="0.9"
      />
      <defs>
        <linearGradient id="buildlyBrandGrad" x1="3.5" y1="2.5" x2="24.5" y2="25.5">
          <stop stopColor="#6366F1" />
          <stop offset="1" stopColor="#8B5CF6" />
        </linearGradient>
      </defs>
    </svg>
  </span>
)

const Navbar = () => {
  const { user, isAuthenticated, isAdmin, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const closeMenu = () => setMenuOpen(false)

  const isActive = (path) =>
    location.pathname === path || location.pathname.startsWith(`${path}/`)

  if (!isAuthenticated) {
    return (
      <nav className="navbar navbar-landing">
        <div className="container">
          <div className="navbar-content">
            <Link to="/" className="navbar-brand" onClick={closeMenu}>
              <BrandMark />
              <span className="navbar-brand-text">Buildly</span>
            </Link>

            <div className={`navbar-links ${menuOpen ? 'open' : ''}`}>
              <div className="navbar-nav">
                <Link to="/" className="nav-link" onClick={closeMenu}>
                  الرئيسية
                </Link>
                <Link to="/courses" className="nav-link" onClick={closeMenu}>
                  المسارات
                </Link>
                <Link to="/projects" className="nav-link" onClick={closeMenu}>
                  المشاريع
                </Link>
                <a href="#about" className="nav-link" onClick={closeMenu}>
                  عن المنصة
                </a>
              </div>
              <div className="navbar-auth-actions">
                <Link to="/login" className="nav-link nav-link-login" onClick={closeMenu}>
                  تسجيل الدخول
                </Link>
                <Link
                  to="/register"
                  className="btn btn-primary navbar-cta"
                  onClick={closeMenu}
                >
                  ابدأ الآن مجاناً
                </Link>
              </div>
            </div>

            <button
              type="button"
              className="menu-toggle"
              aria-label="فتح القائمة"
              aria-expanded={menuOpen}
              onClick={() => setMenuOpen(!menuOpen)}
            >
              <span></span>
              <span></span>
              <span></span>
            </button>
          </div>
        </div>
      </nav>
    )
  }

  return (
    <nav className={`navbar${isAdmin ? ' navbar-admin' : ''}`}>
      <div className="container">
        <div className="navbar-content">
          <Link
            to={isAdmin ? '/admin/dashboard' : '/dashboard'}
            className="navbar-brand"
            onClick={closeMenu}
          >
            <BrandMark />
            <span className="navbar-brand-text">Buildly</span>
          </Link>

          <div className={`navbar-links ${menuOpen ? 'open' : ''}`}>
            <div className="navbar-nav">
              {isAdmin ? (
                <>
                  <Link
                    to="/admin/dashboard"
                    className={`nav-link${isActive('/admin/dashboard') ? ' nav-link-active' : ''}`}
                    onClick={closeMenu}
                  >
                    لوحة التحكم
                  </Link>
                  <Link
                    to="/courses"
                    className={`nav-link${isActive('/courses') && !isActive('/courses/create') ? ' nav-link-active' : ''}`}
                    onClick={closeMenu}
                  >
                    المسارات
                  </Link>
                  <Link
                    to="/courses/create"
                    className={`nav-link${isActive('/courses/create') ? ' nav-link-active' : ''}`}
                    onClick={closeMenu}
                  >
                    إضافة مسار
                  </Link>
                  <Link
                    to="/projects"
                    className={`nav-link${isActive('/projects') && !isActive('/projects/create') ? ' nav-link-active' : ''}`}
                    onClick={closeMenu}
                  >
                    المشاريع
                  </Link>
                  <Link
                    to="/projects/create"
                    className={`nav-link${isActive('/projects/create') ? ' nav-link-active' : ''}`}
                    onClick={closeMenu}
                  >
                    إضافة مشروع
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    to="/dashboard"
                    className={`nav-link${isActive('/dashboard') ? ' nav-link-active' : ''}`}
                    onClick={closeMenu}
                  >
                    لوحة التحكم
                  </Link>
                  <Link
                    to="/courses"
                    className={`nav-link${isActive('/courses') && !isActive('/my-courses') ? ' nav-link-active' : ''}`}
                    onClick={closeMenu}
                  >
                    المسارات
                  </Link>
                  <Link
                    to="/my-courses"
                    className={`nav-link${isActive('/my-courses') ? ' nav-link-active' : ''}`}
                    onClick={closeMenu}
                  >
                    مساراتي
                  </Link>
                  <Link
                    to="/projects"
                    className={`nav-link${isActive('/projects') ? ' nav-link-active' : ''}`}
                    onClick={closeMenu}
                  >
                    المشاريع
                  </Link>
                </>
              )}
            </div>

            <div className="navbar-actions">
              {!isAdmin && <NotificationBell />}
              <Link to="/profile" className="navbar-profile" onClick={closeMenu}>
                {user?.profile_picture_url ? (
                  <img
                    src={user.profile_picture_url}
                    alt="الملف الشخصي"
                    className="nav-avatar"
                  />
                ) : (
                  <span className="nav-avatar nav-avatar-fallback">
                    {(user?.first_name || user?.email || '?').charAt(0).toUpperCase()}
                  </span>
                )}
                <span className="user-email">{user?.first_name || user?.email}</span>
              </Link>
              <button
                type="button"
                onClick={handleLogout}
                className="navbar-logout-btn"
              >
                تسجيل الخروج
              </button>
            </div>
          </div>

          <button
            type="button"
            className="menu-toggle"
            aria-label="فتح القائمة"
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
