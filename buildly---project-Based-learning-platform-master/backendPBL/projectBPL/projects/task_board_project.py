"""Task Board advanced project for Frontend Mastery."""

TASK_BOARD_TITLE = 'Build a Task Board with Vanilla JavaScript'
TASK_BOARD_LEGACY_TITLES = (
    'Build a Task Board with Vanilla JavaScript',
    '[Buildly] لوحة مهام بـ JavaScript',
)

TASK_BOARD_PROJECT = {
    'title': TASK_BOARD_TITLE,
    'level': 'advanced',
    'languages': ['javascript', 'html', 'css'],
    'estimated_time': 6,
    'description': (
        'ابنِ لوحة مهام بأسلوب كانبان باستخدام HTML و CSS و JavaScript فقط. '
        'أنشئ دوال بيانات المهام، واعرض تخطيطاً متجاوباً، ونسّق البطاقات حسب الحالة والأولوية. '
        'أضف أسلوبك البصري مع الحفاظ على البنية والسلوك المطلوبين.'
    ),
    'objectives': (
        'ابنِ لوحة مهام كاملة بمنطق JavaScript ووسوم دلالية وCSS مخصص.'
    ),
    'stories': [
        {
            'title': 'نموذج المهمة',
            'description': (
                'في script.js اكتب دالة createTask(id, title, status, priority) تُرجع كائناً '
                'يحوي id و title و status و priority. الحالة يجب أن تكون واحدةً من: '
                'todo أو doing أو done. والأولوية واحدةً من: high أو medium أو low.'
            ),
            'hint': 'أرجع { id, title, status, priority } وتحقق من القيم المسموحة.',
        },
        {
            'title': 'ترتيب وتصفية المهام',
            'description': (
                'اكتب sortTasksByPriority(tasks) لترتيب المهام high ← medium ← low، و '
                'filterTasksByStatus(tasks, status) لإرجاع المهام ذات الحالة المطلوبة فقط.'
            ),
            'hint': 'استخدم خريطة أولوية مثل { high: 0, medium: 1, low: 2 } للترتيب.',
        },
        {
            'title': 'إحصائيات المهام',
            'description': (
                'اكتب countTasksByStatus(tasks) لتُرجع كائناً بعدّادات todo و doing و done. '
                'واكتب getTaskSummary(tasks) لتُرجع نص ملخص مقروء.'
            ),
            'hint': 'مرّ على المصفوفة وزد العدّادات حسب الحالة.',
        },
        {
            'title': 'عرض بطاقة مهمة',
            'description': (
                'اكتب renderTaskCard(task) لتُرجع نص HTML لمهمة واحدة. كل بطاقة يجب أن تستخدم '
                'الصنف task-card وتشمل العنوان وشارة الحالة والأولوية.'
            ),
            'hint': (
                'أرجع HTML مثل '
                '<article class="task-card">...</article> مع عناصر الحالة/الأولوية.'
            ),
        },
        {
            'title': 'عرض تخطيط اللوحة',
            'description': (
                'اكتب renderTaskBoard(tasks) لتُرجع HTML للوحة كاملة. أدرج غلافاً بمعرّف '
                'task-board وثلاثة أقسام بالصنف board-column لكل حالة: todo و doing و done.'
            ),
            'hint': 'جمّع المهام حسب الحالة واعرض كل عمود باستخدام renderTaskCard.',
        },
        {
            'title': 'ملف تنسيق اللوحة',
            'description': (
                'اكتب getBoardStyles() لتُرجع نص CSS. نسّق #task-board بـ flexbox، '
                'وأضف قواعد .board-column، ونسّق .task-card مع أصناف الأولوية '
                '(.priority-high و .priority-medium و .priority-low).'
            ),
            'hint': 'أرجع template string يحوي كل المحدّدات والخصائص المطلوبة.',
        },
        {
            'title': 'تسميات الأولوية',
            'description': (
                'اكتب formatPriorityLabel(priority) لتُرجع تسمية مقروءة لكل قيمة أولوية.'
            ),
            'hint': 'اربط high → "High Priority" و medium → "Medium Priority" و low → "Low Priority".',
        },
        {
            'title': 'دمج الصفحة',
            'description': (
                'في index.html اربط style.css و script.js، وأضف حاوية جذر بمعرّف app، '
                'واستخدم دوال العرض لعرض اللوحة. طبّق أنماط getBoardStyles() أو انقلها إلى style.css.'
            ),
            'hint': 'احتفظ بمستند HTML كامل واحقن اللوحة المعروضة داخل #app.',
        },
    ],
}

