"""Task Board advanced project for Frontend Mastery."""

TASK_BOARD_TITLE = 'Build a Task Board with Vanilla JavaScript'

TASK_BOARD_PROJECT = {
    'title': TASK_BOARD_TITLE,
    'level': 'advanced',
    'languages': ['javascript', 'html', 'css'],
    'estimated_time': 6,
    'description': (
        'Build a kanban-style task board using HTML, CSS, and vanilla JavaScript. '
        'Create task data helpers, render a responsive board layout, and style cards '
        'by status and priority. Give the project your own visual style while keeping '
        'the required structure and behavior.'
    ),
    'objectives': (
        'Build a complete task board with JavaScript logic, semantic markup, and custom CSS.'
    ),
    'stories': [
        {
            'title': 'Task model',
            'description': (
                'In script.js, write a createTask(id, title, status, priority) function that '
                'returns an object with id, title, status, and priority. Status must be one '
                'of: todo, doing, or done. Priority must be one of: high, medium, or low.'
            ),
            'hint': 'Return { id, title, status, priority } and validate the allowed values.',
        },
        {
            'title': 'Sort and filter tasks',
            'description': (
                'Write sortTasksByPriority(tasks) to order tasks high → medium → low, and '
                'filterTasksByStatus(tasks, status) to return only tasks with the given status.'
            ),
            'hint': 'Use a priority map like { high: 0, medium: 1, low: 2 } for sorting.',
        },
        {
            'title': 'Task statistics',
            'description': (
                'Write countTasksByStatus(tasks) to return an object with todo, doing, and done '
                'counts. Write getTaskSummary(tasks) to return a readable summary string.'
            ),
            'hint': 'Reduce over the tasks array and increment counters per status.',
        },
        {
            'title': 'Render a task card',
            'description': (
                'Write renderTaskCard(task) to return an HTML string for one task. Each card '
                'must use the class task-card and include the title, status badge, and priority.'
            ),
            'hint': (
                'Return markup like '
                '<article class="task-card">...</article> with nested status/priority elements.'
            ),
        },
        {
            'title': 'Render the board layout',
            'description': (
                'Write renderTaskBoard(tasks) to return HTML for the full board. Include a '
                'wrapper with id task-board and three sections with classes board-column, one '
                'for each status: todo, doing, and done.'
            ),
            'hint': 'Group tasks by status and render each column with renderTaskCard.',
        },
        {
            'title': 'Board stylesheet',
            'description': (
                'Write getBoardStyles() to return a CSS string. Style #task-board with flexbox, '
                'add .board-column rules, and style .task-card with spacing, borders, and '
                'priority classes (.priority-high, .priority-medium, .priority-low).'
            ),
            'hint': 'Return a template string containing all required selectors and properties.',
        },
        {
            'title': 'Priority labels',
            'description': (
                'Write formatPriorityLabel(priority) to return a human-readable label for each '
                'priority value.'
            ),
            'hint': 'Map high → "High Priority", medium → "Medium Priority", low → "Low Priority".',
        },
        {
            'title': 'Page integration',
            'description': (
                'In index.html, link style.css and script.js, add a root container with id app, '
                'and use your render functions to display the board. Apply styles from '
                'getBoardStyles() or move them into style.css.'
            ),
            'hint': 'Keep a full HTML document and inject the rendered board into #app.',
        },
    ],
}

