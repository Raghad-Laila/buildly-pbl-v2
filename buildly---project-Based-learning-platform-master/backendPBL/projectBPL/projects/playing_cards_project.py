"""Playing Cards project definition for Frontend Mastery."""

PLAYING_CARDS_TITLE = 'Build a Page of Playing Cards'

PLAYING_CARDS_PROJECT = {
    'title': PLAYING_CARDS_TITLE,
    'level': 'beginner',
    'languages': ['html', 'css'],
    'estimated_time': 4,
    'description': (
        'Build an app that is functionally similar to the example project in the start file. '
        'Try not to copy the example project, give it your own personal style.'
    ),
    'objectives': (
        'Fulfill the user stories below and get all the tests to pass to complete the lab.'
    ),
    'stories': [
        {
            'title': 'Main container',
            'description': (
                'You should have a main element with an id of playing-cards.'
            ),
            'hint': 'Add <main id="playing-cards"> as the wrapper for all your cards.',
        },
        {
            'title': 'Card elements',
            'description': (
                'Inside your #playing-cards element, you should have at least three '
                'div elements, each with a class of card.'
            ),
            'hint': 'Add at least three direct child <div class="card"> elements inside #playing-cards.',
        },
        {
            'title': 'Card structure',
            'description': (
                'Inside each of your .card elements, you should have exactly three div '
                'elements as direct children: the first with a class of left, the second '
                'with a class of middle, and the third with a class of right.'
            ),
            'hint': (
                'Each card needs three direct children: '
                '<div class="left">, <div class="middle">, and <div class="right">.'
            ),
        },
        {
            'title': 'Card dimensions',
            'description': (
                'Each of your .card elements should have a width and a height set in your CSS.'
            ),
            'hint': 'In your stylesheet, add width and height declarations to the .card selector.',
        },
        {
            'title': 'Playing cards layout',
            'description': (
                'Your #playing-cards element should use flexbox to center its children, '
                'allow them to wrap, and put a 20px space between them.'
            ),
            'hint': (
                'On #playing-cards, set display: flex; justify-content: center; '
                'flex-wrap: wrap; and gap: 20px;.'
            ),
        },
        {
            'title': 'Card flex layout',
            'description': (
                'Your .card elements should use flexbox to justify their children using '
                'space-between.'
            ),
            'hint': 'On .card, set display: flex; and justify-content: space-between;.',
        },
        {
            'title': 'Card section alignment',
            'description': (
                'Your .left elements should align to the start, your .middle elements '
                'should align to the center, and your .right elements should align to the end.'
            ),
            'hint': (
                'Use align-self: flex-start on .left, align-self: center on .middle, '
                'and align-self: flex-end on .right.'
            ),
        },
        {
            'title': 'Middle section layout',
            'description': (
                'Your .middle elements should use flexbox with a column direction to stack '
                'their contents vertically.'
            ),
            'hint': 'On .middle, set display: flex; and flex-direction: column;.',
        },
    ],
}

