from .prompts import SYSTEM_PROMPT


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
        files_block = self._format_files(files)
        test_results_block = self._format_test_results(
            test_summary=test_summary,
            failed_tests=failed_tests,
            test_error=test_error,
        )
        failed_count = self._failed_count(test_summary)

        prompt = (
            f'{SYSTEM_PROMPT}\n\n'
            f'=== سياق المشروع ===\n'
            f'العنوان: {title or "غير محدد"}\n\n'
            f'الوصف:\n{description or "غير محدد"}\n\n'
            f'أهداف التعلم / المتطلبات:\n{objectives or "غير محدد"}\n\n'
            f'لغة المشروع: {language or "غير محدد"}\n\n'
            f'=== ملفات مساحة عمل الطالب ===\n'
            f'{files_block}\n'
        )

        if test_results_block:
            prompt += (
                f'\n=== Test Results ===\n'
                f'{test_results_block}\n'
            )

            if failed_count > 0:
                prompt += (
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
                prompt += (
                    '\nاستخدم نتائج الاختبارات لفهم وضع حل الطالب، '
                    'مع الاستمرار في عدم تقديم أي كود أو حل نهائي أو إعادة كتابة التنفيذ.\n'
                )

        return prompt

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

            sections.append(
                f'--- ملف {index}: {name} ---\n'
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

    def _format_test_results(self, test_summary=None, failed_tests=None, test_error=None):
        lines = []

        if test_summary:
            total = self._field(test_summary, 'total', 0) or 0
            passed = self._field(test_summary, 'passed', 0) or 0
            failed = self._field(test_summary, 'failed', 0) or 0
            lines.append(f'Passed tests count: {passed}')
            lines.append(f'Failed tests count: {failed}')
            lines.append(f'Total tests: {total}')

        failed_tests = failed_tests or []
        if failed_tests:
            lines.append('Failed tests / requirements:')
            for index, item in enumerate(failed_tests, start=1):
                test_id = self._field(item, 'id', None)
                name = (self._field(item, 'name', '') or '').strip()
                requirement = (self._field(item, 'requirement', '') or '').strip()
                message = (self._field(item, 'message', '') or '').strip()
                error = (self._field(item, 'error', '') or '').strip()
                stderr = (self._field(item, 'stderr', '') or '').strip()

                label = f'  {index}.'
                if test_id is not None:
                    label += f' [id={test_id}]'
                if name:
                    label += f' {name}'

                details = []
                if requirement:
                    details.append(f'requirement: {requirement}')
                if message:
                    details.append(f'message: {message}')
                if error:
                    details.append(f'error: {error}')
                if stderr:
                    details.append(f'stderr: {stderr}')

                lines.append(
                    f'{label} {" | ".join(details) if details else "(no message)"}'
                )

        runtime_error = (test_error or '').strip()
        if runtime_error:
            lines.append(f'Runtime / execution error: {runtime_error}')

        return '\n'.join(lines).strip()
