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
        'ابنِ واجهة كتالوج منتجات باستخدام React. أنشئ مكوّنات قابلة لإعادة الاستخدام، '
        'وصفِّ المنتجات ورتّبها، واعرض حالة المخزون، وصمّم تخطيط متجر أنيق باستخدام '
        'HTML و CSS و React معاً.'
    ),
    'objectives': (
        'صمّم كتالوج منتجات يعمل بـ React مع مكوّنات قابلة لإعادة الاستخدام ودوال مساعدة.'
    ),
    'stories': [
        {
            'title': 'دوال نموذج المنتج',
            'description': (
                'اكتب الدالتين createProduct(id, name, price, category, inStock) و '
                'formatPrice(price). يجب أن تُرجع formatPrice نصاً مثل $19.99.'
            ),
            'hint': 'أرجع كائن منتج ونسّق الأسعار بخانتين عشريتين.',
        },
        {
            'title': 'تصفية وترتيب المنتجات',
            'description': (
                'اكتب filterProductsByCategory(products, category) و '
                'sortProductsByPrice(products, direction) حيث direction تكون asc أو desc.'
            ),
            'hint': 'استخدم Array.filter و Array.sort دون تعديل المصفوفة الأصلية.',
        },
        {
            'title': 'حالات المخزون والفراغ',
            'description': (
                'اكتب getInStockCount(products) و renderEmptyState(message) للتعامل مع '
                'عدّاد المخزون وحالات الكتالوج الفارغ.'
            ),
            'hint': 'عدّ المنتجات حيث inStock صحيح وأرجع JSX لحالة الفراغ.',
        },
        {
            'title': 'مكوّن ProductCard',
            'description': (
                'اكتب ProductCard({ name, price, category, inStock }) لتُرجع JSX بالأصناف '
                'product-card و product-name و product-price و product-category وشارة مخزون.'
            ),
            'hint': 'استخدم صنف الشارة in-stock أو out-of-stock حسب inStock.',
        },
        {
            'title': 'مكوّن ProductList',
            'description': (
                'اكتب ProductList({ products }) لتُرجع JSX بالصنف product-list يعرض '
                'ProductCard لكل منتج.'
            ),
            'hint': 'مرّ على products واعرض ProductCard لكل عنصر.',
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
                'ProductList داخل غلاف بالصنف catalog-page.'
            ),
            'hint': 'ركّب مكوّني الرأس والقائمة في صفحة واحدة.',
        },
        {
            'title': 'ملف تنسيق الكتالوج',
            'description': (
                'اكتب getCatalogStyles() لتُرجع CSS لـ .catalog-page و .product-list و '
                '.product-card وحالات شارة المخزون. استخدم CSS Grid أو Flexbox للتخطيط.'
            ),
            'hint': 'أرجع template string بالمحدّدات وقواعد التخطيط المطلوبة.',
        },
        {
            'title': 'دمج تطبيق React',
            'description': (
                'في App.jsx اعرض CatalogPage بمنتجات تجريبية. في index.html و style.css '
                'اربط تطبيق React وطبّق أنماط الكتالوج.'
            ),
            'hint': 'ثبّت التطبيق داخل #root واحتفظ ببنية React الابتدائية.',
        },
    ],
}

PRODUCT_CATALOG_TESTS = [
    {
        'name': '1. createProduct تُرجع كائن منتج',
        'story_index': 1,
        'description': 'createProduct يجب أن تُرجع كائناً بالحقول المتوقعة.',
        'test_code': (
            'const product = createProduct(1, "Notebook", 12.5, "stationery", true);\n'
            'if (!product || product.name !== "Notebook" || product.price !== 12.5) '
            'throw new Error("product");\n'
            'if (product.category !== "stationery" || product.inStock !== true) '
            'throw new Error("fields");'
        ),
        'success_message': 'createProduct تُرجع شكل المنتج المتوقع.',
        'failure_message': 'أرجع كائناً يحوي id و name و price و category و inStock.',
    },
    {
        'name': '2. formatPrice تنسّق القيم',
        'story_index': 1,
        'description': 'formatPrice يجب أن تُرجع نص سعر منسّق.',
        'test_code': (
            'const formatted = formatPrice(12.5);\n'
            'if (!formatted || !formatted.includes("12.50")) throw new Error("format");'
        ),
        'success_message': 'formatPrice تنسّق الأسعار بشكل صحيح.',
        'failure_message': 'أرجع نص سعر بخانتين عشريتين.',
    },
    {
        'name': '3. filterProductsByCategory تصفّي المنتجات',
        'story_index': 2,
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
        'name': '4. sortProductsByPrice تصاعدياً',
        'story_index': 2,
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
        'name': '5. sortProductsByPrice تنازلياً',
        'story_index': 2,
        'description': 'sortProductsByPrice يجب أن ترتّب المنتجات تنازلياً حسب السعر.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "B", 30, "home", true),\n'
            '  createProduct(2, "A", 10, "home", true),\n'
            '  createProduct(3, "C", 20, "home", true),\n'
            '];\n'
            'const sorted = sortProductsByPrice(products, "desc");\n'
            'if (sorted[0].price !== 30 || sorted[2].price !== 10) throw new Error("desc");'
        ),
        'success_message': 'الترتيب التنازلي للسعر يعمل.',
        'failure_message': 'رتّب المنتجات من الأعلى سعراً إلى الأقل.',
    },
    {
        'name': '6. getInStockCount تعدّ المتوفر',
        'story_index': 3,
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
        'name': '7. ProductCard تتضمن product-card',
        'story_index': 4,
        'description': 'ProductCard يجب أن تُرجع JSX يحوي product-card.',
        'test_code': (
            'const jsx = ProductCard({ name: "Notebook", price: 12.5, category: "stationery", inStock: true });\n'
            'if (!jsx.includes("product-card")) throw new Error("card");'
        ),
        'success_message': 'ProductCard تتضمن product-card.',
        'failure_message': 'غلّف كل منتج بعنصر بالصنف product-card.',
    },
    {
        'name': '8. ProductCard تعرض تفاصيل المنتج',
        'story_index': 4,
        'description': 'ProductCard يجب أن تعرض الاسم والسعر والفئة.',
        'test_code': (
            'const jsx = ProductCard({ name: "Notebook", price: 12.5, category: "stationery", inStock: true });\n'
            'if (!jsx.includes("Notebook") || !jsx.includes("stationery")) throw new Error("details");\n'
            'if (!jsx.includes("product-name") || !jsx.includes("product-price")) '
            'throw new Error("classes");'
        ),
        'success_message': 'ProductCard تعرض تفاصيل المنتج.',
        'failure_message': 'اعرض الاسم والسعر والفئة بالأصناف المطلوبة.',
    },
    {
        'name': '9. ProductCard تعرض شارة المخزون',
        'story_index': 4,
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
        'name': '10. ProductList تعرض product-list',
        'story_index': 5,
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
        'name': '11. ProductList تعرض عدة بطاقات',
        'story_index': 5,
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
        'name': '12. CatalogHeader تعرض أصناف الرأس',
        'story_index': 6,
        'description': 'CatalogHeader يجب أن تُرجع HTML الرأس المطلوب.',
        'test_code': (
            'const jsx = CatalogHeader({ title: "Shop", subtitle: "Fresh picks", productCount: 4 });\n'
            'if (!jsx.includes("catalog-header") || !jsx.includes("catalog-title")) '
            'throw new Error("header");\n'
            'if (!jsx.includes("Shop") || !jsx.includes("4")) throw new Error("content");'
        ),
        'success_message': 'CatalogHeader تعرض الرأس المطلوب.',
        'failure_message': 'ضمّن catalog-header و catalog-title و catalog-subtitle و catalog-count.',
    },
    {
        'name': '13. renderEmptyState تعرض حالة الفراغ',
        'story_index': 3,
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
        'name': '14. CatalogPage تركّب الصفحة',
        'story_index': 7,
        'description': 'CatalogPage يجب أن تُرجع JSX بالصنف catalog-page.',
        'test_code': (
            'const products = [createProduct(1, "Pen", 2, "stationery", true)];\n'
            'const jsx = CatalogPage({ products, title: "Shop", subtitle: "Daily essentials" });\n'
            'if (!jsx.includes("catalog-page")) throw new Error("page");\n'
            'if (!jsx.includes("catalog-header") || !jsx.includes("product-list")) '
            'throw new Error("composition");'
        ),
        'success_message': 'CatalogPage تركّب تخطيط الكتالوج.',
        'failure_message': 'ادمج الرأس وقائمة المنتجات داخل catalog-page.',
    },
    {
        'name': '15. getCatalogStyles تنسّق catalog-page',
        'story_index': 8,
        'description': 'getCatalogStyles يجب أن تشمل قواعد catalog-page.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes(".catalog-page")) throw new Error("page-style");'
        ),
        'success_message': 'getCatalogStyles تتضمن catalog-page.',
        'failure_message': 'أضف قواعد CSS لـ .catalog-page.',
    },
    {
        'name': '16. getCatalogStyles تنسّق قائمة المنتجات',
        'story_index': 8,
        'description': 'getCatalogStyles يجب أن تشمل قواعد product-list و product-card.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes(".product-list") || !styles.includes(".product-card")) '
            'throw new Error("list-style");'
        ),
        'success_message': 'getCatalogStyles تنسّق القائمة والبطاقات.',
        'failure_message': 'أضف قواعد CSS لـ .product-list و .product-card.',
    },
    {
        'name': '17. getCatalogStyles تستخدم grid أو flex',
        'story_index': 8,
        'description': 'getCatalogStyles يجب أن تستخدم Grid أو Flexbox للتخطيط.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes("grid") && !styles.includes("flex")) throw new Error("layout");'
        ),
        'success_message': 'getCatalogStyles تتضمن تخطيطاً حديثاً.',
        'failure_message': 'استخدم CSS Grid أو Flexbox في أنماط الكتالوج.',
    },
    {
        'name': '18. getCatalogStyles تنسّق شارات المخزون',
        'story_index': 8,
        'description': 'getCatalogStyles يجب أن تنسّق شارات in-stock و out-of-stock.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes(".in-stock") || !styles.includes(".out-of-stock")) '
            'throw new Error("badges");'
        ),
        'success_message': 'أنماط شارات المخزون معرّفة.',
        'failure_message': 'أضف قواعد CSS لـ .in-stock و .out-of-stock.',
    },
]
