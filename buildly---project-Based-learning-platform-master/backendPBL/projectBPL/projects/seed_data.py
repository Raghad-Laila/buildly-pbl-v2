SEED_PREFIX = '[Buildly] '

FRONTEND_COURSE_TITLE = 'Frontend Mastery'
PYTHON_COURSE_TITLE = 'Python'
PYTHON_COURSE_FALLBACK_TITLE = 'مسار تعلم Python'

FRONTEND_PROJECTS = [
    {
        'title': f'{SEED_PREFIX}HTML Welcome Page',
        'legacy_titles': (f'{SEED_PREFIX}صفحة ترحيب HTML',),
        'level': 'beginner',
        'languages': ['html', 'css'],
        'estimated_time': 2,
        'description': (
            'مشروع مبتدئ لبناء صفحة ترحيب باستخدام HTML. '
            'ستتعلم كتابة ملف index.html كامل ببنية HTML5 صحيحة، ثم إضافة المحتوى داخل body.'
        ),
        'objectives': [
            'كتابة بنية HTML5 كاملة (DOCTYPE, html, head, body)',
            'إضافة عنوان h1 داخل body',
            'إضافة فقرة وزر داخل body',
        ],
        'stories': [
            {
                'title': 'هيكل HTML الكامل',
                'description': (
                    'اكتب ملف index.html كامل يبدأ بـ <!DOCTYPE html> '
                    'ويحتوي على <html> و<head> (مع meta charset) و<body>. '
                    'لا تحذف الأقسام الأساسية — عدّل المحتوى داخل body فقط.'
                ),
                'hint': (
                    'الملف يجب أن يحتوي: <!DOCTYPE html> ثم <html> ثم <head> مع '
                    '<meta charset="UTF-8"> ثم <body> ... </body> ثم </html>'
                ),
            },
            {
                'title': 'عنوان الصفحة',
                'description': 'داخل <body> ضع العنوان <h1>مرحباً بك في Buildly</h1>',
                'hint': 'استبدل العنوان الافتراضي داخل body بـ h1 يحتوي النص المطلوب',
            },
            {
                'title': 'فقرة وزر البدء',
                'description': (
                    'داخل <body> أضف فقرة <p>تعلم الفرونت إند خطوة بخطوة</p> '
                    'وزراً <button>ابدأ التعلم</button>'
                ),
                'hint': 'ضع <p> و<button> داخل body مع الإبقاء على هيكل HTML الكامل',
            },
        ],
        'tests': [
            {
                'name': 'بنية HTML كاملة',
                'description': 'يتحقق من وجود DOCTYPE و html و head و body',
                'test_code': (
                    'if (!htmlHasStructure()) throw new Error("structure");'
                ),
                'success_message': 'بنية HTML5 صحيحة وكاملة!',
                'failure_message': (
                    'اكتب ملف HTML كامل: DOCTYPE و html و head (مع charset) و body — '
                    'لا تكتفِ بجزء body فقط'
                ),
            },
            {
                'name': 'عنوان h1',
                'description': 'يتحقق من وجود h1 بالنص الصحيح داخل body',
                'test_code': (
                    'if (!htmlHasTagContent("h1", "مرحباً", "Buildly")) throw new Error("h1");'
                ),
                'success_message': 'العنوان موجود داخل body!',
                'failure_message': 'أضف <h1> يحتوي على ترحيب Buildly داخل body',
            },
            {
                'name': 'فقرة وزر',
                'description': 'يتحقق من الفقرة ونص الزر',
                'test_code': (
                    'if (!htmlHasText("تعلم", "الفرونت", "خطوة")) throw new Error("paragraph");\n'
                    'if (!htmlHasTagContent("button", "ابدأ", "التعلم")) throw new Error("button");'
                ),
                'success_message': 'الفقرة والزر صحيحان!',
                'failure_message': 'أضف الفقرة والزر المطلوبين داخل body',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}CSS Link Styling',
        'legacy_titles': (f'{SEED_PREFIX}تنسيق CSS للروابط',),
        'level': 'beginner',
        'languages': ['html', 'css'],
        'estimated_time': 2,
        'description': (
            'مشروع مبتدئ لتعلم CSS عبر كتابة قواعد تنسيق للروابط في style.css. '
            'ستحدد لون الرابط وحالته عند التمرير.'
        ),
        'objectives': [
            'كتابة قواعد CSS للعنصر a',
            'استخدام :hover',
            'تطبيق التنسيقات داخل style.css',
        ],
        'stories': [
            {
                'title': 'لون الرابط',
                'description': 'في style.css اكتب a { color: #198eee; }',
                'hint': 'أضف قاعدة a { color: #198eee; }',
            },
            {
                'title': 'إزالة الخط السفلي',
                'description': 'أضف text-decoration: none للروابط في style.css',
                'hint': 'أضف text-decoration: none داخل قاعدة a',
            },
            {
                'title': 'تأثير hover',
                'description': 'أضف a:hover { color: #0f6ec7; } في style.css',
                'hint': 'أضف قاعدة ثانية لـ a:hover',
            },
        ],
        'tests': [
            {
                'name': 'لون الرابط',
                'description': 'يتحقق من اللون',
                'test_code': 'if (!css.includes("#198eee")) throw new Error("color");',
                'success_message': 'اللون صحيح!',
                'failure_message': 'استخدم اللون #198eee في style.css',
            },
            {
                'name': 'بدون خط سفلي',
                'description': 'يتحقق من text-decoration',
                'test_code': 'if (!css.includes("text-decoration")) throw new Error("decoration");',
                'success_message': 'تم إزالة الخط السفلي!',
                'failure_message': 'أضف text-decoration: none',
            },
            {
                'name': 'حالة hover',
                'description': 'يتحقق من hover',
                'test_code': 'if (!css.includes(":hover")) throw new Error("hover");',
                'success_message': 'تأثير hover موجود!',
                'failure_message': 'أضف قاعدة a:hover',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Simple JavaScript Calculator',
        'legacy_titles': (f'{SEED_PREFIX}حاسبة JavaScript بسيطة',),
        'level': 'intermediate',
        'languages': ['javascript', 'html'],
        'estimated_time': 3,
        'description': (
            'مشروع متوسط لبناء دوال حاسبة بسيطة في JavaScript. '
            'ستكتب دوال للجمع والطرح والضرب.'
        ),
        'objectives': [
            'كتابة دوال JavaScript قابلة لإعادة الاستخدام',
            'التعامل مع الأعداد',
            'إرجاع نتائج صحيحة من كل دالة',
        ],
        'stories': [
            {
                'title': 'دالة الجمع',
                'description': 'في script.js اكتب دالة add(a, b) تُرجع مجموع العددين',
                'hint': 'return a + b;',
            },
            {
                'title': 'دالة الطرح',
                'description': 'في script.js اكتب دالة subtract(a, b) تُرجع الفرق',
                'hint': 'return a - b;',
            },
            {
                'title': 'دالة الضرب',
                'description': 'في script.js اكتب دالة multiply(a, b) تُرجع حاصل الضرب',
                'hint': 'return a * b;',
            },
        ],
        'tests': [
            {
                'name': 'اختبار الجمع',
                'description': 'add(4, 5) = 9',
                'test_code': 'if (add(4, 5) !== 9) throw new Error("add");',
                'success_message': 'الجمع يعمل!',
                'failure_message': 'راجع دالة add',
            },
            {
                'name': 'اختبار الطرح',
                'description': 'subtract(10, 3) = 7',
                'test_code': 'if (subtract(10, 3) !== 7) throw new Error("subtract");',
                'success_message': 'الطرح يعمل!',
                'failure_message': 'راجع دالة subtract',
            },
            {
                'name': 'اختبار الضرب',
                'description': 'multiply(3, 6) = 18',
                'test_code': 'if (multiply(3, 6) !== 18) throw new Error("multiply");',
                'success_message': 'الضرب يعمل!',
                'failure_message': 'راجع دالة multiply',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Student Array Filtering',
        'legacy_titles': (f'{SEED_PREFIX}فلترة مصفوفة الطلاب',),
        'level': 'intermediate',
        'languages': ['javascript'],
        'estimated_time': 3,
        'description': (
            'مشروع متوسط للتعامل مع المصفوفات في JavaScript. '
            'ستفلتر الطلاب الناجحين وتحسب المعدل.'
        ),
        'objectives': [
            'استخدام filter على المصفوفات',
            'استخدام reduce لحساب المعدل',
            'التعامل مع كائنات JavaScript',
        ],
        'stories': [
            {
                'title': 'الطلاب الناجحون',
                'description': 'اكتب دالة getPassing(students) تُرجع من score >= 60',
                'hint': 'return students.filter(s => s.score >= 60);',
            },
            {
                'title': 'عدد الناجحين',
                'description': 'اكتب دالة countPassing(students) تُرجع عدد الناجحين',
                'hint': 'return getPassing(students).length;',
            },
            {
                'title': 'المعدل العام',
                'description': 'اكتب دالة averageScore(students) تُرجع متوسط الدرجات',
                'hint': 'استخدم reduce لجمع الدرجات ثم اقسم على الطول',
            },
        ],
        'tests': [
            {
                'name': 'فلترة الناجحين',
                'description': 'يتحقق من filter',
                'test_code': 'const data=[{score:80},{score:50},{score:70}];\nif(getPassing(data).length!==2) throw new Error("filter");',
                'success_message': 'الفلترة صحيحة!',
                'failure_message': 'أرجع من score >= 60',
            },
            {
                'name': 'عدد الناجحين',
                'description': 'يتحقق من العدد',
                'test_code': 'const data=[{score:90},{score:40},{score:60}];\nif(countPassing(data)!==2) throw new Error("count");',
                'success_message': 'العدد صحيح!',
                'failure_message': 'راجع countPassing',
            },
            {
                'name': 'المعدل',
                'description': 'يتحقق من المعدل',
                'test_code': 'const data=[{score:80},{score:60}];\nif(averageScore(data)!==70) throw new Error("avg");',
                'success_message': 'المعدل صحيح!',
                'failure_message': 'راجع averageScore',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}React Card Component',
        'legacy_titles': (f'{SEED_PREFIX}مكون بطاقة React',),
        'level': 'advanced',
        'languages': ['react', 'javascript', 'html'],
        'estimated_time': 4,
        'description': (
            'مشروع متقدم لبناء مكون بطاقة React كنص. '
            'ستكتب دوال تُرجع JSX يحتوي على props.'
        ),
        'objectives': [
            'فهم بنية مكون React',
            'تمرير props للمكون',
            'إرجاع JSX صالح كنص',
        ],
        'stories': [
            {
                'title': 'مكون Card',
                'description': 'اكتب دالة Card(props) تُرجع JSX فيه h2 بعنوان props.title',
                'hint': 'return `<div><h2>${props.title}</h2></div>`;',
            },
            {
                'title': 'وصف البطاقة',
                'description': 'أضف فقرة p تعرض props.description',
                'hint': 'أضف <p>${props.description}</p> داخل div',
            },
            {
                'title': 'زر الإجراء',
                'description': 'أضف زراً بنص props.actionLabel',
                'hint': 'أضف <button>${props.actionLabel}</button>',
            },
        ],
        'tests': [
            {
                'name': 'عنوان البطاقة',
                'description': 'يتحقق من العنوان',
                'test_code': 'const jsx=Card({title:"React",description:"d",actionLabel:"Go"});\nif(!jsx.includes("React")) throw new Error("title");',
                'success_message': 'العنوان يظهر!',
                'failure_message': 'اعرض props.title داخل h2',
            },
            {
                'name': 'وصف البطاقة',
                'description': 'يتحقق من الوصف',
                'test_code': 'const jsx=Card({title:"T",description:"تعلم React",actionLabel:"Go"});\nif(!jsx.includes("تعلم React")) throw new Error("desc");',
                'success_message': 'الوصف يظهر!',
                'failure_message': 'اعرض props.description',
            },
            {
                'name': 'زر الإجراء',
                'description': 'يتحقق من الزر',
                'test_code': 'const jsx=Card({title:"T",description:"d",actionLabel:"ابدأ"});\nif(!jsx.includes("ابدأ")) throw new Error("btn");',
                'success_message': 'الزر يظهر!',
                'failure_message': 'أضف زراً بـ props.actionLabel',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Grid Gallery Interface',
        'legacy_titles': (f'{SEED_PREFIX}واجهة Grid Gallery',),
        'level': 'advanced',
        'languages': ['html', 'css'],
        'estimated_time': 4,
        'description': (
            'مشروع متقدم لبناء تخطيط Grid Gallery باستخدام HTML وCSS. '
            'ستبني هيكل المعرض في index.html وتنسّقه في style.css.'
        ),
        'objectives': [
            'استخدام CSS Grid',
            'بناء هيكل gallery في HTML',
            'تنسيق العناصر داخل الشبكة في CSS',
        ],
        'stories': [
            {
                'title': 'هيكل المعرض',
                'description': 'في index.html أنشئ div.gallery يحتوي 3 عناصر div.item',
                'hint': 'أنشئ div.gallery يحتوي 3 div.item داخل body',
            },
            {
                'title': 'تنسيق Grid',
                'description': 'في style.css أضف .gallery { display: grid; }',
                'hint': 'اكتب قاعدة .gallery { display: grid; }',
            },
            {
                'title': 'ثلاث أعمدة',
                'description': 'أضف grid-template-columns: repeat(3, 1fr) لـ .gallery في style.css',
                'hint': 'أضف الخاصية داخل قاعدة .gallery',
            },
        ],
        'tests': [
            {
                'name': 'هيكل gallery',
                'description': 'يتحقق من HTML',
                'test_code': 'if(!html.includes("gallery")) throw new Error("gallery");',
                'success_message': 'الهيكل صحيح!',
                'failure_message': 'أضف div.gallery في index.html',
            },
            {
                'name': 'عناصر item',
                'description': 'يتحقق من العناصر',
                'test_code': 'if((html.match(/item/g)||[]).length<3) throw new Error("items");',
                'success_message': '3 عناصر موجودة!',
                'failure_message': 'أضف 3 عناصر .item في index.html',
            },
            {
                'name': 'CSS Grid',
                'description': 'يتحقق من grid',
                'test_code': 'if(!css.includes("grid-template-columns")) throw new Error("grid");',
                'success_message': 'Grid مضبوط!',
                'failure_message': 'أضف grid-template-columns في style.css',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Counter State Management',
        'legacy_titles': (f'{SEED_PREFIX}إدارة حالة العداد',),
        'level': 'expert',
        'languages': ['javascript', 'typescript'],
        'estimated_time': 5,
        'description': (
            'مشروع خبير لمحاكاة إدارة حالة عداد. '
            'ستبني كائناً يحفظ القيمة ويوفر increment وdecrement وreset.'
        ),
        'objectives': [
            'تصميم كائن حالة',
            'تطبيق increment/decrement',
            'إعادة التعيين reset',
        ],
        'stories': [
            {
                'title': 'إنشاء العداد',
                'description': 'اكتب دالة createCounter(start=0) تُرجع { value, increment, decrement, reset }',
                'hint': 'خزّن value في متغير وأرجع دوال تعدّله',
            },
            {
                'title': 'increment و decrement',
                'description': 'increment تزيد value بـ 1 وdecrement تنقصه',
                'hint': 'عدّل this.value أو المتغير المغلق',
            },
            {
                'title': 'reset',
                'description': 'reset تعيد value إلى القيمة الابتدائية',
                'hint': 'خزّن startValue عند الإنشاء',
            },
        ],
        'tests': [
            {
                'name': 'increment',
                'description': 'يتحقق من الزيادة',
                'test_code': 'const c=createCounter(0);c.increment();if(c.value!==1) throw new Error("inc");',
                'success_message': 'increment يعمل!',
                'failure_message': 'راجع increment',
            },
            {
                'name': 'decrement',
                'description': 'يتحقق من النقصان',
                'test_code': 'const c=createCounter(5);c.decrement();if(c.value!==4) throw new Error("dec");',
                'success_message': 'decrement يعمل!',
                'failure_message': 'راجع decrement',
            },
            {
                'name': 'reset',
                'description': 'يتحقق من reset',
                'test_code': 'const c=createCounter(3);c.increment();c.reset();if(c.value!==3) throw new Error("reset");',
                'success_message': 'reset يعمل!',
                'failure_message': 'راجع reset',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Portfolio Navigation System',
        'legacy_titles': (f'{SEED_PREFIX}نظام تنقل Portfolio',),
        'level': 'expert',
        'languages': ['html', 'css', 'javascript', 'react'],
        'estimated_time': 6,
        'description': (
            'مشروع خبير لبناء نظام تنقل Portfolio متعدد الصفحات. '
            'ستكتب دوال تُرجع HTML لكل قسم.'
        ),
        'objectives': [
            'بناء شريط تنقل',
            'إنشاء صفحات متعددة كنص',
            'ربط الأقسام بشكل منطقي',
        ],
        'stories': [
            {
                'title': 'شريط التنقل',
                'description': 'اكتب buildNav() تُرجع nav فيه روابط: الرئيسية، المشاريع، التواصل',
                'hint': 'استخدم <nav><a> لكل رابط</a></nav>',
            },
            {
                'title': 'الصفحة الرئيسية',
                'description': 'اكتب buildHome() تُرجع section فيه h1 باسمك',
                'hint': 'return "<section><h1>أحمد</h1></section>";',
            },
            {
                'title': 'صفحة المشاريع',
                'description': 'اكتب buildProjects() تُرجع قائمة ul بمشروعين',
                'hint': 'أضف <ul><li>مشروع 1</li><li>مشروع 2</li></ul>',
            },
        ],
        'tests': [
            {
                'name': 'شريط التنقل',
                'description': 'يتحقق من nav',
                'test_code': 'const nav=buildNav();\nif(!nav.includes("المشاريع")||!nav.includes("التواصل")) throw new Error("nav");',
                'success_message': 'التنقل جاهز!',
                'failure_message': 'أضف روابط التنقل الثلاثة',
            },
            {
                'name': 'الصفحة الرئيسية',
                'description': 'يتحقق من home',
                'test_code': 'const home=buildHome();\nif(!home.includes("<h1")) throw new Error("home");',
                'success_message': 'الصفحة الرئيسية جاهزة!',
                'failure_message': 'أضف h1 في buildHome',
            },
            {
                'name': 'صفحة المشاريع',
                'description': 'يتحقق من projects',
                'test_code': 'const p=buildProjects();\nif(!p.includes("<ul")||(p.match(/<li/g)||[]).length<2) throw new Error("projects");',
                'success_message': 'قائمة المشاريع جاهزة!',
                'failure_message': 'أضف قائمة بمشروعين',
            },
        ],
    },
]

PYTHON_PROJECTS = [
    {
        'title': f'{SEED_PREFIX}Python Basic Functions',
        'legacy_titles': (f'{SEED_PREFIX}دوال Python الأساسية', 'دوال Python الأساسية'),
        'level': 'beginner',
        'languages': ['python'],
        'estimated_time': 2,
        'description': (
            'مشروع مبتدئ لتعلم كتابة دوال Python بسيطة. '
            'ستنشئ دالة ترحيب ودالة جمع رقمين.'
        ),
        'objectives': [
            'فهم كيفية تعريف دالة في Python',
            'إرجاع نص من دالة باستخدام f-string',
            'جمع رقمين وإرجاع الناتج',
        ],
        'stories': [
            {
                'title': 'دالة الترحيب',
                'description': 'اكتب دالة greet(name) تُرجع: Hello, {name}!',
                'hint': 'return f"Hello, {name}!"',
            },
            {
                'title': 'دالة الجمع',
                'description': 'اكتب دالة add(a, b) تُرجع مجموع العددين',
                'hint': 'return a + b',
            },
            {
                'title': 'الأعداد السالبة',
                'description': 'تأكد أن add تعمل مع الأعداد السالبة',
                'hint': 'جرب add(-2, 5) يجب أن تُرجع 3',
            },
        ],
        'tests': [
            {
                'name': 'اختبار greet',
                'description': 'يتحقق من greet',
                'test_code': 'assert greet("Sara") == "Hello, Sara!"',
                'success_message': 'دالة greet تعمل!',
                'failure_message': 'راجع greet(name)',
            },
            {
                'name': 'اختبار add',
                'description': 'يتحقق من add',
                'test_code': 'assert add(2, 3) == 5',
                'success_message': 'دالة add تعمل!',
                'failure_message': 'راجع add(a, b)',
            },
            {
                'name': 'اختبار add سالب',
                'description': 'يتحقق من الأعداد السالبة',
                'test_code': 'assert add(-2, 5) == 3',
                'success_message': 'add تعمل مع السالب!',
                'failure_message': 'تأكد من add(-2, 5)',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Working with Lists',
        'legacy_titles': (f'{SEED_PREFIX}التعامل مع القوائم',),
        'level': 'beginner',
        'languages': ['python'],
        'estimated_time': 2,
        'description': (
            'مشروع مبتدئ للتعامل مع قوائم Python. '
            'ستكتب دوال لإيجاد الأكبر وحساب المجموع.'
        ),
        'objectives': [
            'التعامل مع list في Python',
            'استخدام max و sum',
            'كتابة دالة مخصصة للبحث',
        ],
        'stories': [
            {
                'title': 'أكبر عنصر',
                'description': 'اكتب دالة find_max(numbers) تُرجع أكبر رقم',
                'hint': 'return max(numbers)',
            },
            {
                'title': 'مجموع القائمة',
                'description': 'اكتب دالة total(numbers) تُرجع مجموع العناصر',
                'hint': 'return sum(numbers)',
            },
            {
                'title': 'عدد العناصر الزوجية',
                'description': 'اكتب دالة count_even(numbers) تُرجع عدد الأعداد الزوجية',
                'hint': 'استخدم len مع list comprehension',
            },
        ],
        'tests': [
            {
                'name': 'find_max',
                'description': 'يتحقق من find_max',
                'test_code': 'assert find_max([1, 9, 3]) == 9',
                'success_message': 'find_max صحيحة!',
                'failure_message': 'راجع find_max',
            },
            {
                'name': 'total',
                'description': 'يتحقق من total',
                'test_code': 'assert total([2, 3, 5]) == 10',
                'success_message': 'total صحيحة!',
                'failure_message': 'راجع total',
            },
            {
                'name': 'count_even',
                'description': 'يتحقق من count_even',
                'test_code': 'assert count_even([1, 2, 3, 4]) == 2',
                'success_message': 'count_even صحيحة!',
                'failure_message': 'راجع count_even',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Text Processing',
        'legacy_titles': (f'{SEED_PREFIX}معالجة النصوص',),
        'level': 'intermediate',
        'languages': ['python'],
        'estimated_time': 3,
        'description': (
            'مشروع متوسط لمعالجة النصوص في Python. '
            'ستكتب دوال لتنظيف النص وعكسه وعدد الكلمات.'
        ),
        'objectives': [
            'استخدام strip و lower',
            'عكس النصوص',
            'عد الكلمات',
        ],
        'stories': [
            {
                'title': 'تنظيف النص',
                'description': 'اكتب دالة clean_text(text) تُرجع النص بدون مسافات زائدة وبحروف صغيرة',
                'hint': 'return text.strip().lower()',
            },
            {
                'title': 'عكس النص',
                'description': 'اكتب دالة reverse_text(text) تُرجع النص معكوساً',
                'hint': 'return text[::-1]',
            },
            {
                'title': 'عدد الكلمات',
                'description': 'اكتب دالة word_count(text) تُرجع عدد الكلمات',
                'hint': 'return len(text.split())',
            },
        ],
        'tests': [
            {
                'name': 'clean_text',
                'description': 'يتحقق من clean_text',
                'test_code': 'assert clean_text("  Hello ") == "hello"',
                'success_message': 'clean_text تعمل!',
                'failure_message': 'استخدم strip().lower()',
            },
            {
                'name': 'reverse_text',
                'description': 'يتحقق من reverse_text',
                'test_code': 'assert reverse_text("abc") == "cba"',
                'success_message': 'reverse_text تعمل!',
                'failure_message': 'راجع reverse_text',
            },
            {
                'name': 'word_count',
                'description': 'يتحقق من word_count',
                'test_code': 'assert word_count("a b c") == 3',
                'success_message': 'word_count تعمل!',
                'failure_message': 'راجع word_count',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Dictionaries and Lookup',
        'legacy_titles': (f'{SEED_PREFIX}القواميس والبحث',),
        'level': 'intermediate',
        'languages': ['python'],
        'estimated_time': 3,
        'description': (
            'مشروع متوسط للتعامل مع القواميس في Python. '
            'ستبحث عن طالب بالاسم وتحسب معدله.'
        ),
        'objectives': [
            'التعامل مع dict',
            'البحث في قائمة قواميس',
            'حساب المعدل',
        ],
        'stories': [
            {
                'title': 'البحث عن طالب',
                'description': 'اكتب دالة find_student(students, name) تُرجع قاموس الطالب أو None',
                'hint': 'استخدم حلقة for للبحث عن name',
            },
            {
                'title': 'درجة الطالب',
                'description': 'اكتب دالة get_score(students, name) تُرجع الدرجة أو 0',
                'hint': 'student = find_student(...); return student["score"] if student else 0',
            },
            {
                'title': 'المعدل',
                'description': 'اكتب دالة average_score(students) تُرجع متوسط score',
                'hint': 'اجمع الدرجات واقسم على len(students)',
            },
        ],
        'tests': [
            {
                'name': 'find_student',
                'description': 'يتحقق من البحث',
                'test_code': 'data=[{"name":"Ali","score":80}]\nassert find_student(data,"Ali")["score"]==80',
                'success_message': 'البحث يعمل!',
                'failure_message': 'راجع find_student',
            },
            {
                'name': 'get_score',
                'description': 'يتحقق من get_score',
                'test_code': 'data=[{"name":"Noor","score":90}]\nassert get_score(data,"Noor")==90',
                'success_message': 'get_score تعمل!',
                'failure_message': 'راجع get_score',
            },
            {
                'name': 'average_score',
                'description': 'يتحقق من المعدل',
                'test_code': 'data=[{"name":"A","score":80},{"name":"B","score":60}]\nassert average_score(data)==70',
                'success_message': 'المعدل صحيح!',
                'failure_message': 'راجع average_score',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}OOP Classes',
        'legacy_titles': (f'{SEED_PREFIX}الأصناف OOP',),
        'level': 'advanced',
        'languages': ['python'],
        'estimated_time': 4,
        'description': (
            'مشروع متقدم لتعلم البرمجة كائنية التوجه في Python. '
            'ستنشئ صنف BankAccount مع إيداع وسحب.'
        ),
        'objectives': [
            'تعريف class في Python',
            'استخدام __init__',
            'كتابة methods للإيداع والسحب',
        ],
        'stories': [
            {
                'title': 'صنف BankAccount',
                'description': 'أنشئ class BankAccount مع __init__(self, balance=0)',
                'hint': 'self.balance = balance',
            },
            {
                'title': 'deposit',
                'description': 'أضف method deposit(self, amount) تزيد الرصيد',
                'hint': 'self.balance += amount',
            },
            {
                'title': 'withdraw',
                'description': 'أضف method withdraw(self, amount) تنقص الرصيد إن أمكن',
                'hint': 'إذا amount <= self.balance: self.balance -= amount',
            },
        ],
        'tests': [
            {
                'name': 'إنشاء الحساب',
                'description': 'يتحقق من الإنشاء',
                'test_code': 'acc=BankAccount(100)\nassert acc.balance==100',
                'success_message': 'الصنف يعمل!',
                'failure_message': 'راجع BankAccount.__init__',
            },
            {
                'name': 'deposit',
                'description': 'يتحقق من الإيداع',
                'test_code': 'acc=BankAccount(50)\nacc.deposit(30)\nassert acc.balance==80',
                'success_message': 'deposit يعمل!',
                'failure_message': 'راجع deposit',
            },
            {
                'name': 'withdraw',
                'description': 'يتحقق من السحب',
                'test_code': 'acc=BankAccount(100)\nacc.withdraw(40)\nassert acc.balance==60',
                'success_message': 'withdraw يعمل!',
                'failure_message': 'راجع withdraw',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Error Handling',
        'legacy_titles': (f'{SEED_PREFIX}معالجة الأخطاء',),
        'level': 'advanced',
        'languages': ['python'],
        'estimated_time': 4,
        'description': (
            'مشروع متقدم لتعلم معالجة الأخطاء في Python. '
            'ستكتب دوال آمنة للقسمة وتحويل النص إلى رقم.'
        ),
        'objectives': [
            'استخدام try/except',
            'إرجاع قيم افتراضية عند الخطأ',
            'التحقق من المدخلات',
        ],
        'stories': [
            {
                'title': 'قسمة آمنة',
                'description': 'اكتب دالة safe_divide(a, b) تُرجع None عند القسمة على صفر',
                'hint': 'استخدم try/except ZeroDivisionError',
            },
            {
                'title': 'تحويل نص لرقم',
                'description': 'اكتب دالة to_int(value) تُرجع int أو None',
                'hint': 'try: return int(value) except ValueError: return None',
            },
            {
                'title': 'جمع آمن',
                'description': 'اكتب دالة safe_add(a, b) تجمع رقمين أو تُرجع 0 عند الخطأ',
                'hint': 'حوّل القيم بـ to_int ثم اجمع',
            },
        ],
        'tests': [
            {
                'name': 'safe_divide',
                'description': 'يتحقق من القسمة الآمنة',
                'test_code': 'assert safe_divide(10, 2)==5\nassert safe_divide(5, 0) is None',
                'success_message': 'safe_divide تعمل!',
                'failure_message': 'عالج القسمة على صفر',
            },
            {
                'name': 'to_int',
                'description': 'يتحقق من to_int',
                'test_code': 'assert to_int("42")==42\nassert to_int("x") is None',
                'success_message': 'to_int تعمل!',
                'failure_message': 'راجع to_int',
            },
            {
                'name': 'safe_add',
                'description': 'يتحقق من safe_add',
                'test_code': 'assert safe_add("2","3")==5\nassert safe_add("a","1")==0',
                'success_message': 'safe_add تعمل!',
                'failure_message': 'راجع safe_add',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Binary Search',
        'legacy_titles': (f'{SEED_PREFIX}البحث الثنائي',),
        'level': 'expert',
        'languages': ['python'],
        'estimated_time': 5,
        'description': (
            'مشروع خبير لتطبيق خوارزمية البحث الثنائي في Python. '
            'ستكتب دالة تبحث في قائمة مرتبة.'
        ),
        'objectives': [
            'فهم البحث الثنائي',
            'التعامل مع الحدود left/right',
            'إرجاع الفهرس أو -1',
        ],
        'stories': [
            {
                'title': 'البحث الثنائي',
                'description': 'اكتب دالة binary_search(nums, target) تُرجع الفهرس أو -1',
                'hint': 'استخدم while left <= right مع mid',
            },
            {
                'title': 'العنصر الأول',
                'description': 'تأكد أن الدالة تجد العنصر في بداية القائمة',
                'hint': 'جرب [1,2,3] و target=1',
            },
            {
                'title': 'عنصر غير موجود',
                'description': 'تُرجع -1 إذا لم يوجد العنصر',
                'hint': 'return -1 بعد انتهاء الحلقة',
            },
        ],
        'tests': [
            {
                'name': 'عنصر في الوسط',
                'description': 'يتحقق من البحث',
                'test_code': 'assert binary_search([1,3,5,7,9], 5)==2',
                'success_message': 'البحث يعمل!',
                'failure_message': 'راجع binary_search',
            },
            {
                'name': 'عنصر في البداية',
                'description': 'يتحقق من البداية',
                'test_code': 'assert binary_search([2,4,6,8], 2)==0',
                'success_message': 'وجد في البداية!',
                'failure_message': 'تأكد من حالة البداية',
            },
            {
                'name': 'غير موجود',
                'description': 'يتحقق من -1',
                'test_code': 'assert binary_search([1,2,3], 9)==-1',
                'success_message': 'يعيد -1 بشكل صحيح!',
                'failure_message': 'أرجع -1 عند عدم الوجود',
            },
        ],
    },
    {
        'title': f'{SEED_PREFIX}Higher-Order Functions',
        'legacy_titles': (f'{SEED_PREFIX}دوال عالية المستوى',),
        'level': 'expert',
        'languages': ['python'],
        'estimated_time': 5,
        'description': (
            'مشروع خبير لاستخدام map و filter و sorted في Python. '
            'ستعالج قائمة بيانات طلاب.'
        ),
        'objectives': [
            'استخدام map لتحويل البيانات',
            'استخدام filter للتصفية',
            'ترتيب النتائج بـ sorted',
        ],
        'stories': [
            {
                'title': 'تربيع الأعداد',
                'description': 'اكتب دالة square_all(nums) تُرجع مربعات الأعداد',
                'hint': 'return list(map(lambda x: x*x, nums))',
            },
            {
                'title': 'تصفية الموجب',
                'description': 'اكتب دالة only_positive(nums) تُرجع الأعداد الموجبة فقط',
                'hint': 'return list(filter(lambda x: x>0, nums))',
            },
            {
                'title': 'ترتيب الطلاب',
                'description': 'اكتب دالة sort_by_score(students) تُرتب حسب score تنازلياً',
                'hint': 'return sorted(students, key=lambda s: s["score"], reverse=True)',
            },
        ],
        'tests': [
            {
                'name': 'square_all',
                'description': 'يتحقق من map',
                'test_code': 'assert square_all([1,2,3])==[1,4,9]',
                'success_message': 'square_all تعمل!',
                'failure_message': 'راجع square_all',
            },
            {
                'name': 'only_positive',
                'description': 'يتحقق من filter',
                'test_code': 'assert only_positive([-1,2,-3,4])==[2,4]',
                'success_message': 'only_positive تعمل!',
                'failure_message': 'راجع only_positive',
            },
            {
                'name': 'sort_by_score',
                'description': 'يتحقق من الترتيب',
                'test_code': 'data=[{"name":"A","score":70},{"name":"B","score":90}]\nassert sort_by_score(data)[0]["name"]=="B"',
                'success_message': 'الترتيب صحيح!',
                'failure_message': 'راجع sort_by_score',
            },
        ],
    },
]
