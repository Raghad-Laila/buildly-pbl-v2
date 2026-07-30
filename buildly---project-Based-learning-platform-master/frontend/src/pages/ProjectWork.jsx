import React, { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import MultiFileEditor from '../components/MultiFileEditor'
import FileExplorer from '../components/FileExplorer'
import BottomDock from '../components/BottomDock'
import ExecutionPanel from '../components/ExecutionPanel'
import RunningTestsPanel from '../components/RunningTestsPanel'
import ProjectWorkProgress from '../components/ProjectWorkProgress'
import ProjectWorkSidebar from '../components/ProjectWorkSidebar'
import AiReviewDrawer from '../components/AiReviewDrawer'
import CodeQualityDrawer from '../components/CodeQualityDrawer'
import '../components/CodeQualityDrawer.css'
import { projectsAPI } from '../services/api'
import {
    addFile,
    deleteFile,
    detectLanguageFromFile,
    getActiveFile,
    getDefaultWorkspace,
    getMainExecutableFile,
    parseWorkspace,
    renameFile,
    serializeWorkspace,
    setActiveFile,
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
    runClientTests,
    resolveCheckCodePlan,
    pickPythonTestEntryFile,
    getPythonTestMountFiles,
} from '../utils/testRunner'
import { linkResultsByTask } from '../utils/testResultLinking'
import { getProjectTestProgress } from '../utils/projectProgress'
import {
    getPrimaryProjectLanguage,
    getProjectLanguages,
} from '../utils/projectLanguages'
import {
    DOCK_HEIGHT_DEFAULT,
    DOCK_HEIGHT_MAX,
    DOCK_TAB_DEFAULT,
    EDITOR_HEIGHT_DEFAULT,
    EDITOR_HEIGHT_MAX,
    EXPLORER_WIDTH_DEFAULT,
    clampDockHeight as clampStoredDockHeight,
    clampEditorHeight as clampStoredEditorHeight,
    clampExplorerWidth as clampStoredExplorerWidth,
    loadWorkspaceUiPrefs,
    saveWorkspaceUiPrefs,
} from '../utils/workspaceUiStorage'
import './ProjectWork.css'

const RESIZE_BREAKPOINT = 1100

const ProjectWork = () => {
    const { id } = useParams()
    const navigate = useNavigate()

    const [project, setProject] = useState(null)
    const [tasks, setTasks] = useState([])
    const [tests, setTests] = useState([])

    const [workspace, setWorkspace] = useState(null)
    const [textAnswer, setTextAnswer] = useState('')
    const [branches, setBranches] = useState([])
    const [selectedBranch, setSelectedBranch] = useState(null)

    const [loading, setLoading] = useState(true)
    const [execution, setExecution] = useState(createExecutionState())
    const [running, setRunning] = useState(false)
    const [runningTests, setRunningTests] = useState(false)
    const [testResults, setTestResults] = useState(null)
    const [testError, setTestError] = useState('')
    const [aiReviewOpen, setAiReviewOpen] = useState(false)
    const [aiReviewing, setAiReviewing] = useState(false)
    const [aiReviewResult, setAiReviewResult] = useState(null)
    const [aiReviewError, setAiReviewError] = useState('')
    const [qualityReviewOpen, setQualityReviewOpen] = useState(false)
    const [qualityReviewing, setQualityReviewing] = useState(false)
    const [qualityReviewResult, setQualityReviewResult] = useState(null)
    const [qualityReviewError, setQualityReviewError] = useState('')
    const [revealedHintIds, setRevealedHintIds] = useState([])

    const workspaceRef = useRef('')
    const workspaceStateRef = useRef(null)
    const runningRef = useRef(false)
    const textRef = useRef('')
    const selectedBranchRef = useRef(null)
    const streamBlocksRef = useRef([])
    const workspaceLayoutRef = useRef(null)
    const resizeDragRef = useRef(null)
    const resizeRafRef = useRef(null)
    const livePanelSizesRef = useRef({
        explorerWidth: EXPLORER_WIDTH_DEFAULT,
        editorHeight: EDITOR_HEIGHT_DEFAULT,
        dockHeight: DOCK_HEIGHT_DEFAULT,
    })
    const pendingActiveFileIdRef = useRef(null)

    const [explorerWidth, setExplorerWidth] = useState(EXPLORER_WIDTH_DEFAULT)
    const [editorHeight, setEditorHeight] = useState(EDITOR_HEIGHT_DEFAULT)
    const [dockHeight, setDockHeight] = useState(DOCK_HEIGHT_DEFAULT)
    const [dockActiveTab, setDockActiveTab] = useState(DOCK_TAB_DEFAULT)
    const [explorerCollapsed, setExplorerCollapsed] = useState(false)
    const [uiHydrated, setUiHydrated] = useState(false)

    const projectLanguage = getPrimaryProjectLanguage(project)

    const isResizeEnabled = () => window.matchMedia(`(max-width: ${RESIZE_BREAKPOINT}px)`).matches === false

    const applyPanelSizeVariables = (width, nextEditorHeight, nextDockHeight) => {
        const layout = workspaceLayoutRef.current
        if (!layout) return
        layout.style.setProperty('--explorer-width', `${width}px`)
        layout.style.setProperty('--editor-height', `${nextEditorHeight}px`)
        layout.style.setProperty('--dock-height', `${nextDockHeight}px`)
    }

    const getMaxEditorHeight = () =>
        Math.min(EDITOR_HEIGHT_MAX, Math.round(window.innerHeight * 0.75))

    const getMaxDockHeight = () =>
        Math.min(DOCK_HEIGHT_MAX, Math.round(window.innerHeight * 0.7))

    const clampExplorerWidth = (width) =>
        clampStoredExplorerWidth(width) ?? EXPLORER_WIDTH_DEFAULT

    const clampEditorHeight = (height) =>
        clampStoredEditorHeight(height, getMaxEditorHeight()) ?? EDITOR_HEIGHT_DEFAULT

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

            const {
                explorerWidth: width,
                editorHeight: nextEditorHeight,
                dockHeight: height,
            } = livePanelSizesRef.current
            applyPanelSizeVariables(width, nextEditorHeight, height)
            refreshEditorLayout()
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

        document.body.classList.remove(
            'workspace-resizing',
            'workspace-resizing-x',
            'workspace-resizing-y',
            'workspace-resizing-editor',
            'workspace-resizing-dock'
        )

        const {
            explorerWidth: nextExplorerWidth,
            editorHeight: nextEditorHeight,
            dockHeight: nextDockHeight,
        } = livePanelSizesRef.current

        applyPanelSizeVariables(nextExplorerWidth, nextEditorHeight, nextDockHeight)
        setExplorerWidth(nextExplorerWidth)
        setEditorHeight(nextEditorHeight)
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

    const handleEditorResizeStart = (event) => {
        if (!isResizeEnabled()) return

        event.preventDefault()
        resizeDragRef.current = {
            axis: 'editor',
            startPointer: event.clientY,
            startSize: livePanelSizesRef.current.editorHeight,
        }

        document.body.classList.add('workspace-resizing', 'workspace-resizing-y', 'workspace-resizing-editor')
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

        document.body.classList.add('workspace-resizing', 'workspace-resizing-y', 'workspace-resizing-dock')
        event.currentTarget.setPointerCapture(event.pointerId)
    }

    const handlePanelResizeMove = (event) => {
        const drag = resizeDragRef.current
        if (!drag) return

        if (drag.axis === 'explorer') {
            const delta = event.clientX - drag.startPointer
            livePanelSizesRef.current.explorerWidth = clampExplorerWidth(drag.startSize + delta)
        } else if (drag.axis === 'editor') {
            // Independent: drag down grows editor only; console height unchanged.
            const delta = event.clientY - drag.startPointer
            livePanelSizesRef.current.editorHeight = clampEditorHeight(drag.startSize + delta)
        } else {
            // Independent: drag down grows console only; editor height unchanged.
            const delta = event.clientY - drag.startPointer
            livePanelSizesRef.current.dockHeight = clampDockHeight(drag.startSize + delta)
        }

        schedulePanelSizePaint()
    }

    useEffect(() => {
        livePanelSizesRef.current = { explorerWidth, editorHeight, dockHeight }

        if (resizeDragRef.current) return

        applyPanelSizeVariables(explorerWidth, editorHeight, dockHeight)
    }, [explorerWidth, editorHeight, dockHeight])

    useEffect(() => {
        return () => {
            if (resizeRafRef.current != null) {
                cancelAnimationFrame(resizeRafRef.current)
            }
            document.body.classList.remove(
                'workspace-resizing',
                'workspace-resizing-x',
                'workspace-resizing-y',
                'workspace-resizing-editor',
                'workspace-resizing-dock'
            )
        }
    }, [])

    useEffect(() => {
        setUiHydrated(false)

        const prefs = loadWorkspaceUiPrefs(id)
        setExplorerWidth(prefs.explorerWidth)
        setEditorHeight(prefs.editorHeight)
        setDockHeight(prefs.dockHeight)
        setDockActiveTab(prefs.dockActiveTab)
        setExplorerCollapsed(prefs.explorerCollapsed)
        pendingActiveFileIdRef.current = prefs.activeFileId
        livePanelSizesRef.current = {
            explorerWidth: prefs.explorerWidth,
            editorHeight: prefs.editorHeight,
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
        workspaceStateRef.current = nextWorkspace
        workspaceRef.current = serializeWorkspace(nextWorkspace)
        setWorkspace(nextWorkspace)
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
                editorHeight,
                dockHeight,
                dockActiveTab,
                activeFileId,
                explorerCollapsed,
            },
            {
                maxEditorHeight: getMaxEditorHeight(),
                maxDockHeight: getMaxDockHeight(),
            }
        )
    }, [
        uiHydrated,
        id,
        explorerWidth,
        editorHeight,
        dockHeight,
        dockActiveTab,
        explorerCollapsed,
        workspace?.activeFileId,
    ])

    useEffect(() => {
        if (!workspace || !uiHydrated) return

        const frame = requestAnimationFrame(() => {
            const nextEditor = clampEditorHeight(editorHeight)
            const nextDock = clampDockHeight(dockHeight)
            if (nextEditor === editorHeight && nextDock === dockHeight) return

            livePanelSizesRef.current.editorHeight = nextEditor
            livePanelSizesRef.current.dockHeight = nextDock
            setEditorHeight(nextEditor)
            setDockHeight(nextDock)
            applyPanelSizeVariables(explorerWidth, nextEditor, nextDock)
        })

        return () => cancelAnimationFrame(frame)
    }, [workspace, uiHydrated])

    useEffect(() => {
        setRevealedHintIds([])
        fetchData()
    }, [id])

    useEffect(() => {
        if (!tasks.length || !workspace) return

        const interval = setInterval(() => {
            saveProjectWork()
        }, 5000)

        return () => clearInterval(interval)
    }, [tasks, workspace, textAnswer, selectedBranch])

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
        workspaceStateRef.current = nextWorkspace
        workspaceRef.current = serializeWorkspace(nextWorkspace)
        setWorkspace(nextWorkspace)
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

    const applyWorkspaceToEditor = (nextWorkspace) => {
        workspaceStateRef.current = nextWorkspace
        workspaceRef.current = serializeWorkspace(nextWorkspace)
        setWorkspace(nextWorkspace)
    }

    const setActiveBranch = (branchSummary) => {
        setSelectedBranch(branchSummary)
        selectedBranchRef.current = branchSummary
    }

    const refreshBranches = async (projectId) => {
        const res = await projectsAPI.getBranches(projectId)
        const list = res.data.branches || []
        setBranches(list)
        return list
    }

    const loadBranchIntoEditor = async (branchSummary, language) => {
        const res = await projectsAPI.getBranch(branchSummary.id)
        const branch = res.data.branch
        const summary = {
            id: branch.id,
            name: branch.name,
            is_main: branch.is_main,
            created_at: branch.created_at,
        }
        setActiveBranch(summary)
        applyWorkspaceToEditor(parseWorkspace(branch.files_json || '', language))
        return summary
    }

    const persistCurrentBranch = async () => {
        const currentBranch = selectedBranchRef.current
        if (!currentBranch?.id || !workspaceRef.current.trim()) return
        await projectsAPI.updateBranch(currentBranch.id, {
            files_json: workspaceRef.current,
        })
    }

    const saveProjectWork = async () => {
        try {
            await persistCurrentBranch()

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

    const handleSelectBranch = async (event) => {
        const nextId = Number(event.target.value)
        if (!nextId || selectedBranchRef.current?.id === nextId) return

        const summary = branches.find((branch) => branch.id === nextId)
        if (!summary) return

        try {
            await persistCurrentBranch()
            await loadBranchIntoEditor(summary, projectLanguage)
        } catch (err) {
            console.error('Branch switch error:', err)
            alert(err.response?.data?.message || 'Failed to switch branch.')
        }
    }

    const handleCreateBranch = async () => {
        const name = window.prompt('New branch name')
        if (!name?.trim()) return

        try {
            await persistCurrentBranch()
            const res = await projectsAPI.createBranch(id, { name: name.trim() })
            const created = res.data.branch
            const list = await refreshBranches(id)
            const summary =
                list.find((branch) => branch.id === created.id) || {
                    id: created.id,
                    name: created.name,
                    is_main: created.is_main,
                    created_at: created.created_at,
                }
            await loadBranchIntoEditor(summary, projectLanguage)
        } catch (err) {
            console.error('Create branch error:', err)
            alert(err.response?.data?.message || 'Failed to create branch.')
        }
    }

    const handleDeleteBranch = async () => {
        const current = selectedBranchRef.current
        if (!current?.id || current.is_main) return
        if (!window.confirm(`Delete branch "${current.name}"?`)) return

        try {
            await projectsAPI.deleteBranch(current.id)
            const list = await refreshBranches(id)
            const main = list.find((branch) => branch.is_main) || list[0]
            if (main) {
                await loadBranchIntoEditor(main, projectLanguage)
            } else {
                setActiveBranch(null)
                applyWorkspaceToEditor(getDefaultWorkspace(projectLanguage))
            }
        } catch (err) {
            console.error('Delete branch error:', err)
            alert(err.response?.data?.message || 'Failed to delete branch.')
        }
    }

    const handleMergeIntoMain = async () => {
        const current = selectedBranchRef.current
        if (!current?.id || current.is_main) return

        const confirmed = window.confirm(
            'Merge this branch into Main?\n\nThis will replace the current Main branch.'
        )
        if (!confirmed) return

        try {
            await persistCurrentBranch()
            const res = await projectsAPI.mergeBranch(current.id)
            alert(res.data?.message || 'Branch merged successfully.')

            const list = await refreshBranches(id)
            const main = list.find((branch) => branch.is_main) || list[0]
            if (main) {
                await loadBranchIntoEditor(main, projectLanguage)
            }
        } catch (err) {
            console.error('Merge branch error:', err)
            alert(err.response?.data?.message || 'Failed to merge branch.')
        }
    }

    useEffect(() => {
        workspaceStateRef.current = workspace
    }, [workspace])

    useEffect(() => {
        runningRef.current = running
    }, [running])

    const runCode = async () => {
        const currentWorkspace = getWorkspaceSnapshot(
            workspaceRef,
            workspaceStateRef.current || workspace
        )
        if (!currentWorkspace || runningRef.current) return

        const runId = Date.now()

        runningRef.current = true
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
            const activeFile = getActiveFile(currentWorkspace)
            const executeOptions = {
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
            }

            // Run Code only: execute the active Python tab when applicable.
            if (
                activeFile &&
                detectLanguageFromFile(activeFile, projectLanguage) === 'python'
            ) {
                executeOptions.entryFileName = activeFile.name
            }

            const raw = await executeWorkspace(
                currentWorkspace,
                projectLanguage,
                executeOptions
            )

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
            runningRef.current = false
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
        const projectLanguages = getProjectLanguages(project)

        // CHECK CODE ROUTING
        const checkPlan = resolveCheckCodePlan({
            languages: projectLanguages,
            workspace: currentWorkspace,
            tests,
            projectLanguage,
        })

        if (checkPlan.mode === 'unsupported') {
            setTestError('تشغيل الاختبارات غير مدعوم لهذه اللغة حالياً.')
            setTestResults(null)
            return
        }

        if (checkPlan.mode === 'client') {
            if (checkPlan.needsWorkspaceHtmlCss) {
                const hasHtml = (currentWorkspace.files || []).some(
                    (file) =>
                        /\.html?$/i.test(file?.name || '') &&
                        String(file?.content || '').trim()
                )
                const hasCss = (currentWorkspace.files || []).some(
                    (file) =>
                        /\.css$/i.test(file?.name || '') &&
                        String(file?.content || '').trim()
                )
                if (!hasHtml && !hasCss) {
                    setTestError('اكتب الكود أولاً قبل تشغيل الاختبارات.')
                    setTestResults(null)
                    return
                }
            }

            if (checkPlan.needsJsSource) {
                const jsLanguageHint =
                    projectLanguages.find((language) =>
                        ['react', 'javascript', 'typescript'].includes(language)
                    ) || 'javascript'
                const jsFile = getMainExecutableFile(currentWorkspace, jsLanguageHint)
                const extension = jsFile?.name?.split('.').pop()?.toLowerCase()
                const jsLikeExtension = ['js', 'mjs', 'cjs', 'jsx', 'tsx', 'ts'].includes(
                    extension
                )
                const jsContent = jsLikeExtension
                    ? String(jsFile?.content || '').trim()
                    : ''
                const legacyCode = getStudentCode(currentWorkspace)

                if (!jsContent && !legacyCode) {
                    setTestError('اكتب الكود أولاً قبل تشغيل الاختبارات.')
                    setTestResults(null)
                    return
                }
            }

            if (!checkPlan.needsWorkspaceHtmlCss && !checkPlan.needsJsSource) {
                const code = getStudentCode(currentWorkspace)
                if (!code) {
                    setTestError('اكتب الكود أولاً قبل تشغيل الاختبارات.')
                    setTestResults(null)
                    return
                }
            }
        } else {
            const mountFiles = getPythonTestMountFiles(currentWorkspace)
            const hasPythonContent = mountFiles.some(
                (file) =>
                    /\.py$/i.test(file.name || '') && String(file.content || '').trim()
            )
            if (!hasPythonContent && !getStudentCode(currentWorkspace)) {
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
            setDockActiveTab('tests')
            return
        }

        setDockActiveTab('tests')
        setRunningTests(true)
        setTestError('')
        setTestResults(null)

        try {
            let payload

            // CHECK CODE ROUTING
            if (checkPlan.mode === 'client') {
                payload = runClientTests(getStudentCode(currentWorkspace), tests, {
                    workspace: currentWorkspace,
                    projectLanguage,
                    languages: projectLanguages,
                })
            } else {
                const mountFiles = getPythonTestMountFiles(currentWorkspace)
                const entryFile = pickPythonTestEntryFile(currentWorkspace)
                const entryFileName =
                    entryFile?.name && /\.py$/i.test(entryFile.name)
                        ? entryFile.name
                        : 'main.py'
                const response = await projectsAPI.runTests(id, {
                    code: getStudentCode(currentWorkspace) || entryFile?.content || '',
                    language: 'python',
                    files: mountFiles.length ? mountFiles : undefined,
                    entryFileName,
                })
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
            setDockActiveTab('tests')
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

    const runAiReview = async () => {
        const hasCodeTasks = tasks.some((item) => item.task_type === 'code')
        const hintIds = tasks
            .filter((item) => item.hint?.trim())
            .map((item) => item.id)
        const hintsUnlocked =
            hintIds.length === 0 ||
            hintIds.every((hintId) => revealedHintIds.includes(hintId))
        const testsExist = tests.length > 0
        const latestCheckFailed = (testResults?.summary?.failed ?? 0) > 0
        const aiUnlocked = hintsUnlocked && (!testsExist || latestCheckFailed)

        if (!workspace || aiReviewing || !hasCodeTasks || !aiUnlocked) return

        const currentWorkspace = getWorkspaceSnapshot(workspaceRef, workspace)
        const files = (currentWorkspace?.files || [])
            .filter((file) => file?.name)
            .map((file) => ({
                name: file.name,
                content: file.content ?? '',
            }))

        if (!files.length || !files.some((file) => String(file.content || '').trim())) {
            setAiReviewOpen(true)
            setAiReviewResult(null)
            setAiReviewError('اكتب بعض الكود أولاً قبل طلب المراجعة الذكية.')
            return
        }

        setAiReviewOpen(true)
        setAiReviewing(true)
        setAiReviewError('')
        setAiReviewResult(null)

        const payload = {
            project_id: Number(id),
            files,
        }

        if (testResults?.summary) {
            payload.test_summary = {
                total: testResults.summary.total ?? 0,
                passed: testResults.summary.passed ?? 0,
                failed: testResults.summary.failed ?? 0,
            }
        }

        const failedTests = (testResults?.results || [])
            .filter((result) => !result?.passed)
            .map((result) => {
                const meta =
                    result.id != null
                        ? tests.find((test) => test.id === result.id) || null
                        : null
                const story =
                    meta?.task != null
                        ? tasks.find((task) => task.id === meta.task) || null
                        : null
                const storyTitle = story?.title || ''
                const storyText = story?.description?.trim() || story?.title || ''
                const requirementParts = [
                    storyTitle,
                    storyText && storyText !== storyTitle ? storyText : null,
                    meta?.description,
                ].filter(Boolean)

                const item = {
                    message: result.message || '',
                    error: result.error || '',
                    stderr: result.stderr || '',
                    name: result.name || meta?.name || '',
                    requirement: requirementParts.join(' — ') || '',
                }

                if (result.id != null) {
                    item.id = result.id
                } else if (meta?.id != null) {
                    item.id = meta.id
                }

                return item
            })

        if (failedTests.length) {
            payload.failed_tests = failedTests
        }

        if (testError?.trim()) {
            payload.test_error = testError.trim()
        }

        try {
            const response = await projectsAPI.aiReview(payload)
            if (response.data?.success === false) {
                setAiReviewResult(null)
                setAiReviewError(
                    response.data?.error ||
                        'خدمة المراجعة الذكية غير متاحة حالياً. حاول مرة أخرى لاحقاً.'
                )
            } else {
                setAiReviewResult(response.data?.review || null)
                setAiReviewError('')
            }
        } catch {
            setAiReviewResult(null)
            setAiReviewError(
                'تعذّر إكمال المراجعة الذكية حالياً. حاول مرة أخرى بعد قليل.'
            )
        } finally {
            setAiReviewing(false)
        }
    }

    const runCodeQualityReview = async () => {
        const hasCodeTasks = tasks.some((item) => item.task_type === 'code')
        const progress = getProjectTestProgress(tests, testResults)

        if (!workspace || qualityReviewing || !hasCodeTasks || !progress.allPassed) return

        const currentWorkspace = getWorkspaceSnapshot(workspaceRef, workspace)
        const files = (currentWorkspace?.files || [])
            .filter((file) => file?.name)
            .map((file) => ({
                name: file.name,
                content: file.content ?? '',
            }))

        if (!files.length || !files.some((file) => String(file.content || '').trim())) {
            setQualityReviewOpen(true)
            setQualityReviewResult(null)
            setQualityReviewError('اكتب بعض الكود أولاً قبل طلب تقرير جودة الكود.')
            return
        }

        setQualityReviewOpen(true)
        setQualityReviewing(true)
        setQualityReviewError('')
        setQualityReviewResult(null)

        const payload = {
            project_id: Number(id),
            files,
        }

        if (testResults?.summary) {
            payload.test_summary = {
                total: testResults.summary.total ?? 0,
                passed: testResults.summary.passed ?? 0,
                failed: testResults.summary.failed ?? 0,
            }
        }

        try {
            const response = await projectsAPI.qualityReview(payload)
            setQualityReviewResult(response.data?.review || null)
        } catch {
            setQualityReviewResult(null)
            setQualityReviewError(
                'تعذّر إكمال تقرير جودة الكود حالياً. حاول مرة أخرى بعد قليل.'
            )
        } finally {
            setQualityReviewing(false)
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

            const hasCodeTasks = taskList.some((item) => item.task_type === 'code')
            if (hasCodeTasks) {
                const list = await refreshBranches(id)
                const main = list.find((branch) => branch.is_main) || list[0]
                if (main) {
                    await loadBranchIntoEditor(main, lang)
                } else {
                    setActiveBranch(null)
                    applyWorkspaceToEditor(getDefaultWorkspace(lang))
                }
            } else {
                setBranches([])
                setActiveBranch(null)
                setWorkspace(null)
                workspaceStateRef.current = null
                workspaceRef.current = ''
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

    const testProgress = getProjectTestProgress(tests, testResults)
    const canFinish =
        isTaskCompleted() &&
        (!testProgress.hasTests || testProgress.allPassed)

    const handleFinish = async () => {
        if (!canFinish) return

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

    const userStoriesWithStatus = linkResultsByTask(userStories, tests, testResults)

    const availableHints = tasks
        .map((t, index) => ({ id: t.id, index, title: t.title, hint: t.hint }))
        .filter((item) => item.hint?.trim())

    const allStaticHintsRevealed =
        availableHints.length === 0 ||
        availableHints.every((hint) => revealedHintIds.includes(hint.id))

    const hasProjectTests = tests.length > 0
    const checkCodeFailed = (testResults?.summary?.failed ?? 0) > 0
    const aiAssistantUnlocked =
        allStaticHintsRevealed && (!hasProjectTests || checkCodeFailed)

    const aiLockedMessage = !allStaticHintsRevealed
        ? 'Reveal all available hints to unlock the AI Assistant.'
        : 'Run Check Code and fix failing tests to unlock the AI Assistant.'

    const handleRevealHint = (hintId) => {
        setRevealedHintIds((prev) =>
            prev.includes(hintId) ? prev : [...prev, hintId]
        )
    }

    if (loading) return <div className="loading">Loading...</div>
    if (!project) return <div>Project not found</div>

    return (
        <div className="fcc-workspace">
            <header className="fcc-header">
                <div>
                    <p className="fcc-breadcrumb">مساحة تنفيذ المشروع</p>
                    <h1>{project.title}</h1>
                </div>
                <div className="fcc-header-actions">
                    {!canFinish &&
                        testProgress.hasTests &&
                        !testProgress.allPassed && (
                        <span className="fcc-finish-hint">
                            {!testResults?.summary
                                ? 'شغّل Check Code أولاً لاجتياز الاختبارات قبل التسليم.'
                                : 'يجب اجتياز جميع الاختبارات قبل تسليم المشروع.'}
                        </span>
                    )}
                    <button
                        type="button"
                        className="btn btn-success fcc-submit-btn"
                        onClick={handleFinish}
                        disabled={!canFinish}
                    >
                        تسليم المشروع
                    </button>
                </div>
            </header>

            <div className="fcc-layout">
                <ProjectWorkSidebar
                    project={project}
                    objective={objective}
                    userStoriesWithStatus={userStoriesWithStatus}
                    availableHints={availableHints}
                    revealedHintIds={revealedHintIds}
                    onRevealHint={handleRevealHint}
                />

                <div className="fcc-main">
                    <ProjectWorkProgress
                        progress={testProgress}
                        showImproveCode={
                            testProgress.allPassed &&
                            tasks.some((item) => item.task_type === 'code')
                        }
                        onImproveCode={runCodeQualityReview}
                        improveCodeLoading={qualityReviewing}
                    />

                    <section className="fcc-section fcc-editor-section">
                        <div className="fcc-section-title-row">
                            <h2 className="fcc-section-title">Code Editor</h2>
                            {tasks.some((item) => item.task_type === 'code') && (
                                <div className="branch-toolbar">
                                    <label className="branch-toolbar-label" htmlFor="workspace-branch-select">
                                        Branch
                                    </label>
                                    <select
                                        id="workspace-branch-select"
                                        className="branch-select"
                                        value={selectedBranch?.id || ''}
                                        onChange={handleSelectBranch}
                                        disabled={!branches.length}
                                    >
                                        {branches.map((branch) => (
                                            <option key={branch.id} value={branch.id}>
                                                {branch.is_main ? `${branch.name} (Main)` : branch.name}
                                            </option>
                                        ))}
                                    </select>
                                    <button
                                        type="button"
                                        className="btn branch-toolbar-btn"
                                        onClick={handleCreateBranch}
                                    >
                                        New Branch
                                    </button>
                                    <button
                                        type="button"
                                        className="btn branch-toolbar-btn branch-toolbar-btn-danger"
                                        onClick={handleDeleteBranch}
                                        disabled={!selectedBranch || selectedBranch.is_main}
                                    >
                                        Delete
                                    </button>
                                    {!selectedBranch?.is_main && (
                                        <button
                                            type="button"
                                            className="btn branch-toolbar-btn branch-toolbar-btn-merge"
                                            onClick={handleMergeIntoMain}
                                        >
                                            Merge into Main
                                        </button>
                                    )}
                                </div>
                            )}
                        </div>
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
                                        className="workspace-resize-handle workspace-resize-handle-horizontal workspace-resize-handle-editor"
                                        role="separator"
                                        aria-orientation="horizontal"
                                        aria-label="Resize code editor"
                                        onPointerDown={handleEditorResizeStart}
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

                                    <div
                                        className="workspace-resize-handle workspace-resize-handle-horizontal workspace-resize-handle-dock"
                                        role="separator"
                                        aria-orientation="horizontal"
                                        aria-label="Resize console panel"
                                        onPointerDown={handleDockResizeStart}
                                        onPointerMove={handlePanelResizeMove}
                                        onPointerUp={finishPanelResize}
                                        onPointerCancel={finishPanelResize}
                                    />
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
                                    className="btn fcc-run-btn"
                                    onClick={runCode}
                                    disabled={
                                        running ||
                                        !workspace ||
                                        !tasks.some((item) => item.task_type === 'code')
                                    }
                                >
                                    {running ? (
                                        <>
                                            <span className="execution-spinner" />
                                            Running...
                                        </>
                                    ) : (
                                        'Run'
                                    )}
                                </button>

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

                                {aiAssistantUnlocked ? (
                                    <button
                                        type="button"
                                        className="btn fcc-ai-review-btn"
                                        onClick={runAiReview}
                                        disabled={
                                            aiReviewing ||
                                            !workspace ||
                                            !tasks.some((item) => item.task_type === 'code')
                                        }
                                    >
                                        {aiReviewing ? (
                                            <>
                                                <span className="execution-spinner" />
                                                جاري المراجعة...
                                            </>
                                        ) : (
                                            '🤖 Ask AI Assistant'
                                        )}
                                    </button>
                                ) : (
                                    <span className="fcc-ai-locked-hint">
                                        {aiLockedMessage}
                                    </span>
                                )}

                                {testProgress.allPassed &&
                                    tasks.some((item) => item.task_type === 'code') && (
                                    <button
                                        type="button"
                                        className="btn fcc-quality-review-btn"
                                        onClick={runCodeQualityReview}
                                        disabled={
                                            qualityReviewing ||
                                            !workspace
                                        }
                                    >
                                        {qualityReviewing ? (
                                            <>
                                                <span className="execution-spinner" />
                                                Analyzing...
                                            </>
                                        ) : (
                                            '✨ Improve Code with AI'
                                        )}
                                    </button>
                                )}

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

            <AiReviewDrawer
                open={aiReviewOpen}
                loading={aiReviewing}
                error={aiReviewError}
                review={aiReviewResult}
                failedTestsCount={testResults?.summary?.failed ?? 0}
                onClose={() => setAiReviewOpen(false)}
            />

            <CodeQualityDrawer
                open={qualityReviewOpen}
                loading={qualityReviewing}
                error={qualityReviewError}
                review={qualityReviewResult}
                onClose={() => setQualityReviewOpen(false)}
            />
        </div>
    )
}

export default ProjectWork
