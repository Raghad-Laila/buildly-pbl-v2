import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// إضافة token تلقائياً للطلبات
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// معالجة الأخطاء تلقائياً
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/account/token/refresh/`, {
            refresh: refreshToken,
          })

          const { access } = response.data
          localStorage.setItem('access_token', access)
          originalRequest.headers.Authorization = `Bearer ${access}`

          return api(originalRequest)
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Account APIs
export const accountAPI = {
  login: (email, password) =>
    api.post('/account/login/', { email, password }),

  registerLearner: (email, password, password2) =>
    api.post('/account/register/learner/', { email, password, password2 }),

  registerAdmin: (email, password, password2) =>
    api.post('/account/register/admin/', { email, password, password2 }),

  verifyEmail: (email, code) =>
    api.post('/account/verify/confirm/', { email, code }),

  resendOTP: (email) =>
    api.post('/account/verify/resend/', { email }),

  requestPasswordReset: (email) =>
    api.post('/account/password-reset/request/', { email }),

  resendPasswordResetOTP: (email) =>
    api.post('/account/password-reset/resend/', { email }),

  verifyPasswordResetOTP: (email, code) =>
    api.post('/account/password-reset/verify-otp/', { email, code }),

  confirmPasswordReset: (data) =>
    api.post('/account/password-reset/confirm/', data),

  logout: (refreshToken) =>
    api.post('/account/logout/', { refresh_token: refreshToken }),

  getProfile: () =>
    api.get('/account/profile/'),

  updateProfile: (data) =>
    api.patch('/account/profile/', data),

  uploadAvatar: (file) => {
    const formData = new FormData()
    formData.append('profile_picture', file)

    return api.patch('/account/profile/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  deleteAvatar: () =>
    api.delete('/account/profile/avatar/'),

  changePassword: (data) =>
    api.post('/account/profile/change-password/', data),

  getLearnerDashboard: () =>
    api.get('/account/learner/dashboard/'),

  getLearnerProgress: () =>
    api.get('/account/learner/progress/'),

  submitQuiz: (level) =>
    api.post("/account/quiz/submit/", { level }),

  getFavorites: () =>
    api.get('/account/favorites/'),

  toggleFavorite: (data) =>
    api.post('/account/favorites/toggle/', data),

  getNotifications: () =>
    api.get('/account/notifications/'),

  getUnreadNotificationsCount: () =>
    api.get('/account/notifications/unread-count/'),

  markNotificationRead: (notificationId) =>
    api.post(`/account/notifications/${notificationId}/read/`),

  markAllNotificationsRead: () =>
    api.post('/account/notifications/read-all/'),

  deleteNotification: (notificationId) =>
    api.delete(`/account/notifications/${notificationId}/`),

  deleteAllNotifications: () =>
    api.post('/account/notifications/delete-all/'),
}

// Courses APIs
export const coursesAPI = {
  list: () =>
    api.get('/courses/'),

  get: (id) =>
    api.get(`/courses/${id}/`),

  getDetails: (id) =>
    api.get(`/courses/${id}/details/`),

  create: (data) => {
    if (data.image instanceof File) {
      const formData = new FormData()
      Object.keys(data).forEach((key) => {
        if (data[key] === undefined || data[key] === null) return
        if (key === 'image' && !(data[key] instanceof File)) return
        const value = typeof data[key] === 'boolean' ? String(data[key]) : data[key]
        formData.append(key, value)
      })
      return api.post('/courses/create/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    }
    return api.post('/courses/create/', data)
  },

  update: (id, data) => {
    if (data.image instanceof File) {
      const formData = new FormData()
      Object.keys(data).forEach((key) => {
        if (data[key] === undefined || data[key] === null) return
        if (key === 'image' && !(data[key] instanceof File)) return
        const value = typeof data[key] === 'boolean' ? String(data[key]) : data[key]
        formData.append(key, value)
      })
      return api.put(`/courses/${id}/update/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    }
    const { image, ...rest } = data
    return api.put(`/courses/${id}/update/`, rest)
  },

  delete: (id) =>
    api.delete(`/courses/${id}/delete/`),

  confirmDelete: (id) =>
    api.get(`/courses/${id}/confirm-delete/`),

  confirmArchive: (id) =>
    api.get(`/courses/${id}/confirm-archive/`),

  archive: (id) =>
    api.post(`/courses/${id}/archive/`),

  listArchived: () =>
    api.get('/courses/archived/'),

  join: (id) =>
    api.post(`/courses/${id}/join/`),

  checkEnrollment: (id) =>
    api.get(`/courses/${id}/check-enrollment/`),

  myCourses: () =>
    api.get('/courses/my-courses/'),
}

