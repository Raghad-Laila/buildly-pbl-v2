"""Product Catalog expert React project for Frontend Mastery."""

PRODUCT_CATALOG_TITLE = 'Build a Product Catalog with React'

PRODUCT_CATALOG_PROJECT = {
    'title': PRODUCT_CATALOG_TITLE,
    'level': 'expert',
    'languages': ['react', 'javascript', 'html', 'css'],
    'estimated_time': 8,
    'description': (
        'Build a product catalog interface with React. Create reusable components, filter and '
        'sort products, display stock state, and design a polished storefront layout using '
        'HTML, CSS, and React together.'
    ),
    'objectives': (
        'Design a React-powered product catalog with reusable components and catalog utilities.'
    ),
    'stories': [
        {
            'title': 'Product model helpers',
            'description': (
                'Write createProduct(id, name, price, category, inStock) and formatPrice(price) '
                'utility functions. formatPrice should return a string like $19.99.'
            ),
            'hint': 'Return a product object and format prices with two decimal places.',
        },
        {
            'title': 'Filter and sort products',
            'description': (
                'Write filterProductsByCategory(products, category) and sortProductsByPrice(products, '
                'direction) where direction is asc or desc.'
            ),
            'hint': 'Use Array.filter and Array.sort without mutating the original array.',
        },
        {
            'title': 'Stock and empty states',
            'description': (
                'Write getInStockCount(products) and renderEmptyState(message) to handle inventory '
                'counts and empty catalog states.'
            ),
            'hint': 'Count products where inStock is true and return JSX for the empty state.',
        },
        {
            'title': 'ProductCard component',
            'description': (
                'Write ProductCard({ name, price, category, inStock }) to return JSX with classes '
                'product-card, product-name, product-price, product-category, and a stock badge.'
            ),
            'hint': 'Use a stock badge class in-stock or out-of-stock based on inStock.',
        },
        {
            'title': 'ProductList component',
            'description': (
                'Write ProductList({ products }) to return JSX with class product-list that renders '
                'a ProductCard for each product.'
            ),
            'hint': 'Map over products and render ProductCard for each item.',
        },
        {
            'title': 'Catalog header',
            'description': (
                'Write CatalogHeader({ title, subtitle, productCount }) to return JSX with '
                'catalog-header, catalog-title, catalog-subtitle, and catalog-count.'
            ),
            'hint': 'Display the title, subtitle, and total number of products.',
        },
        {
            'title': 'Catalog layout',
            'description': (
                'Write CatalogPage({ products, title, subtitle }) to combine CatalogHeader and '
                'ProductList inside a wrapper with class catalog-page.'
            ),
            'hint': 'Compose your header and list components into one page component.',
        },
        {
            'title': 'Catalog stylesheet',
            'description': (
                'Write getCatalogStyles() to return CSS for .catalog-page, .product-list, '
                '.product-card, and stock badge states. Use CSS Grid or Flexbox for the layout.'
            ),
            'hint': 'Return a template string with the required selectors and layout rules.',
        },
        {
            'title': 'React app integration',
            'description': (
                'In App.jsx, render CatalogPage with sample products. In index.html and style.css, '
                'wire the React app and apply your catalog styles.'
            ),
            'hint': 'Mount the app into #root and keep the starter React structure intact.',
        },
    ],
}