TASK_BOARD_TESTS = [
    {
        'name': '1. createTask تُرجع كائن مهمة',
        'story_index': 1,
        'description': 'createTask يجب أن تُرجع كائناً يحوي id و title و status و priority.',
        'test_code': (
            'const task = createTask(1, "Fix navbar", "todo", "high");\n'
            'if (!task || task.id !== 1 || task.title !== "Fix navbar") throw new Error("task");\n'
            'if (task.status !== "todo" || task.priority !== "high") throw new Error("fields");'
        ),
        'success_message': 'createTask تُرجع شكل المهمة المتوقع.',
        'failure_message': 'أرجع كائناً يحوي id و title و status و priority.',
    },
    {
        'name': '2. createTask تتحقق من الحالة',
        'story_index': 1,
        'description': 'createTask يجب أن ترفض قيم الحالة غير الصالحة.',
        'test_code': (
            'let failed = false;\n'
            'try { createTask(2, "Bad", "invalid", "low"); } catch (e) { failed = true; }\n'
            'if (!failed) throw new Error("status");'
        ),
        'success_message': 'createTask تتحقق من الحالة بشكل صحيح.',
        'failure_message': 'ارمِ خطأ عندما لا تكون الحالة todo أو doing أو done.',
    },
    {
        'name': '3. createTask تتحقق من الأولوية',
        'story_index': 1,
        'description': 'createTask يجب أن ترفض قيم الأولوية غير الصالحة.',
        'test_code': (
            'let failed = false;\n'
            'try { createTask(3, "Bad", "todo", "urgent"); } catch (e) { failed = true; }\n'
            'if (!failed) throw new Error("priority");'
        ),
        'success_message': 'createTask تتحقق من الأولوية بشكل صحيح.',
        'failure_message': 'ارمِ خطأ عندما لا تكون الأولوية high أو medium أو low.',
    },
    {
        'name': '4. sortTasksByPriority ترتّب المهام',
        'story_index': 2,
        'description': 'sortTasksByPriority يجب أن ترتّب high قبل medium قبل low.',
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
        'success_message': 'المهام مرتّبة حسب الأولوية.',
        'failure_message': 'رتّب المهام بالترتيب high ← medium ← low.',
    },
    {
        'name': '5. filterTasksByStatus تصفّي المهام',
        'story_index': 2,
        'description': 'filterTasksByStatus يجب أن تُرجع المهام المطابقة فقط.',
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
        'success_message': 'filterTasksByStatus تعمل بشكل صحيح.',
        'failure_message': 'أرجع فقط المهام ذات الحالة المطلوبة.',
    },
    {
        'name': '6. countTasksByStatus تعدّ المهام',
        'story_index': 3,
        'description': 'countTasksByStatus يجب أن تُرجع عدّادات todo و doing و done.',
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
        'success_message': 'عدّادات المهام صحيحة.',
        'failure_message': 'أرجع كائناً بعدّادات todo و doing و done الدقيقة.',
    },
    {
        'name': '7. renderTaskCard تتضمن task-card',
        'story_index': 4,
        'description': 'renderTaskCard يجب أن تُرجع HTML يحوي الصنف task-card.',
        'test_code': (
            'const markup = renderTaskCard(createTask(1, "Ship feature", "doing", "high"));\n'
            'if (!markup.includes("task-card")) throw new Error("card");'
        ),
        'success_message': 'renderTaskCard تتضمن task-card.',
        'failure_message': 'استخدم الصنف task-card في HTML البطاقة.',
    },
    {
        'name': '8. renderTaskCard تعرض العنوان والأولوية',
        'story_index': 4,
        'description': 'renderTaskCard يجب أن تشمل عنوان المهمة والأولوية.',
        'test_code': (
            'const markup = renderTaskCard(createTask(2, "Write tests", "todo", "medium"));\n'
            'if (!markup.includes("Write tests") || !markup.includes("medium")) '
            'throw new Error("content");'
        ),
        'success_message': 'renderTaskCard تعرض العنوان والأولوية.',
        'failure_message': 'اعرض عنوان المهمة والأولوية في كل بطاقة.',
    },
    {
        'name': '9. renderTaskCard تعرض شارة الحالة',
        'story_index': 4,
        'description': 'renderTaskCard يجب أن تشمل شارة حالة للمهمة.',
        'test_code': (
            'const markup = renderTaskCard(createTask(3, "Review PR", "done", "low"));\n'
            'if (!markup.includes("status-badge") || !markup.includes("done")) '
            'throw new Error("badge");'
        ),
        'success_message': 'renderTaskCard تتضمن شارة حالة.',
        'failure_message': 'أضف عنصراً بالصنف status-badge يعرض حالة المهمة.',
    },
    {
        'name': '10. renderTaskBoard لها غلاف task-board',
        'story_index': 5,
        'description': 'renderTaskBoard يجب أن تُرجع HTML بمعرّف task-board.',
        'test_code': (
            'const tasks = [createTask(1, "A", "todo", "high")];\n'
            'const board = renderTaskBoard(tasks);\n'
            'if (!board.includes(\'id="task-board"\') && !board.includes("id=\'task-board\'")) '
            'throw new Error("board");'
        ),
        'success_message': 'renderTaskBoard تتضمن #task-board.',
        'failure_message': 'غلّف اللوحة بعنصر id="task-board".',
    },
    {
        'name': '11. renderTaskBoard لها ثلاثة أعمدة',
        'story_index': 5,
        'description': 'renderTaskBoard يجب أن تشمل أعمدة todo و doing و done.',
        'test_code': (
            'const tasks = [createTask(1, "A", "todo", "low")];\n'
            'const board = renderTaskBoard(tasks);\n'
            'if (!board.includes("board-column")) throw new Error("columns");\n'
            'if (!board.includes("todo") || !board.includes("doing") || !board.includes("done")) '
            'throw new Error("status-columns");'
        ),
        'success_message': 'renderTaskBoard تعرض الأعمدة الثلاثة.',
        'failure_message': 'أضف أقسام board-column لـ todo و doing و done.',
    },
    {
        'name': '12. renderTaskBoard تعرض عدة بطاقات',
        'story_index': 5,
        'description': 'renderTaskBoard يجب أن تعرض بطاقة لكل مهمة.',
        'test_code': (
            'const tasks = [\n'
            '  createTask(1, "A", "todo", "high"),\n'
            '  createTask(2, "B", "done", "low"),\n'
            '];\n'
            'const board = renderTaskBoard(tasks);\n'
            'if ((board.match(/task-card/g) || []).length < 2) throw new Error("cards");'
        ),
        'success_message': 'renderTaskBoard تعرض كل بطاقات المهام.',
        'failure_message': 'اعرض كل مهمة كبطاقة task-card داخل اللوحة.',
    },
    {
        'name': '13. getBoardStyles تستخدم تخطيط flex',
        'story_index': 6,
        'description': 'getBoardStyles يجب أن تنسّق اللوحة بـ flexbox.',
        'test_code': (
            'const styles = getBoardStyles();\n'
            'if (!styles.includes("#task-board") || !styles.includes("display") '
            '|| !styles.includes("flex")) throw new Error("flex");'
        ),
        'success_message': 'getBoardStyles تتضمن تخطيط flex للوحة.',
        'failure_message': 'نسّق #task-board بـ display: flex.',
    },
    {
        'name': '14. getBoardStyles تنسّق بطاقات المهام',
        'story_index': 6,
        'description': 'getBoardStyles يجب أن تشمل قواعد .task-card.',
        'test_code': (
            'const styles = getBoardStyles();\n'
            'if (!styles.includes(".task-card")) throw new Error("card-style");'
        ),
        'success_message': 'getBoardStyles تتضمن قواعد .task-card.',
        'failure_message': 'أضف قواعد CSS لـ .task-card في getBoardStyles.',
    },
    {
        'name': '15. getBoardStyles تتضمن أصناف الأولوية',
        'story_index': 6,
        'description': 'getBoardStyles يجب أن تنسّق أولويات high و medium و low.',
        'test_code': (
            'const styles = getBoardStyles();\n'
            'if (!styles.includes(".priority-high") || !styles.includes(".priority-medium") '
            '|| !styles.includes(".priority-low")) throw new Error("priority");'
        ),
        'success_message': 'أصناف الأولوية منسّقة.',
        'failure_message': 'أضف قواعد .priority-high و .priority-medium و .priority-low.',
    },
    {
        'name': '16. formatPriorityLabel تُرجع نصاً مقروءاً',
        'story_index': 7,
        'description': 'formatPriorityLabel يجب أن تُرجع تسمية مقروءة.',
        'test_code': (
            'const label = formatPriorityLabel("high");\n'
            'if (!label || label.length < 3 || !/high/i.test(label)) throw new Error("label");'
        ),
        'success_message': 'formatPriorityLabel تُرجع نصاً مقروءاً.',
        'failure_message': 'أرجع تسمية مقروءة لكل قيمة أولوية.',
    },
    {
        'name': '17. getTaskSummary تُرجع نص ملخص',
        'story_index': 3,
        'description': 'getTaskSummary يجب أن تُرجع نص ملخص غير فارغ.',
        'test_code': (
            'const tasks = [\n'
            '  createTask(1, "A", "todo", "low"),\n'
            '  createTask(2, "B", "done", "high"),\n'
            '];\n'
            'const summary = getTaskSummary(tasks);\n'
            'if (!summary || summary.length < 5) throw new Error("summary");'
        ),
        'success_message': 'getTaskSummary تُرجع ملخصاً مفيداً.',
        'failure_message': 'أرجع نص ملخص مقروء للمهام الحالية.',
    },
]
