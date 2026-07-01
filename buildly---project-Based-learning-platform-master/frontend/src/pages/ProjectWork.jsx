import React, { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import MultiFileEditor from '../components/MultiFileEditor'
import ExecutionPanel from '../components/ExecutionPanel'
import { projectsAPI } from '../services/api'
import {
    getDefaultWorkspace,
    parseWorkspace,
    serializeWorkspace,
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
import './ProjectWork.css'

const ProjectWork = () => {
    const { id } = useParams()
    const navigate = useNavigate()

    const [project, setProject] = useState(null)
    const [tasks, setTasks] = useState([])
    const [currentIndex, setCurrentIndex] = useState(0)

    const [workspace, setWorkspace] = useState(null)
    const [textAnswer, setTextAnswer] = useState('')
    const [showHint, setShowHint] = useState(false)

    const [loading, setLoading] = useState(true)
    const [execution, setExecution] = useState(createExecutionState())
    const [running, setRunning] = useState(false)

    const workspaceRef = useRef('')
    const textRef = useRef('')
    const streamBlocksRef = useRef([])

    const isLastTask = currentIndex === tasks.length - 1

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
                        project.language
                    )
                    setWorkspace(ws)
                    workspaceRef.current = serializeWorkspace(ws)
                } else if (task.task_type === 'text') {
                    setTextAnswer(res.data.progress.answer || '')
                    textRef.current = res.data.progress.answer || ''
                }
            } catch (err) {
                if (task.task_type === 'code') {
                    const ws = getDefaultWorkspace(project.language)
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

        setRunning(true)
        streamBlocksRef.current = []

        const kernelLabel = getKernelLabel(project.language, workspace)

        setExecution({
            ...createExecutionState('running'),
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
            const raw = await executeWorkspace(workspace, project.language, {
                onStream,
                runServerPython: async (code) => {
                    const res = await projectsAPI.executeCode(code, project.language)
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
            const res = await projectsAPI.getTasks(id)
            const proj_res = await projectsAPI.get(id)

            const p = proj_res.data.project
            setProject(p)
            setTasks(res.data || [])

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
        setShowHint(false)
    }

    const handlePrev = () => {
        resetTaskState()
        setCurrentIndex((prev) => Math.max(prev - 1, 0))
    }

    const handleNext = async () => {
        if (!isTaskCompleted()) return

        await saveTask()
        resetTaskState()
        setCurrentIndex((prev) => Math.min(prev + 1, tasks.length - 1))
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

    const progressPercentage = tasks.length > 0
        ? Math.round(((currentIndex + 1) / tasks.length) * 100)
        : 0

    const showKernelReset =
        project?.language === 'python' || project?.language === 'javascript'

    if (loading) return <div className="loading">Loading...</div>
    if (!project) return <div>Project not found</div>

    return (
        <div className="workspace">
            <div className="sidebar">
                <h3>{project.title}</h3>
                <ul>
                    {tasks.map((t, i) => (
                        <li
                            key={t.id}
                            className={i === currentIndex ? 'active' : ''}
                        >
                            {t.title}
                        </li>
                    ))}
                </ul>
            </div>

            <div className="workmain">
                <div className="progress-container">
                    <div className="progress-label">
                        <span>نسبة الإنجاز</span>
                        <span>{progressPercentage}%</span>
                    </div>
                    <div className="progress-bar-bg">
                        <div
                            className="progress-bar-fill"
                            style={{ width: `${progressPercentage}%` }}
                        ></div>
                    </div>
                </div>

                <div className="task-header">
                    <h2>{task?.title}</h2>
                    <span>{currentIndex + 1} / {tasks.length}</span>
                </div>

                <div className="quiz-question">
                    <h3>{task?.description}</h3>
                </div>

                <div className="task-body">
                    {task?.task_type === 'code' && workspace && (
                        <div className="deepnote-workspace">
                            <div className="deepnote-toolbar">
                                <button
                                    className="btn btn-success deepnote-run-btn"
                                    onClick={runCode}
                                    disabled={running}
                                >
                                    {running ? (
                                        <>
                                            <span className="execution-spinner" />
                                            جاري التشغيل...
                                        </>
                                    ) : (
                                        <>▶ تشغيل</>
                                    )}
                                </button>
                                <span className="deepnote-shortcut-hint">
                                    <kbd>Ctrl</kbd> + <kbd>Enter</kbd>
                                </span>
                            </div>

                            <div className="deepnote-split">
                                <div className="deepnote-editor-pane">
                                    <MultiFileEditor
                                        workspace={workspace}
                                        onChange={handleWorkspaceChange}
                                        onRun={runCode}
                                        editorHeight="470px"
                                        defaultMonacoLanguage={getMonacoLanguage(project.language)}
                                    />
                                </div>

                                <div className="deepnote-output-pane">
                                    <ExecutionPanel
                                        execution={execution}
                                        kernelLabel={getKernelLabel(project.language, workspace)}
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

                    <div className="hint-section">
                        <button
                            className="btn btn-secondary"
                            onClick={() => setShowHint(!showHint)}
                        >
                            💡 عرض التلميح
                        </button>

                        {showHint && (
                            <div className="hint-box">
                                {task?.hint}
                            </div>
                        )}
                    </div>
                </div>

                <div className="quiz-actions">
                    <button
                        className="btn btn-secondary"
                        onClick={handlePrev}
                        disabled={currentIndex === 0}
                    >
                        السابق
                    </button>

                    {isLastTask ? (
                        <button
                            className="btn btn-success"
                            onClick={handleFinish}
                            disabled={!isTaskCompleted()}
                        >
                            تسليم المشروع
                        </button>
                    ) : (
                        <button
                            className="btn btn-primary"
                            onClick={handleNext}
                            disabled={!isTaskCompleted()}
                        >
                            التالي
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}

export default ProjectWork
