export function createExecutionState(status = 'idle') {
  return {
    status,
    durationMs: null,
    kernelMessage: '',
    blocks: [],
    previewHtml: null,
    activeTab: 'console',
  }
}

export function normalizeExecutionResult(raw, durationMs) {
  const blocks = []
  const hasError = Boolean(raw?.stderr || raw?.error || raw?.status === 'error')

  if (raw?.stdout?.trim()) {
    blocks.push({ id: `stdout-${Date.now()}`, type: 'stdout', content: raw.stdout.trimEnd() })
  }

  if (raw?.stderr?.trim()) {
    blocks.push({ id: `stderr-${Date.now()}`, type: 'stderr', content: raw.stderr.trimEnd() })
  }

  if (raw?.error?.trim()) {
    blocks.push({ id: `error-${Date.now()}`, type: 'error', content: raw.error.trimEnd() })
  }

  if (raw?.returnValue?.trim()) {
    blocks.push({
      id: `result-${Date.now()}`,
      type: 'result',
      content: raw.returnValue.trimEnd(),
    })
  }

  if (!blocks.length && !raw?.previewHtml && !hasError) {
    blocks.push({
      id: `info-${Date.now()}`,
      type: 'info',
      content: 'تم التنفيذ بنجاح — لا يوجد مخرجات.',
    })
  }

  return {
    status: hasError ? 'error' : 'success',
    durationMs: Math.round(durationMs),
    kernelMessage: raw?.kernelMessage || '',
    blocks,
    previewHtml: raw?.previewHtml || null,
    activeTab: raw?.previewHtml ? 'preview' : 'console',
  }
}

export function appendStreamBlock(blocks, type, chunk) {
  const last = blocks[blocks.length - 1]

  if (last && last.type === type && last.streaming) {
    return [
      ...blocks.slice(0, -1),
      { ...last, content: last.content + chunk },
    ]
  }

  return [
    ...blocks,
    {
      id: `${type}-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      type,
      content: chunk,
      streaming: true,
    },
  ]
}

export function finalizeStreamBlocks(blocks) {
  return blocks.map((block) => ({ ...block, streaming: false }))
}
