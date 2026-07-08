import React, { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { coursesAPI, projectsAPI } from '../services/api'
import ProjectContentSections from '../components/ProjectContentSections'
import ProjectLanguageSelect from '../components/ProjectLanguageSelect'
import {
  joinLines,
  createEmptyStory,
  buildTasksFromSections,
} from '../utils/projectContentMapper'
import './Form.css'

const ProjectCreate = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const courseIdFromState = location.state?.courseId
  const [courses, setCourses] = useState([])
  const [formData, setFormData] = useState({
    course_id: courseIdFromState || '',
    title: '',
    description: '',
    estimated_time: '',
    level: 'beginner',
    order: '',
  })
  const [selectedLanguages, setSelectedLanguages] = useState(['python'])
  const [languageError, setLanguageError] = useState('')
  const [objectiveItems, setObjectiveItems] = useState([''])
  const [userStories, setUserStories] = useState([createEmptyStory()])
  const [hintItems, setHintItems] = useState([''])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [fetchingCourses, setFetchingCourses] = useState(true)
  const [starterFile, setStarterFile] = useState(null)
  const [projectImage, setProjectImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)

  useEffect(() => {
    fetchCourses()
  }, [])

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setProjectImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const fetchCourses = async () => {
    try {
      setFetchingCourses(true)
      const response = await coursesAPI.list()
      setCourses(response.data.courses || [])
      if (courseIdFromState) {
        setFormData((prev) => ({ ...prev, course_id: courseIdFromState }))
      }
    } catch (err) {
      console.error('Error fetching courses:', err)
    } finally {
      setFetchingCourses(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value,
    })
    setError('')
  }

  const handleSubmit = async (e) => {
    if (e) e.preventDefault()
    setError('')

    const validStories = userStories.filter(
      (story) => story.title?.trim() && story.description?.trim()
    )

    if (validStories.length === 0) {
      setError('يجب إضافة قصة مستخدم واحدة على الأقل (عنوان ووصف)')
      return null
    }

    if (selectedLanguages.length === 0) {
      setLanguageError('يجب اختيار لغة واحدة على الأقل')
      return null
    }

    setLoading(true)

    try {
      const submitData = {
        ...formData,
        objectives: joinLines(objectiveItems),
        languages: selectedLanguages,
        course_id: parseInt(formData.course_id),
        estimated_time: parseInt(formData.estimated_time),
        order: formData.order ? parseInt(formData.order) : undefined,
        image: projectImage,
      }

      const response = await projectsAPI.create(submitData)

      if (response.data.success) {
        const projectId = response.data.project.project_id

        if (starterFile) {
          await projectsAPI.uploadStarterFile(projectId, starterFile)
        }

        const tasksToCreate = buildTasksFromSections({
          userStories,
          hintItems,
          projectId,
        })

        await Promise.all(
          tasksToCreate.map((task) => projectsAPI.createTask(task))
        )

        return projectId
      }
    } catch (err) {
      const errorData = err.response?.data

      if (errorData?.errors) {
        setError(
          Array.isArray(errorData.errors)
            ? errorData.errors.join(', ')
            : errorData.errors
        )
      } else if (errorData?.message) {
        setError(errorData.message)
      } else {
        setError('حدث خطأ أثناء إنشاء المشروع')
      }
      return null
    } finally {
      setLoading(false)
    }
  }

  const handleCreateAndGoToTests = async () => {
    const projectId = await handleSubmit()
    if (projectId) {
      navigate(`/projects/${projectId}/tests`)
    }
  }

  const handleFormSubmit = async (e) => {
    const projectId = await handleSubmit(e)
    if (projectId) {
      navigate(`/projects/${projectId}`)
    }
  }

  if (fetchingCourses) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1>إنشاء مشروع جديد</h1>
      </div>

      <div className="form-container">
        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleFormSubmit} className="form">
          <div className="input-group">
            <label htmlFor="course_id">المسار التعليمي *</label>
            <select
              id="course_id"
              name="course_id"
              value={formData.course_id}
              onChange={handleChange}
              required
            >
              <option value="">اختر المسار</option>
              {courses.map((course) => (
                <option key={course.id} value={course.id}>
                  {course.title}
                </option>
              ))}
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="title">عنوان المشروع *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              minLength={3}
              placeholder="أدخل عنوان المشروع"
            />
          </div>

          <div className="input-group">
            <label htmlFor="description">وصف المشروع *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              minLength={20}
              placeholder="أدخل وصفاً مفصلاً للمشروع"
            />
          </div>

          <ProjectContentSections
            objectiveItems={objectiveItems}
            onObjectiveItemsChange={setObjectiveItems}
            userStories={userStories}
            onUserStoriesChange={setUserStories}
            hintItems={hintItems}
            onHintItemsChange={setHintItems}
          />

          <div className="input-group">
            <label htmlFor="level">المستوى *</label>
            <select
              id="level"
              name="level"
              value={formData.level}
              onChange={handleChange}
              required
            >
              <option value="beginner">مبتدئ</option>
              <option value="intermediate">متوسط</option>
              <option value="advanced">متقدم</option>
              <option value="expert">خبير</option>
            </select>
          </div>

          <ProjectLanguageSelect
            selectedLanguages={selectedLanguages}
            onChange={(languages) => {
              setSelectedLanguages(languages)
              setLanguageError('')
            }}
            error={languageError}
          />

          <div className="input-group">
            <label htmlFor="project_image">صورة المشروع</label>
            <input
              type="file"
              id="project_image"
              accept="image/*"
              onChange={handleImageChange}
            />
            {imagePreview && (
              <div className="image-preview-container">
                <img src={imagePreview} alt="Preview" className="image-preview" />
              </div>
            )}
            <small className="input-hint">
              قم برفع صورة تعبيرية للمشروع (يفضل مقاس 16:9)
            </small>
          </div>

          <div className="input-group">
            <label htmlFor="starter_file">ملف البداية (اختياري)</label>
            <input
              type="file"
              id="starter_file"
              onChange={(e) => setStarterFile(e.target.files[0])}
            />
            <small className="input-hint">
              يمكنك رفع ملف يحتوي على كود مبدئي للمشروع
            </small>
          </div>

          <div className="form-row">
            <div className="input-group">
              <label htmlFor="estimated_time">الوقت المقدر (بالساعات) *</label>
              <input
                type="number"
                id="estimated_time"
                name="estimated_time"
                value={formData.estimated_time}
                onChange={handleChange}
                required
                min="1"
                max="500"
                placeholder="أدخل الوقت المقدر"
              />
            </div>

            <div className="input-group">
              <label htmlFor="order">الترتيب</label>
              <input
                type="number"
                id="order"
                name="order"
                value={formData.order}
                onChange={handleChange}
                min="0"
                placeholder="ترتيب المشروع في المسار"
              />
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'جاري الإنشاء...' : 'إنشاء المشروع'}
            </button>
            <button
              type="button"
              onClick={handleCreateAndGoToTests}
              className="btn btn-secondary"
              disabled={loading}
            >
              الاختبارات
            </button>
            <button
              type="button"
              onClick={() => navigate('/projects')}
              className="btn btn-secondary"
            >
              إلغاء
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ProjectCreate