PRODUCT_CATALOG_TESTS = [
    {
        'name': '1. createProduct returns a product object',
        'story_index': 1,
        'description': 'createProduct should return an object with the expected fields.',
        'test_code': (
            'const product = createProduct(1, "Notebook", 12.5, "stationery", true);\n'
            'if (!product || product.name !== "Notebook" || product.price !== 12.5) '
            'throw new Error("product");\n'
            'if (product.category !== "stationery" || product.inStock !== true) '
            'throw new Error("fields");'
        ),
        'success_message': 'createProduct returns the expected product shape.',
        'failure_message': 'Return an object with id, name, price, category, and inStock.',
    },
    {
        'name': '2. formatPrice formats values',
        'story_index': 1,
        'description': 'formatPrice should return a formatted price string.',
        'test_code': (
            'const formatted = formatPrice(12.5);\n'
            'if (!formatted || !formatted.includes("12.50")) throw new Error("format");'
        ),
        'success_message': 'formatPrice formats prices correctly.',
        'failure_message': 'Return a price string with two decimal places.',
    },
    {
        'name': '3. filterProductsByCategory filters products',
        'story_index': 2,
        'description': 'filterProductsByCategory should return only matching products.',
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
        'success_message': 'filterProductsByCategory works correctly.',
        'failure_message': 'Return only products in the requested category.',
    },
    {
        'name': '4. sortProductsByPrice ascending',
        'story_index': 2,
        'description': 'sortProductsByPrice should sort products ascending by price.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "B", 30, "home", true),\n'
            '  createProduct(2, "A", 10, "home", true),\n'
            '  createProduct(3, "C", 20, "home", true),\n'
            '];\n'
            'const sorted = sortProductsByPrice(products, "asc");\n'
            'if (sorted[0].price !== 10 || sorted[2].price !== 30) throw new Error("asc");'
        ),
        'success_message': 'Ascending price sort works.',
        'failure_message': 'Sort products from lowest to highest price.',
    },
    {
        'name': '5. sortProductsByPrice descending',
        'story_index': 2,
        'description': 'sortProductsByPrice should sort products descending by price.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "B", 30, "home", true),\n'
            '  createProduct(2, "A", 10, "home", true),\n'
            '  createProduct(3, "C", 20, "home", true),\n'
            '];\n'
            'const sorted = sortProductsByPrice(products, "desc");\n'
            'if (sorted[0].price !== 30 || sorted[2].price !== 10) throw new Error("desc");'
        ),
        'success_message': 'Descending price sort works.',
        'failure_message': 'Sort products from highest to lowest price.',
    },
    {
        'name': '6. getInStockCount counts in-stock products',
        'story_index': 3,
        'description': 'getInStockCount should count only in-stock products.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "A", 10, "home", true),\n'
            '  createProduct(2, "B", 20, "home", false),\n'
            '  createProduct(3, "C", 30, "home", true),\n'
            '];\n'
            'if (getInStockCount(products) !== 2) throw new Error("stock");'
        ),
        'success_message': 'getInStockCount works correctly.',
        'failure_message': 'Count only products where inStock is true.',
    },
    {
        'name': '7. ProductCard includes product-card class',
        'story_index': 4,
        'description': 'ProductCard should return JSX containing product-card.',
        'test_code': (
            'const jsx = ProductCard({ name: "Notebook", price: 12.5, category: "stationery", inStock: true });\n'
            'if (!jsx.includes("product-card")) throw new Error("card");'
        ),
        'success_message': 'ProductCard includes product-card.',
        'failure_message': 'Wrap each product in an element with class product-card.',
    },
    {
        'name': '8. ProductCard shows product details',
        'story_index': 4,
        'description': 'ProductCard should show name, price, and category.',
        'test_code': (
            'const jsx = ProductCard({ name: "Notebook", price: 12.5, category: "stationery", inStock: true });\n'
            'if (!jsx.includes("Notebook") || !jsx.includes("stationery")) throw new Error("details");\n'
            'if (!jsx.includes("product-name") || !jsx.includes("product-price")) '
            'throw new Error("classes");'
        ),
        'success_message': 'ProductCard shows product details.',
        'failure_message': 'Display the name, price, and category with the required classes.',
    },
    {
        'name': '9. ProductCard shows stock badge',
        'story_index': 4,
        'description': 'ProductCard should render an in-stock or out-of-stock badge.',
        'test_code': (
            'const inStock = ProductCard({ name: "Pen", price: 2, category: "stationery", inStock: true });\n'
            'const outStock = ProductCard({ name: "Pen", price: 2, category: "stationery", inStock: false });\n'
            'if (!inStock.includes("in-stock") || !outStock.includes("out-of-stock")) '
            'throw new Error("badge");'
        ),
        'success_message': 'ProductCard renders stock badges correctly.',
        'failure_message': 'Use in-stock and out-of-stock classes for the stock badge.',
    },
    {
        'name': '10. ProductList renders product-list',
        'story_index': 5,
        'description': 'ProductList should return JSX with class product-list.',
        'test_code': (
            'const products = [createProduct(1, "Pen", 2, "stationery", true)];\n'
            'const jsx = ProductList({ products });\n'
            'if (!jsx.includes("product-list")) throw new Error("list");'
        ),
        'success_message': 'ProductList includes product-list.',
        'failure_message': 'Wrap the rendered products in an element with class product-list.',
    },
    {
        'name': '11. ProductList renders multiple cards',
        'story_index': 5,
        'description': 'ProductList should render a card for each product.',
        'test_code': (
            'const products = [\n'
            '  createProduct(1, "Pen", 2, "stationery", true),\n'
            '  createProduct(2, "Mug", 8, "home", true),\n'
            '];\n'
            'const jsx = ProductList({ products });\n'
            'if ((jsx.match(/product-card/g) || []).length < 2) throw new Error("cards");'
        ),
        'success_message': 'ProductList renders all product cards.',
        'failure_message': 'Render a ProductCard for every product.',
    },
    {
        'name': '12. CatalogHeader renders header classes',
        'story_index': 6,
        'description': 'CatalogHeader should return the required header markup.',
        'test_code': (
            'const jsx = CatalogHeader({ title: "Shop", subtitle: "Fresh picks", productCount: 4 });\n'
            'if (!jsx.includes("catalog-header") || !jsx.includes("catalog-title")) '
            'throw new Error("header");\n'
            'if (!jsx.includes("Shop") || !jsx.includes("4")) throw new Error("content");'
        ),
        'success_message': 'CatalogHeader renders the required header.',
        'failure_message': 'Include catalog-header, catalog-title, catalog-subtitle, and catalog-count.',
    },
    {
        'name': '13. renderEmptyState renders empty state',
        'story_index': 3,
        'description': 'renderEmptyState should return JSX for an empty catalog.',
        'test_code': (
            'const jsx = renderEmptyState("No products found");\n'
            'if (!jsx.includes("empty-state") || !jsx.includes("No products found")) '
            'throw new Error("empty");'
        ),
        'success_message': 'renderEmptyState renders correctly.',
        'failure_message': 'Return JSX with class empty-state and the provided message.',
    },
    {
        'name': '14. CatalogPage composes the page',
        'story_index': 7,
        'description': 'CatalogPage should return JSX with class catalog-page.',
        'test_code': (
            'const products = [createProduct(1, "Pen", 2, "stationery", true)];\n'
            'const jsx = CatalogPage({ products, title: "Shop", subtitle: "Daily essentials" });\n'
            'if (!jsx.includes("catalog-page")) throw new Error("page");\n'
            'if (!jsx.includes("catalog-header") || !jsx.includes("product-list")) '
            'throw new Error("composition");'
        ),
        'success_message': 'CatalogPage composes the catalog layout.',
        'failure_message': 'Combine the header and product list inside catalog-page.',
    },
    {
        'name': '15. getCatalogStyles styles catalog-page',
        'story_index': 8,
        'description': 'getCatalogStyles should include catalog-page rules.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes(".catalog-page")) throw new Error("page-style");'
        ),
        'success_message': 'getCatalogStyles includes catalog-page.',
        'failure_message': 'Add CSS rules for .catalog-page.',
    },
    {
        'name': '16. getCatalogStyles styles product list',
        'story_index': 8,
        'description': 'getCatalogStyles should include product-list and product-card rules.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes(".product-list") || !styles.includes(".product-card")) '
            'throw new Error("list-style");'
        ),
        'success_message': 'getCatalogStyles styles the product list and cards.',
        'failure_message': 'Add CSS rules for .product-list and .product-card.',
    },
    {
        'name': '17. getCatalogStyles uses grid or flex layout',
        'story_index': 8,
        'description': 'getCatalogStyles should use Grid or Flexbox for layout.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes("grid") && !styles.includes("flex")) throw new Error("layout");'
        ),
        'success_message': 'getCatalogStyles includes a modern layout.',
        'failure_message': 'Use CSS Grid or Flexbox in your catalog styles.',
    },
    {
        'name': '18. getCatalogStyles styles stock badges',
        'story_index': 8,
        'description': 'getCatalogStyles should style in-stock and out-of-stock badges.',
        'test_code': (
            'const styles = getCatalogStyles();\n'
            'if (!styles.includes(".in-stock") || !styles.includes(".out-of-stock")) '
            'throw new Error("badges");'
        ),
        'success_message': 'Stock badge styles are defined.',
        'failure_message': 'Add CSS rules for .in-stock and .out-of-stock.',
    },
]
