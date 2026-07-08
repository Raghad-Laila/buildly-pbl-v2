import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { projectsAPI } from '../services/api'
import ProjectContentSections from '../components/ProjectContentSections'
import ProjectLanguageSelect from '../components/ProjectLanguageSelect'
import {
  splitLines,
  joinLines,
  createEmptyStory,
  tasksToEditorState,
  syncProjectTasksOnEdit,
} from '../utils/projectContentMapper'
import { getProjectLanguages } from '../utils/projectLanguages'
import './Form.css'

const ProjectEdit = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
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
  const [originalTasks, setOriginalTasks] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(true)
  const [projectImage, setProjectImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [starterFile, setStarterFile] = useState(null)
  const [existingStarterFile, setExistingStarterFile] = useState(null)

  useEffect(() => {
    fetchProject()
  }, [id])

  const fetchProject = async () => {
    try {
      setFetching(true)
      const response = await projectsAPI.get(id)
      const project = response.data.project
      setFormData({
        title: project.title,
        description: project.description,
        estimated_time: project.estimated_time,
        level: project.level,
        order: project.order || '',
      })
      setSelectedLanguages(getProjectLanguages(project))
      setImagePreview(project.image)
      setExistingStarterFile(project.starter_file)

      const objectives = splitLines(project.objectives)
      setObjectiveItems(objectives.length > 0 ? objectives : [''])

      const tasksResponse = await projectsAPI.getTasks(id)
      const tasks = tasksResponse.data || []
      setOriginalTasks(tasks)

      const { userStories: loadedStories, hintItems: loadedHints } =
        tasksToEditorState(tasks)
      setUserStories(loadedStories)
      setHintItems(loadedHints)
    } catch (err) {
      setError('فشل تحميل بيانات المشروع')
    } finally {
      setFetching(false)
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

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    const validStories = userStories.filter(
      (story) => story.title?.trim() && story.description?.trim()
    )

    if (validStories.length === 0) {
      setError('يجب إضافة قصة مستخدم واحدة على الأقل (عنوان ووصف)')
      return
    }

    if (selectedLanguages.length === 0) {
      setLanguageError('يجب اختيار لغة واحدة على الأقل')
      return
    }

    setLoading(true)

    try {
      const submitData = {
        ...formData,
        objectives: joinLines(objectiveItems),
        languages: selectedLanguages,
        estimated_time: parseInt(formData.estimated_time),
        order: formData.order ? parseInt(formData.order) : undefined,
      }

      if (projectImage) {
        submitData.image = projectImage
      }

      await projectsAPI.update(id, submitData)

      if (starterFile) {
        await projectsAPI.uploadStarterFile(id, starterFile)
      }

      await syncProjectTasksOnEdit({
        projectId: id,
        originalTasks,
        userStories,
        hintItems,
        projectsAPI,
      })

      navigate(`/projects/${id}`)
    } catch (err) {
      const errorData = err.response?.data
      console.error('Error updating project:', err.response?.data || err.message)

      if (errorData?.message) {
        setError(errorData.message)
      } else if (errorData?.errors) {
        if (typeof errorData.errors === 'object' && !Array.isArray(errorData.errors)) {
          const fieldErrors = Object.entries(errorData.errors)
            .map(([field, messages]) => {
              const fieldName = field === 'non_field_errors' ? '' : `${field}: `
              return Array.isArray(messages)
                ? `${fieldName}${messages.join(', ')}`
                : `${fieldName}${messages}`
            })
            .join('\n')
          setError(fieldErrors || 'حدث خطأ أثناء تحديث المشروع')
        } else {
          setError(
            Array.isArray(errorData.errors)
              ? errorData.errors.join(', ')
              : errorData.errors
          )
        }
      } else if (errorData?.detail) {
        setError(errorData.detail)
      } else {
        setError(err.message || 'حدث خطأ أثناء تحديث المشروع')
      }
    } finally {
      setLoading(false)
    }
  }

  if (fetching) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1>تعديل المشروع</h1>
      </div>

      <div className="form-container">
        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} className="form">
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
              يمكنك تغيير صورة المشروع الحالية
            </small>
          </div>

          <div className="input-group">
            <label htmlFor="starter_file">ملف البداية (اختياري)</label>
            <input
              type="file"
              id="starter_file"
              onChange={(e) => setStarterFile(e.target.files[0])}
            />
            {existingStarterFile && (
              <p className="existing-file-info">
                الملف الحالي: <a href={existingStarterFile.file_url} target="_blank" rel="noreferrer">{existingStarterFile.file_name}</a>
              </p>
            )}
            <small className="input-hint">
              يمكنك تغيير ملف البداية الخاص بالمشروع
            </small>
          </div>

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
              {loading ? 'جاري التحديث...' : 'حفظ التغييرات'}
            </button>
            <button
              type="button"
              onClick={() => navigate(`/projects/${id}/tests`)}
              className="btn btn-secondary"
            >
              الاختبارات
            </button>
            <button
              type="button"
              onClick={() => navigate(`/projects/${id}`)}
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

export default ProjectEdit
