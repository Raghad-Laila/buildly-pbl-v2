export const formatNotificationTime = (timestamp) => {
  return new Date(timestamp).toLocaleString('ar-SY', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export const getNotificationPath = (notification) => {
  if (notification?.project_id) {
    if (notification.type === 'project_started') {
      return `/projects/${notification.project_id}/work`
    }
    return `/projects/${notification.project_id}`
  }

  if (notification?.type === 'account_created') {
    return '/dashboard'
  }

  if (notification?.type === 'password_reset') {
    return '/profile'
  }

  return null
}