// Projects APIs
export const projectsAPI = {
  list: (courseId = null, search = '') => {
    const params = {}
    if (courseId) params.course_id = courseId
    if (search?.trim()) params.search = search.trim()
    return api.get('/projects/', { params })
  },

  get: (id) =>
    api.get(`/projects/${id}/`),

  create: (data) => {
    if (data.image instanceof File) {
      const formData = new FormData()
      Object.keys(data).forEach((key) => {
        if (key === 'languages') {
          data[key].forEach((lang) => formData.append('languages', lang))
        } else {
          formData.append(key, data[key])
        }
      })
      return api.post('/projects/create/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    }
    return api.post('/projects/create/', data)
  },

  update: (id, data) => {
    if (data.image instanceof File) {
      const formData = new FormData()
      Object.keys(data).forEach((key) => {
        if (key === 'languages') {
          data[key].forEach((lang) => formData.append('languages', lang))
        } else if (data[key] !== undefined) {
          formData.append(key, data[key])
        }
      })
      return api.patch(`/projects/${id}/update/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    }
    return api.patch(`/projects/${id}/update/`, data)
  },

  delete: (id) =>
    api.delete(`/projects/${id}/delete/`),

  confirmDelete: (id) =>
    api.get(`/projects/${id}/confirm-delete/`),

  getByCourse: (courseId) =>
    api.get(`/projects/course/${courseId}/`),

  start: (id) =>
    api.post(`/projects/${id}/start/`),

  getProgress: () =>
    api.get('/progress/projects/'),

  uploadStarterFolder: (projectId, files) => {
    const formData = new FormData()
    Array.from(files).forEach((file) => {
      formData.append('files', file, file.webkitRelativePath || file.name)
    })

    return api.post(`/projects/${projectId}/starter-file/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  uploadStarterFile: (projectId, file) => {
    const formData = new FormData()
    formData.append('file', file)

    return api.post(`/projects/${projectId}/starter-file/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  createTask: (data) =>
    api.post('/projects/tasks/create/', data),

  getTasks: (projectId) =>
    api.get(`/projects/${projectId}/tasks/`),

  executeCode: ({ code, files, entryFileName, language } = {}) =>
    api.post('/projects/code/execute/', {
      ...(code != null ? { code: String(code) } : {}),
      ...(Array.isArray(files) && files.length
        ? { files, entryFileName: entryFileName || 'main.py' }
        : {}),
      language: language || 'python',
    }),

  aiReview: ({ project_id, files, test_summary, failed_tests, test_error } = {}) =>
    api.post('/projects/code/ai-review/', {
      project_id,
      files,
      ...(test_summary != null ? { test_summary } : {}),
      ...(failed_tests != null ? { failed_tests } : {}),
      ...(test_error != null && String(test_error).trim()
        ? { test_error: String(test_error).trim() }
        : {}),
    }),

  qualityReview: ({ project_id, files, test_summary } = {}) =>
    api.post('/projects/code/quality-review/', {
      project_id,
      files,
      ...(test_summary != null ? { test_summary } : {}),
    }),

  getBranches: (projectId) =>
    api.get(`/projects/${projectId}/branches/`),

  createBranch: (projectId, data) =>
    api.post(`/projects/${projectId}/branches/`, data),

  getBranch: (branchId) =>
    api.get(`/projects/branches/${branchId}/`),

  updateBranch: (branchId, data) =>
    api.patch(`/projects/branches/${branchId}/`, data),

  deleteBranch: (branchId) =>
    api.delete(`/projects/branches/${branchId}/`),

  mergeBranch: (branchId) =>
    api.post(`/projects/branches/${branchId}/merge/`),

  saveTaskSubmission: (taskId, data) =>
    api.post(`/projects/tasks/${taskId}/save/`, data),

  getTaskSubmission: (taskId) =>
    api.get(`/projects/tasks/${taskId}/get/`),

  complete: (id) =>
    api.post(`/progress/projects/${id}/complete/`),

  getProjectProgress: (projectId) =>
    api.get(`/progress/projects/${projectId}/progress/`),

  deleteTask: (taskId) =>
    api.delete(`/projects/tasks/${taskId}/delete/`),

  createTest: (data) =>
    api.post('/projects/tests/create/', data),

  getTests: (projectId) =>
    api.get(`/projects/${projectId}/tests/`),

  getTest: (testId) =>
    api.get(`/projects/tests/${testId}/`),

  updateTest: (testId, data) =>
    api.put(`/projects/tests/${testId}/update/`, data),

  deleteTest: (testId) =>
    api.delete(`/projects/tests/${testId}/delete/`),

  runTests: (projectId, { code, language, files, entryFileName } = {}) =>
    api.post(`/projects/${projectId}/tests/run/`, {
      code,
      language,
      ...(Array.isArray(files) && files.length ? { files, entryFileName } : {}),
    }),

  getSubmissions: (projectId) =>
    api.get(`/progress/projects/${projectId}/submissions/`),

  saveTaskFeedback: (taskId, userId, data) => {
    return api.post(`/projects/tasks/${taskId}/feedback/`, {
      userId,
      ...data
    });
  },

  submitFinalGrade: (projectId, userId, data) => {
    return api.post(`/progress/projects/${projectId}/review/`, {
      userId,
      ...data
    });
  },

  getStudentTaskSubmission: (taskId, userId) => {
    return api.get(`/projects/tasks/${taskId}/submission/${userId}/`);
  },

  getSingleSubmission: (projectId, userId) => 
    api.get(`/progress/projects/${projectId}/review/${userId}/`),

  getVersions: (projectId) =>
    api.get(`/projects/versions/${projectId}/`),

  rollback: (projectId, versionId) =>
    api.get(`/projects/rollback/${projectId}/${versionId}/`),
}

export const placementAPI = {
  getStatus: (courseId) =>
    api.get(`/placement/status/${courseId}/`),

  start: (courseId) =>
    api.post('/placement/start/', { course_id: Number(courseId) }),

  submitAnswer: (payload) =>
    api.post('/placement/submit-answer/', payload),

  replaceQuestion: (payload) =>
    api.post('/placement/replace-question/', payload),
}

export default api

