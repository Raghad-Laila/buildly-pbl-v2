import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import NotificationBell from './NotificationBell'
import './Navbar.css'

const Navbar = () => {
  const { user, isAuthenticated, isAdmin, logout } = useAuth()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  if (!isAuthenticated) {
    return (
      <nav className="navbar">
        <div className="container">
          <div className="navbar-content">
            <Link to="/" className="navbar-brand">
              منصة التعلم
            </Link>
            <div className="navbar-links">
              <Link to="/login" className="nav-link">تسجيل الدخول</Link>
              <Link to="/register" className="nav-link btn btn-primary">إنشاء حساب</Link>
            </div>
          </div>
        </div>
      </nav>
    )
  }

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to={isAdmin ? "/admin/dashboard" : "/dashboard"} className="navbar-brand">
            منصة التعلم
          </Link>
          
          <div className={`navbar-links ${menuOpen ? 'open' : ''}`}>
            {isAdmin ? (
              <>
                <Link to="/admin/dashboard" className="nav-link">لوحة التحكم</Link>
                <Link to="/courses" className="nav-link">المسارات</Link>
                <Link to="/courses/create" className="nav-link">إضافة مسار</Link>
                <Link to="/projects" className="nav-link">المشاريع</Link>
                <Link to="/projects/create" className="nav-link">إضافة مشروع</Link>
              </>
            ) : (
              <>
                <Link to="/dashboard" className="nav-link">لوحة التحكم</Link>
                <Link to="/courses" className="nav-link">المسارات</Link>
                <Link to="/my-courses" className="nav-link">مساراتي</Link>
                <Link to="/projects" className="nav-link">المشاريع</Link>
              </>
            )}
            {!isAdmin && <NotificationBell />}
            <Link to="/profile" className="nav-link profile-nav-link">
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
            <button onClick={handleLogout} className="btn btn-secondary">
              تسجيل الخروج
            </button>
          </div>
          
          <button
            className="menu-toggle"
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

