const PYODIDE_VERSION = '0.26.4'
const PYODIDE_BASE = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`

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
    script.onerror = () => reject(new Error('تعذّر تحميل Python kernel'))
    document.head.appendChild(script)
  })

export function isPythonKernelReady() {
  return Boolean(pyodideInstance)
}

export function isPythonKernelLoading() {
  return Boolean(pyodideLoading) && !pyodideInstance
}

export async function ensurePythonKernel(onStatus) {
  if (pyodideInstance) {
    return pyodideInstance
  }

  if (!pyodideLoading) {
    pyodideLoading = (async () => {
      onStatus?.('جاري الاتصال بـ Python kernel...')

      await loadScript(`${PYODIDE_BASE}pyodide.js`)

      if (!window.loadPyodide) {
        throw new Error('Pyodide غير متوفر')
      }

      const pyodide = await window.loadPyodide({ indexURL: PYODIDE_BASE })
      pyodideInstance = pyodide
      onStatus?.('Python kernel جاهز')
      return pyodide
    })()
  }

  return pyodideLoading
}

export async function runPythonKernel(code, onStream) {
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
    const result = await pyodide.runPythonAsync(code)
    let returnValue = ''

    if (result !== undefined && result !== null) {
      returnValue = String(result)
    }

    return {
      stdout,
      stderr,
      returnValue,
      status: 'success',
      kernelMessage: 'Python kernel',
    }
  } catch (error) {
    const message = error.message || String(error)
    onStream?.('stderr', message)

    return {
      stdout,
      stderr: message,
      returnValue: '',
      status: 'error',
      kernelMessage: 'Python kernel',
    }
  }
}

export function resetPythonKernel() {
  pyodideInstance = null
  pyodideLoading = null
}
