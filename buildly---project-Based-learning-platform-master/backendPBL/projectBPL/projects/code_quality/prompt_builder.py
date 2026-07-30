from .prompts import QUALITY_SYSTEM_PROMPT


class CodeQualityPromptBuilder:
    """Compose the final code quality review prompt from project context and student files."""

    def build(self, project, files, test_summary=None):
        title = (getattr(project, 'title', None) or '').strip()
        description = (getattr(project, 'description', None) or '').strip()
        objectives = (getattr(project, 'objectives', None) or '').strip()
        language = self._format_language(project)
        files_block = self._format_files(files)
        test_results_block = self._format_test_summary(test_summary)

        user_prompt = (
            f'=== سياق المشروع ===\n'
            f'العنوان: {title or "غير محدد"}\n\n'
            f'الوصف:\n{description or "غير محدد"}\n\n'
            f'أهداف التعلم / المتطلبات:\n{objectives or "غير محدد"}\n\n'
            f'لغة المشروع: {language or "غير محدد"}\n\n'
            f'=== حالة الاختبارات ===\n'
            f'{test_results_block}\n\n'
            f'=== ملفات مساحة عمل الطالب ===\n'
            f'{files_block}\n\n'
            f'تذكير: الاختبارات نجحت. راجع جودة الكود فقط '
            f'(الكفاءة، التعقيد، النظافة، الأداء) دون تصحيح أخطاء أو إعادة كتابة الحل.\n'
        )

        return {
            'system': QUALITY_SYSTEM_PROMPT,
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

    def _format_test_summary(self, test_summary):
        if not test_summary:
            return (
                'حالة الاختبارات: نجح الطالب في التقييم التلقائي '
                '(لم تُرسل تفاصيل إضافية للملخص).'
            )

        if isinstance(test_summary, dict) or hasattr(test_summary, 'get'):
            getter = test_summary.get
        else:
            getter = lambda key, default=0: getattr(test_summary, key, default)

        total = int(getter('total', 0) or 0)
        passed = int(getter('passed', 0) or 0)
        failed = int(getter('failed', 0) or 0)

        return (
            f'النتائج: total={total}, passed={passed}, failed={failed}.\n'
            'جميع الاختبارات ناجحة؛ راجع جودة الكود فقط.'
        )
