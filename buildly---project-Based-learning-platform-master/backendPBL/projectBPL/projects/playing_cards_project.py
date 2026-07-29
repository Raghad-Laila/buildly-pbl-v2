"""Playing Cards project definition for Frontend Mastery."""

PLAYING_CARDS_TITLE = 'Build a Page of Playing Cards'
PLAYING_CARDS_LEGACY_TITLES = (
    'Build a Page of Playing Cards',
    '[Buildly] صفحة بطاقات لعب',
)

PLAYING_CARDS_PROJECT = {
    'title': PLAYING_CARDS_TITLE,
    'level': 'beginner',
    'languages': ['html', 'css'],
    'estimated_time': 4,
    'description': (
        'ابنِ تطبيقاً مشابهاً لمثال ملف البداية من ناحية الوظيفة. '
        'حاول ألا تنسخ المثال حرفياً، وأضف أسلوبك الشخصي في التصميم.'
    ),
    'objectives': (
        'نفّذ قصص المستخدم أدناه واجتز كل الاختبارات لإكمال المختبر.'
    ),
    'stories': [
        {
            'title': 'الحاوية الرئيسية',
            'description': (
                'يجب أن يكون لديك عنصر main بمعرّف playing-cards.'
            ),
            'hint': 'أضف <main id="playing-cards"> كحاوية لكل البطاقات.',
        },
        {
            'title': 'عناصر البطاقات',
            'description': (
                'داخل #playing-cards يجب أن يكون لديك ثلاثة عناصر div على الأقل، '
                'كل منها بالصنف card.'
            ),
            'hint': 'أضف ثلاثة أبناء مباشرين على الأقل: <div class="card"> داخل #playing-cards.',
        },
        {
            'title': 'بنية البطاقة',
            'description': (
                'داخل كل عنصر .card يجب أن يكون لديك بالضبط ثلاثة عناصر div كأبناء مباشرين: '
                'الأول بالصنف left، والثاني بالصنف middle، والثالث بالصنف right.'
            ),
            'hint': (
                'كل بطاقة تحتاج ثلاثة أبناء مباشرين: '
                '<div class="left"> و <div class="middle"> و <div class="right">.'
            ),
        },
        {
            'title': 'أبعاد البطاقة',
            'description': (
                'كل عنصر .card يجب أن يحدد له width و height في ملف CSS.'
            ),
            'hint': 'في ملف التنسيق أضف width و height لمحدّد .card.',
        },
        {
            'title': 'تخطيط صفحة البطاقات',
            'description': (
                'عنصر #playing-cards يجب أن يستخدم flexbox لتوسيط الأبناء، '
                'والسماح بالتفافهم، مع مسافة 20px بينهم.'
            ),
            'hint': (
                'على #playing-cards ضع: display: flex; justify-content: center; '
                'flex-wrap: wrap; و gap: 20px;.'
            ),
        },
        {
            'title': 'تخطيط flex للبطاقة',
            'description': (
                'عناصر .card يجب أن تستخدم flexbox مع justify-content: space-between '
                'لأبنائها.'
            ),
            'hint': 'على .card ضع display: flex; و justify-content: space-between;.',
        },
        {
            'title': 'محاذاة أقسام البطاقة',
            'description': (
                'عناصر .left تُحاذى للبداية، و .middle للوسط، و .right للنهاية.'
            ),
            'hint': (
                'استخدم align-self: flex-start على .left و align-self: center على .middle '
                'و align-self: flex-end على .right.'
            ),
        },
        {
            'title': 'تخطيط القسم الأوسط',
            'description': (
                'عناصر .middle يجب أن تستخدم flexbox باتجاه عمودي لتكديس المحتوى.'
            ),
            'hint': 'على .middle ضع display: flex; و flex-direction: column;.',
        },
    ],
}

