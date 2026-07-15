export function createEmptyStarterSelection() {
  return { mode: null, folderFiles: null, zipFile: null }
}

export function hasStarterFolderSelection(selection, existingFile = null) {
  if (existingFile) {
    return true
  }

  if (!selection) {
    return false
  }

  if (selection.mode === 'folder') {
    return Boolean(selection.folderFiles && selection.folderFiles.length > 0)
  }

  if (selection.mode === 'zip') {
    return Boolean(selection.zipFile)
  }

  return false
}

export function getStarterFolderLabel(selection) {
  if (!selection) {
    return ''
  }

  if (selection.mode === 'zip' && selection.zipFile) {
    return selection.zipFile.name
  }

  const folderFiles = selection.folderFiles
  if (!folderFiles?.length) {
    return ''
  }

  const rootFolder = folderFiles[0]?.webkitRelativePath?.split('/')[0]
  if (rootFolder) {
    return `${rootFolder} (${folderFiles.length} ملف)`
  }

  return `${folderFiles.length} ملف`
}

export async function uploadStarterSelection(projectId, selection, projectsAPI) {
  if (!selection?.mode) {
    return null
  }

  if (selection.mode === 'zip' && selection.zipFile) {
    return projectsAPI.uploadStarterFile(projectId, selection.zipFile)
  }

  if (selection.mode === 'folder' && selection.folderFiles?.length) {
    return projectsAPI.uploadStarterFolder(projectId, selection.folderFiles)
  }

  return null
}
