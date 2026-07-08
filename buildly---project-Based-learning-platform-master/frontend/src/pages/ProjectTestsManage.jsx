import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { projectsAPI } from '../services/api'
import './ProjectTestsManage.css'
import './Form.css'

const emptyTestForm = () => ({
  name: '',
  description: '',
  test_code: '',
  success_message: '',
  failure_message: '',
})

const ProjectTestsManage = () => {
  const { id: projectId } = useParams()
  const [project, setProject] = useState(null)
  const [tests, setTests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [editingTest, setEditingTest] = useState(null)
  const [formData, setFormData] = useState(emptyTestForm())

  useEffect(() => {
    fetchData()
  }, [projectId])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError('')
      const [projectRes, testsRes] = await Promise.all([
        projectsAPI.get(projectId),
        projectsAPI.getTests(projectId),
      ])
      setProject(projectRes.data.project)
      setTests(testsRes.data || [])
    } catch (err) {
      console.error('Error loading tests:', err)
      setError('فشل تحميل بيانات الاختبارات')
    } finally {
      setLoading(false)
    }
  }

  const openCreateModal = () => {
    setEditingTest(null)
    setFormData(emptyTestForm())
    setShowModal(true)
  }

  const openEditModal = (test) => {
    setEditingTest(test)
    setFormData({
      name: test.name || '',
      description: test.description || '',
      test_code: test.test_code || '',
      success_message: test.success_message || '',
      failure_message: test.failure_message || '',
    })
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setEditingTest(null)
    setFormData(emptyTestForm())
  }

  const handleFormChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSave = async (e) => {
    e.preventDefault()

    if (!formData.name.trim() || !formData.description.trim()) {
      setError('اسم الاختبار والوصف مطلوبان')
      return
    }

    setSaving(true)
    setError('')

    try {
      if (editingTest) {
        await projectsAPI.updateTest(editingTest.id, {
          project: Number(projectId),
          ...formData,
        })
      } else {
        await projectsAPI.createTest({
          project: Number(projectId),
          ...formData,
        })
      }

      closeModal()
      await fetchData()
    } catch (err) {
      const errorData = err.response?.data
      setError(
        errorData?.message ||
          errorData?.detail ||
          'حدث خطأ أثناء حفظ الاختبار'
      )
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (test) => {
    if (!window.confirm(`هل أنت متأكد من حذف الاختبار "${test.name}"؟`)) {
      return
    }

    try {
      await projectsAPI.deleteTest(test.id)
      setTests((prev) => prev.filter((item) => item.id !== test.id))
    } catch (err) {
      alert('فشل حذف الاختبار')
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="page-header tests-manage-header">
        <div>
          <Link to={`/projects/${projectId}`} className="back-link">
            ← العودة للمشروع
          </Link>
          <h1>الاختبارات</h1>
          {project && <p className="tests-manage-subtitle">{project.title}</p>}
        </div>
        <button type="button" className="btn btn-primary" onClick={openCreateModal}>
          + إضافة اختبار
        </button>
      </div>

      {error && !showModal && <div className="alert alert-error">{error}</div>}

      <div className="tests-manage-content">
        {tests.length === 0 ? (
          <div className="tests-empty-state">
            <p>لا توجد اختبارات لهذا المشروع بعد.</p>
            <button type="button" className="btn btn-secondary" onClick={openCreateModal}>
              إضافة أول اختبار
            </button>
          </div>
        ) : (
          <div className="tests-list">
            {tests.map((test, index) => (
              <article key={test.id} className="test-manage-card">
                <div className="test-manage-card-header">
                  <div>
                    <span className="test-manage-index">{index + 1}</span>
                    <h3>{test.name}</h3>
                  </div>
                  <div className="test-manage-actions">
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={() => openEditModal(test)}
                    >
                      تعديل
                    </button>
                    <button
                      type="button"
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDelete(test)}
                    >
                      حذف
                    </button>
                  </div>
                </div>

                <p className="test-manage-description">{test.description}</p>

                <div className="test-manage-meta">
                  <div className="test-manage-code-block">
                    <span className="test-manage-label">Test Code</span>
                    <pre>{test.test_code || '—'}</pre>
                  </div>
                  <div className="test-manage-messages">
                    <div>
                      <span className="test-manage-label success">Success Message</span>
                      <p>{test.success_message || '—'}</p>
                    </div>
                    <div>
                      <span className="test-manage-label failure">Failure Message</span>
                      <p>{test.failure_message || '—'}</p>
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal tests-modal" onClick={(e) => e.stopPropagation()}>
            <h3>{editingTest ? 'تعديل الاختبار' : 'إضافة اختبار جديد'}</h3>

            {error && showModal && <div className="alert alert-error">{error}</div>}

            <form onSubmit={handleSave} className="tests-form">
              <div className="input-group">
                <label htmlFor="name">Name *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleFormChange}
                  required
                  placeholder="اسم الاختبار"
                />
              </div>

              <div className="input-group">
                <label htmlFor="description">Description *</label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleFormChange}
                  required
                  rows={3}
                  placeholder="وصف ما يتحقق منه هذا الاختبار"
                />
              </div>

              <div className="input-group">
                <label htmlFor="test_code">Test Code</label>
                <textarea
                  id="test_code"
                  name="test_code"
                  value={formData.test_code}
                  onChange={handleFormChange}
                  rows={6}
                  placeholder="كود الاختبار (لن يُنفَّذ حالياً)"
                  className="code-textarea"
                />
              </div>

              <div className="input-group">
                <label htmlFor="success_message">Success Message</label>
                <textarea
                  id="success_message"
                  name="success_message"
                  value={formData.success_message}
                  onChange={handleFormChange}
                  rows={2}
                  placeholder="الرسالة عند نجاح الاختبار"
                />
              </div>

              <div className="input-group">
                <label htmlFor="failure_message">Failure Message</label>
                <textarea
                  id="failure_message"
                  name="failure_message"
                  value={formData.failure_message}
                  onChange={handleFormChange}
                  rows={2}
                  placeholder="الرسالة عند فشل الاختبار"
                />
              </div>

              <div className="modal-actions">
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? 'جاري الحفظ...' : editingTest ? 'حفظ التعديلات' : 'إضافة الاختبار'}
                </button>
                <button type="button" className="btn btn-secondary" onClick={closeModal}>
                  إلغاء
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProjectTestsManage
