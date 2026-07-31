"""Portfolio Navigation System project for Frontend Mastery."""

PORTFOLIO_TITLE = 'Build a Portfolio Navigation System'
PORTFOLIO_LEGACY_TITLES = (
    'Build a Portfolio Navigation System',
    '[Buildly] Portfolio Navigation System',
    '[Buildly] نظام تنقل Portfolio',
)

PORTFOLIO_PROJECT = {
    'title': PORTFOLIO_TITLE,
    'level': 'expert',
    'languages': ['html', 'css', 'javascript'],
    'estimated_time': 7,
    'description': (
        'ابنِ موقع Portfolio متعدد الأقسام باستخدام HTML و CSS و JavaScript. '
        'أنشئ هيكل صفحة كامل، شريط تنقل، أقسام الرئيسية والمشاريع والتواصل، '
        'ودوال تعرض كل قسم كنص HTML مع تنسيق CSS واضح.'
    ),
    'objectives': (
        'نفّذ قصص المستخدم أدناه واجتز كل الاختبارات لإكمال موقع Portfolio متكامل.'
    ),
    'stories': [
        {
            'title': 'هيكل الصفحة',
            'description': (
                'في index.html أنشئ مستنداً كاملاً يربط style.css و script.js، '
                'ويحتوي header و nav بمعرّف site-nav وحاوية رئيسية main بمعرّف app و footer.'
            ),
            'hint': (
                'استخدم <link rel="stylesheet" href="style.css"> و '
                '<script src="script.js"></script> مع <main id="app"></main>.'
            ),
        },
        {
            'title': 'روابط التنقل في HTML',
            'description': (
                'داخل #site-nav أضف ثلاثة روابط على الأقل: الرئيسية (#home) و '
                'المشاريع (#projects) و التواصل (#contact).'
            ),
            'hint': 'أضف عناصر <a href="#home"> و <a href="#projects"> و <a href="#contact">.',
        },
        {
            'title': 'تنسيق شريط التنقل',
            'description': (
                'في style.css نسّق #site-nav بـ display: flex مع مسافة بين الروابط، '
                'وأضف قاعدة لـ #app أو .portfolio-page.'
            ),
            'hint': 'اكتب #site-nav { display: flex; gap: 16px; } وقاعدة لحاوية المحتوى.',
        },
        {
            'title': 'دالة buildNav',
            'description': (
                'في script.js اكتب buildNav() تُرجع نص HTML لـ <nav> يحوي روابط '
                'الرئيسية والمشاريع والتواصل.'
            ),
            'hint': 'أرجع template string فيه <nav> وثلاثة عناصر <a>.',
        },
        {
            'title': 'دالة buildHome',
            'description': (
                'اكتب buildHome() تُرجع <section id="home" class="portfolio-page"> '
                'فيها <h1> باسمك وفقرة تعريفية قصيرة.'
            ),
            'hint': 'ضمّن id="home" و class="portfolio-page" ووسم <h1> ونص تعريفي.',
        },
        {
            'title': 'دالة buildProjects',
            'description': (
                'اكتب buildProjects() تُرجع <section id="projects" class="portfolio-page"> '
                'فيها قائمة <ul> بمشروعين على الأقل كعناصر <li>.'
            ),
            'hint': 'أضف <ul> داخل القسم مع عنصرين <li> على الأقل.',
        },
        {
            'title': 'دالة buildContact',
            'description': (
                'اكتب buildContact() تُرجع <section id="contact" class="portfolio-page"> '
                'فيها وسيلة تواصل (نموذج أو رابط بريد) بالصنف contact-info.'
            ),
            'hint': 'غلّف محتوى التواصل بعنصر بالصنف contact-info داخل القسم.',
        },
        {
            'title': 'توجيه الصفحات',
            'description': (
                'اكتب renderPortfolio(page) حيث page تكون home أو projects أو contact. '
                'يجب أن تُرجع HTML يجمع ناتج buildNav() مع القسم المطلوب.'
            ),
            'hint': 'اختر الدالة المناسبة حسب page وألصقها بعد buildNav().',
        },
        {
            'title': 'أنماط Portfolio',
            'description': (
                'اكتب getPortfolioStyles() تُرجع نص CSS ينسّق #site-nav و .portfolio-page '
                'و .contact-info، ويستخدم flex أو grid في التخطيط.'
            ),
            'hint': 'أرجع template string يحوي المحدّدات المطلوبة و display: flex أو grid.',
        },
        {
            'title': 'دمج التطبيق',
            'description': (
                'عند تحميل الصفحة اعرض المحتوى داخل #app باستخدام renderPortfolio("home") '
                'أو حقن الأقسام يدوياً، وطبّق أنماط getPortfolioStyles() أو انقلها إلى style.css.'
            ),
            'hint': 'استخدم DOMContentLoaded واضبط app.innerHTML = renderPortfolio("home").',
        },
    ],
}

PORTFOLIO_TESTS = [
    {
        'name': '1. ربط ملفات CSS و JS',
        'story_index': 1,
        'description': 'index.html يجب أن يربط style.css و script.js.',
        'test_code': (
            'if (!html.includes("style.css")) throw new Error("css-link");\n'
            'if (!html.includes("script.js")) throw new Error("js-link");'
        ),
        'success_message': 'ملفات CSS و JS مربوطة.',
        'failure_message': 'أضف رابط style.css و script.js في index.html.',
    },
    {
        'name': '2. وجود #site-nav و #app',
        'story_index': 1,
        'description': 'الصفحة يجب أن تحوي nav#site-nav و main#app.',
        'test_code': (
            'const nav = getEl("site-nav");\n'
            'const app = getEl("app");\n'
            'if (!nav) throw new Error("site-nav");\n'
            'if (!app) throw new Error("app");'
        ),
        'success_message': 'هيكل #site-nav و #app موجود.',
        'failure_message': 'أضف عناصر بمعرّفي site-nav و app.',
    },
    {
        'name': '3. وجود header و footer',
        'story_index': 1,
        'description': 'الصفحة يجب أن تحوي header و footer.',
        'test_code': (
            'if (!html.includes("<header") || !html.includes("<footer")) '
            'throw new Error("landmarks");'
        ),
        'success_message': 'header و footer موجودان.',
        'failure_message': 'أضف عنصري <header> و <footer> في index.html.',
    },
    {
        'name': '4. روابط التنقل الثلاثة',
        'story_index': 2,
        'description': 'يجب وجود روابط #home و #projects و #contact.',
        'test_code': (
            'if (!html.includes("#home") || !html.includes("#projects") '
            '|| !html.includes("#contact")) throw new Error("anchors");'
        ),
        'success_message': 'روابط الأقسام الثلاثة موجودة.',
        'failure_message': 'أضف روابط href="#home" و "#projects" و "#contact".',
    },
    {
        'name': '5. نصوص روابط عربية',
        'story_index': 2,
        'description': 'روابط التنقل يجب أن تعرض الرئيسية والمشاريع والتواصل.',
        'test_code': (
            'if (!html.includes("الرئيسية") || !html.includes("المشاريع") '
            '|| !html.includes("التواصل")) throw new Error("labels");'
        ),
        'success_message': 'تسميات الروابط صحيحة.',
        'failure_message': 'استخدم نصوص الرئيسية والمشاريع والتواصل في الروابط.',
    },
    {
        'name': '6. تنسيق #site-nav بـ flex',
        'story_index': 3,
        'description': 'style.css يجب أن ينسّق #site-nav بـ flex.',
        'test_code': (
            'if (!css.includes("#site-nav")) throw new Error("nav-selector");\n'
            'if (!css.includes("flex")) throw new Error("flex");'
        ),
        'success_message': 'تنسيق شريط التنقل مضبوط.',
        'failure_message': 'أضف قاعدة #site-nav تستخدم display: flex.',
    },
    {
        'name': '7. تنسيق حاوية المحتوى',
        'story_index': 3,
        'description': 'style.css يجب أن ينسّق #app أو .portfolio-page.',
        'test_code': (
            'if (!css.includes("#app") && !css.includes(".portfolio-page")) '
            'throw new Error("content-style");'
        ),
        'success_message': 'حاوية المحتوى منسّقة.',
        'failure_message': 'أضف قواعد CSS لـ #app أو .portfolio-page.',
    },
    {
        'name': '8. buildNav تُرجع nav مع الروابط',
        'story_index': 4,
        'description': 'buildNav يجب أن تُرجع HTML فيه nav والروابط الثلاثة.',
        'test_code': (
            'const nav = buildNav();\n'
            'if (!nav || !nav.includes("<nav")) throw new Error("nav");\n'
            'if (!nav.includes("المشاريع") || !nav.includes("التواصل") '
            '|| !nav.includes("الرئيسية")) throw new Error("links");'
        ),
        'success_message': 'buildNav تُرجع شريط التنقل المطلوب.',
        'failure_message': 'أرجع <nav> يحوي روابط الرئيسية والمشاريع والتواصل.',
    },
    {
        'name': '9. buildHome تعرض القسم الرئيسي',
        'story_index': 5,
        'description': 'buildHome يجب أن تُرجع section#home مع h1.',
        'test_code': (
            'const home = buildHome();\n'
            'if (!home.includes(\'id="home"\') && !home.includes("id=\'home\'")) '
            'throw new Error("home-id");\n'
            'if (!home.includes("portfolio-page")) throw new Error("page-class");\n'
            'if (!home.includes("<h1")) throw new Error("heading");'
        ),
        'success_message': 'buildHome تعرض الصفحة الرئيسية.',
        'failure_message': 'أرجع section بمعرّف home وصنف portfolio-page ووسم h1.',
    },
    {
        'name': '10. buildProjects تعرض قائمة مشاريع',
        'story_index': 6,
        'description': 'buildProjects يجب أن تُرجع قسم مشاريع بقائمة عنصرين على الأقل.',
        'test_code': (
            'const projects = buildProjects();\n'
            'if (!projects.includes(\'id="projects"\') && !projects.includes("id=\'projects\'")) '
            'throw new Error("projects-id");\n'
            'if (!projects.includes("<ul") || (projects.match(/<li/g) || []).length < 2) '
            'throw new Error("list");'
        ),
        'success_message': 'buildProjects تعرض قائمة المشاريع.',
        'failure_message': 'أرجع section#projects فيها <ul> بمشروعين على الأقل.',
    },
    {
        'name': '11. buildContact تعرض قسم التواصل',
        'story_index': 7,
        'description': 'buildContact يجب أن تُرجع قسم تواصل مع contact-info.',
        'test_code': (
            'const contact = buildContact();\n'
            'if (!contact.includes(\'id="contact"\') && !contact.includes("id=\'contact\'")) '
            'throw new Error("contact-id");\n'
            'if (!contact.includes("contact-info")) throw new Error("contact-info");\n'
            'if (!contact.includes("portfolio-page")) throw new Error("page-class");'
        ),
        'success_message': 'buildContact تعرض قسم التواصل.',
        'failure_message': 'أرجع section#contact مع صنف contact-info.',
    },
    {
        'name': '12. renderPortfolio للرئيسية',
        'story_index': 8,
        'description': 'renderPortfolio("home") يجب أن تجمع التنقل والرئيسية.',
        'test_code': (
            'const page = renderPortfolio("home");\n'
            'if (!page.includes("<nav") || !page.includes("<h1")) throw new Error("home-page");\n'
            'if (!page.includes("home")) throw new Error("home-marker");'
        ),
        'success_message': 'renderPortfolio تعرض الرئيسية مع التنقل.',
        'failure_message': 'اجمع buildNav() مع buildHome() عند page=home.',
    },
    {
        'name': '13. renderPortfolio للمشاريع',
        'story_index': 8,
        'description': 'renderPortfolio("projects") يجب أن تعرض قسم المشاريع.',
        'test_code': (
            'const page = renderPortfolio("projects");\n'
            'if (!page.includes("<nav") || !page.includes("<ul")) throw new Error("projects-page");\n'
            'if (!page.includes("projects")) throw new Error("projects-marker");'
        ),
        'success_message': 'renderPortfolio تعرض صفحة المشاريع.',
        'failure_message': 'اجمع buildNav() مع buildProjects() عند page=projects.',
    },
    {
        'name': '14. renderPortfolio للتواصل',
        'story_index': 8,
        'description': 'renderPortfolio("contact") يجب أن تعرض قسم التواصل.',
        'test_code': (
            'const page = renderPortfolio("contact");\n'
            'if (!page.includes("<nav") || !page.includes("contact-info")) '
            'throw new Error("contact-page");'
        ),
        'success_message': 'renderPortfolio تعرض صفحة التواصل.',
        'failure_message': 'اجمع buildNav() مع buildContact() عند page=contact.',
    },
    {
        'name': '15. getPortfolioStyles تنسّق التنقل والصفحات',
        'story_index': 9,
        'description': 'getPortfolioStyles يجب أن تشمل قواعد #site-nav و .portfolio-page.',
        'test_code': (
            'const styles = getPortfolioStyles();\n'
            'if (!styles.includes("#site-nav") || !styles.includes(".portfolio-page")) '
            'throw new Error("selectors");\n'
            'if (!styles.includes(".contact-info")) throw new Error("contact-style");'
        ),
        'success_message': 'getPortfolioStyles تتضمن المحدّدات المطلوبة.',
        'failure_message': 'أضف قواعد #site-nav و .portfolio-page و .contact-info.',
    },
    {
        'name': '16. getPortfolioStyles تستخدم flex أو grid',
        'story_index': 9,
        'description': 'getPortfolioStyles يجب أن تستخدم flex أو grid.',
        'test_code': (
            'const styles = getPortfolioStyles();\n'
            'if (!styles.includes("flex") && !styles.includes("grid")) '
            'throw new Error("layout");'
        ),
        'success_message': 'تخطيط Portfolio يستخدم flex أو grid.',
        'failure_message': 'استخدم display: flex أو grid في getPortfolioStyles.',
    },
    {
        'name': '17. دمج #app في الصفحة',
        'story_index': 10,
        'description': 'index.html يجب أن يحتوي حاوية #app جاهزة للدمج.',
        'test_code': (
            'const app = getEl("app");\n'
            'if (!app) throw new Error("app");\n'
            'if (!html.includes("script.js")) throw new Error("script");'
        ),
        'success_message': 'حاوية التطبيق جاهزة للدمج.',
        'failure_message': 'تأكد من وجود #app وربط script.js.',
    },
]