PLAYING_CARDS_TESTS = [
    {
        'name': '1. وجود main#playing-cards',
        'story_index': 1,
        'description': 'يجب أن يكون لديك عنصر main بمعرّف playing-cards.',
        'test_code': (
            'const el = getEl("playing-cards");\n'
            'if (!el || el.tagName.toLowerCase() !== "main") throw new Error("playing-cards");'
        ),
        'success_message': 'عنصر main#playing-cards موجود.',
        'failure_message': 'أضف عنصراً <main id="playing-cards"> إلى الصفحة.',
    },
    {
        'name': '2. ثلاث بطاقات .card على الأقل',
        'story_index': 2,
        'description': (
            'داخل #playing-cards يجب أن يكون لديك ثلاثة عناصر div بالصنف card على الأقل.'
        ),
        'test_code': (
            'const container = getEl("playing-cards");\n'
            'if (!container) throw new Error("container");\n'
            'const cards = Array.from(container.children).filter((el) => '
            'el.classList.contains("card"));\n'
            'if (cards.length < 3) throw new Error("cards");'
        ),
        'success_message': 'يوجد ثلاث بطاقات .card على الأقل داخل #playing-cards.',
        'failure_message': 'أضف ثلاثة عناصر <div class="card"> على الأقل داخل #playing-cards.',
    },
    {
        'name': '3. .card لها width و height في CSS',
        'story_index': 4,
        'description': 'كل عنصر .card يجب أن يحدد له width و height في CSS.',
        'test_code': (
            'if (!cssHasDeclaration(".card", "width")) throw new Error("width");\n'
            'if (!cssHasDeclaration(".card", "height")) throw new Error("height");'
        ),
        'success_message': '.card لديها width و height في CSS.',
        'failure_message': 'أضف تصريحات width و height لمحدّد .card في CSS.',
    },
    {
        'name': '4. كل .card تحتوي 3 أبناء div',
        'story_index': 3,
        'description': 'كل عنصر .card يجب أن يحتوي بالضبط ثلاثة عناصر div كأبناء.',
        'test_code': (
            'const container = getEl("playing-cards");\n'
            'if (!container) throw new Error("container");\n'
            'const cards = Array.from(container.children).filter((el) => '
            'el.classList.contains("card"));\n'
            'if (cards.length < 3) throw new Error("cards");\n'
            'for (const card of cards) {\n'
            '  const divChildren = Array.from(card.children).filter((el) => '
            'el.tagName.toLowerCase() === "div");\n'
            '  if (divChildren.length !== 3) throw new Error("children");\n'
            '}'
        ),
        'success_message': 'كل بطاقة .card تحتوي ثلاثة أبناء div بالضبط.',
        'failure_message': 'كل .card يجب أن تحتوي بالضبط ثلاثة عناصر div أبناء مباشرين.',
    },
    {
        'name': '5. .left داخل كل .card',
        'story_index': 3,
        'description': 'داخل كل .card يجب أن يكون لديك div بالصنف left.',
        'test_code': (
            'const container = getEl("playing-cards");\n'
            'if (!container) throw new Error("container");\n'
            'const cards = Array.from(container.children).filter((el) => '
            'el.classList.contains("card"));\n'
            'if (cards.length < 3) throw new Error("cards");\n'
            'for (const card of cards) {\n'
            '  const left = Array.from(card.children).find((el) => '
            'el.classList.contains("left"));\n'
            '  if (!left || left.tagName.toLowerCase() !== "div") throw new Error("left");\n'
            '}'
        ),
        'success_message': 'كل بطاقة تحتوي قسماً .left.',
        'failure_message': 'أضف <div class="left"> داخل كل عنصر .card.',
    },
    {
        'name': '6. .middle داخل كل .card',
        'story_index': 3,
        'description': 'داخل كل .card يجب أن يكون لديك div بالصنف middle.',
        'test_code': (
            'const container = getEl("playing-cards");\n'
            'if (!container) throw new Error("container");\n'
            'const cards = Array.from(container.children).filter((el) => '
            'el.classList.contains("card"));\n'
            'if (cards.length < 3) throw new Error("cards");\n'
            'for (const card of cards) {\n'
            '  const middle = Array.from(card.children).find((el) => '
            'el.classList.contains("middle"));\n'
            '  if (!middle || middle.tagName.toLowerCase() !== "div") throw new Error("middle");\n'
            '}'
        ),
        'success_message': 'كل بطاقة تحتوي قسماً .middle.',
        'failure_message': 'أضف <div class="middle"> داخل كل عنصر .card.',
    },
    {
        'name': '7. .right داخل كل .card',
        'story_index': 3,
        'description': 'داخل كل .card يجب أن يكون لديك div بالصنف right.',
        'test_code': (
            'const container = getEl("playing-cards");\n'
            'if (!container) throw new Error("container");\n'
            'const cards = Array.from(container.children).filter((el) => '
            'el.classList.contains("card"));\n'
            'if (cards.length < 3) throw new Error("cards");\n'
            'for (const card of cards) {\n'
            '  const right = Array.from(card.children).find((el) => '
            'el.classList.contains("right"));\n'
            '  if (!right || right.tagName.toLowerCase() !== "div") throw new Error("right");\n'
            '}'
        ),
        'success_message': 'كل بطاقة تحتوي قسماً .right.',
        'failure_message': 'أضف <div class="right"> داخل كل عنصر .card.',
    },
    {
        'name': '8. #playing-cards بـ display flex',
        'story_index': 5,
        'description': 'محدّد #playing-cards يجب أن يضبط display إلى flex.',
        'test_code': (
            'if (!cssHasDeclaration("#playing-cards", "display", "flex")) '
            'throw new Error("display");'
        ),
        'success_message': '#playing-cards يستخدم display: flex.',
        'failure_message': 'اضبط display: flex على محدّد #playing-cards.',
    },
    {
        'name': '9. #playing-cards بـ justify-content center',
        'story_index': 5,
        'description': 'محدّد #playing-cards يجب أن يضبط justify-content إلى center.',
        'test_code': (
            'if (!cssHasDeclaration("#playing-cards", "justify-content", "center")) '
            'throw new Error("justify-content");'
        ),
        'success_message': '#playing-cards يستخدم justify-content: center.',
        'failure_message': 'اضبط justify-content: center على محدّد #playing-cards.',
    },
    {
        'name': '10. #playing-cards بـ flex-wrap wrap',
        'story_index': 5,
        'description': 'محدّد #playing-cards يجب أن يضبط flex-wrap إلى wrap.',
        'test_code': (
            'if (!cssHasDeclaration("#playing-cards", "flex-wrap", "wrap")) '
            'throw new Error("flex-wrap");'
        ),
        'success_message': '#playing-cards يستخدم flex-wrap: wrap.',
        'failure_message': 'اضبط flex-wrap: wrap على محدّد #playing-cards.',
    },
    {
        'name': '11. #playing-cards بـ gap 20px',
        'story_index': 5,
        'description': 'محدّد #playing-cards يجب أن يضبط gap إلى 20px.',
        'test_code': (
            'if (!cssHasDeclaration("#playing-cards", "gap", "20px")) '
            'throw new Error("gap");'
        ),
        'success_message': '#playing-cards يستخدم gap: 20px.',
        'failure_message': 'اضبط gap: 20px على محدّد #playing-cards.',
    },
    {
        'name': '12. .card بـ display flex',
        'story_index': 6,
        'description': 'محدّد .card يجب أن يضبط display إلى flex.',
        'test_code': (
            'if (!cssHasDeclaration(".card", "display", "flex")) '
            'throw new Error("display");'
        ),
        'success_message': '.card يستخدم display: flex.',
        'failure_message': 'اضبط display: flex على محدّد .card.',
    },
    {
        'name': '13. .card بـ justify-content space-between',
        'story_index': 6,
        'description': 'محدّد .card يجب أن يضبط justify-content إلى space-between.',
        'test_code': (
            'if (!cssHasDeclaration(".card", "justify-content", "space-between")) '
            'throw new Error("justify-content");'
        ),
        'success_message': '.card يستخدم justify-content: space-between.',
        'failure_message': 'اضبط justify-content: space-between على محدّد .card.',
    },
    {
        'name': '14. .left بـ align-self flex-start',
        'story_index': 7,
        'description': 'محدّد .left يجب أن يضبط align-self إلى flex-start.',
        'test_code': (
            'if (!cssHasDeclaration(".left", "align-self", "flex-start")) '
            'throw new Error("align-self");'
        ),
        'success_message': '.left يستخدم align-self: flex-start.',
        'failure_message': 'اضبط align-self: flex-start على محدّد .left.',
    },
    {
        'name': '15. .middle بـ align-self center',
        'story_index': 7,
        'description': 'محدّد .middle يجب أن يضبط align-self إلى center.',
        'test_code': (
            'if (!cssHasDeclaration(".middle", "align-self", "center")) '
            'throw new Error("align-self");'
        ),
        'success_message': '.middle يستخدم align-self: center.',
        'failure_message': 'اضبط align-self: center على محدّد .middle.',
    },
    {
        'name': '16. .right بـ align-self flex-end',
        'story_index': 7,
        'description': 'محدّد .right يجب أن يضبط align-self إلى flex-end.',
        'test_code': (
            'if (!cssHasDeclaration(".right", "align-self", "flex-end")) '
            'throw new Error("align-self");'
        ),
        'success_message': '.right يستخدم align-self: flex-end.',
        'failure_message': 'اضبط align-self: flex-end على محدّد .right.',
    },
    {
        'name': '17. .middle بـ display flex',
        'story_index': 8,
        'description': 'محدّد .middle يجب أن يضبط display إلى flex.',
        'test_code': (
            'if (!cssHasDeclaration(".middle", "display", "flex")) '
            'throw new Error("display");'
        ),
        'success_message': '.middle يستخدم display: flex.',
        'failure_message': 'اضبط display: flex على محدّد .middle.',
    },
    {
        'name': '18. .middle بـ flex-direction column',
        'story_index': 8,
        'description': 'محدّد .middle يجب أن يضبط flex-direction إلى column.',
        'test_code': (
            'if (!cssHasDeclaration(".middle", "flex-direction", "column")) '
            'throw new Error("flex-direction");'
        ),
        'success_message': '.middle يستخدم flex-direction: column.',
        'failure_message': 'اضبط flex-direction: column على محدّد .middle.',
    },
]
