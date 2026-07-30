from pathlib import Path

from .prompts import SYSTEM_PROMPT

# Keep stderr/error snippets short so the model focuses on signal, not noise.
_STDERR_MAX_CHARS = 500
_STORY_LIMIT = 40
_TEST_CATALOG_LIMIT = 80


class PromptBuilder:
    """Compose the final AI review prompt from project context and student files."""

    def build(
        self,
        project,
        files,
        test_summary=None,
        failed_tests=None,
        test_error=None,
    ):
        title = (getattr(project, 'title', None) or '').strip()
        description = (getattr(project, 'description', None) or '').strip()
        objectives = (getattr(project, 'objectives', None) or '').strip()
        language = self._format_language(project)
        stories_block = self._format_user_stories(project)
        tests_catalog_block = self._format_project_tests_catalog(project)
        ideas_block = self._format_ideas_to_test(project)
        files_block = self._format_files(files)
        test_results_block = self._format_test_results(
            test_summary=test_summary,
            failed_tests=failed_tests,
            test_error=test_error,
        )
        failed_count = self._failed_count(test_summary)

        user_prompt = (
            f'=== سياق المشروع ===\n'
            f'العنوان: {title or "غير محدد"}\n\n'
            f'الوصف:\n{description or "غير محدد"}\n\n'
            f'أهداف التعلم / المتطلبات:\n{objectives or "غير محدد"}\n\n'
            f'لغة / لغات المشروع: {language or "غير محدد"}\n\n'
            f'=== قصص المستخدم (متطلبات المشروع) ===\n'
            f'{stories_block}\n\n'
            f'=== كتالوج اختبارات المشروع ===\n'
            f'{tests_catalog_block}\n'
        )

        if ideas_block:
            user_prompt += f'\n=== أفكار / نقاط تحقق إضافية ===\n{ideas_block}\n'

        user_prompt += (
            f'\n=== ملفات مساحة عمل الطالب ===\n'
            f'{files_block}\n'
            f'\n=== إرشاد ربط المشكلات بالملفات ===\n'
            f'- عند ذكر مشكلة، اجعل حقل file مطابقاً لاسم ملف موجود أعلاه قدر الإمكان.\n'
            f'- اجعل line رقماً تقريبياً داخل ذلك الملف (1-based) عند وجود موضع منطقي.\n'
            f'- إذا ارتبطت المشكلة باختبار فاشل، اذكر اسم الاختبار في title أو explanation.\n'
        )

        if test_results_block:
            user_prompt += (
                f'\n=== نتائج Check Code ===\n'
                f'{test_results_block}\n'
            )

            if failed_count > 0:
                user_prompt += (
                    '\n=== قواعد إلزامية عند فشل الاختبارات ===\n'
                    '- نتائج الاختبارات الفاشلة هي مصدر الحقيقة لحالة إكمال المشروع.\n'
                    '- يجب ذكر المتطلبات/قصص المستخدم الفاشلة في issues.\n'
                    '- issues يجب ألا تكون فارغة.\n'
                    '- ممنوع عبارات النجاح مثل "عمل ممتاز" أو "لا توجد مشكلات مهمة".\n'
                    '- overall_score يجب أن يكون 45 أو أقل.\n'
                    '- اشرح الخلل المنطقي فقط.\n'
                    '- لا تقدّم أي كود أو حل نهائي أو إعادة كتابة للتنفيذ.\n'
                )
            else:
                user_prompt += (
                    '\nاستخدم نتائج الاختبارات لفهم وضع حل الطالب، '
                    'مع الاستمرار في عدم تقديم أي كود أو حل نهائي أو إعادة كتابة التنفيذ.\n'
                )

        return {
            'system': SYSTEM_PROMPT,
            'user': user_prompt.strip(),
        }

    def _format_language(self, project):
        if hasattr(project, 'get_languages_display_list'):
            languages = project.get_languages_display_list()
            if languages:
                return ', '.join(languages)

        if hasattr(project, 'get_languages_list'):
            languages = project.get_languages_list()
            if languages:
                return ', '.join(languages)

        return (getattr(project, 'language', None) or '').strip()

    def _format_user_stories(self, project):
        tasks_manager = getattr(project, 'tasks', None)
        if tasks_manager is None:
            return 'لا توجد قصص مستخدم مسجّلة في قاعدة البيانات.'

        try:
            tasks = list(tasks_manager.all().order_by('order', 'id')[:_STORY_LIMIT])
        except Exception:
            return 'تعذّر تحميل قصص المستخدم.'

        if not tasks:
            return 'لا توجد قصص مستخدم مسجّلة لهذا المشروع.'

        lines = []
        for index, task in enumerate(tasks, start=1):
            title = (getattr(task, 'title', None) or '').strip() or f'قصة {index}'
            description = (getattr(task, 'description', None) or '').strip()
            task_type = (getattr(task, 'task_type', None) or '').strip()
            order = getattr(task, 'order', index)
            line = f'{index}. [order={order}] {title}'
            if task_type:
                line += f' (نوع: {task_type})'
            if description:
                line += f'\n   {description}'
            lines.append(line)

        return '\n'.join(lines)

    def _format_project_tests_catalog(self, project):
        tests_manager = getattr(project, 'tests', None)
        if tests_manager is None:
            return 'لا يوجد كتالوج اختبارات مسجّل.'

        try:
            tests = list(
                tests_manager.select_related('task').all().order_by('id')[:_TEST_CATALOG_LIMIT]
            )
        except Exception:
            try:
                tests = list(tests_manager.all().order_by('id')[:_TEST_CATALOG_LIMIT])
            except Exception:
                return 'تعذّر تحميل كتالوج الاختبارات.'

        if not tests:
            return 'لا توجد اختبارات معرّفة لهذا المشروع.'

        lines = []
        for index, test in enumerate(tests, start=1):
            name = (getattr(test, 'name', None) or '').strip() or f'اختبار {index}'
            description = (getattr(test, 'description', None) or '').strip()
            test_id = getattr(test, 'id', None)
            task = getattr(test, 'task', None)
            task_title = ''
            if task is not None:
                task_title = (getattr(task, 'title', None) or '').strip()

            line = f'{index}.'
            if test_id is not None:
                line += f' [id={test_id}]'
            line += f' {name}'
            if task_title:
                line += f' ← قصة: {task_title}'
            if description:
                line += f'\n   {description}'
            lines.append(line)

        return '\n'.join(lines)

    def _format_ideas_to_test(self, project):
        ideas = getattr(project, 'ideas_to_test', None) or []
        if not isinstance(ideas, list) or not ideas:
            return ''

        lines = []
        for index, idea in enumerate(ideas[:30], start=1):
            text = str(idea).strip()
            if text:
                lines.append(f'{index}. {text}')
        return '\n'.join(lines)

    def _detect_file_language(self, file_name):
        suffix = Path(str(file_name or '')).suffix.lower()
        mapping = {
            '.py': 'python',
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.js': 'javascript',
            '.mjs': 'javascript',
            '.cjs': 'javascript',
            '.jsx': 'react/javascript',
            '.ts': 'typescript',
            '.tsx': 'react/typescript',
            '.json': 'json',
            '.md': 'markdown',
            '.txt': 'text',
        }
        return mapping.get(suffix, 'unknown')

    def _format_files(self, files):
        if not files:
            return 'لا توجد ملفات مرسلة.'

        sections = []
        for index, file_data in enumerate(files, start=1):
            if isinstance(file_data, dict):
                name = (file_data.get('name') or f'file_{index}').strip()
                content = file_data.get('content', '')
            else:
                name = (getattr(file_data, 'name', None) or f'file_{index}').strip()
                content = getattr(file_data, 'content', '')

            if content is None:
                content = ''

            language = self._detect_file_language(name)
            line_count = str(content).count('\n') + (1 if str(content) else 0)

            sections.append(
                f'--- ملف {index}: {name} | اللغة: {language} | أسطر تقريباً: {line_count} ---\n'
                f'{content}'
            )

        return '\n\n'.join(sections)

    def _field(self, item, key, default=None):
        if isinstance(item, dict) or hasattr(item, 'get'):
            return item.get(key, default)
        return getattr(item, key, default)

    def _failed_count(self, test_summary):
        if not test_summary:
            return 0
        return int(self._field(test_summary, 'failed', 0) or 0)

    def _clip(self, text, max_chars=_STDERR_MAX_CHARS):
        cleaned = (text or '').strip()
        if len(cleaned) <= max_chars:
            return cleaned
        return cleaned[: max_chars - 1].rstrip() + '…'

    def _format_test_results(self, test_summary=None, failed_tests=None, test_error=None):
        lines = []

        if test_summary:
            total = self._field(test_summary, 'total', 0) or 0
            passed = self._field(test_summary, 'passed', 0) or 0
            failed = self._field(test_summary, 'failed', 0) or 0
            lines.append(f'عدد الناجح: {passed}')
            lines.append(f'عدد الفاشل: {failed}')
            lines.append(f'الإجمالي: {total}')

        failed_tests = failed_tests or []
        if failed_tests:
            lines.append('تفاصيل الاختبارات/المتطلبات الفاشلة:')
            for index, item in enumerate(failed_tests, start=1):
                test_id = self._field(item, 'id', None)
                name = (self._field(item, 'name', '') or '').strip()
                requirement = (self._field(item, 'requirement', '') or '').strip()
                message = (self._field(item, 'message', '') or '').strip()
                error = self._clip(self._field(item, 'error', '') or '')
                stderr = self._clip(self._field(item, 'stderr', '') or '')

                label = f'  {index}.'
                if test_id is not None:
                    label += f' [id={test_id}]'
                if name:
                    label += f' {name}'

                details = []
                if requirement:
                    details.append(f'المتطلب: {requirement}')
                if message:
                    details.append(f'رسالة: {message}')
                if error:
                    details.append(f'error: {error}')
                if stderr:
                    details.append(f'stderr: {stderr}')

                lines.append(
                    f'{label} {" | ".join(details) if details else "(بدون تفاصيل)"}'
                )

        runtime_error = self._clip((test_error or '').strip(), max_chars=800)
        if runtime_error:
            lines.append(f'خطأ تشغيل / تنفيذ: {runtime_error}')

        return '\n'.join(lines).strip()
