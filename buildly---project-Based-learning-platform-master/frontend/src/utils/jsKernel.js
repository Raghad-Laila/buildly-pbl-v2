let sandboxFrame = null
let sandboxWindow = null
let capturedLogs = []

function ensureJsSandbox() {
  if (sandboxFrame) {
    return sandboxWindow
  }

  sandboxFrame = document.createElement('iframe')
  sandboxFrame.setAttribute('sandbox', 'allow-scripts allow-same-origin')
  sandboxFrame.style.display = 'none'
  sandboxFrame.title = 'js-kernel'
  document.body.appendChild(sandboxFrame)

  sandboxWindow = sandboxFrame.contentWindow

  sandboxWindow.console = {
    log: (...args) => {
      const line = args.map((value) => formatValue(value)).join(' ')
      capturedLogs.push(line)
    },
    error: (...args) => {
      capturedLogs.push(`[error] ${args.map((value) => formatValue(value)).join(' ')}`)
    },
    warn: (...args) => {
      capturedLogs.push(`[warn] ${args.map((value) => formatValue(value)).join(' ')}`)
    },
  }

  return sandboxWindow
}

function formatValue(value) {
  if (value === null) return 'null'
  if (value === undefined) return 'undefined'
  if (typeof value === 'object') {
    try {
      return JSON.stringify(value)
    } catch {
      return String(value)
    }
  }
  return String(value)
}

export function resetJsKernel() {
  if (sandboxFrame) {
    sandboxFrame.remove()
    sandboxFrame = null
    sandboxWindow = null
  }
  capturedLogs = []
}

export function runJsKernel(code, onStream) {
  const sandbox = ensureJsSandbox()
  capturedLogs = []

  try {
    sandbox.eval(code)

    capturedLogs.forEach((line) => onStream?.('stdout', `${line}\n`))

    return {
      stdout: capturedLogs.join('\n'),
      stderr: '',
      returnValue: '',
      status: 'success',
      kernelMessage: 'JavaScript kernel',
    }
  } catch (error) {
    const message = error.message || String(error)
    onStream?.('stderr', message)

    return {
      stdout: capturedLogs.join('\n'),
      stderr: message,
      returnValue: '',
      status: 'error',
      kernelMessage: 'JavaScript kernel',
    }
  }
}
