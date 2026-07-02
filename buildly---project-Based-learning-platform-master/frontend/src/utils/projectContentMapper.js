export const splitLines = (text) => {
  if (!text?.trim()) return []
  return text
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
}

export const joinLines = (items) => {
  return items
    .map((item) => (typeof item === 'string' ? item : item?.text || ''))
    .map((text) => text.trim())
    .filter(Boolean)
    .join('\n')
}

export const createEmptyStory = () => ({
  id: null,
  title: '',
  description: '',
})

export const tasksToEditorState = (tasks = []) => {
  const userStories = tasks.map((task) => ({
    id: task.id,
    title: task.title || '',
    description: task.description || '',
  }))

  const hintItems = tasks.map((task) => task.hint || '')
  if (hintItems.length === 0) {
    hintItems.push('')
  }

  return { userStories, hintItems }
}

export const buildTasksFromSections = ({
  userStories,
  hintItems,
  projectId,
  taskType = 'code',
}) => {
  return userStories
    .map((story, index) => ({
      id: story.id || null,
      title: story.title?.trim() || '',
      description: story.description?.trim() || '',
      hint: (hintItems[index] || '').trim(),
      order: index + 1,
    }))
    .filter((story) => story.title && story.description)
    .map((story) => ({
      project: projectId,
      title: story.title,
      description: story.description,
      task_type: taskType,
      hint: story.hint,
      expected_answer: '',
      teaching: '',
      order: story.order,
    }))
}

export const storySnapshot = (story) =>
  `${story.title?.trim()}|${story.description?.trim()}`

export const hasStoryChanged = (story, originalStory) => {
  if (!originalStory) return true
  return storySnapshot(story) !== storySnapshot(originalStory)
}

export const hasHintChanged = (hint, originalHint) => {
  return (hint || '').trim() !== (originalHint || '').trim()
}

export const syncProjectTasksOnEdit = async ({
  projectId,
  originalTasks,
  userStories,
  hintItems,
  projectsAPI,
}) => {
  const validStories = userStories
    .map((story, index) => ({
      story,
      hint: (hintItems[index] || '').trim(),
    }))
    .filter(({ story }) => story.title?.trim() && story.description?.trim())

  const originalMap = new Map(originalTasks.map((task) => [task.id, task]))
  const referencedIds = new Set(
    validStories.filter(({ story }) => story.id).map(({ story }) => story.id)
  )

  for (const original of originalTasks) {
    if (!referencedIds.has(original.id)) {
      await projectsAPI.deleteTask(original.id)
    }
  }

  for (let index = 0; index < validStories.length; index += 1) {
    const { story, hint } = validStories[index]
    const order = index + 1
    const original = story.id ? originalMap.get(story.id) : null

    const unchanged =
      original &&
      !hasStoryChanged(story, original) &&
      !hasHintChanged(hint, original.hint) &&
      original.order === order

    if (unchanged) continue

    if (original) {
      await projectsAPI.deleteTask(original.id)
    }

    await projectsAPI.createTask({
      project: projectId,
      title: story.title.trim(),
      description: story.description.trim(),
      task_type: original?.task_type || 'code',
      hint,
      expected_answer: original?.expected_answer || '',
      teaching: original?.teaching || '',
      order,
    })
  }
}
