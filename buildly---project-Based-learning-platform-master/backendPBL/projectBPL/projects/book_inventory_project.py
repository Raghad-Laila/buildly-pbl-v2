"""Book Inventory project definition for Frontend Mastery."""

BOOK_INVENTORY_TITLE = 'Build a Book Inventory App'

BOOK_INVENTORY_PROJECT = {
    'title': BOOK_INVENTORY_TITLE,
    'level': 'beginner',
    'languages': ['html', 'css'],
    'estimated_time': 5,
    'description': (
        'Build an app that is functionally similar to the example project in the start file. '
        'Try not to copy the example project, give it your own personal style.'
    ),
    'objectives': (
        'Fulfill the user stories below and get all the tests to pass to complete the lab.'
    ),
    'stories': [
        {
            'title': 'Page heading',
            'description': (
                'You should have an h1 element with the text Book Inventory, and only one h1 '
                'element on the page.'
            ),
            'hint': 'Add a single <h1>Book Inventory</h1> at the top of your page.',
        },
        {
            'title': 'Table structure',
            'description': (
                'You should have a table element with one thead and one tbody. Inside thead, '
                'include one tr with five th elements named Title, Author, Category, Status, '
                'and Rate.'
            ),
            'hint': (
                'Build <table><thead><tr><th>Title</th>... with all five column headings, '
                'then add <tbody> for your book rows.'
            ),
        },
        {
            'title': 'Table rows and columns',
            'description': (
                'Your table should have at least four rows total (one heading row plus at least '
                'three book rows). Each tbody row should have exactly five columns.'
            ),
            'hint': 'Add at least three tr elements inside tbody, each with five td cells.',
        },
        {
            'title': 'Row status classes',
            'description': (
                'Each table row inside the table body should have either the class read, '
                'to-read, or in-progress.'
            ),
            'hint': (
                'Use <tr class="read">, <tr class="to-read">, or <tr class="in-progress"> '
                'on every tbody row.'
            ),
        },
        {
            'title': 'Status column markup',
            'description': (
                'td elements in the Status column should contain a span element with the class '
                'status surrounding the text Read, To Read, or In Progress, depending on the '
                'class of that row.'
            ),
            'hint': (
                'In the fourth column, wrap status text in '
                '<span class="status">Read</span>, <span class="status">To Read</span>, or '
                '<span class="status">In Progress</span>.'
            ),
        },
        {
            'title': 'Rate column markup',
            'description': (
                'td elements in the Rate column should contain a span element with the class '
                'rate wrapping three empty span elements.'
            ),
            'hint': (
                'In the last column, use '
                '<span class="rate"><span></span><span></span><span></span></span>.'
            ),
        },
        {
            'title': 'Read row ratings',
            'description': (
                'rate elements placed inside read rows should have an additional class with '
                'the value of either one, two, or three, depending on the personal rate. '
                'This value should come after rate.'
            ),
            'hint': (
                'On read rows only, add a second class such as '
                '<span class="rate one">, <span class="rate two">, or <span class="rate three">.'
            ),
        },
        {
            'title': 'Row background gradients',
            'description': (
                'Create three attribute selectors to target rows with the classes read, to-read, '
                'and in-progress, and set their background-image property to use a linear-gradient '
                'of your choice.'
            ),
            'hint': (
                'Use selectors like tr[class="read"], tr[class="to-read"], and '
                'tr[class="in-progress"] with background-image: linear-gradient(...).'
            ),
        },
        {
            'title': 'Span display and status styling',
            'description': (
                'Set the display property of each span element to inline-block. Use attribute '
                'selectors to target status spans that are descendants of read, to-read, and '
                'in-progress rows, and set their border and background-image properties.'
            ),
            'hint': (
                'Add span { display: inline-block; } and rules such as '
                'tr[class="read"] span[class="status"] { border: ...; background-image: ...; }.'
            ),
        },
        {
            'title': 'Status and rate sizing',
            'description': (
                'Use an attribute selector to target span elements with the class status and '
                'span elements whose class value starts with rate, then set their height, width, '
                'and padding properties.'
            ),
            'hint': (
                'Style span[class="status"] and span[class^="rate"] with height, width, '
                'and padding in the same rule or separate rules.'
            ),
        },
        {
            'title': 'Rate dot styling',
            'description': (
                'Use an attribute selector to target span elements that are direct children of '
                'span elements whose class value starts with rate, and set their border, '
                'border-radius, margin, height, width, and background-color properties.'
            ),
            'hint': (
                'Target span[class^="rate"] > span and style the empty rating dots as small '
                'circles or squares.'
            ),
        },
        {
            'title': 'Rating gradient fills',
            'description': (
                'Use attribute selectors to style rating dots with linear-gradient fills: target '
                'the first descendant of spans whose class contains the word one, the first two '
                'descendants of spans whose class contains the word two, and all three descendant '
                'spans of spans whose class contains the word three.'
            ),
            'hint': (
                'Use [class~="one"], [class~="two"], and [class~="three"] with descendant '
                'selectors such as span[class~="one"] :first-child and '
                'span[class~="three"] span.'
            ),
        },
    ],
}

