"""Product Catalog expert React project for Frontend Mastery."""

PRODUCT_CATALOG_TITLE = 'Build a Product Catalog with React'
PRODUCT_CATALOG_LEGACY_TITLES = (
    'Build a Product Catalog with React',
    '[Buildly] كتالوج منتجات بـ React',
)

PRODUCT_CATALOG_PROJECT = {
    'title': PRODUCT_CATALOG_TITLE,
    'level': 'expert',
    'languages': ['react', 'javascript', 'html', 'css'],
    'estimated_time': 8,
    'description': (
        'ابنِ واجهة كتالوج منتجات متكاملة باستخدام React مع HTML و CSS. '
        'أنشئ مكوّنات قابلة لإعادة الاستخدام، دوال تصفية وترتيب، عرض المخزون، '
        'وهيكل صفحة حقيقي يربط App.jsx و style.css داخل #root.'
    ),
    'objectives': (
        'صمّم كتالوج منتجات كامل: بيانات + مكوّنات React + تنسيق CSS + دمج في الصفحة.'
    ),
    'stories': [
        {
            'title': 'هيكل تطبيق React',
            'description': (
                'في index.html أضف حاوية #root واربط style.css و App.jsx. '
                'هذا أساس تشغيل واجهة الكتالوج.'
            ),
            'hint': 'استخدم <div id="root"></div> مع رابط CSS وملف App.jsx.',
        },
        {
            'title': 'دوال نموذج المنتج',
            'description': (
                'اكتب createProduct(id, name, price, category, inStock) و formatPrice(price). '
                'يجب أن ترفض createProduct السعر السالب، وأن تُرجع formatPrice نصاً مثل $12.50.'
            ),
            'hint': 'ارمِ خطأ إذا كان price < 0، ونسّق السعر بخانتين عشريتين مع رمز $.',
        },
        {
            'title': 'تصفية وترتيب المنتجات',
            'description': (
                'اكتب filterProductsByCategory(products, category) و '
                'sortProductsByPrice(products, direction) حيث direction تكون asc أو desc. '
                'لا تعدّل المصفوفة الأصلية.'
            ),
            'hint': 'أرجع مصفوفة جديدة عبر filter أو [...products].sort(...).',
        },
        {
            'title': 'حالات المخزون والفراغ',
            'description': (
                'اكتب getInStockCount(products) و renderEmptyState(message) للتعامل مع '
                'عدّاد المخزون وحالات الكتالوج الفارغ بالصنف empty-state.'
            ),
            'hint': 'عدّ المنتجات حيث inStock صحيح وأرجع JSX لحالة الفراغ.',
        },
        {
            'title': 'مكوّن ProductCard',
            'description': (
                'اكتب ProductCard({ name, price, category, inStock }) لتُرجع JSX بالأصناف '
                'product-card و product-name و product-price و product-category وشارة مخزون '
                '(in-stock أو out-of-stock). اعرض السعر عبر formatPrice.'
            ),
            'hint': 'استخدم صنف الشارة حسب inStock واعرض السعر المنسّق.',
        },
        {
            'title': 'مكوّن ProductList',
            'description': (
                'اكتب ProductList({ products }) لتُرجع JSX بالصنف product-list يعرض '
                'ProductCard لكل منتج. إذا كانت القائمة فارغة أرجع renderEmptyState.'
            ),
            'hint': 'إذا !products.length استخدم renderEmptyState("No products found").',
        },
        {
            'title': 'رأس الكتالوج',
            'description': (
                'اكتب CatalogHeader({ title, subtitle, productCount }) لتُرجع JSX بالأصناف '
                'catalog-header و catalog-title و catalog-subtitle و catalog-count.'
            ),
            'hint': 'اعرض العنوان والعنوان الفرعي والعدد الإجمالي للمنتجات.',
        },
        {
            'title': 'تخطيط الكتالوج',
            'description': (
                'اكتب CatalogPage({ products, title, subtitle }) لدمج CatalogHeader و '
                'ProductList داخل غلاف بالصنف catalog-page. مرّر productCount من طول القائمة.'
            ),
            'hint': 'ركّب الرأس والقائمة ومرّر products.length إلى CatalogHeader.',
        },
        {
            'title': 'ملف تنسيق الكتالوج',
            'description': (
                'اكتب getCatalogStyles() لتُرجع CSS لـ .catalog-page و .catalog-header و '
                '.product-list و .product-card و .empty-state وحالات شارة المخزون. '
                'استخدم CSS Grid أو Flexbox. انقل القواعد أيضاً إلى style.css أو احقنها من الدالة.'
            ),
            'hint': 'أرجع template string بالمحدّدات وقواعد التخطيط المطلوبة.',
        },
        {
            'title': 'دمج تطبيق React',
            'description': (
                'في App.jsx اعرض CatalogPage بمنتجات تجريبية (3 منتجات على الأقل من فئتين). '
                'في style.css طبّق أنماط الكتالوج عبر getCatalogStyles أو قواعد مكافئة.'
            ),
            'hint': 'ثبّت CatalogPage داخل #root واحتفظ بمنتجات تجريبية واضحة.',
        },
    ],
}

