const PYODIDE_VERSION = '0.26.4'
const PYODIDE_BASE = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`
const WORKSPACE_DIR = '/workspace'

let pyodideInstance = null
let pyodideLoading = null

const loadScript = (src) =>
  new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.src = src
    script.onload = resolve
    script.onerror = () => reject(new Error('Failed to load Python kernel'))
    document.head.appendChild(script)
  })

export function isPythonKernelReady() {
  return Boolean(pyodideInstance)
}

export function isPythonKernelLoading() {
  return Boolean(pyodideLoading) && !pyodideInstance
}

/**
 * Initialize (or reuse) the shared Pyodide instance.
 * Subsequent runs share the same kernel until resetPythonKernel().
 */
export async function ensurePythonKernel(onStatus) {
  if (pyodideInstance) {
    onStatus?.('Python Kernel: Ready')
    return pyodideInstance
  }

  if (!pyodideLoading) {
    pyodideLoading = (async () => {
      onStatus?.('Python Kernel: Loading…')

      await loadScript(`${PYODIDE_BASE}pyodide.js`)

      if (!window.loadPyodide) {
        throw new Error('Pyodide is not available')
      }

      const pyodide = await window.loadPyodide({ indexURL: PYODIDE_BASE })
      pyodideInstance = pyodide
      pyodideLoading = null
      onStatus?.('Python Kernel: Ready')
      return pyodide
    })().catch((error) => {
      pyodideLoading = null
      pyodideInstance = null
      throw error
    })
  }

  return pyodideLoading
}

function isMountablePythonWorkspaceFile(fileName) {
  return /\.(py|json|txt)$/i.test(fileName || '')
}

/** Keep writes inside /workspace; drop ".." segments. */
function toWorkspaceRelativePath(fileName) {
  return String(fileName || '')
    .replace(/\\/g, '/')
    .replace(/^\/+/, '')
    .split('/')
    .filter((part) => part && part !== '.' && part !== '..')
    .join('/')
}

/**
 * Pyodide `batched` strips the trailing newline from complete lines.
 * Restore it so console output matches real Python (and JS kernel).
 */
function restoreBatchedChunk(text) {
  const chunk = String(text ?? '')
  if (!chunk) return ''
  return chunk.endsWith('\n') ? chunk : `${chunk}\n`
}

function destroyPyProxy(value) {
  if (value && typeof value.destroy === 'function') {
    try {
      value.destroy()
    } catch {
      // Proxy may already be destroyed.
    }
  }
}

/**
 * Wipe and remount /workspace for a clean run.
 * Must leave the directory before rmtree — cwd pins the inode and causes
 * OSError: [Errno 10] Resource busy: '/workspace' on the 2nd+ Run.
 */
function resetAndPrepareWorkspace(pyodide) {
  // Leave via Emscripten FS first so Python rmtree cannot hit EBUSY.
  try {
    pyodide.FS.chdir('/')
  } catch {
    // FS may not have /workspace yet on the first run.
  }

  pyodide.runPython(`
import os
import shutil
import sys

workspace = ${JSON.stringify(WORKSPACE_DIR)}

# Drop cached imports from previous runs so edited siblings reload.
for module_name, module in list(sys.modules.items()):
    module_file = getattr(module, "__file__", None) or ""
    if isinstance(module_file, str) and module_file.startswith(workspace):
        del sys.modules[module_name]

# Leave /workspace before deleting it (cwd keeps the dir busy).
try:
    cwd = os.getcwd()
except OSError:
    cwd = "/"
if cwd == workspace or cwd.startswith(workspace + "/"):
    os.chdir("/")

if os.path.exists(workspace):
    shutil.rmtree(workspace)

os.makedirs(workspace, exist_ok=True)
os.chdir(workspace)

if workspace in sys.path:
    sys.path.remove(workspace)
