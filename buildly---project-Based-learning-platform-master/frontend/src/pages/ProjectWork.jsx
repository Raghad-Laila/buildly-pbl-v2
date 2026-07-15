import React, { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import MultiFileEditor from '../components/MultiFileEditor'
import FileExplorer from '../components/FileExplorer'
import BottomDock from '../components/BottomDock'
import ExecutionPanel from '../components/ExecutionPanel'
import RunningTestsPanel from '../components/RunningTestsPanel'
import ProjectWorkProgress from '../components/ProjectWorkProgress'
import ProjectWorkSidebar from '../components/ProjectWorkSidebar'
import { projectsAPI } from '../services/api'
import {
    addFile,
    deleteFile,
    getDefaultWorkspace,
    getMainExecutableFile,
    parseWorkspace,
    renameFile,
    serializeWorkspace,
    setActiveFile,
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
import {
    DOCK_HEIGHT_DEFAULT,
    DOCK_HEIGHT_MAX_RATIO,
    DOCK_TAB_DEFAULT,
    EXPLORER_WIDTH_DEFAULT,
    clampDockHeight as clampStoredDockHeight,
    clampExplorerWidth as clampStoredExplorerWidth,
    loadWorkspaceUiPrefs,
    saveWorkspaceUiPrefs,
} from '../utils/workspaceUiStorage'
import './ProjectWork.css'

const RESIZE_BREAKPOINT = 1100

async function loadSharedProjectWorkspace(taskList, projectLanguage) {
    const codeTasks = taskList.filter((item) => item.task_type === 'code')
    if (!codeTasks.length) {
        return null
    }

    let bestWorkspace = null
    let bestScore = -1

    for (const codeTask of codeTasks) {
        try {
            const res = await projectsAPI.getTaskSubmission(codeTask.id)
            const answer = res.data.progress?.answer || ''
            if (!answer.trim()) continue

            const parsed = parseWorkspace(answer, projectLanguage)
            const score = parsed.files?.reduce(
                (sum, file) => sum + (file.content?.length || 0),
                0
            ) || 0

            if (score > bestScore) {
                bestScore = score
                bestWorkspace = parsed
            }
        } catch {
            // ignore missing submissions
        }
    }

    return bestWorkspace || getDefaultWorkspace(projectLanguage)
}

const ProjectWork = () => {
    const { id } = useParams()
    const navigate = useNavigate()

    const [project, setProject] = useState(null)
    const [tasks, setTasks] = useState([])
    const [tests, setTests] = useState([])

    const [workspace, setWorkspace] = useState(null)
    const [textAnswer, setTextAnswer] = useState('')

    const [loading, setLoading] = useState(true)
    const [execution, setExecution] = useState(createExecutionState())
    const [running, setRunning] = useState(false)
    const [runningTests, setRunningTests] = useState(false)
    const [testResults, setTestResults] = useState(null)
    const [testError, setTestError] = useState('')

    const workspaceRef = useRef('')
    const textRef = useRef('')
    const streamBlocksRef = useRef([])
    const workspaceLayoutRef = useRef(null)
    const resizeDragRef = useRef(null)
    const resizeRafRef = useRef(null)
    const livePanelSizesRef = useRef({
        explorerWidth: EXPLORER_WIDTH_DEFAULT,
        dockHeight: DOCK_HEIGHT_DEFAULT,
    })
    const pendingActiveFileIdRef = useRef(null)

    const [explorerWidth, setExplorerWidth] = useState(EXPLORER_WIDTH_DEFAULT)
    const [dockHeight, setDockHeight] = useState(DOCK_HEIGHT_DEFAULT)
    const [dockActiveTab, setDockActiveTab] = useState(DOCK_TAB_DEFAULT)
    const [explorerCollapsed, setExplorerCollapsed] = useState(false)
    const [uiHydrated, setUiHydrated] = useState(false)

    const projectLanguage = getPrimaryProjectLanguage(project)

    const isResizeEnabled = () => window.matchMedia(`(max-width: ${RESIZE_BREAKPOINT}px)`).matches === false

    const applyPanelSizeVariables = (width, height) => {
        const layout = workspaceLayoutRef.current
        if (!layout) return
        layout.style.setProperty('--explorer-width', `${width}px`)
        layout.style.setProperty('--dock-height', `${height}px`)
    }

    const getMaxDockHeight = () => {
        const layout = workspaceLayoutRef.current
        return layout ? layout.clientHeight * DOCK_HEIGHT_MAX_RATIO : Number.POSITIVE_INFINITY
    }

    const clampExplorerWidth = (width) =>
        clampStoredExplorerWidth(width) ?? EXPLORER_WIDTH_DEFAULT

    const clampDockHeight = (height) =>
        clampStoredDockHeight(height, getMaxDockHeight()) ?? DOCK_HEIGHT_DEFAULT

    const refreshEditorLayout = () => {
        window.dispatchEvent(new Event('resize'))
    }

    const schedulePanelSizePaint = () => {
        if (resizeRafRef.current != null) return

        resizeRafRef.current = requestAnimationFrame(() => {
            resizeRafRef.current = null
            if (!resizeDragRef.current) return

            const { explorerWidth: width, dockHeight: height } = livePanelSizesRef.current
            applyPanelSizeVariables(width, height)
        })
    }

    const finishPanelResize = (event) => {
        const drag = resizeDragRef.current
        if (!drag) return

        resizeDragRef.current = null

        if (resizeRafRef.current != null) {
            cancelAnimationFrame(resizeRafRef.current)
            resizeRafRef.current = null
        }

        document.body.classList.remove('workspace-resizing', 'workspace-resizing-x', 'workspace-resizing-y')

        const { explorerWidth: nextExplorerWidth, dockHeight: nextDockHeight } =
            livePanelSizesRef.current

        applyPanelSizeVariables(nextExplorerWidth, nextDockHeight)
        setExplorerWidth(nextExplorerWidth)
        setDockHeight(nextDockHeight)
        refreshEditorLayout()

        if (event?.currentTarget?.hasPointerCapture?.(event.pointerId)) {
            event.currentTarget.releasePointerCapture(event.pointerId)
        }
    }

    const handleExplorerResizeStart = (event) => {
        if (!isResizeEnabled()) return

        event.preventDefault()
        resizeDragRef.current = {
            axis: 'explorer',
            startPointer: event.clientX,
            startSize: livePanelSizesRef.current.explorerWidth,
        }

        document.body.classList.add('workspace-resizing', 'workspace-resizing-x')
        event.currentTarget.setPointerCapture(event.pointerId)
    }

    const handleDockResizeStart = (event) => {
        if (!isResizeEnabled()) return

        event.preventDefault()
        resizeDragRef.current = {
            axis: 'dock',
            startPointer: event.clientY,
            startSize: livePanelSizesRef.current.dockHeight,
        }

        document.body.classList.add('workspace-resizing', 'workspace-resizing-y')
        event.currentTarget.setPointerCapture(event.pointerId)
    }

    const handlePanelResizeMove = (event) => {
        const drag = resizeDragRef.current
        if (!drag) return

        if (drag.axis === 'explorer') {
            const delta = event.clientX - drag.startPointer
            livePanelSizesRef.current.explorerWidth = clampExplorerWidth(drag.startSize + delta)
        } else {
            const delta = event.clientY - drag.startPointer
            livePanelSizesRef.current.dockHeight = clampDockHeight(drag.startSize + delta)
        }

        schedulePanelSizePaint()
    }

    useEffect(() => {
        livePanelSizesRef.current = { explorerWidth, dockHeight }

        if (resizeDragRef.current) return

        applyPanelSizeVariables(explorerWidth, dockHeight)
    }, [explorerWidth, dockHeight])

    useEffect(() => {
        return () => {
            if (resizeRafRef.current != null) {
                cancelAnimationFrame(resizeRafRef.current)
            }
            document.body.classList.remove('workspace-resizing', 'workspace-resizing-x', 'workspace-resizing-y')
        }
    }, [])

    useEffect(() => {
        setUiHydrated(false)

        const prefs = loadWorkspaceUiPrefs(id)
        setExplorerWidth(prefs.explorerWidth)
        setDockHeight(prefs.dockHeight)
        setDockActiveTab(prefs.dockActiveTab)
        setExplorerCollapsed(prefs.explorerCollapsed)
        pendingActiveFileIdRef.current = prefs.activeFileId
        livePanelSizesRef.current = {
            explorerWidth: prefs.explorerWidth,
            dockHeight: prefs.dockHeight,
        }

        setUiHydrated(true)
    }, [id])

    useEffect(() => {
        if (!workspace) return

        const pendingId = pendingActiveFileIdRef.current
        if (!pendingId) return

        pendingActiveFileIdRef.current = null

        const exists = workspace.files.some((file) => file.id === pendingId)
        if (!exists || workspace.activeFileId === pendingId) return

        const nextWorkspace = setActiveFile(workspace, pendingId)
        setWorkspace(nextWorkspace)
        workspaceRef.current = serializeWorkspace(nextWorkspace)
    }, [workspace])

    useEffect(() => {
        if (!uiHydrated || !id) return

        let activeFileId = null
        if (workspace?.files?.length) {
            activeFileId = workspace.files.some((file) => file.id === workspace.activeFileId)
                ? workspace.activeFileId
                : null
        } else {
            activeFileId = pendingActiveFileIdRef.current
        }

        saveWorkspaceUiPrefs(
            id,
            {
                explorerWidth,
                dockHeight,
                dockActiveTab,
                activeFileId,
                explorerCollapsed,
            },
            { maxDockHeight: getMaxDockHeight() }
        )
    }, [
        uiHydrated,
        id,
        explorerWidth,
        dockHeight,
        dockActiveTab,
        explorerCollapsed,
        workspace?.activeFileId,
    ])

    useEffect(() => {
        if (!workspace || !uiHydrated) return

        const frame = requestAnimationFrame(() => {
            const clamped = clampDockHeight(dockHeight)
            if (clamped === dockHeight) return

            livePanelSizesRef.current.dockHeight = clamped
            setDockHeight(clamped)
            applyPanelSizeVariables(explorerWidth, clamped)
        })

        return () => cancelAnimationFrame(frame)
    }, [workspace, uiHydrated])

    useEffect(() => {
        fetchData()
    }, [id])

    useEffect(() => {
        if (!tasks.length || !workspace) return

        const interval = setInterval(() => {
            saveProjectWork()
        }, 5000)

        return () => clearInterval(interval)
    }, [tasks, workspace, textAnswer])

    useEffect(() => {
        if (!tasks.length || !project) return

        const textTask = tasks.find((item) => item.task_type === 'text')
        if (!textTask) return

        const loadTextSubmission = async () => {
            try {
                const res = await projectsAPI.getTaskSubmission(textTask.id)
                const answer = res.data.progress?.answer || ''
                setTextAnswer(answer)
                textRef.current = answer
            } catch {
                setTextAnswer('')
                textRef.current = ''
            }
        }

        loadTextSubmission()
    }, [tasks, project])

    const handleWorkspaceChange = (nextWorkspace) => {
        setWorkspace(nextWorkspace)
        workspaceRef.current = serializeWorkspace(nextWorkspace)
    }

    const handleExplorerSelectFile = (fileId) => {
        if (!workspace) return
        handleWorkspaceChange(setActiveFile(workspace, fileId))
    }

    const handleExplorerAddFile = (name) => {
        if (!workspace) return
        handleWorkspaceChange(addFile(workspace, name))
    }

    const handleExplorerRenameFile = (fileId, newName) => {
        if (!workspace) return
        handleWorkspaceChange(renameFile(workspace, fileId, newName))
    }

    const handleExplorerDeleteFile = (fileId) => {
        if (!workspace) return
        handleWorkspaceChange(deleteFile(workspace, fileId))
    }

    const saveProjectWork = async () => {
        const codeTasks = tasks.filter((item) => item.task_type === 'code')

        try {
            if (codeTasks.length && workspaceRef.current.trim()) {
                await Promise.all(
                    codeTasks.map((codeTask) =>
                        projectsAPI.saveTaskSubmission(codeTask.id, {
                            answer: workspaceRef.current,
                        })
                    )
                )
            }

            const textTask = tasks.find((item) => item.task_type === 'text')
            if (textTask && textRef.current.trim()) {
                await projectsAPI.saveTaskSubmission(textTask.id, {
                    answer: textRef.current,
                })
            }
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
            kernelMessage: 'Executing workspace...',
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
                runServerPython: async ({ files, entryFileName, code } = {}) => {
                    const mountableFiles = (files || [])
                        .filter((file) => /\.(py|json|txt)$/i.test(file?.name || ''))
                        .map((file) => ({
                            name: file.name,
                            content: file.content || '',
                        }))

                    const res = await projectsAPI.executeCode({
                        code,
                        files: mountableFiles.length ? mountableFiles : undefined,
                        entryFileName: entryFileName || 'main.py',
                        language: projectLanguage,
                    })
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
        const hasCodeTasks = tasks.some((item) => item.task_type === 'code')
        if (!workspace || runningTests || !hasCodeTasks) return

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
            const taskList = tasksRes.data || []
            const lang = getPrimaryProjectLanguage(p)

            setProject(p)
            setTasks(taskList)
            setTests(testsRes.data || [])

            const sharedWorkspace = await loadSharedProjectWorkspace(taskList, lang)
            if (sharedWorkspace) {
                setWorkspace(sharedWorkspace)
                workspaceRef.current = serializeWorkspace(sharedWorkspace)
            }

            setLoading(false)
        } catch (err) {
            console.error(err)
            setLoading(false)
        }
    }

    const hasTextTasks = tasks.some((item) => item.task_type === 'text')

    const isTaskCompleted = () => {
        const codeTasks = tasks.filter((item) => item.task_type === 'code')
        if (codeTasks.length > 0) {
            return workspace ? workspaceHasContent(workspace) : false
        }

        if (hasTextTasks) {
            return textAnswer.trim().length > 0
        }

        return false
    }

    const handleFinish = async () => {
        if (!isTaskCompleted()) return

        try {
            await saveProjectWork()
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

    const objective = project?.objectives?.trim() || ''
    const userStories = tasks.length
        ? tasks.map((t, index) => ({
            id: t.id,
            index,
            text: t.description?.trim() || t.title,
            title: t.title,
        }))
        : []

    const userStoriesWithStatus = linkResultsByIndex(userStories, testResults)

    const availableHints = tasks
        .map((t, index) => ({ id: t.id, index, title: t.title, hint: t.hint }))
        .filter((item) => item.hint?.trim())

    const testProgress = getProjectTestProgress(tests, testResults)

    if (loading) return <div className="loading">Loading...</div>
    if (!project) return <div>Project not found</div>

    return (
        <div className="fcc-workspace">
            <header className="fcc-header">
                <div>
                    <p className="fcc-breadcrumb">مساحة تنفيذ المشروع</p>
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
                <ProjectWorkSidebar
                    project={project}
                    objective={objective}
                    userStoriesWithStatus={userStoriesWithStatus}
                    availableHints={availableHints}
                />

                <div className="fcc-main">
                    <ProjectWorkProgress progress={testProgress} />

                    <section className="fcc-section fcc-editor-section">
                        <h2 className="fcc-section-title">Code Editor</h2>
                        <div className="fcc-section-body">
                            {tasks.some((item) => item.task_type === 'code') && workspace && (
                                <div ref={workspaceLayoutRef} className="deepnote-workspace">
                                    <div className="deepnote-coding-area">
                                        <div className="editor-with-explorer">
                                            <div className="file-explorer-panel">
                                                <FileExplorer
                                                    workspace={workspace}
                                                    onSelectFile={handleExplorerSelectFile}
                                                    onAddFile={handleExplorerAddFile}
                                                    onRenameFile={handleExplorerRenameFile}
                                                    onDeleteFile={handleExplorerDeleteFile}
                                                />
                                            </div>

                                            <div
                                                className="workspace-resize-handle workspace-resize-handle-vertical"
                                                role="separator"
                                                aria-orientation="vertical"
                                                aria-label="Resize file explorer"
                                                onPointerDown={handleExplorerResizeStart}
                                                onPointerMove={handlePanelResizeMove}
                                                onPointerUp={finishPanelResize}
                                                onPointerCancel={finishPanelResize}
                                            />

                                            <div className="editor-with-explorer-main">
                                                <MultiFileEditor
                                                    workspace={workspace}
                                                    onChange={handleWorkspaceChange}
                                                    onRun={runCode}
                                                    editorHeight="100%"
                                                    defaultMonacoLanguage={getMonacoLanguage(projectLanguage)}
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    <div
                                        className="workspace-resize-handle workspace-resize-handle-horizontal"
                                        role="separator"
                                        aria-orientation="horizontal"
                                        aria-label="Resize bottom dock"
                                        onPointerDown={handleDockResizeStart}
                                        onPointerMove={handlePanelResizeMove}
                                        onPointerUp={finishPanelResize}
                                        onPointerCancel={finishPanelResize}
                                    />

                                    <div className="bottom-dock-panel">
                                        <BottomDock
                                            activeTab={dockActiveTab}
                                            onActiveTabChange={setDockActiveTab}
                                            executionBlocks={execution?.blocks || []}
                                            output={
                                                <ExecutionPanel
                                                    execution={execution}
                                                    kernelLabel={getKernelLabel(projectLanguage, workspace)}
                                                    onClear={clearExecution}
                                                    onResetKernel={resetKernel}
                                                    showResetKernel={showKernelReset}
                                                />
                                            }
                                            tests={
                                                <RunningTestsPanel
                                                    running={runningTests}
                                                    testError={testError}
                                                    testResults={testResults}
                                                    testsCount={tests.length}
                                                />
                                            }
                                        />
                                    </div>
                                </div>
                            )}

                            {hasTextTasks && (
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
                                    disabled={runningTests || !workspace || !tasks.some((item) => item.task_type === 'code')}
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

                                {tasks.some((item) => item.task_type === 'code') && (
                                    <span className="fcc-check-hint">
                                        أو استخدم <kbd>Ctrl</kbd> + <kbd>Enter</kbd> لتشغيل الكود
                                    </span>
                                )}
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    )
}

export default ProjectWork
