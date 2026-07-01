import {
  bundleWorkspaceFiles,
  detectLanguageFromFile,
  getMainExecutableFile,
} from './codeWorkspace'

const FRONTEND_LANGUAGES = new Set([
  'html',
  'css',
  'javascript',
  'typescript',
  'react',
])

const loadScript = (src) =>
  new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.src = src
    script.onload = resolve
    script.onerror = () => reject(new Error(`Failed to load ${src}`))
    document.head.appendChild(script)
  })

export function isFrontendLanguage(language) {
  return FRONTEND_LANGUAGES.has(language)
}

export function resolveExecutionLanguage(code, projectLanguage) {
  if (isFrontendLanguage(projectLanguage)) {
    return projectLanguage
  }

  const trimmed = code.trim()
  if (!trimmed) {
    return projectLanguage
  }

  const looksLikeHtml =
    trimmed.startsWith('<!DOCTYPE') ||
    trimmed.startsWith('<html') ||
    (trimmed.startsWith('<') && trimmed.includes('</'))

  const looksLikeReact =
    /<[A-Za-z][\w-]*[\s/>]/.test(trimmed) &&
    (trimmed.includes('function ') ||
      trimmed.includes('const ') ||
      trimmed.includes('return'))

  const looksLikeCss =
    !looksLikeHtml &&
    !looksLikeReact &&
    /[{][^}]*[}]/.test(trimmed) &&
    /[:;]/.test(trimmed) &&
    !trimmed.includes('function ') &&
    !trimmed.includes('console.log')

  const looksLikeJavaScript =
    trimmed.includes('console.log') ||
    /^(const|let|var|function)\s/m.test(trimmed)

  if (looksLikeHtml && !looksLikeReact) return 'html'
  if (looksLikeReact) return 'react'
  if (looksLikeCss) return 'css'
  if (looksLikeJavaScript) return 'javascript'

  return projectLanguage
}

export function getMonacoLanguage(language) {
  const map = {
    react: 'javascript',
    html: 'html',
    css: 'css',
    javascript: 'javascript',
    typescript: 'typescript',
  }

  return map[language] || language || 'javascript'
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

function runJavaScript(code) {
  const logs = []
  const originalLog = console.log
  const originalError = console.error
  const originalWarn = console.warn

  console.log = (...args) => {
    logs.push(args.map(formatValue).join(' '))
  }
  console.error = (...args) => {
    logs.push(`[error] ${args.map(formatValue).join(' ')}`)
  }
  console.warn = (...args) => {
    logs.push(`[warn] ${args.map(formatValue).join(' ')}`)
  }

  let stderr = ''

  try {
    const fn = new Function(code)
    const result = fn()
    if (result !== undefined) {
      logs.push(formatValue(result))
    }
  } catch (error) {
    stderr = error.message
  } finally {
    console.log = originalLog
    console.error = originalError
    console.warn = originalWarn
  }

  return {
    stdout: logs.join('\n'),
    stderr,
    previewHtml: null,
    hasPreview: false,
  }
}

async function transpileTypeScript(code) {
  await loadScript('https://unpkg.com/typescript@5.3.3/lib/typescript.js')

  if (!window.ts) {
    throw new Error('TypeScript compiler failed to load')
  }

  return window.ts.transpile(code, {
    target: window.ts.ScriptTarget.ES2020,
    module: window.ts.ModuleKind.None,
  })
}

function runHtml(code) {
  return {
    stdout: '',
    stderr: '',
    previewHtml: code,
    hasPreview: true,
  }
}

function runCss(code) {
  const previewHtml = `<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 16px;
      margin: 0;
      background: #f8fafc;
      color: #1e293b;
    }
    ${code}
  </style>
</head>
<body>
  <h1>عنوان تجريبي</h1>
  <p>هذا نص تجريبي لمعاينة تنسيقات CSS.</p>
  <button class="btn">زر تجريبي</button>
  <div class="box">صندوق تجريبي</div>
</body>
</html>`

  return {
    stdout: '',
    stderr: '',
    previewHtml,
    hasPreview: true,
  }
}

function runReact(code) {
  const escapedCode = code.replace(/<\/script>/gi, '<\\/script>')
  const hasManualRender = /ReactDOM\.(createRoot|render)|createRoot\(/.test(code)

  const autoRenderBlock = hasManualRender
    ? ''
    : `
      if (typeof App !== 'undefined') {
        const root = ReactDOM.createRoot(rootElement);
        root.render(React.createElement(App));
      } else if (typeof Component !== 'undefined') {
        const root = ReactDOM.createRoot(rootElement);
        root.render(React.createElement(Component));
      } else {
        rootElement.innerHTML = '<p>اكتب مكوّن React باسم App أو Component، أو استخدم ReactDOM.createRoot يدوياً.</p>';
      }
    `

  const previewHtml = `<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 16px;
      margin: 0;
    }
    .runtime-error {
      color: #dc2626;
      white-space: pre-wrap;
      font-family: monospace;
    }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const showError = (error) => {
      const root = document.getElementById('root');
      root.innerHTML = '<pre class="runtime-error">' + error.message + '</pre>';
    };

    try {
      ${escapedCode}

      const rootElement = document.getElementById('root');
      ${autoRenderBlock}
    } catch (error) {
      showError(error);
    }
  </script>
</body>
</html>`

  return {
    stdout: '',
    stderr: '',
    previewHtml,
    hasPreview: true,
  }
}

export async function runFrontendCode(code, language) {
  switch (language) {
    case 'html':
      return runHtml(code)
    case 'css':
      return runCss(code)
    case 'javascript':
      return runJavaScript(code)
    case 'typescript': {
      try {
        const jsCode = await transpileTypeScript(code)
        return runJavaScript(jsCode)
      } catch (error) {
        return {
          stdout: '',
          stderr: error.message,
          previewHtml: null,
          hasPreview: false,
        }
      }
    }
    case 'react':
      return runReact(code)
    default:
      return {
        stdout: '',
        stderr: 'لغة frontend غير مدعومة',
        previewHtml: null,
        hasPreview: false,
      }
  }
}

export async function runWorkspace(workspace, projectLanguage) {
  const { files } = workspace

  if (!files?.length) {
    return {
      stdout: '',
      stderr: 'لا توجد ملفات للتنفيذ',
      previewHtml: null,
      hasPreview: false,
    }
  }

  const bundledHtml = bundleWorkspaceFiles(files)

  if (bundledHtml) {
    return runHtml(bundledHtml)
  }

  if (files.length === 1) {
    const file = files[0]
    const language = detectLanguageFromFile(file, projectLanguage)
    const executionLanguage = resolveExecutionLanguage(file.content, language)
    return runFrontendCode(file.content, executionLanguage)
  }

  const mainFile = getMainExecutableFile(workspace, projectLanguage)
  const language = detectLanguageFromFile(mainFile, projectLanguage)
  const executionLanguage = resolveExecutionLanguage(mainFile.content, language)

  if (isFrontendLanguage(executionLanguage)) {
    return runFrontendCode(mainFile.content, executionLanguage)
  }

  return {
    stdout: '',
    stderr: 'لم يتم العثور على ملف HTML للمعاينة. أنشئ index.html واربط ملفات CSS/JS داخله.',
    previewHtml: null,
    hasPreview: false,
  }
}