PLAYING_CARDS_TESTS = [
    {
        'name': '1. main#playing-cards exists',
        'description': 'You should have a main element with an id of playing-cards.',
        'test_code': (
            'const el = getEl("playing-cards");\n'
            'if (!el || el.tagName.toLowerCase() !== "main") throw new Error("playing-cards");'
        ),
        'success_message': 'main#playing-cards is present.',
        'failure_message': 'Add a <main id="playing-cards"> element to your page.',
    },
    {
        'name': '2. At least 3 .card in #playing-cards',
        'description': (
            'Inside your #playing-cards element, you should have at least three '
            'div elements with a class of card.'
        ),
        'test_code': (
            'const container = getEl("playing-cards");\n'
            'if (!container) throw new Error("container");\n'
            'const cards = Array.from(container.children).filter((el) => '
            'el.classList.contains("card"));\n'
            'if (cards.length < 3) throw new Error("cards");'
        ),
        'success_message': 'At least three .card elements are inside #playing-cards.',
        'failure_message': 'Add at least three <div class="card"> elements inside #playing-cards.',
    },
    {
        'name': '3. .card has width and height in CSS',
        'description': (
            'Each of your .card elements should have a width and a height set in your CSS.'
        ),
        'test_code': (
            'if (!cssHasDeclaration(".card", "width")) throw new Error("width");\n'
            'if (!cssHasDeclaration(".card", "height")) throw new Error("height");'
        ),
        'success_message': '.card has width and height in CSS.',
        'failure_message': 'Add width and height declarations to your .card selector in CSS.',
    },
    {
        'name': '4. Each .card has exactly 3 div children',
        'description': (
            'Each of your .card elements should have exactly three div elements as children.'
        ),
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
        'success_message': 'Every .card has exactly three div children.',
        'failure_message': 'Each .card must contain exactly three direct child div elements.',
    },
    {
        'name': '5. .left in each .card',
        'description': (
            'Inside each of your .card elements, you should have a div with a class of left.'
        ),
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
        'success_message': 'Every .card has a .left section.',
        'failure_message': 'Add a <div class="left"> inside each .card element.',
    },
    {
        'name': '6. .middle in each .card',
        'description': (
            'Inside each of your .card elements, you should have a div with a class of middle.'
        ),
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
        'success_message': 'Every .card has a .middle section.',
        'failure_message': 'Add a <div class="middle"> inside each .card element.',
    },
    {
        'name': '7. .right in each .card',
        'description': (
            'Inside each of your .card elements, you should have a div with a class of right.'
        ),
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
        'success_message': 'Every .card has a .right section.',
        'failure_message': 'Add a <div class="right"> inside each .card element.',
    },
    {
        'name': '8. #playing-cards display flex',
        'description': 'Your #playing-cards selector should set display to flex.',
        'test_code': (
            'if (!cssHasDeclaration("#playing-cards", "display", "flex")) '
            'throw new Error("display");'
        ),
        'success_message': '#playing-cards uses display: flex.',
        'failure_message': 'Set display: flex on your #playing-cards selector.',
    },
    {
        'name': '9. #playing-cards justify-content center',
        'description': 'Your #playing-cards selector should set justify-content to center.',
        'test_code': (
            'if (!cssHasDeclaration("#playing-cards", "justify-content", "center")) '
            'throw new Error("justify-content");'
        ),
        'success_message': '#playing-cards uses justify-content: center.',
        'failure_message': 'Set justify-content: center on your #playing-cards selector.',
    },
    {
        'name': '10. #playing-cards flex-wrap wrap',
        'description': 'Your #playing-cards selector should set flex-wrap to wrap.',
        'test_code': (
            'if (!cssHasDeclaration("#playing-cards", "flex-wrap", "wrap")) '
            'throw new Error("flex-wrap");'
        ),
        'success_message': '#playing-cards uses flex-wrap: wrap.',
        'failure_message': 'Set flex-wrap: wrap on your #playing-cards selector.',
    },
    {
        'name': '11. #playing-cards gap 20px',
        'description': 'Your #playing-cards selector should set gap to 20px.',
        'test_code': (
            'if (!cssHasDeclaration("#playing-cards", "gap", "20px")) '
            'throw new Error("gap");'
        ),
        'success_message': '#playing-cards uses gap: 20px.',
        'failure_message': 'Set gap: 20px on your #playing-cards selector.',
    },
    {
        'name': '12. .card display flex',
        'description': 'Your .card selector should set display to flex.',
        'test_code': (
            'if (!cssHasDeclaration(".card", "display", "flex")) '
            'throw new Error("display");'
        ),
        'success_message': '.card uses display: flex.',
        'failure_message': 'Set display: flex on your .card selector.',
    },
    {
        'name': '13. .card justify-content space-between',
        'description': 'Your .card selector should set justify-content to space-between.',
        'test_code': (
            'if (!cssHasDeclaration(".card", "justify-content", "space-between")) '
            'throw new Error("justify-content");'
        ),
        'success_message': '.card uses justify-content: space-between.',
        'failure_message': 'Set justify-content: space-between on your .card selector.',
    },
    {
        'name': '14. .left align-self flex-start',
        'description': 'Your .left selector should set align-self to flex-start.',
        'test_code': (
            'if (!cssHasDeclaration(".left", "align-self", "flex-start")) '
            'throw new Error("align-self");'
        ),
        'success_message': '.left uses align-self: flex-start.',
        'failure_message': 'Set align-self: flex-start on your .left selector.',
    },
    {
        'name': '15. .middle align-self center',
        'description': 'Your .middle selector should set align-self to center.',
        'test_code': (
            'if (!cssHasDeclaration(".middle", "align-self", "center")) '
            'throw new Error("align-self");'
        ),
        'success_message': '.middle uses align-self: center.',
        'failure_message': 'Set align-self: center on your .middle selector.',
    },
    {
        'name': '16. .right align-self flex-end',
        'description': 'Your .right selector should set align-self to flex-end.',
        'test_code': (
            'if (!cssHasDeclaration(".right", "align-self", "flex-end")) '
            'throw new Error("align-self");'
        ),
        'success_message': '.right uses align-self: flex-end.',
        'failure_message': 'Set align-self: flex-end on your .right selector.',
    },
    {
        'name': '17. .middle display flex',
        'description': 'Your .middle selector should set display to flex.',
        'test_code': (
            'if (!cssHasDeclaration(".middle", "display", "flex")) '
            'throw new Error("display");'
        ),
        'success_message': '.middle uses display: flex.',
        'failure_message': 'Set display: flex on your .middle selector.',
    },
    {
        'name': '18. .middle flex-direction column',
        'description': 'Your .middle selector should set flex-direction to column.',
        'test_code': (
            'if (!cssHasDeclaration(".middle", "flex-direction", "column")) '
            'throw new Error("flex-direction");'
        ),
        'success_message': '.middle uses flex-direction: column.',
        'failure_message': 'Set flex-direction: column on your .middle selector.',
    },
]