PRODUCT_CATALOG_TESTS = [
    {
        'name': '1. وجود #root وربط الملفات',
        'story_index': 1,
        'description': 'index.html يجب أن يحوي #root ويربط style.css و App.jsx.',
        'test_code': (
            'const root = getEl("root");\n'
            'if (!root) throw new Error("root");\n'
            'if (!html.includes("style.css")) throw new Error("css-link");\n'
            'if (!html.includes("App.jsx") && !html.includes("app.jsx")) '
            'throw new Error("app-link");'
        ),
        'success_message': 'هيكل React الأساسي موجود.',
        'failure_message': 'أضف #root واربط style.css و App.jsx في index.html.',
    },
    {
        'name': '2. createProduct تُرجع كائن منتج',
        'story_index': 2,
        'description': 'createProduct يجب أن تُرجع كائناً بالحقول المتوقعة.',
        'test_code': (
            'const product = createProduct(1, "Notebook", 12.5, "stationery", true);\n'
            'if (!product || product.id !== 1 || product.name !== "Notebook" '
            '|| product.price !== 12.5) throw new Error("product");\n'
            'if (product.category !== "stationery" || product.inStock !== true) '
            'throw new Error("fields");'
        ),
        'success_message': 'createProduct تُرجع شكل المنتج المتوقع.',
        'failure_message': 'أرجع كائناً يحوي id و name و price و category و inStock.',
    },
    {
        'name': '3. createProduct ترفض السعر السالب',
        'story_index': 2,
        'description': 'createProduct يجب أن ترمي خطأ عندما يكون السعر سالباً.',
        'test_code': (
            'let failed = false;\n'
            'try { createProduct(9, "Bad", -1, "home", true); } catch (e) { failed = true; }\n'
            'if (!failed) throw new Error("negative-price");'
        ),
        'success_message': 'createProduct تتحقق من السعر.',
        'failure_message': 'ارمِ خطأ إذا كان price أقل من 0.',
    },
    {
        'name': '4. formatPrice تنسّق القيم بـ $',
        'story_index': 2,
        'description': 'formatPrice يجب أن تُرجع نص سعر منسّق مع رمز الدولار.',
        'test_code': (
            'const formatted = formatPrice(12.5);\n'
            'if (!formatted || !formatted.includes("12.50") || !formatted.includes("$")) '
            'throw new Error("format");'
        ),
        'success_message': 'formatPrice تنسّق الأسعار بشكل صحيح.',
        'failure_message': 'أرجع نص سعر مثل $12.50 بخانتين عشريتين.',
    },
    {
        'name': '5. filterProductsByCategory تصفّي المنتجات',
        'story_index': 3,
        'description': 'filterProductsByCategory يجب أن تُرجع المنتجات المطابقة فقط.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "Pen", 2, "stationery", true),\n'
            '  createProduct(2, "Mug", 8, "home", true),\n'
            '  createProduct(3, "Marker", 3, "stationery", false),\n'
            '];\n'
            'const filtered = filterProductsByCategory(products, "stationery");\n'
            'if (filtered.length !== 2 || filtered.some((p) => p.category !== "stationery")) '
            'throw new Error("filter");'
        ),
        'success_message': 'filterProductsByCategory تعمل بشكل صحيح.',
        'failure_message': 'أرجع فقط المنتجات في الفئة المطلوبة.',
    },
    {
        'name': '6. التصفية لا تعدّل المصفوفة الأصلية',
        'story_index': 3,
        'description': 'filterProductsByCategory يجب ألا تعدّل المصفوفة الأصلية.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "Pen", 2, "stationery", true),\n'
            '  createProduct(2, "Mug", 8, "home", true),\n'
            '];\n'
            'const before = products.length;\n'
            'filterProductsByCategory(products, "stationery");\n'
            'if (products.length !== before) throw new Error("mutated");'
        ),
        'success_message': 'التصفية لا تعدّل المصدر.',
        'failure_message': 'لا تعدّل مصفوفة products الأصلية عند التصفية.',
    },
    {
        'name': '7. sortProductsByPrice تصاعدياً',
        'story_index': 3,
        'description': 'sortProductsByPrice يجب أن ترتّب المنتجات تصاعدياً حسب السعر.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "B", 30, "home", true),\n'
            '  createProduct(2, "A", 10, "home", true),\n'
            '  createProduct(3, "C", 20, "home", true),\n'
            '];\n'
            'const sorted = sortProductsByPrice(products, "asc");\n'
            'if (sorted[0].price !== 10 || sorted[2].price !== 30) throw new Error("asc");'
        ),
        'success_message': 'الترتيب التصاعدي للسعر يعمل.',
        'failure_message': 'رتّب المنتجات من الأقل سعراً إلى الأعلى.',
    },
    {
        'name': '8. sortProductsByPrice تنازلياً',
        'story_index': 3,
        'description': 'sortProductsByPrice يجب أن ترتّب المنتجات تنازلياً حسب السعر.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "B", 30, "home", true),\n'
            '  createProduct(2, "A", 10, "home", true),\n'
            '  createProduct(3, "C", 20, "home", true),\n'
            '];\n'
            'const originalFirst = products[0].price;\n'
            'const sorted = sortProductsByPrice(products, "desc");\n'
            'if (sorted[0].price !== 30 || sorted[2].price !== 10) throw new Error("desc");\n'
            'if (products[0].price !== originalFirst) throw new Error("mutated");'
        ),
        'success_message': 'الترتيب التنازلي يعمل دون تعديل المصدر.',
        'failure_message': 'رتّب تنازلياً دون تعديل المصفوفة الأصلية.',
    },
    {
        'name': '9. getInStockCount تعدّ المتوفر',
        'story_index': 4,
        'description': 'getInStockCount يجب أن تعدّ المنتجات المتوفرة فقط.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "A", 10, "home", true),\n'
            '  createProduct(2, "B", 20, "home", false),\n'
            '  createProduct(3, "C", 30, "home", true),\n'
            '];\n'
            'if (getInStockCount(products) !== 2) throw new Error("stock");'
        ),
        'success_message': 'getInStockCount تعمل بشكل صحيح.',
        'failure_message': 'عدّ فقط المنتجات حيث inStock صحيح.',
    },
    {
        'name': '10. renderEmptyState تعرض حالة الفراغ',
        'story_index': 4,
        'description': 'renderEmptyState يجب أن تُرجع JSX لكتالوج فارغ.',
        'test_code': (
            'const jsx = renderEmptyState("No products found");\n'
            'if (!jsx.includes("empty-state") || !jsx.includes("No products found")) '
            'throw new Error("empty");'
        ),
        'success_message': 'renderEmptyState تعمل بشكل صحيح.',
        'failure_message': 'أرجع JSX بالصنف empty-state والرسالة المعطاة.',
    },
    {
        'name': '11. ProductCard تتضمن product-card',
        'story_index': 5,
        'description': 'ProductCard يجب أن تُرجع JSX يحوي product-card.',
        'test_code': (
            'const jsx = ProductCard({ name: "Notebook", price: 12.5, category: "stationery", inStock: true });\n'
            'if (!jsx.includes("product-card")) throw new Error("card");'
        ),
        'success_message': 'ProductCard تتضمن product-card.',
        'failure_message': 'غلّف كل منتج بعنصر بالصنف product-card.',
    },
    {
        'name': '12. ProductCard تعرض تفاصيل المنتج والسعر',
        'story_index': 5,
        'description': 'ProductCard يجب أن تعرض الاسم والسعر المنسّق والفئة.',
        'test_code': (
            'const jsx = ProductCard({ name: "Notebook", price: 12.5, category: "stationery", inStock: true });\n'
            'if (!jsx.includes("Notebook") || !jsx.includes("stationery")) throw new Error("details");\n'
            'if (!jsx.includes("product-name") || !jsx.includes("product-price") '
            '|| !jsx.includes("product-category")) throw new Error("classes");\n'
            'if (!jsx.includes("12.50")) throw new Error("price-format");'
        ),
        'success_message': 'ProductCard تعرض تفاصيل المنتج والسعر.',
        'failure_message': 'اعرض الاسم والسعر المنسّق والفئة بالأصناف المطلوبة.',
    },
    {
        'name': '13. ProductCard تعرض شارة المخزون',
        'story_index': 5,
        'description': 'ProductCard يجب أن تعرض شارة in-stock أو out-of-stock.',
        'test_code': (
            'const inStock = ProductCard({ name: "Pen", price: 2, category: "stationery", inStock: true });\n'
            'const outStock = ProductCard({ name: "Pen", price: 2, category: "stationery", inStock: false });\n'
            'if (!inStock.includes("in-stock") || !outStock.includes("out-of-stock")) '
            'throw new Error("badge");'
        ),
        'success_message': 'ProductCard تعرض شارات المخزون بشكل صحيح.',
        'failure_message': 'استخدم الصنفين in-stock و out-of-stock لشارة المخزون.',
    },
    {
        'name': '14. ProductList تعرض product-list',
        'story_index': 6,
        'description': 'ProductList يجب أن تُرجع JSX بالصنف product-list.',
        'test_code': (
            'const products = [createProduct(1, "Pen", 2, "stationery", true)];\n'
            'const jsx = ProductList({ products });\n'
            'if (!jsx.includes("product-list")) throw new Error("list");'
        ),
        'success_message': 'ProductList تتضمن product-list.',
        'failure_message': 'غلّف المنتجات المعروضة بعنصر بالصنف product-list.',
    },
    {
        'name': '15. ProductList تعرض عدة بطاقات',
        'story_index': 6,
        'description': 'ProductList يجب أن تعرض بطاقة لكل منتج.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "Pen", 2, "stationery", true),\n'
            '  createProduct(2, "Mug", 8, "home", true),\n'
            '];\n'
            'const jsx = ProductList({ products });\n'
            'if ((jsx.match(/product-card/g) || []).length < 2) throw new Error("cards");'
        ),
        'success_message': 'ProductList تعرض كل بطاقات المنتجات.',
        'failure_message': 'اعرض ProductCard لكل منتج.',
    },
    {
        'name': '16. ProductList تعرض حالة الفراغ',
        'story_index': 6,
        'description': 'ProductList يجب أن تعرض empty-state عندما لا توجد منتجات.',
        'test_code': (
            'const jsx = ProductList({ products: [] });\n'
            'if (!jsx.includes("empty-state")) throw new Error("empty-list");'
        ),
        'success_message': 'ProductList تتعامل مع القائمة الفارغة.',
        'failure_message': 'أرجع renderEmptyState عندما تكون products فارغة.',
    },
    {
        'name': '17. CatalogHeader تعرض أصناف الرأس',
        'story_index': 7,
        'description': 'CatalogHeader يجب أن تُرجع HTML الرأس المطلوب.',
        'test_code': (
            'const jsx = CatalogHeader({ title: "Shop", subtitle: "Fresh picks", productCount: 4 });\n'
            'if (!jsx.includes("catalog-header") || !jsx.includes("catalog-title")) '
            'throw new Error("header");\n'
            'if (!jsx.includes("catalog-subtitle") || !jsx.includes("catalog-count")) '
            'throw new Error("meta");\n'
            'if (!jsx.includes("Shop") || !jsx.includes("Fresh picks") || !jsx.includes("4")) '
            'throw new Error("content");'
        ),
        'success_message': 'CatalogHeader تعرض الرأس المطلوب.',
        'failure_message': 'ضمّن catalog-header و catalog-title و catalog-subtitle و catalog-count.',
    },
    {
        'name': '18. CatalogPage تركّب الصفحة',
        'story_index': 8,
        'description': 'CatalogPage يجب أن تُرجع JSX بالصنف catalog-page.',
        'test_code': (
            'const products = [createProduct(1, "Pen", 2, "stationery", true)];\n'
            'const jsx = CatalogPage({ products, title: "Shop", subtitle: "Daily essentials" });\n'
            'if (!jsx.includes("catalog-page")) throw new Error("page");\n'
            'if (!jsx.includes("catalog-header") || !jsx.includes("product-list")) '
            'throw new Error("composition");\n'
            'if (!jsx.includes("1")) throw new Error("count");'
        ),
        'success_message': 'CatalogPage تركّب تخطيط الكتالوج.',
        'failure_message': 'ادمج الرأس وقائمة المنتجات داخل catalog-page مع العدد.',
    },
    {
        'name': '19. getCatalogStyles تنسّق العناصر الأساسية',
        'story_index': 9,
        'description': 'getCatalogStyles يجب أن تشمل قواعد الصفحة والرأس والقائمة.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes(".catalog-page") || !styles.includes(".catalog-header")) '
            'throw new Error("page-style");\n'
            'if (!styles.includes(".product-list") || !styles.includes(".product-card")) '
            'throw new Error("list-style");\n'
            'if (!styles.includes(".empty-state")) throw new Error("empty-style");'
        ),
        'success_message': 'getCatalogStyles تتضمن القواعد الأساسية.',
        'failure_message': 'أضف قواعد .catalog-page و .catalog-header و .product-list و .product-card و .empty-state.',
    },
    {
        'name': '20. getCatalogStyles تستخدم grid أو flex',
        'story_index': 9,
        'description': 'getCatalogStyles يجب أن تستخدم Grid أو Flexbox للتخطيط.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes("grid") && !styles.includes("flex")) throw new Error("layout");'
        ),
        'success_message': 'getCatalogStyles تتضمن تخطيطاً حديثاً.',
        'failure_message': 'استخدم CSS Grid أو Flexbox في أنماط الكتالوج.',
    },
    {
        'name': '21. getCatalogStyles تنسّق شارات المخزون',
        'story_index': 9,
        'description': 'getCatalogStyles يجب أن تنسّق شارات in-stock و out-of-stock.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes(".in-stock") || !styles.includes(".out-of-stock")) '
            'throw new Error("badges");'
        ),
        'success_message': 'أنماط شارات المخزون معرّفة.',
        'failure_message': 'أضف قواعد CSS لـ .in-stock و .out-of-stock.',
    },
    {
        'name': '22. CatalogPage جاهزة للدمج مع منتجات تجريبية',
        'story_index': 10,
        'description': 'CatalogPage يجب أن تعمل مع 3 منتجات من فئتين على الأقل.',
        'test_code': (
            'if (typeof CatalogPage !== "function") throw new Error("missing-catalog");\n'
            'const sample = [\n'
            '  createProduct(1, "Pen", 2, "stationery", true),\n'
            '  createProduct(2, "Mug", 8, "home", true),\n'
            '  createProduct(3, "Notebook", 12.5, "stationery", false),\n'
            '];\n'
            'const jsx = CatalogPage({ products: sample, title: "Shop", subtitle: "Demo" });\n'
            'if ((jsx.match(/product-card/g) || []).length < 3) throw new Error("samples");\n'
            'if (!jsx.includes("stationery") || !jsx.includes("home")) throw new Error("categories");'
        ),
        'success_message': 'CatalogPage جاهزة للدمج مع منتجات تجريبية.',
        'failure_message': 'تأكد من عمل CatalogPage مع 3 منتجات من فئتين على الأقل.',
    },
]