BOOK_INVENTORY_TESTS = [
    {
        'name': '1. h1 text is Book Inventory',
        'description': 'You should have an h1 element with the text Book Inventory.',
        'test_code': (
            'const h1 = getDoc().querySelector("h1");\n'
            'if (!h1 || getText(h1) !== "Book Inventory") throw new Error("h1");'
        ),
        'success_message': 'h1 displays Book Inventory.',
        'failure_message': 'Add <h1>Book Inventory</h1> to your page.',
    },
    {
        'name': '2. Only one h1 element',
        'description': 'You should have only one h1 element.',
        'test_code': (
            'if (getDoc().querySelectorAll("h1").length !== 1) throw new Error("count");'
        ),
        'success_message': 'The page has exactly one h1.',
        'failure_message': 'Use only one h1 element on the page.',
    },
    {
        'name': '3. table element exists',
        'description': 'You should have a table element.',
        'test_code': (
            'if (getDoc().querySelectorAll("table").length !== 1) throw new Error("table");'
        ),
        'success_message': 'A table element is present.',
        'failure_message': 'Add a <table> element to your page.',
    },
    {
        'name': '4. thead and tbody inside table',
        'description': 'You should have one thead element and one tbody element inside table.',
        'test_code': (
            'if (getDoc().querySelectorAll("table > thead").length !== 1) '
            'throw new Error("thead");\n'
            'if (getDoc().querySelectorAll("table > tbody").length !== 1) '
            'throw new Error("tbody");'
        ),
        'success_message': 'table contains thead and tbody.',
        'failure_message': 'Add one <thead> and one <tbody> as direct children of table.',
    },
    {
        'name': '5. thead has one tr with 5 th elements',
        'description': 'Inside thead there should be one tr with 5 th elements.',
        'test_code': (
            'if (getDoc().querySelectorAll("table > thead > tr").length !== 1) '
            'throw new Error("tr");\n'
            'if (getDoc().querySelectorAll("table > thead > tr > th").length !== 5) '
            'throw new Error("th");'
        ),
        'success_message': 'thead has one row with five th elements.',
        'failure_message': 'Add one tr with five th elements inside thead.',
    },
    {
        'name': '6. First column heading is Title',
        'description': 'Your first column should have the text Title as the heading.',
        'test_code': (
            'const headings = getTableHeadings();\n'
            'if (headings[0] !== "Title") throw new Error("title");'
        ),
        'success_message': 'First column heading is Title.',
        'failure_message': 'Set the first th text to Title.',
    },
    {
        'name': '7. Second column heading is Author',
        'description': 'Your second column should have the text Author as the heading.',
        'test_code': (
            'const headings = getTableHeadings();\n'
            'if (headings[1] !== "Author") throw new Error("author");'
        ),
        'success_message': 'Second column heading is Author.',
        'failure_message': 'Set the second th text to Author.',
    },
    {
        'name': '8. Third column heading is Category',
        'description': 'Your third column should have the text Category as the heading.',
        'test_code': (
            'const headings = getTableHeadings();\n'
            'if (headings[2] !== "Category") throw new Error("category");'
        ),
        'success_message': 'Third column heading is Category.',
        'failure_message': 'Set the third th text to Category.',
    },
    {
        'name': '9. Fourth column heading is Status',
        'description': 'Your fourth column should have the text Status as the heading.',
        'test_code': (
            'const headings = getTableHeadings();\n'
            'if (headings[3] !== "Status") throw new Error("status");'
        ),
        'success_message': 'Fourth column heading is Status.',
        'failure_message': 'Set the fourth th text to Status.',
    },
    {
        'name': '10. Fifth column heading is Rate',
        'description': 'Your fifth column should have the text Rate as the heading.',
        'test_code': (
            'const headings = getTableHeadings();\n'
            'if (headings[4] !== "Rate") throw new Error("rate");'
        ),
        'success_message': 'Fifth column heading is Rate.',
        'failure_message': 'Set the fifth th text to Rate.',
    },
    {
        'name': '11. Table has at least 4 rows',
        'description': 'Your table should have at least four rows.',
        'test_code': (
            'if (getDoc().querySelectorAll("tr").length < 4) throw new Error("rows");'
        ),
        'success_message': 'The table has at least four rows.',
        'failure_message': 'Add at least four tr elements (heading row plus three book rows).',
    },
    {
        'name': '12. Each tbody row has 5 columns',
        'description': 'Each row should always have 5 columns.',
        'test_code': (
            'const rows = getTableBodyRows();\n'
            'if (!rows.length) throw new Error("rows");\n'
            'for (const row of rows) {\n'
            '  if (row.children.length !== 5) throw new Error("columns");\n'
            '}'
        ),
        'success_message': 'Every tbody row has five columns.',
        'failure_message': 'Each tbody tr must contain exactly five td elements.',
    },
    {
        'name': '13. tbody rows use read, to-read, or in-progress',
        'description': (
            'Each table row inside the table body should have either the class read, '
            'to-read, or in-progress.'
        ),
        'test_code': (
            'const rows = getTableBodyRows();\n'
            'if (!rows.length) throw new Error("rows");\n'
            'const allowed = ["read", "to-read", "in-progress"];\n'
            'for (const row of rows) {\n'
            '  const match = allowed.some((name) => row.classList.contains(name));\n'
            '  if (!match) throw new Error("class");\n'
            '}'
        ),
        'success_message': 'Every tbody row has a valid status class.',
        'failure_message': (
            'Give each tbody tr one of these classes: read, to-read, or in-progress.'
        ),
    },
    {
        'name': '14. Status column cells contain span elements',
        'description': 'td elements of the Status column should contain a span element.',
        'test_code': (
            'const cells = getDoc().querySelectorAll("tbody tr td:nth-child(4)");\n'
            'if (!cells.length) throw new Error("cells");\n'
            'for (const cell of cells) {\n'
            '  if (!cell.children[0] || cell.children[0].tagName.toLowerCase() !== "span") '
            'throw new Error("span");\n'
            '}'
        ),
        'success_message': 'Status column cells contain span elements.',
        'failure_message': 'Wrap each Status column value in a span element.',
    },
    {
        'name': '15. Status spans have class status',
        'description': 'Each span element of the Status column should have the class of status.',
        'test_code': (
            'const spans = getDoc().querySelectorAll("tbody tr td:nth-child(4) > span");\n'
            'if (!spans.length) throw new Error("spans");\n'
            'for (const span of spans) {\n'
            '  if (!span.classList.contains("status")) throw new Error("status");\n'
            '}'
        ),
        'success_message': 'Status spans use the status class.',
        'failure_message': 'Add class="status" to each Status column span.',
    },
    {
        'name': '16. Status text matches row class',
        'description': (
            'Each status element should have the text Read, To Read, or In Progress, '
            'depending on the class of its row.'
        ),
        'test_code': (
            'const rows = getTableBodyRows();\n'
            'if (!rows.length) throw new Error("rows");\n'
            'for (const row of rows) {\n'
            '  const span = row.querySelector("td:nth-child(4) > span");\n'
            '  if (!span) throw new Error("span");\n'
            '  const text = getText(span);\n'
            '  if (text === "Read" && !row.classList.contains("read")) throw new Error("read");\n'
            '  if (text === "To Read" && !row.classList.contains("to-read")) '
            'throw new Error("to-read");\n'
            '  if (text === "In Progress" && !row.classList.contains("in-progress")) '
            'throw new Error("in-progress");\n'
            '  if (!["Read", "To Read", "In Progress"].includes(text)) throw new Error("text");\n'
            '}'
        ),
        'success_message': 'Status text matches each row class.',
        'failure_message': (
            'Use Read for read rows, To Read for to-read rows, and In Progress for in-progress rows.'
        ),
    },
    {
        'name': '17. Rate column cells contain span elements',
        'description': 'td elements of the Rate column should contain a span element.',
        'test_code': (
            'const cells = getDoc().querySelectorAll("tbody tr td:last-child");\n'
            'if (!cells.length) throw new Error("cells");\n'
            'for (const cell of cells) {\n'
            '  if (!cell.children[0] || cell.children[0].tagName.toLowerCase() !== "span") '
            'throw new Error("span");\n'
            '}'
        ),
        'success_message': 'Rate column cells contain span elements.',
        'failure_message': 'Wrap each Rate column value in a span element.',
    },
    {
        'name': '18. Rate spans use rate as first class',
        'description': (
            'Each span element which is a direct child of a td element of the Rate column '
            'should have the class of rate as the first class.'
        ),
        'test_code': (
            'const spans = getDoc().querySelectorAll("tbody tr td:last-child > span:first-child");\n'
            'if (!spans.length) throw new Error("spans");\n'
            'for (const span of spans) {\n'
            '  if (span.classList[0] !== "rate") throw new Error("rate");\n'
            '}'
        ),
        'success_message': 'Rate spans use rate as their first class.',
        'failure_message': 'Make rate the first class on each Rate column span.',
    },
    {
        'name': '19. Each rate span has 3 empty child spans',
        'description': 'Each rate element should contain three empty span elements.',
        'test_code': (
            'const rates = getDoc().getElementsByClassName("rate");\n'
            'if (!rates.length) throw new Error("rates");\n'
            'for (const rate of rates) {\n'
            '  if (rate.children.length !== 3) throw new Error("count");\n'
            '  for (const child of rate.children) {\n'
            '    if (child.tagName.toLowerCase() !== "span") throw new Error("tag");\n'
            '    if (getText(child)) throw new Error("empty");\n'
            '  }\n'
            '}'
        ),
        'success_message': 'Each rate span wraps three empty child spans.',
        'failure_message': (
            'Inside each .rate span, add three empty child <span></span> elements.'
        ),
    },
    {
        'name': '20. Read row rate spans include one, two, or three',
        'description': (
            'rate elements placed inside read rows should have an additional class after rate '
            'with the value of either one, two, or three.'
        ),
        'test_code': (
            'const rates = getDoc().querySelectorAll(".read .rate");\n'
            'if (!rates.length) throw new Error("rates");\n'
            'const allowed = ["one", "two", "three"];\n'
            'for (const rate of rates) {\n'
            '  if (!allowed.includes(rate.classList[1])) throw new Error("rating");\n'
            '}'
        ),
        'success_message': 'Read row rate spans include one, two, or three.',
        'failure_message': (
            'On read rows, add a second class of one, two, or three to each .rate span.'
        ),
    },
    {
        'name': '21. Attribute selector for read rows',
        'description': 'You should have an attribute selector to target rows that have the class of read.',
        'test_code': (
            'if (!cssHasRowAttrSelector("read")) throw new Error("selector");'
        ),
        'success_message': 'An attribute selector targets read rows.',
        'failure_message': 'Add a tr attribute selector for rows with class read.',
    },
    {
        'name': '22. Read rows use linear-gradient background-image',
        'description': (
            'You should use an attribute selector to target rows that have the class of read '
            'and set their background-image property to a linear gradient.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'tr[class="read"]\', "background-image", "linear-gradient")) '
            'throw new Error("gradient");'
        ),
        'success_message': 'Read rows use a linear-gradient background-image.',
        'failure_message': (
            'Set background-image: linear-gradient(...) on your read row attribute selector.'
        ),
    },
    {
        'name': '23. Attribute selector for to-read rows',
        'description': (
            'You should have an attribute selector to target rows that have the class of to-read.'
        ),
        'test_code': (
            'if (!cssHasRowAttrSelector("to-read")) throw new Error("selector");'
        ),
        'success_message': 'An attribute selector targets to-read rows.',
        'failure_message': 'Add a tr attribute selector for rows with class to-read.',
    },
    {
        'name': '24. to-read rows use linear-gradient background-image',
        'description': (
            'You should use an attribute selector to target rows that have the class of to-read '
            'and set their background-image property to a linear gradient.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'tr[class="to-read"]\', "background-image", "linear-gradient")) '
            'throw new Error("gradient");'
        ),
        'success_message': 'to-read rows use a linear-gradient background-image.',
        'failure_message': (
            'Set background-image: linear-gradient(...) on your to-read row attribute selector.'
        ),
    },
    {
        'name': '25. Attribute selector for in-progress rows',
        'description': (
            'You should have an attribute selector to target rows that have the class of in-progress.'
        ),
        'test_code': (
            'if (!cssHasRowAttrSelector("in-progress")) throw new Error("selector");'
        ),
        'success_message': 'An attribute selector targets in-progress rows.',
        'failure_message': 'Add a tr attribute selector for rows with class in-progress.',
    },
    {
        'name': '26. in-progress rows use linear-gradient background-image',
        'description': (
            'You should use an attribute selector to target rows that have the class of '
            'in-progress and set their background-image property to a linear gradient.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'tr[class="in-progress"]\', "background-image", "linear-gradient")) '
            'throw new Error("gradient");'
        ),
        'success_message': 'in-progress rows use a linear-gradient background-image.',
        'failure_message': (
            'Set background-image: linear-gradient(...) on your in-progress row attribute selector.'
        ),
    },
    {
        'name': '27. span display is inline-block',
        'description': 'You should set the display property of each span element to inline-block.',
        'test_code': (
            'if (!cssHasDeclaration("span", "display", "inline-block")) throw new Error("display");'
        ),
        'success_message': 'span elements use display: inline-block.',
        'failure_message': 'Set display: inline-block on your span selector.',
    },
    {
        'name': '28. to-read status descendant selector exists',
        'description': (
            'You should have an attribute selector to target the span elements with the class '
            'of status that are descendants of tr elements with the class of to-read.'
        ),
        'test_code': (
            'if (!cssHasAttributeSelector(\'tr[class="to-read"] span[class="status"]\')) '
            'throw new Error("selector");'
        ),
        'success_message': 'A to-read status descendant selector exists.',
        'failure_message': (
            'Add tr[class="to-read"] span[class="status"] to your CSS.'
        ),
    },
    {
        'name': '29. to-read status spans have border',
        'description': (
            'You should use an attribute selector to target status spans inside to-read rows '
            'and set their border property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'tr[class="to-read"] span[class="status"]\', "border")) '
            'throw new Error("border");'
        ),
        'success_message': 'to-read status spans have a border.',
        'failure_message': 'Set border on tr[class="to-read"] span[class="status"].',
    },
    {
        'name': '30. to-read status spans have background-image',
        'description': (
            'You should use an attribute selector to target status spans inside to-read rows '
            'and set their background-image property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'tr[class="to-read"] span[class="status"]\', "background-image")) '
            'throw new Error("background-image");'
        ),
        'success_message': 'to-read status spans have a background-image.',
        'failure_message': 'Set background-image on tr[class="to-read"] span[class="status"].',
    },
    {
        'name': '31. read status descendant selector exists',
        'description': (
            'You should have an attribute selector to target the span elements with the class '
            'of status that are descendants of tr elements with the class of read.'
        ),
        'test_code': (
            'if (!cssHasAttributeSelector(\'tr[class="read"] span[class="status"]\')) '
            'throw new Error("selector");'
        ),
        'success_message': 'A read status descendant selector exists.',
        'failure_message': 'Add tr[class="read"] span[class="status"] to your CSS.',
    },
    {
        'name': '32. read status spans have border',
        'description': (
            'You should use an attribute selector to target status spans inside read rows '
            'and set their border property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'tr[class="read"] span[class="status"]\', "border")) '
            'throw new Error("border");'
        ),
        'success_message': 'read status spans have a border.',
        'failure_message': 'Set border on tr[class="read"] span[class="status"].',
    },
    {
        'name': '33. read status spans have background-image',
        'description': (
            'You should use an attribute selector to target status spans inside read rows '
            'and set their background-image property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'tr[class="read"] span[class="status"]\', "background-image")) '
            'throw new Error("background-image");'
        ),
        'success_message': 'read status spans have a background-image.',
        'failure_message': 'Set background-image on tr[class="read"] span[class="status"].',
    },
    {
        'name': '34. in-progress status descendant selector exists',
        'description': (
            'You should have an attribute selector to target the span elements with the class '
            'of status that are descendants of tr elements with the class of in-progress.'
        ),
        'test_code': (
            'if (!cssHasAttributeSelector(\'tr[class="in-progress"] span[class="status"]\')) '
            'throw new Error("selector");'
        ),
        'success_message': 'An in-progress status descendant selector exists.',
        'failure_message': (
            'Add tr[class="in-progress"] span[class="status"] to your CSS.'
        ),
    },
    {
        'name': '35. in-progress status spans have border',
        'description': (
            'You should use an attribute selector to target status spans inside in-progress rows '
            'and set their border property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'tr[class="in-progress"] span[class="status"]\', "border")) '
            'throw new Error("border");'
        ),
        'success_message': 'in-progress status spans have a border.',
        'failure_message': 'Set border on tr[class="in-progress"] span[class="status"].',
    },
    {
        'name': '36. in-progress status spans have background-image',
        'description': (
            'You should use an attribute selector to target status spans inside in-progress rows '
            'and set their background-image property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'tr[class="in-progress"] span[class="status"]\', "background-image")) '
            'throw new Error("background-image");'
        ),
        'success_message': 'in-progress status spans have a background-image.',
        'failure_message': (
            'Set background-image on tr[class="in-progress"] span[class="status"].'
        ),
    },
    {
        'name': '37. status and rate attribute selectors exist',
        'description': (
            'You should have an attribute selector to target span elements with the class of '
            'status and span elements with the class value starting with rate.'
        ),
        'test_code': (
            'const hasCombined = cssHasAttributeSelector(\'span[class="status"], span[class^="rate"]\') '
            '|| cssHasAttributeSelector(\'span[class^="rate"], span[class="status"]\');\n'
            'const hasBoth = cssHasAttributeSelector(\'span[class="status"]\') '
            '&& cssHasAttributeSelector(\'span[class^="rate"]\');\n'
            'if (!hasCombined && !hasBoth) throw new Error("selector");'
        ),
        'success_message': 'Status and rate attribute selectors are present.',
        'failure_message': (
            'Add attribute selectors for span[class="status"] and span[class^="rate"].'
        ),
    },
    {
        'name': '38. status and rate spans have height',
        'description': (
            'You should use an attribute selector to target status spans and rate spans '
            'and set their height property.'
        ),
        'test_code': (
            'const hasHeight = cssAttrRuleHasProperty(\'span[class="status"], span[class^="rate"]\', "height") '
            '|| cssAttrRuleHasProperty(\'span[class^="rate"], span[class="status"]\', "height") '
            '|| (cssAttrRuleHasProperty(\'span[class="status"]\', "height") '
            '&& cssAttrRuleHasProperty(\'span[class^="rate"]\', "height"));\n'
            'if (!hasHeight) throw new Error("height");'
        ),
        'success_message': 'Status and rate spans have height set.',
        'failure_message': 'Set height on your status and rate span attribute selectors.',
    },
    {
        'name': '39. status and rate spans have width',
        'description': (
            'You should use an attribute selector to target status spans and rate spans '
            'and set their width property.'
        ),
        'test_code': (
            'const hasWidth = cssAttrRuleHasProperty(\'span[class="status"], span[class^="rate"]\', "width") '
            '|| cssAttrRuleHasProperty(\'span[class^="rate"], span[class="status"]\', "width") '
            '|| (cssAttrRuleHasProperty(\'span[class="status"]\', "width") '
            '&& cssAttrRuleHasProperty(\'span[class^="rate"]\', "width"));\n'
            'if (!hasWidth) throw new Error("width");'
        ),
        'success_message': 'Status and rate spans have width set.',
        'failure_message': 'Set width on your status and rate span attribute selectors.',
    },
    {
        'name': '40. status and rate spans have padding',
        'description': (
            'You should use an attribute selector to target status spans and rate spans '
            'and set their padding property.'
        ),
        'test_code': (
            'const hasPadding = cssAttrRuleHasProperty(\'span[class="status"], span[class^="rate"]\', "padding") '
            '|| cssAttrRuleHasProperty(\'span[class^="rate"], span[class="status"]\', "padding") '
            '|| (cssAttrRuleHasProperty(\'span[class="status"]\', "padding") '
            '&& cssAttrRuleHasProperty(\'span[class^="rate"]\', "padding"));\n'
            'if (!hasPadding) throw new Error("padding");'
        ),
        'success_message': 'Status and rate spans have padding set.',
        'failure_message': 'Set padding on your status and rate span attribute selectors.',
    },
    {
        'name': '41. rate child span attribute selector exists',
        'description': (
            'You should have an attribute selector to target span elements which are direct '
            'children of span elements with the class value starting with rate.'
        ),
        'test_code': (
            'if (!cssHasAttributeSelector(\'span[class^="rate"] > span\')) throw new Error("selector");'
        ),
        'success_message': 'A rate child span attribute selector exists.',
        'failure_message': 'Add span[class^="rate"] > span to your CSS.',
    },
    {
        'name': '42. rate child spans have border',
        'description': (
            'You should use an attribute selector to target direct child spans of rate spans '
            'and set their border property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'span[class^="rate"] > span\', "border")) '
            'throw new Error("border");'
        ),
        'success_message': 'Rate child spans have border set.',
        'failure_message': 'Set border on span[class^="rate"] > span.',
    },
    {
        'name': '43. rate child spans have border-radius',
        'description': (
            'You should use an attribute selector to target direct child spans of rate spans '
            'and set their border-radius property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'span[class^="rate"] > span\', "border-radius")) '
            'throw new Error("border-radius");'
        ),
        'success_message': 'Rate child spans have border-radius set.',
        'failure_message': 'Set border-radius on span[class^="rate"] > span.',
    },
    {
        'name': '44. rate child spans have margin',
        'description': (
            'You should use an attribute selector to target direct child spans of rate spans '
            'and set their margin property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'span[class^="rate"] > span\', "margin")) '
            'throw new Error("margin");'
        ),
        'success_message': 'Rate child spans have margin set.',
        'failure_message': 'Set margin on span[class^="rate"] > span.',
    },
    {
        'name': '45. rate child spans have height',
        'description': (
            'You should use an attribute selector to target direct child spans of rate spans '
            'and set their height property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'span[class^="rate"] > span\', "height")) '
            'throw new Error("height");'
        ),
        'success_message': 'Rate child spans have height set.',
        'failure_message': 'Set height on span[class^="rate"] > span.',
    },
    {
        'name': '46. rate child spans have width',
        'description': (
            'You should use an attribute selector to target direct child spans of rate spans '
            'and set their width property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'span[class^="rate"] > span\', "width")) '
            'throw new Error("width");'
        ),
        'success_message': 'Rate child spans have width set.',
        'failure_message': 'Set width on span[class^="rate"] > span.',
    },
    {
        'name': '47. rate child spans have background-color',
        'description': (
            'You should use an attribute selector to target direct child spans of rate spans '
            'and set their background-color property.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'span[class^="rate"] > span\', "background-color")) '
            'throw new Error("background-color");'
        ),
        'success_message': 'Rate child spans have background-color set.',
        'failure_message': 'Set background-color on span[class^="rate"] > span.',
    },
    {
        'name': '48. one rating first descendant selector exists',
        'description': (
            'You should have an attribute selector to target the first descendant of span '
            'elements that have the word one as a part of their class value.'
        ),
        'test_code': (
            'const oneSelectors = [\n'
            '  \'span[class~="one"] :first-child\',\n'
            '  \'span[class~="one"] :nth-child(1)\',\n'
            '  \'span[class~="one"] :first-of-type\',\n'
            '  \'span[class~="one"] span:first-child\',\n'
            '  \'span[class~="one"] span:nth-child(1)\',\n'
            '  \'span[class~="one"] span:first-of-type\',\n'
            '  \'span[class~="one"] > :first-child\',\n'
            '  \'span[class~="one"] > :nth-child(1)\',\n'
            '  \'span[class~="one"] > :first-of-type\',\n'
            '  \'span[class~="one"] > span:first-child\',\n'
            '  \'span[class~="one"] > span:nth-child(1)\',\n'
            '  \'span[class~="one"] > span:first-of-type\'\n'
            '];\n'
            'let foundOne = false;\n'
            'for (const selector of oneSelectors) {\n'
            '  if (cssHasAttributeSelector(selector)) { foundOne = true; break; }\n'
            '}\n'
            'if (!foundOne) throw new Error("selector");'
        ),
        'success_message': 'A one-rating first descendant selector exists.',
        'failure_message': (
            'Add an attribute selector such as span[class~="one"] :first-child.'
        ),
    },
    {
        'name': '49. one rating first descendant uses linear-gradient',
        'description': (
            'You should use an attribute selector to target the first descendant of span '
            'elements that have the word one as a part of their class value and set its '
            'background-image property to use a linear-gradient.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'class~="one"\', "background-image", "linear-gradient")) '
            'throw new Error("gradient");'
        ),
        'success_message': 'One-rating dots use a linear-gradient background-image.',
        'failure_message': (
            'Set background-image: linear-gradient(...) on your one-rating descendant selector.'
        ),
    },
    {
        'name': '50. two rating first two descendants selector exists',
        'description': (
            'You should have an attribute selector to target the first two descendants of span '
            'elements that have the word two as a part of their class value.'
        ),
        'test_code': (
            'const twoSelectors = [\n'
            '  \'span[class~="two"] :nth-child(1), span[class~="two"] :nth-child(2)\',\n'
            '  \'span[class~="two"] :first-child, span[class~="two"] :nth-child(2)\',\n'
            '  \'span[class~="two"] :nth-of-type(-n+2)\',\n'
            '  \'span[class~="two"] :nth-child(-n+2)\',\n'
            '  \'span[class~="two"] span:nth-child(1), span[class~="two"] span:nth-child(2)\',\n'
            '  \'span[class~="two"] span:first-child, span[class~="two"] span:nth-child(2)\',\n'
            '  \'span[class~="two"] span:nth-of-type(-n+2)\',\n'
            '  \'span[class~="two"] span:nth-child(-n+2)\',\n'
            '  \'span[class~="two"] > :nth-child(1), span[class~="two"] > :nth-child(2)\',\n'
            '  \'span[class~="two"] > :first-child, span[class~="two"] > :nth-child(2)\',\n'
            '  \'span[class~="two"] > :nth-of-type(-n+2)\',\n'
            '  \'span[class~="two"] > :nth-child(-n+2)\',\n'
            '  \'span[class~="two"] > span:nth-child(1), span[class~="two"] > span:nth-child(2)\',\n'
            '  \'span[class~="two"] > span:first-child, span[class~="two"] > span:nth-child(2)\',\n'
            '  \'span[class~="two"] > span:nth-of-type(-n+2)\',\n'
            '  \'span[class~="two"] > span:nth-child(-n+2)\'\n'
            '];\n'
            'let foundTwo = false;\n'
            'for (const selector of twoSelectors) {\n'
            '  if (cssHasAttributeSelector(selector)) { foundTwo = true; break; }\n'
            '}\n'
            'if (!foundTwo) throw new Error("selector");'
        ),
        'success_message': 'A two-rating first-two-descendants selector exists.',
        'failure_message': (
            'Add an attribute selector that targets the first two descendants of span[class~="two"].'
        ),
    },
    {
        'name': '51. two rating first two descendants use linear-gradient',
        'description': (
            'You should use an attribute selector to target the first two descendants of span '
            'elements that have the word two as a part of their class value and set their '
            'background-image property to use a linear-gradient.'
        ),
        'test_code': (
            'if (!cssAttrRuleHasProperty(\'class~="two"\', "background-image", "linear-gradient")) '
            'throw new Error("gradient");'
        ),
        'success_message': 'Two-rating dots use a linear-gradient background-image.',
        'failure_message': (
            'Set background-image: linear-gradient(...) on your two-rating descendant selector.'
        ),
    },
    {
        'name': '52. three rating descendant selector exists',
        'description': (
            'You should have an attribute selector to target the span elements that are '
            'descendants of span elements that have the word three as a part of their class value.'
        ),
        'test_code': (
            'const hasThree = cssHasAttributeSelector(\'span[class~="three"] span\') '
            '|| cssHasAttributeSelector(\'span[class~="three"] > span\');\n'
            'if (!hasThree) throw new Error("selector");'
        ),
        'success_message': 'A three-rating descendant selector exists.',
        'failure_message': (
            'Add span[class~="three"] span or span[class~="three"] > span to your CSS.'
        ),
    },
    {
        'name': '53. three rating descendants use linear-gradient',
        'description': (
            'You should use an attribute selector to target the span elements that are '
            'descendants of span elements that have the word three as a part of their class '
            'value and set their background-image property to use a linear-gradient.'
        ),
        'test_code': (
            'const hasGradient = cssAttrRuleHasProperty(\'span[class~="three"] span\', "background-image", "linear-gradient") '
            '|| cssAttrRuleHasProperty(\'span[class~="three"] > span\', "background-image", "linear-gradient") '
            '|| cssAttrRuleHasProperty(\'class~="three"\', "background-image", "linear-gradient");\n'
            'if (!hasGradient) throw new Error("gradient");'
        ),
        'success_message': 'Three-rating dots use a linear-gradient background-image.',
        'failure_message': (
            'Set background-image: linear-gradient(...) on your three-rating descendant selector.'
        ),
    },
]
