import React, { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import MultiFileEditor from '../components/MultiFileEditor'
import ExecutionPanel from '../components/ExecutionPanel'
import RunningTestsPanel from '../components/RunningTestsPanel'
import ProjectWorkProgress from '../components/ProjectWorkProgress'
import TestLinkStatus from '../components/TestLinkStatus'
import { projectsAPI } from '../services/api'
import {
    getDefaultWorkspace,
    getMainExecutableFile,
    parseWorkspace,
    serializeWorkspace,
    getWorkspaceFileContent,
    getWorkspaceSnapshot,
    workspaceHasContent,
} from '../utils/codeWorkspace'
import { executeWorkspace, getKernelLabel } from '../utils/executionEngine'
import {
    appendStreamBlock,
    createExecutionState,
    finalizeStreamBlocks,
    normalizeExecutionResult,
} from '../utils/executionResult'
import { getMonacoLanguage } from '../utils/frontendCodeRunner'
import { resetJsKernel } from '../utils/jsKernel'
import { resetPythonKernel } from '../utils/pythonKernel'
import {
    canRunTestsOnClient,
    runClientTests,
    shouldUseWorkspaceFileTests,
} from '../utils/testRunner'
import { linkResultsByIndex } from '../utils/testResultLinking'
import { getProjectTestProgress } from '../utils/projectProgress'
import { getPrimaryProjectLanguage } from '../utils/projectLanguages'
import './ProjectWork.css'

const parseLines = (text) => {
    if (!text?.trim()) return []
    return text
        .split('\n')
        .map((line) => line.trim())
        .filter(Boolean)
}

const ProjectWork = () => {
    const { id } = useParams()
    const navigate = useNavigate()

    const [project, setProject] = useState(null)
    const [tasks, setTasks] = useState([])
    const [tests, setTests] = useState([])
    const [currentIndex, setCurrentIndex] = useState(0)

    const [workspace, setWorkspace] = useState(null)
    const [textAnswer, setTextAnswer] = useState('')
    const [hintsOpen, setHintsOpen] = useState(false)
    const [showCurrentHint, setShowCurrentHint] = useState(false)

    const [loading, setLoading] = useState(true)
    const [execution, setExecution] = useState(createExecutionState())
    const [running, setRunning] = useState(false)
    const [runningTests, setRunningTests] = useState(false)
    const [testResults, setTestResults] = useState(null)
    const [testError, setTestError] = useState('')

    const workspaceRef = useRef('')
    const textRef = useRef('')
    const streamBlocksRef = useRef([])
    const projectLanguage = getPrimaryProjectLanguage(project)

    useEffect(() => {
        fetchData()
    }, [id])

    useEffect(() => {
        if (!tasks.length || !workspace) return

        const interval = setInterval(() => {
            saveTask()
        }, 5000)

        return () => clearInterval(interval)
    }, [tasks, currentIndex, workspace])

    useEffect(() => {
        if (!tasks.length || !project) return
        const task = tasks[currentIndex]

        const loadSubmission = async () => {
            try {
                const res = await projectsAPI.getTaskSubmission(task.id)
                if (task.task_type === 'code') {
                    const ws = parseWorkspace(
                        res.data.progress.answer || '',
                        projectLanguage
                    )
                    setWorkspace(ws)
                    workspaceRef.current = serializeWorkspace(ws)
                } else if (task.task_type === 'text') {
                    setTextAnswer(res.data.progress.answer || '')
                    textRef.current = res.data.progress.answer || ''
                }
            } catch (err) {
                if (task.task_type === 'code') {
                    const ws = getDefaultWorkspace(projectLanguage)
                    setWorkspace(ws)
                    workspaceRef.current = serializeWorkspace(ws)
                }
            }
        }

        loadSubmission()
    }, [tasks, currentIndex, project])

    const handleWorkspaceChange = (nextWorkspace) => {
        setWorkspace(nextWorkspace)
        workspaceRef.current = serializeWorkspace(nextWorkspace)
    }

    const saveTask = async () => {
        const currentTask = tasks[currentIndex]
        if (!currentTask) return

        try {
            const value =
                currentTask.task_type === 'code'
                    ? workspaceRef.current
                    : textRef.current

            if (!value.trim()) return

            await projectsAPI.saveTaskSubmission(currentTask.id, {
                answer: value
            })
        } catch (err) {
            console.error('Autosave error:', err)
        }
    }

    const runCode = async () => {
        if (!workspace || running) return

        const currentWorkspace = getWorkspaceSnapshot(workspaceRef, workspace)
        const runId = Date.now()

        setRunning(true)
        streamBlocksRef.current = []

        const kernelLabel = getKernelLabel(projectLanguage, currentWorkspace)

        setExecution({
            ...createExecutionState('running'),
            runId,
            previewHtml: null,
            kernelMessage: 'جاري التنفيذ...',
            blocks: [],
        })

        const start = performance.now()

        const onStream = (type, chunk) => {
            if (type === 'status') {
                setExecution((prev) => ({
                    ...prev,
                    kernelMessage: chunk,
                }))
                return
            }

            if (type === 'stdout' || type === 'stderr') {
                streamBlocksRef.current = appendStreamBlock(
                    streamBlocksRef.current,
                    type,
                    chunk
                )

                setExecution((prev) => ({
                    ...prev,
                    status: 'running',
                    blocks: [...streamBlocksRef.current],
                }))
            }
        }

        try {
            const raw = await executeWorkspace(currentWorkspace, projectLanguage, {
                onStream,
                runServerPython: async (code) => {
                    const res = await projectsAPI.executeCode(code, projectLanguage)
                    const stderr = res.data.stderr || res.data.error || ''
                    const stdout = res.data.stdout || ''

                    return {
                        stdout,
                        stderr,
                        returnValue: '',
                        status: res.data.returncode === 0 && !stderr ? 'success' : 'error',
                        kernelMessage: 'Docker Python',
                        previewHtml: null,
                        hasPreview: false,
                    }
                },
            })

            const normalized = normalizeExecutionResult(raw, performance.now() - start)
            const streamed = finalizeStreamBlocks(streamBlocksRef.current)

            setExecution({
                ...normalized,
                runId,
                blocks: streamed.length ? streamed : normalized.blocks,
                previewHtml: raw.previewHtml || null,
                activeTab: raw.previewHtml ? 'preview' : 'console',
                kernelMessage: raw.kernelMessage || kernelLabel,
            })
        } catch (err) {
            setExecution({
                ...createExecutionState('error'),
                durationMs: Math.round(performance.now() - start),
                kernelMessage: kernelLabel,
                blocks: [
                    {
                        id: `error-${Date.now()}`,
                        type: 'error',
                        content: err.message || 'Error running code',
                    },
                ],
            })
        } finally {
            setRunning(false)
        }
    }

    const getStudentCode = (currentWorkspace = workspace) => {
        if (!currentWorkspace || !project) return ''
        const mainFile = getMainExecutableFile(currentWorkspace, projectLanguage)
        return mainFile?.content?.trim() || ''
    }

    const runTests = async () => {
        if (!workspace || runningTests || task?.task_type !== 'code') return

        const currentWorkspace = getWorkspaceSnapshot(workspaceRef, workspace)
        const useWorkspaceTests = shouldUseWorkspaceFileTests(projectLanguage, tests)

        if (useWorkspaceTests) {
            const html = getWorkspaceFileContent(currentWorkspace, 'index.html').trim()
            const css = getWorkspaceFileContent(currentWorkspace, 'style.css').trim()

            if (projectLanguage === 'css' ? !css && !html : !html) {
                setTestError('اكتب الكود أولاً قبل تشغيل الاختبارات.')
                setTestResults(null)
                return
            }
        } else {
            const code = getStudentCode(currentWorkspace)
            if (!code) {
                setTestError('اكتب الكود أولاً قبل تشغيل الاختبارات.')
                setTestResults(null)
                return
            }
        }

        if (!tests.length) {
            setTestError('')
            setTestResults({
                results: [],
                summary: { total: 0, passed: 0, failed: 0 },
            })
            return
        }

        setRunningTests(true)
        setTestError('')
        setTestResults(null)

        try {
            let payload

            if (canRunTestsOnClient(projectLanguage)) {
                payload = runClientTests(getStudentCode(currentWorkspace), tests, {
                    workspace: currentWorkspace,
                    projectLanguage,
                })
            } else {
                const response = await projectsAPI.runTests(
                    id,
                    getStudentCode(currentWorkspace),
                    projectLanguage
                )
                payload = {
                    results: response.data.results || [],
                    summary: response.data.summary || {
                        total: 0,
                        passed: 0,
                        failed: 0,
                    },
                }
            }

            setTestResults(payload)
        } catch (err) {
            const message =
                err.response?.data?.error ||
                err.response?.data?.message ||
                err.message ||
                'فشل تشغيل الاختبارات'
            setTestError(message)
            setTestResults(null)
        } finally {
            setRunningTests(false)
        }
    }

    const clearExecution = () => {
        setExecution(createExecutionState())
        streamBlocksRef.current = []
    }

    const resetKernel = () => {
        resetPythonKernel()
        resetJsKernel()
        clearExecution()
    }

    const fetchData = async () => {
        try {
            const [tasksRes, projectRes, testsRes] = await Promise.all([
                projectsAPI.getTasks(id),
                projectsAPI.get(id),
                projectsAPI.getTests(id).catch(() => ({ data: [] })),
            ])

            const p = projectRes.data.project
            setProject(p)
            setTasks(tasksRes.data || [])
            setTests(testsRes.data || [])

            setLoading(false)
        } catch (err) {
            console.error(err)
            setLoading(false)
        }
    }

    const task = tasks[currentIndex]

    const isTaskCompleted = () => {
        if (!task) return false

        if (task.task_type === 'code') {
            return workspace ? workspaceHasContent(workspace) : false
        }

        if (task.task_type === 'text') {
            return textAnswer.trim().length > 0
        }

        return false
    }

    const resetTaskState = () => {
        setWorkspace(null)
        workspaceRef.current = ''
        setTextAnswer('')
        textRef.current = ''
        clearExecution()
        setHintsOpen(false)
        setShowCurrentHint(false)
    }

    const handleSelectTask = (index) => {
        if (index === currentIndex) return
        resetTaskState()
        setCurrentIndex(index)
    }

    const handleFinish = async () => {
        if (!isTaskCompleted()) return

        try {
            await saveTask()
            await projectsAPI.complete(id)
            alert('🎉 تم إكمال المشروع بنجاح!')
            navigate('/projects')
        } catch (err) {
            console.error('Error completing project:', err)
            alert('حدث خطأ أثناء الحفظ.')
        }
    }

    const showKernelReset =
        projectLanguage === 'python' || projectLanguage === 'javascript'

    const objectives = parseLines(project?.objectives)
    const userStories = tasks.length
        ? tasks.map((t, index) => ({
            id: t.id,
            index,
            text: t.description?.trim() || t.title,
            title: t.title,
        }))
        : []

    const objectivesWithStatus = linkResultsByIndex(
        objectives.map((text, index) => ({ id: index, index, text })),
        testResults
    )

    const userStoriesWithStatus = linkResultsByIndex(userStories, testResults)

    const availableHints = tasks
        .map((t, index) => ({ id: t.id, index, title: t.title, hint: t.hint }))
        .filter((item) => item.hint?.trim())

    const currentHint = task?.hint?.trim()
    const testProgress = getProjectTestProgress(tests, testResults)

    if (loading) return <div className="loading">Loading...</div>
    if (!project) return <div>Project not found</div>

    return (
        <div className="fcc-workspace">
            <header className="fcc-header">
                <div>
                    <p className="fcc-breadcrumb">Project Workspace</p>
                    <h1>{project.title}</h1>
                </div>
                <button
                    type="button"
                    className="btn btn-success fcc-submit-btn"
                    onClick={handleFinish}
                    disabled={!isTaskCompleted()}
                >
                    تسليم المشروع
                </button>
            </header>

            <div className="fcc-layout">
                <div className="fcc-content">
                    <ProjectWorkProgress progress={testProgress} />

                    <section className="fcc-section">
                        <h2 className="fcc-section-title">Project Description</h2>
                        <div className="fcc-section-body">
                            <p className="fcc-description">{project.description}</p>
                        </div>
                    </section>

                    <section className="fcc-section">
                        <h2 className="fcc-section-title">Objectives</h2>
                        <div className="fcc-section-body">
                            {objectivesWithStatus.length > 0 ? (
                                <ul className="fcc-list">
                                    {objectivesWithStatus.map((item) => (
                                        <li key={item.id} className="fcc-list-item-with-status">
                                            <span className="fcc-list-item-text">{item.text}</span>
                                            <TestLinkStatus status={item.testStatus} />
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p className="fcc-empty-note">لا توجد أهداف محددة لهذا المشروع بعد.</p>
                            )}
                        </div>
                    </section>

                    <section className="fcc-section">
                        <h2 className="fcc-section-title">User Stories</h2>
                        <div className="fcc-section-body">
                            {userStoriesWithStatus.length > 0 ? (
                                <ul className="fcc-story-list">
                                    {userStoriesWithStatus.map((story) => (
                                        <li key={story.id}>
                                            <button
                                                type="button"
                                                className={`fcc-story-item ${story.index === currentIndex ? 'active' : ''}`}
                                                onClick={() => handleSelectTask(story.index)}
                                            >
                                                <span className="fcc-story-marker" aria-hidden="true" />
                                                <span className="fcc-story-text">
                                                    <span className="fcc-story-title-row">
                                                        <strong>{story.title}</strong>
                                                        <TestLinkStatus status={story.testStatus} />
                                                    </span>
                                                    <span>{story.text}</span>
                                                </span>
                                            </button>
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p className="fcc-empty-note">لا توجد قصص مستخدم لهذا المشروع بعد.</p>
                            )}
                        </div>
                    </section>

                    <section className="fcc-section fcc-hints-section">
                        <button
                            type="button"
                            className="fcc-hints-toggle"
                            onClick={() => setHintsOpen((prev) => !prev)}
                            aria-expanded={hintsOpen}
                        >
                            <span>Hints</span>
                            <span className="fcc-hints-icon">{hintsOpen ? '−' : '+'}</span>
                        </button>

                        {hintsOpen && (
                            <div className="fcc-hints-panel">
                                {availableHints.length > 0 ? (
                                    availableHints.map((item) => (
                                        <div key={item.id} className="fcc-hint-card">
                                            <h4>{item.title}</h4>
                                            <p>{item.hint}</p>
                                        </div>
                                    ))
                                ) : currentHint ? (
                                    <div className="fcc-hint-card">
                                        <p>{currentHint}</p>
                                    </div>
                                ) : (
                                    <p className="fcc-empty-note">لا توجد تلميحات متاحة حالياً.</p>
                                )}
                            </div>
                        )}
                    </section>

                    <section className="fcc-section fcc-editor-section">
                        <h2 className="fcc-section-title">Code Editor</h2>
                        <div className="fcc-section-body">
                            {task && (
                                <p className="fcc-current-task-label">
                                    المهمة الحالية: <strong>{task.title}</strong>
                                </p>
                            )}

                            {task?.task_type === 'code' && workspace && (
                                <div className="deepnote-workspace">
                                    <div className="deepnote-split">
                                        <div className="deepnote-editor-pane">
                                            <MultiFileEditor
                                                workspace={workspace}
                                                onChange={handleWorkspaceChange}
                                                onRun={runCode}
                                                editorHeight="470px"
                                                defaultMonacoLanguage={getMonacoLanguage(projectLanguage)}
                                            />
                                        </div>

                                        <div className="deepnote-output-pane">
                                            <ExecutionPanel
                                                execution={execution}
                                                kernelLabel={getKernelLabel(projectLanguage, workspace)}
                                                onClear={clearExecution}
                                                onResetKernel={resetKernel}
                                                showResetKernel={showKernelReset}
                                            />
                                        </div>
                                    </div>
                                </div>
                            )}

                            {task?.task_type === 'text' && (
                                <textarea
                                    className="text-input"
                                    value={textAnswer}
                                    onChange={(e) => {
                                        textRef.current = e.target.value
                                        setTextAnswer(e.target.value)
                                    }}
                                    placeholder="اكتب إجابتك هنا..."
                                />
                            )}

                            <div className="fcc-check-row">
                                <button
                                    type="button"
                                    className="btn btn-primary fcc-check-btn"
                                    onClick={runTests}
                                    disabled={runningTests || task?.task_type !== 'code' || !workspace}
                                >
                                    {runningTests ? (
                                        <>
                                            <span className="execution-spinner" />
                                            Checking...
                                        </>
                                    ) : (
                                        'Check Code'
                                    )}
                                </button>

                                <button
                                    type="button"
                                    className="btn btn-secondary fcc-show-hint-btn"
                                    onClick={() => setShowCurrentHint((prev) => !prev)}
                                    disabled={!currentHint}
                                >
                                    {showCurrentHint ? 'Hide Hint' : 'Show Hint'}
                                </button>

                                {task?.task_type === 'code' && (
                                    <span className="fcc-check-hint">
                                        أو استخدم <kbd>Ctrl</kbd> + <kbd>Enter</kbd> لتشغيل الكود
                                    </span>
                                )}
                            </div>

                            {showCurrentHint && currentHint && (
                                <div className="fcc-current-hint-panel">
                                    <h4>تلميح للمهمة الحالية</h4>
                                    <p>{currentHint}</p>
                                </div>
                            )}
                        </div>
                    </section>

                    <RunningTestsPanel
                        running={runningTests}
                        testError={testError}
                        testResults={testResults}
                        testsCount={tests.length}
                    />
                </div>
            </div>
        </div>
    )
}

export default ProjectWork