sys.path.insert(0, workspace)
`)
}

function writeWorkspaceFiles(pyodide, files) {
  const written = []

  for (const file of files || []) {
    const relativePath = toWorkspaceRelativePath(file?.name)
    if (!relativePath || !isMountablePythonWorkspaceFile(relativePath)) {
      continue
    }

    const absolutePath = `${WORKSPACE_DIR}/${relativePath}`
    const parent = absolutePath.slice(0, absolutePath.lastIndexOf('/'))

    if (parent && parent !== WORKSPACE_DIR) {
      const segments = parent.replace(`${WORKSPACE_DIR}/`, '').split('/')
      let current = WORKSPACE_DIR
      for (const segment of segments) {
        current = `${current}/${segment}`
        try {
          pyodide.FS.mkdir(current)
        } catch {
          // Directory already exists.
        }
      }
    }

    pyodide.FS.writeFile(absolutePath, file.content ?? '')
    written.push(relativePath)
  }

  return written
}

function resolveEntryRelativePath(files, entryFileName, writtenPaths) {
  const requested = toWorkspaceRelativePath(entryFileName)
  if (requested && writtenPaths.includes(requested)) {
    return requested
  }

  if (writtenPaths.includes('main.py')) {
    return 'main.py'
  }

  const firstPy = (files || [])
    .map((file) => toWorkspaceRelativePath(file?.name))
    .find((name) => name && name.toLowerCase().endsWith('.py') && writtenPaths.includes(name))

  return firstPy || requested || 'main.py'
}

/**
 * Run a Python workspace on the shared kernel.
 * Mounts .py/.json/.txt into /workspace, then executes the entry file once.
 *
 * @param {{ files?: Array<{name: string, content?: string}>, entryFileName?: string, onStream?: Function }} options
 */
export async function runPythonKernel({
  files = [],
  entryFileName = 'main.py',
  onStream,
} = {}) {
  const pyodide = await ensurePythonKernel((message) => onStream?.('status', message))

  let stdout = ''
  let stderr = ''

  pyodide.setStdout({
    batched: (text) => {
      const chunk = restoreBatchedChunk(text)
      stdout += chunk
      onStream?.('stdout', chunk)
    },
  })

  pyodide.setStderr({
    batched: (text) => {
      const chunk = restoreBatchedChunk(text)
      stderr += chunk
      onStream?.('stderr', chunk)
    },
  })

  try {
    onStream?.('status', 'Preparing Python workspace...')
    resetAndPrepareWorkspace(pyodide)
    const writtenPaths = writeWorkspaceFiles(pyodide, files)

    if (!writtenPaths.length) {
      return {
        stdout: '',
        stderr: 'No Python workspace files (.py) found to execute.',
        returnValue: '',
        status: 'error',
        kernelMessage: 'Python Kernel',
        previewHtml: null,
        hasPreview: false,
      }
    }

    const entryRelativePath = resolveEntryRelativePath(files, entryFileName, writtenPaths)
    const entryAbsolutePath = `${WORKSPACE_DIR}/${entryRelativePath}`

    onStream?.('status', 'Executing workspace...')

    // Trailing `None` discards runpy's module dict so it never becomes a
    // junk "result" block in the console.
    const result = await pyodide.runPythonAsync(`
import runpy
runpy.run_path(${JSON.stringify(entryAbsolutePath)}, run_name="__main__")
None
`)
    destroyPyProxy(result)

    return {
      stdout,
      stderr,
      returnValue: '',
      status: 'success',
      kernelMessage: 'Python Kernel: Ready',
      previewHtml: null,
      hasPreview: false,
    }
  } catch (error) {
    const message = error.message || String(error)
    const chunk = restoreBatchedChunk(message)
    if (!stderr.includes(message)) {
      stderr += chunk
      onStream?.('stderr', chunk)
    }

    return {
      stdout,
      stderr,
      returnValue: '',
      status: 'error',
      kernelMessage: 'Python Kernel',
      previewHtml: null,
      hasPreview: false,
    }
  }
}

export function resetPythonKernel() {
  pyodideInstance = null
  pyodideLoading = null
}
