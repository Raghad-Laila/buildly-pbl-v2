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

function resetAndPrepareWorkspace(pyodide) {
  pyodide.runPython(`
import os
import shutil
import sys

workspace = ${JSON.stringify(WORKSPACE_DIR)}

if os.path.exists(workspace):
    shutil.rmtree(workspace)

os.makedirs(workspace, exist_ok=True)
os.chdir(workspace)

if workspace in sys.path:
    sys.path.remove(workspace)
sys.path.insert(0, workspace)

# Drop cached imports from previous runs so edited siblings reload.
for module_name, module in list(sys.modules.items()):
    module_file = getattr(module, "__file__", None) or ""
    if isinstance(module_file, str) and module_file.startswith(workspace):
        del sys.modules[module_name]
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
      stdout += text
      onStream?.('stdout', text)
    },
  })

  pyodide.setStderr({
    batched: (text) => {
      stderr += text
      onStream?.('stderr', text)
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

    const result = await pyodide.runPythonAsync(`
import runpy
runpy.run_path(${JSON.stringify(entryAbsolutePath)}, run_name="__main__")
`)

    let returnValue = ''
    if (result !== undefined && result !== null) {
      returnValue = String(result)
    }

    return {
      stdout,
      stderr,
      returnValue,
      status: 'success',
      kernelMessage: 'Python Kernel: Ready',
      previewHtml: null,
      hasPreview: false,
    }
  } catch (error) {
    const message = error.message || String(error)
    onStream?.('stderr', message)

    return {
      stdout,
      stderr: message,
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