TASK_BOARD_TESTS = [
    {
        'name': '1. createTask returns a task object',
        'story_index': 1,
        'description': 'createTask should return an object with id, title, status, and priority.',
        'test_code': (
            'const task = createTask(1, "Fix navbar", "todo", "high");\n'
            'if (!task || task.id !== 1 || task.title !== "Fix navbar") throw new Error("task");\n'
            'if (task.status !== "todo" || task.priority !== "high") throw new Error("fields");'
        ),
        'success_message': 'createTask returns the expected task shape.',
        'failure_message': 'Return an object with id, title, status, and priority.',
    },
    {
        'name': '2. createTask validates status',
        'story_index': 1,
        'description': 'createTask should reject invalid status values.',
        'test_code': (
            'let failed = false;\n'
            'try { createTask(2, "Bad", "invalid", "low"); } catch (e) { failed = true; }\n'
            'if (!failed) throw new Error("status");'
        ),
        'success_message': 'createTask validates status correctly.',
        'failure_message': 'Throw an error when status is not todo, doing, or done.',
    },
    {
        'name': '3. createTask validates priority',
        'story_index': 1,
        'description': 'createTask should reject invalid priority values.',
        'test_code': (
            'let failed = false;\n'
            'try { createTask(3, "Bad", "todo", "urgent"); } catch (e) { failed = true; }\n'
            'if (!failed) throw new Error("priority");'
        ),
        'success_message': 'createTask validates priority correctly.',
        'failure_message': 'Throw an error when priority is not high, medium, or low.',
    },
    {
        'name': '4. sortTasksByPriority orders tasks',
        'story_index': 2,
        'description': 'sortTasksByPriority should order high before medium before low.',
        'test_code': (
            'const tasks = [\n'
            '  createTask(1, "A", "todo", "low"),\n'
            '  createTask(2, "B", "todo", "high"),\n'
            '  createTask(3, "C", "todo", "medium"),\n'
            '];\n'
            'const sorted = sortTasksByPriority(tasks);\n'
            'if (sorted[0].priority !== "high" || sorted[2].priority !== "low") '
            'throw new Error("order");'
        ),
        'success_message': 'Tasks are sorted by priority.',
        'failure_message': 'Sort tasks in high → medium → low order.',
    },
    {
        'name': '5. filterTasksByStatus filters tasks',
        'story_index': 2,
        'description': 'filterTasksByStatus should return only matching tasks.',
        'test_code': (
            'const tasks = [\n'
            '  createTask(1, "A", "todo", "low"),\n'
            '  createTask(2, "B", "done", "high"),\n'
            '  createTask(3, "C", "todo", "medium"),\n'
            '];\n'
            'const filtered = filterTasksByStatus(tasks, "todo");\n'
            'if (filtered.length !== 2 || filtered.some((t) => t.status !== "todo")) '
            'throw new Error("filter");'
        ),
        'success_message': 'filterTasksByStatus works correctly.',
        'failure_message': 'Return only tasks that match the requested status.',
    },
    {
        'name': '6. countTasksByStatus counts tasks',
        'story_index': 3,
        'description': 'countTasksByStatus should return todo, doing, and done counts.',
        'test_code': (
            'const tasks = [\n'
            '  createTask(1, "A", "todo", "low"),\n'
            '  createTask(2, "B", "doing", "high"),\n'
            '  createTask(3, "C", "done", "medium"),\n'
            '  createTask(4, "D", "todo", "low"),\n'
            '];\n'
            'const counts = countTasksByStatus(tasks);\n'
            'if (counts.todo !== 2 || counts.doing !== 1 || counts.done !== 1) '
            'throw new Error("counts");'
        ),
        'success_message': 'Task counts are correct.',
        'failure_message': 'Return an object with accurate todo, doing, and done counts.',
    },
    {
        'name': '7. renderTaskCard includes task-card',
        'story_index': 4,
        'description': 'renderTaskCard should return markup containing the task-card class.',
        'test_code': (
            'const markup = renderTaskCard(createTask(1, "Ship feature", "doing", "high"));\n'
            'if (!markup.includes("task-card")) throw new Error("card");'
        ),
        'success_message': 'renderTaskCard includes task-card.',
        'failure_message': 'Use the task-card class in your card markup.',
    },
    {
        'name': '8. renderTaskCard shows title and priority',
        'story_index': 4,
        'description': 'renderTaskCard should include the task title and priority.',
        'test_code': (
            'const markup = renderTaskCard(createTask(2, "Write tests", "todo", "medium"));\n'
            'if (!markup.includes("Write tests") || !markup.includes("medium")) '
            'throw new Error("content");'
        ),
        'success_message': 'renderTaskCard shows title and priority.',
        'failure_message': 'Display the task title and priority in each card.',
    },
    {
        'name': '9. renderTaskCard shows status badge',
        'story_index': 4,
        'description': 'renderTaskCard should include a status badge for the task.',
        'test_code': (
            'const markup = renderTaskCard(createTask(3, "Review PR", "done", "low"));\n'
            'if (!markup.includes("status-badge") || !markup.includes("done")) '
            'throw new Error("badge");'
        ),
        'success_message': 'renderTaskCard includes a status badge.',
        'failure_message': 'Add a status-badge element that shows the task status.',
    },
    {
        'name': '10. renderTaskBoard has task-board wrapper',
        'story_index': 5,
        'description': 'renderTaskBoard should return markup with id task-board.',
        'test_code': (
            'const tasks = [createTask(1, "A", "todo", "high")];\n'
            'const board = renderTaskBoard(tasks);\n'
            'if (!board.includes(\'id="task-board"\') && !board.includes("id=\'task-board\'")) '
            'throw new Error("board");'
        ),
        'success_message': 'renderTaskBoard includes #task-board.',
        'failure_message': 'Wrap the board in an element with id="task-board".',
    },
    {
        'name': '11. renderTaskBoard has three columns',
        'story_index': 5,
        'description': 'renderTaskBoard should include todo, doing, and done columns.',
        'test_code': (
            'const tasks = [createTask(1, "A", "todo", "low")];\n'
            'const board = renderTaskBoard(tasks);\n'
            'if (!board.includes("board-column")) throw new Error("columns");\n'
            'if (!board.includes("todo") || !board.includes("doing") || !board.includes("done")) '
            'throw new Error("status-columns");'
        ),
        'success_message': 'renderTaskBoard renders all three columns.',
        'failure_message': 'Add board-column sections for todo, doing, and done.',
    },
    {
        'name': '12. renderTaskBoard renders multiple cards',
        'story_index': 5,
        'description': 'renderTaskBoard should render a card for each task.',
        'test_code': (
            'const tasks = [\n'
            '  createTask(1, "A", "todo", "high"),\n'
            '  createTask(2, "B", "done", "low"),\n'
            '];\n'
            'const board = renderTaskBoard(tasks);\n'
            'if ((board.match(/task-card/g) || []).length < 2) throw new Error("cards");'
        ),
        'success_message': 'renderTaskBoard renders all task cards.',
        'failure_message': 'Render every task as a task-card inside the board.',
    },
    {
        'name': '13. getBoardStyles uses flex layout',
        'story_index': 6,
        'description': 'getBoardStyles should style the board with flexbox.',
        'test_code': (
            'const styles = getBoardStyles();\n'
            'if (!styles.includes("#task-board") || !styles.includes("display") '
            '|| !styles.includes("flex")) throw new Error("flex");'
        ),
        'success_message': 'getBoardStyles includes flex layout for the board.',
        'failure_message': 'Style #task-board with a flex display.',
    },
    {
        'name': '14. getBoardStyles styles task cards',
        'story_index': 6,
        'description': 'getBoardStyles should include .task-card rules.',
        'test_code': (
            'const styles = getBoardStyles();\n'
            'if (!styles.includes(".task-card")) throw new Error("card-style");'
        ),
        'success_message': 'getBoardStyles includes .task-card rules.',
        'failure_message': 'Add CSS rules for .task-card in getBoardStyles.',
    },
    {
        'name': '15. getBoardStyles includes priority classes',
        'story_index': 6,
        'description': 'getBoardStyles should style high, medium, and low priorities.',
        'test_code': (
            'const styles = getBoardStyles();\n'
            'if (!styles.includes(".priority-high") || !styles.includes(".priority-medium") '
            '|| !styles.includes(".priority-low")) throw new Error("priority");'
        ),
        'success_message': 'Priority classes are styled.',
        'failure_message': 'Add .priority-high, .priority-medium, and .priority-low rules.',
    },
    {
        'name': '16. formatPriorityLabel returns readable text',
        'story_index': 7,
        'description': 'formatPriorityLabel should return a readable label.',
        'test_code': (
            'const label = formatPriorityLabel("high");\n'
            'if (!label || label.length < 3 || !/high/i.test(label)) throw new Error("label");'
        ),
        'success_message': 'formatPriorityLabel returns readable text.',
        'failure_message': 'Return a readable label for each priority value.',
    },
    {
        'name': '17. getTaskSummary returns summary text',
        'story_index': 3,
        'description': 'getTaskSummary should return a non-empty summary string.',
        'test_code': (
            'const tasks = [\n'
            '  createTask(1, "A", "todo", "low"),\n'
            '  createTask(2, "B", "done", "high"),\n'
            '];\n'
            'const summary = getTaskSummary(tasks);\n'
            'if (!summary || summary.length < 5) throw new Error("summary");'
        ),
        'success_message': 'getTaskSummary returns a useful summary.',
        'failure_message': 'Return a readable summary string for the current tasks.',
    },
]
