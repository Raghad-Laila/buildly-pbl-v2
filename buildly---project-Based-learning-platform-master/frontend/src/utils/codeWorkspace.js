const WORKSPACE_VERSION = 1

const FRONTEND_PROJECT_LANGUAGES = new Set([
  'html',
  'css',
  'javascript',
  'typescript',
  'react',
])

export function createFileId() {
  return `file-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
}

export function getDefaultFileName(projectLanguage) {
  const map = {
    python: 'main.py',
    html: 'index.html',
    css: 'style.css',
    javascript: 'script.js',
    typescript: 'main.ts',
    react: 'App.jsx',
    java: 'Main.java',
  }

  return map[projectLanguage] || 'main.txt'
}

function getStarterHtml(projectLanguage) {
  if (projectLanguage === 'react') {
    return `<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My React App</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div id="root"></div>
  <script type="text/babel" src="App.jsx"></script>
</body>
</html>`
  }

  return `<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Project</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <!-- عدّل المحتوى هنا — احتفظ ببنية HTML الكاملة -->
  <h1>مرحباً</h1>
  <p>ابدأ بكتابة الكود هنا</p>
  <script src="script.js"></script>
</body>
</html>`
}

function getStarterReactComponent() {
  return `function App() {
  return (
    <div>
      <h1>مرحباً من Buildly!</h1>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);`
}

export function getDefaultWorkspace(projectLanguage) {
  if (FRONTEND_PROJECT_LANGUAGES.has(projectLanguage)) {
    const htmlId = createFileId()
    const cssId = createFileId()
    const jsId = createFileId()

    const files =
      projectLanguage === 'react'
        ? [
            { id: htmlId, name: 'index.html', content: getStarterHtml('react') },
            { id: cssId, name: 'style.css', content: '' },
            { id: jsId, name: 'App.jsx', content: getStarterReactComponent() },
          ]
        : [
            { id: htmlId, name: 'index.html', content: getStarterHtml(projectLanguage) },
            { id: cssId, name: 'style.css', content: '' },
            { id: jsId, name: 'script.js', content: '' },
          ]

    return {
      version: WORKSPACE_VERSION,
      activeFileId: htmlId,
      files,
    }
  }

  const id = createFileId()

  return {
    version: WORKSPACE_VERSION,
    activeFileId: id,
    files: [{ id, name: getDefaultFileName(projectLanguage), content: '' }],
  }
}

export function parseWorkspace(answer, projectLanguage) {
  if (!answer || !answer.trim()) {
    return getDefaultWorkspace(projectLanguage)
  }

  try {
    const parsed = JSON.parse(answer)
    if (
      parsed?.version === WORKSPACE_VERSION &&
      Array.isArray(parsed.files) &&
      parsed.files.length > 0
    ) {
      const activeExists = parsed.files.some((file) => file.id === parsed.activeFileId)
      return {
        version: WORKSPACE_VERSION,
        activeFileId: activeExists ? parsed.activeFileId : parsed.files[0].id,
        files: parsed.files.map((file) => ({
          id: file.id || createFileId(),
          name: file.name || 'untitled.txt',
          content: file.content || '',
        })),
      }
    }
  } catch {
    // legacy single-file answer
  }

  const id = createFileId()

  return {
    version: WORKSPACE_VERSION,
    activeFileId: id,
    files: [{ id, name: getDefaultFileName(projectLanguage), content: answer }],
  }
}

export function serializeWorkspace(workspace) {
  return JSON.stringify(workspace)
}

export function getMonacoLanguageFromFileName(fileName) {
  const extension = fileName.split('.').pop()?.toLowerCase()
  const map = {
    html: 'html',
    htm: 'html',
    css: 'css',
    js: 'javascript',
    jsx: 'javascript',
    mjs: 'javascript',
    ts: 'typescript',
    tsx: 'typescript',
    py: 'python',
    java: 'java',
    json: 'json',
    md: 'markdown',
  }

  return map[extension] || 'plaintext'
}

export function workspaceHasContent(workspace) {
  return workspace?.files?.some((file) => file.content.trim().length > 0)
}

export function getActiveFile(workspace) {
  return (
    workspace.files.find((file) => file.id === workspace.activeFileId) ||
    workspace.files[0]
  )
}

export function updateFileContent(workspace, fileId, content) {
  return {
    ...workspace,
    files: workspace.files.map((file) =>
      file.id === fileId ? { ...file, content } : file
    ),
  }
}

export function setActiveFile(workspace, fileId) {
  return { ...workspace, activeFileId: fileId }
}

export function addFile(workspace, name) {
  const trimmedName = name.trim()
  if (!trimmedName) return workspace

  const exists = workspace.files.some(
    (file) => file.name.toLowerCase() === trimmedName.toLowerCase()
  )
  if (exists) return workspace

  const id = createFileId()

  return {
    ...workspace,
    activeFileId: id,
    files: [...workspace.files, { id, name: trimmedName, content: '' }],
  }
}

export function renameFile(workspace, fileId, newName) {
  const trimmedName = newName.trim()
  if (!trimmedName) return workspace

  const exists = workspace.files.some(
    (file) =>
      file.id !== fileId && file.name.toLowerCase() === trimmedName.toLowerCase()
  )
  if (exists) return workspace

  return {
    ...workspace,
    files: workspace.files.map((file) =>
      file.id === fileId ? { ...file, name: trimmedName } : file
    ),
  }
}

export function deleteFile(workspace, fileId) {
  if (workspace.files.length <= 1) return workspace

  const remaining = workspace.files.filter((file) => file.id !== fileId)
  const activeFileId =
    workspace.activeFileId === fileId ? remaining[0].id : workspace.activeFileId

  return {
    ...workspace,
    activeFileId,
    files: remaining,
  }
}

function resolveFileRef(href, files) {
  const normalized = href.replace(/^\.\//, '').split('?')[0].split('#')[0]

  return files.find(
    (file) =>
      file.name === normalized ||
      file.name.split('/').pop() === normalized ||
      file.name.endsWith(`/${normalized}`)
  )
}

function injectReactRuntime(html) {
  if (html.includes('react.development.js')) {
    return html
  }

  const reactScripts = `
  <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>`

  if (html.includes('</head>')) {
    return html.replace('</head>', `${reactScripts}\n</head>`)
  }

  return reactScripts + html
}

function inlineStylesheets(html, files) {
  const linkPattern =
    /<link\b[^>]*\brel=["']stylesheet["'][^>]*\bhref=["']([^"']+)["'][^>]*\/?>/gi

  let result = html.replace(linkPattern, (match, href) => {
    const file = resolveFileRef(href, files)
    return file ? `<style>\n${file.content}\n</style>` : match
  })

  const reverseLinkPattern =
    /<link\b[^>]*\bhref=["']([^"']+)["'][^>]*\brel=["']stylesheet["'][^>]*\/?>/gi

  result = result.replace(reverseLinkPattern, (match, href) => {
    const file = resolveFileRef(href, files)
    return file ? `<style>\n${file.content}\n</style>` : match
  })

  return result
}

function inlineScripts(html, files) {
  const scriptPattern =
    /<script\b([^>]*)\bsrc=["']([^"']+)["']([^>]*)>\s*<\/script>/gi

  return html.replace(scriptPattern, (match, beforeSrc, src, afterSrc) => {
    const file = resolveFileRef(src, files)
    if (!file) return match

    const attrs = `${beforeSrc || ''} ${afterSrc || ''}`
    const isBabel =
      /\.(jsx|tsx)$/i.test(file.name) || /type=["']text\/babel["']/i.test(attrs)

    if (isBabel) {
      return `<script type="text/babel">\n${file.content.replace(/<\/script>/gi, '<\\/script>')}\n</script>`
    }

    return `<script>\n${file.content.replace(/<\/script>/gi, '<\\/script>')}\n</script>`
  })
}

function appendUnlinkedAssets(html, files, htmlFileName) {
  const linkedNames = new Set()
  const linkMatches = html.matchAll(/href=["']([^"']+)["']/gi)
  const scriptMatches = html.matchAll(/src=["']([^"']+)["']/gi)

  for (const match of linkMatches) linkedNames.add(match[1].replace(/^\.\//, ''))
  for (const match of scriptMatches) linkedNames.add(match[1].replace(/^\.\//, ''))

  let result = html
  const unlinkedCss = files.filter(
    (file) =>
      file.name !== htmlFileName &&
      file.name.endsWith('.css') &&
      !linkedNames.has(file.name)
  )

  if (unlinkedCss.length && result.includes('</head>')) {
    const styles = unlinkedCss.map((file) => `<style>\n${file.content}\n</style>`).join('\n')
    result = result.replace('</head>', `${styles}\n</head>`)
  }

  const unlinkedJs = files.filter(
    (file) =>
      file.name !== htmlFileName &&
      /\.(js|jsx|ts|tsx|mjs)$/i.test(file.name) &&
      !linkedNames.has(file.name)
  )

  if (unlinkedJs.length && result.includes('</body>')) {
    const scripts = unlinkedJs
      .map((file) => {
        const isBabel = /\.(jsx|tsx)$/i.test(file.name)
        const escaped = file.content.replace(/<\/script>/gi, '<\\/script>')
        return isBabel
          ? `<script type="text/babel">\n${escaped}\n</script>`
          : `<script>\n${escaped}\n</script>`
      })
      .join('\n')
    result = result.replace('</body>', `${scripts}\n</body>`)
  }

  return result
}

export function bundleWorkspaceFiles(files) {
  const htmlFile =
    files.find((file) => /^index\.html?$/i.test(file.name)) ||
    files.find((file) => /\.html?$/i.test(file.name))

  if (!htmlFile) {
    return null
  }

  let html = htmlFile.content
  html = inlineStylesheets(html, files)
  html = inlineScripts(html, files)
  html = appendUnlinkedAssets(html, files, htmlFile.name)

  const usesReact =
    files.some((file) => /\.(jsx|tsx)$/i.test(file.name)) ||
    html.includes('type="text/babel"')

  if (usesReact) {
    html = injectReactRuntime(html)
  }

  if (!html.includes('<!DOCTYPE')) {
    html = `<!DOCTYPE html>\n${html}`
  }

  return html
}

export function getWorkspaceFileContent(workspace, fileName) {
  const target = fileName.toLowerCase()
  const file = workspace?.files?.find(
    (item) =>
      item.name.toLowerCase() === target ||
      item.name.toLowerCase().split('/').pop() === target
  )

  return file?.content || ''
}

export function getWorkspaceSnapshot(workspaceRef, fallbackWorkspace) {
  if (workspaceRef?.current?.trim()) {
    try {
      const parsed = JSON.parse(workspaceRef.current)
      if (
        parsed?.version === WORKSPACE_VERSION &&
        Array.isArray(parsed.files) &&
        parsed.files.length > 0
      ) {
        return parsed
      }
    } catch {
      // ignore invalid snapshot
    }
  }

  return fallbackWorkspace
}

export function getMainExecutableFile(workspace, projectLanguage) {
  const { files } = workspace

  const priorityByLanguage = {
    html: ['index.html', 'style.css', 'script.js'],
    css: ['style.css', 'index.html', 'script.js'],
    javascript: ['script.js', 'index.html', 'style.css'],
    typescript: ['main.ts', 'script.js', 'index.html'],
    react: ['App.jsx', 'index.html', 'style.css'],
    python: ['main.py'],
  }

  const priorityNames = priorityByLanguage[projectLanguage] || [
    'index.html',
    'main.py',
    'script.js',
    'App.jsx',
    'main.ts',
    'style.css',
  ]

  for (const name of priorityNames) {
    const file = files.find((item) => item.name.toLowerCase() === name.toLowerCase())
    if (file) return file
  }

  return getActiveFile(workspace) || files[0]
}

export function detectLanguageFromFile(file, projectLanguage) {
  const extension = file.name.split('.').pop()?.toLowerCase()

  const extensionMap = {
    html: 'html',
    htm: 'html',
    css: 'css',
    js: 'javascript',
    mjs: 'javascript',
    ts: 'typescript',
    jsx: 'react',
    tsx: 'react',
    py: 'python',
  }

  return extensionMap[extension] || projectLanguage
}
