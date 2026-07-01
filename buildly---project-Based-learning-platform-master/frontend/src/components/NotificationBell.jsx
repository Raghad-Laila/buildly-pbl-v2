import React, { useState, useEffect, useRef, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { accountAPI } from '../services/api'
import { formatNotificationTime, getNotificationPath } from '../utils/notificationUtils'
import './NotificationBell.css'

const POLL_INTERVAL_MS = 30000

const NotificationBell = () => {
  const navigate = useNavigate()
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [isOpen, setIsOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const containerRef = useRef(null)

  const fetchUnreadCount = useCallback(async () => {
    try {
      const response = await accountAPI.getUnreadNotificationsCount()
      setUnreadCount(response.data.unread_count || 0)
    } catch (error) {
      console.error('Failed to fetch unread notifications count', error)
    }
  }, [])

  const fetchNotifications = useCallback(async () => {
    try {
      setLoading(true)
      const response = await accountAPI.getNotifications()
      setNotifications(response.data.notifications || [])
      setUnreadCount(response.data.unread_count || 0)
    } catch (error) {
      console.error('Failed to fetch notifications', error)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchUnreadCount()
    const intervalId = setInterval(fetchUnreadCount, POLL_INTERVAL_MS)
    return () => clearInterval(intervalId)
  }, [fetchUnreadCount])

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleToggle = async () => {
    const nextOpen = !isOpen
    setIsOpen(nextOpen)
    if (nextOpen) {
      await fetchNotifications()
    }
  }

  const handleNotificationClick = async (notification) => {
    try {
      if (!notification.read) {
        await accountAPI.markNotificationRead(notification.id)
        setNotifications((prev) =>
          prev.map((item) =>
            item.id === notification.id ? { ...item, read: true } : item
          )
        )
        setUnreadCount((prev) => Math.max(0, prev - 1))
      }
    } catch (error) {
      console.error('Failed to mark notification as read', error)
    }

    setIsOpen(false)

    const path = getNotificationPath(notification)
    if (path) {
      navigate(path)
    }
  }

  const handleMarkAllRead = async () => {
    try {
      await accountAPI.markAllNotificationsRead()
      setNotifications((prev) => prev.map((item) => ({ ...item, read: true })))
      setUnreadCount(0)
    } catch (error) {
      console.error('Failed to mark all notifications as read', error)
    }
  }

  const handleDeleteNotification = async (event, notification) => {
    event.stopPropagation()

    try {
      await accountAPI.deleteNotification(notification.id)
      setNotifications((prev) => prev.filter((item) => item.id !== notification.id))
      if (!notification.read) {
        setUnreadCount((prev) => Math.max(0, prev - 1))
      }
    } catch (error) {
      console.error('Failed to delete notification', error)
    }
  }

  const handleDeleteAll = async () => {
    try {
      await accountAPI.deleteAllNotifications()
      setNotifications([])
      setUnreadCount(0)
    } catch (error) {
      console.error('Failed to delete all notifications', error)
    }
  }

  return (
    <div className="notification-bell" ref={containerRef}>
      <button
        type="button"
        className="notification-bell-button"
        onClick={handleToggle}
        aria-label="الإشعارات"
        aria-expanded={isOpen}
      >
        <span className="notification-bell-icon" aria-hidden="true">🔔</span>
        {unreadCount > 0 && (
          <span className="notification-badge" title={`${unreadCount} إشعار غير مقروء`}>
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="notification-dropdown">
          <div className="notification-dropdown-header">
            <div className="notification-dropdown-title">
              <h3>الإشعارات</h3>
              {unreadCount > 0 && (
                <span className="notification-header-count">{unreadCount} غير مقروء</span>
              )}
            </div>
            {notifications.length > 0 && (
              <div className="notification-header-actions">
                {unreadCount > 0 && (
                  <button
                    type="button"
                    className="notification-action-btn"
                    onClick={handleMarkAllRead}
                  >
                    تحديد الكل كمقروء
                  </button>
                )}
                <button
                  type="button"
                  className="notification-action-btn notification-action-danger"
                  onClick={handleDeleteAll}
                >
                  حذف الكل
                </button>
              </div>
            )}
          </div>

          <div className="notification-dropdown-body">
            {loading ? (
              <p className="notification-empty">جاري التحميل...</p>
            ) : notifications.length > 0 ? (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`notification-dropdown-item ${!notification.read ? 'unread' : ''}`}
                >
                  <button
                    type="button"
                    className="notification-item-content"
                    onClick={() => handleNotificationClick(notification)}
                  >
                    <div className="notification-item-header">
                      <strong>{notification.title}</strong>
                      {!notification.read && <span className="notification-unread-dot" />}
                    </div>
                    <p>{notification.message}</p>
                    <span className="notification-item-time">
                      {formatNotificationTime(notification.timestamp)}
                    </span>
                  </button>
                  <button
                    type="button"
                    className="notification-delete-btn"
                    onClick={(event) => handleDeleteNotification(event, notification)}
                    aria-label="حذف الإشعار"
                    title="حذف الإشعار"
                  >
                    ×
                  </button>
                </div>
              ))
            ) : (
              <p className="notification-empty">لا توجد إشعارات</p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default NotificationBell
