"""Survey Form project definition for Frontend Mastery."""

SURVEY_FORM_TITLE = 'Build a Survey Form'

SURVEY_FORM_PROJECT = {
    'title': SURVEY_FORM_TITLE,
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
            'title': 'Page title',
            'description': (
                'You should have a page title in an h1 element with an id of title.'
            ),
            'hint': 'Add <h1 id="title"> with your survey title inside the page.',
        },
        {
            'title': 'Short explanation',
            'description': (
                'You should have a short explanation in a p element with an id of description.'
            ),
            'hint': 'Add <p id="description"> describing what the survey is about.',
        },
        {
            'title': 'Survey form',
            'description': (
                'You should have a form element with an id of survey-form.'
            ),
            'hint': 'Wrap all form fields inside <form id="survey-form">.',
        },
        {
            'title': 'Name field',
            'description': (
                'Inside the form element you should have a required input field to enter '
                'your name that has an id of name and a type of text.'
            ),
            'hint': 'Use <input id="name" type="text" required>.',
        },
        {
            'title': 'Email field',
            'description': (
                'Inside the form element you should have a required input field to enter '
                'your email that has an id of email. If you enter an email that is not '
                'formatted correctly, you should see an HTML5 validation error.'
            ),
            'hint': 'Use <input id="email" type="email" required> for built-in validation.',
        },
        {
            'title': 'Number field',
            'description': (
                'Inside the form element you should have an input field to enter a number '
                'that has an id of number. The number input should not accept non-numbers, '
                'either by preventing you from typing them or by showing an HTML5 validation '
                'error. If you enter numbers outside the range defined by min and max, you '
                'should see an HTML5 validation error.'
            ),
            'hint': 'Use <input id="number" type="number" min="..." max="...">.',
        },
        {
            'title': 'Field labels',
            'description': (
                'For the name, email, and number input fields, you should have corresponding '
                'label elements in the form with ids: name-label, email-label, and number-label.'
            ),
            'hint': 'Add <label id="name-label">, <label id="email-label">, and <label id="number-label">.',
        },
        {
            'title': 'Placeholder text',
            'description': (
                'For the name, email, and number input fields, you should have placeholder '
                'text that gives a description or instructions for each field.'
            ),
            'hint': 'Add a placeholder attribute on each of the three inputs.',
        },
        {
            'title': 'Dropdown select',
            'description': (
                'Inside the form element, you should have a select dropdown element with an '
                'id of dropdown and at least two options to choose from.'
            ),
            'hint': 'Use <select id="dropdown"> with at least two <option> elements.',
        },
        {
            'title': 'Radio buttons',
            'description': (
                'Inside the form element, you can select an option from a group of at least '
                'two radio buttons that are grouped using the name attribute.'
            ),
            'hint': 'Add at least two <input type="radio"> elements sharing the same name.',
        },
        {
            'title': 'Checkboxes',
            'description': (
                'Inside the form element, you can select several fields from a series of '
                'checkboxes, each of which must have a value attribute.'
            ),
            'hint': 'Add multiple <input type="checkbox" value="..."> inside the form.',
        },
        {
            'title': 'Comments textarea',
            'description': (
                'Inside the form element, you should have a textarea for additional comments.'
            ),
            'hint': 'Add <textarea> inside the form for optional comments.',
        },
        {
            'title': 'Submit button',
            'description': (
                'Inside the form element, you should have a button with id of submit to '
                'submit all the inputs.'
            ),
            'hint': 'Add <button type="submit" id="submit"> or <input type="submit" id="submit">.',
        },
    ],
}

SURVEY_FORM_TESTS = [
    {
        'name': '1. h1#title exists',
        'description': 'You should have an h1 element with an id of title.',
        'test_code': (
            'const el = getEl("title");\n'
            'if (!el || el.tagName.toLowerCase() !== "h1") throw new Error("title");'
        ),
        'success_message': 'h1#title is present.',
        'failure_message': 'Add an <h1 id="title"> element to your page.',
    },
    {
        'name': '2. #title is not empty',
        'description': 'Your #title should not be empty.',
        'test_code': (
            'const el = getEl("title");\n'
            'if (!el || !getText(el)) throw new Error("empty");'
        ),
        'success_message': '#title has content.',
        'failure_message': 'Add text inside your #title element.',
    },
    {
        'name': '3. p#description exists',
        'description': 'You should have a p element with an id of description.',
        'test_code': (
            'const el = getEl("description");\n'
            'if (!el || el.tagName.toLowerCase() !== "p") throw new Error("description");'
        ),
        'success_message': 'p#description is present.',
        'failure_message': 'Add a <p id="description"> element to your page.',
    },
    {
        'name': '4. #description is not empty',
        'description': 'Your #description should not be empty.',
        'test_code': (
            'const el = getEl("description");\n'
            'if (!el || !getText(el)) throw new Error("empty");'
        ),
        'success_message': '#description has content.',
        'failure_message': 'Add text inside your #description element.',
    },
    {
        'name': '5. form#survey-form exists',
        'description': 'You should have a form element with an id of survey-form.',
        'test_code': (
            'const el = getEl("survey-form");\n'
            'if (!el || el.tagName.toLowerCase() !== "form") throw new Error("form");'
        ),
        'success_message': 'form#survey-form is present.',
        'failure_message': 'Add a <form id="survey-form"> element.',
    },
    {
        'name': '6. input#name exists',
        'description': 'You should have an input element with an id of name.',
        'test_code': (
            'const el = getEl("name");\n'
            'if (!el || el.tagName.toLowerCase() !== "input") throw new Error("name");'
        ),
        'success_message': 'input#name is present.',
        'failure_message': 'Add an <input id="name"> inside your form.',
    },
    {
        'name': '7. #name type is text',
        'description': 'Your #name should have a type of text.',
        'test_code': (
            'const el = getEl("name");\n'
            'if (!el || el.getAttribute("type") !== "text") throw new Error("type");'
        ),
        'success_message': '#name has type="text".',
        'failure_message': 'Set type="text" on your #name input.',
    },
    {
        'name': '8. #name is required',
        'description': 'Your #name should require input.',
        'test_code': (
            'const el = getEl("name");\n'
            'if (!el || !el.hasAttribute("required")) throw new Error("required");'
        ),
        'success_message': '#name is required.',
        'failure_message': 'Add the required attribute to #name.',
    },
    {
        'name': '9. #name inside #survey-form',
        'description': 'Your #name should be a descendant of #survey-form.',
        'test_code': (
            'if (!isDescendantOf("name", "survey-form")) throw new Error("descendant");'
        ),
        'success_message': '#name is inside the form.',
        'failure_message': 'Place #name inside #survey-form.',
    },
    {
        'name': '10. input#email exists',
        'description': 'You should have an input element with an id of email.',
        'test_code': (
            'const el = getEl("email");\n'
            'if (!el || el.tagName.toLowerCase() !== "input") throw new Error("email");'
        ),
        'success_message': 'input#email is present.',
        'failure_message': 'Add an <input id="email"> inside your form.',
    },
    {
        'name': '11. #email type is email',
        'description': 'Your #email should have a type of email.',
        'test_code': (
            'const el = getEl("email");\n'
            'if (!el || el.getAttribute("type") !== "email") throw new Error("type");'
        ),
        'success_message': '#email has type="email".',
        'failure_message': 'Set type="email" on your #email input.',
    },
    {
        'name': '12. #email is required',
        'description': 'Your #email should require input.',
        'test_code': (
            'const el = getEl("email");\n'
            'if (!el || !el.hasAttribute("required")) throw new Error("required");'
        ),
        'success_message': '#email is required.',
        'failure_message': 'Add the required attribute to #email.',
    },
    {
        'name': '13. #email inside #survey-form',
        'description': 'Your #email should be a descendant of #survey-form.',
        'test_code': (
            'if (!isDescendantOf("email", "survey-form")) throw new Error("descendant");'
        ),
        'success_message': '#email is inside the form.',
        'failure_message': 'Place #email inside #survey-form.',
    },
    {
        'name': '14. input#number exists',
        'description': 'You should have an input element with an id of number.',
        'test_code': (
            'const el = getEl("number");\n'
            'if (!el || el.tagName.toLowerCase() !== "input") throw new Error("number");'
        ),
        'success_message': 'input#number is present.',
        'failure_message': 'Add an <input id="number"> inside your form.',
    },
    {
        'name': '15. #number inside #survey-form',
        'description': 'Your #number should be a descendant of #survey-form.',
        'test_code': (
            'if (!isDescendantOf("number", "survey-form")) throw new Error("descendant");'
        ),
        'success_message': '#number is inside the form.',
        'failure_message': 'Place #number inside #survey-form.',
    },
    {
        'name': '16. #number type is number',
        'description': 'Your #number should have a type of number.',
        'test_code': (
            'const el = getEl("number");\n'
            'if (!el || el.getAttribute("type") !== "number") throw new Error("type");'
        ),
        'success_message': '#number has type="number".',
        'failure_message': 'Set type="number" on your #number input.',
    },
    {
        'name': '17. #number has min',
        'description': 'Your #number should have a min attribute with a numeric value.',
        'test_code': (
            'const el = getEl("number");\n'
            'if (!hasNumericAttr(el, "min")) throw new Error("min");'
        ),
        'success_message': '#number has a numeric min attribute.',
        'failure_message': 'Add a numeric min attribute to #number.',
    },
    {
        'name': '18. #number has max',
        'description': 'Your #number should have a max attribute with a numeric value.',
        'test_code': (
            'const el = getEl("number");\n'
            'if (!hasNumericAttr(el, "max")) throw new Error("max");'
        ),
        'success_message': '#number has a numeric max attribute.',
        'failure_message': 'Add a numeric max attribute to #number.',
    },
    {
        'name': '19. label#name-label exists',
        'description': 'You should have a label element with an id of name-label.',
        'test_code': (
            'const el = getEl("name-label");\n'
            'if (!el || el.tagName.toLowerCase() !== "label") throw new Error("name-label");'
        ),
        'success_message': 'label#name-label is present.',
        'failure_message': 'Add a <label id="name-label"> element.',
    },
    {
        'name': '20. label#email-label exists',
        'description': 'You should have a label element with an id of email-label.',
        'test_code': (
            'const el = getEl("email-label");\n'
            'if (!el || el.tagName.toLowerCase() !== "label") throw new Error("email-label");'
        ),
        'success_message': 'label#email-label is present.',
        'failure_message': 'Add a <label id="email-label"> element.',
    },
    {
        'name': '21. label#number-label exists',
        'description': 'You should have a label element with an id of number-label.',
        'test_code': (
            'const el = getEl("number-label");\n'
            'if (!el || el.tagName.toLowerCase() !== "label") throw new Error("number-label");'
        ),
        'success_message': 'label#number-label is present.',
        'failure_message': 'Add a <label id="number-label"> element.',
    },
    {
        'name': '22. #name-label has text',
        'description': 'Your #name-label should contain text that describes the input.',
        'test_code': (
            'const el = getEl("name-label");\n'
            'if (!el || !getText(el)) throw new Error("text");'
        ),
        'success_message': '#name-label describes the name field.',
        'failure_message': 'Add descriptive text inside #name-label.',
    },
    {
        'name': '23. #email-label has text',
        'description': 'Your #email-label should contain text that describes the input.',
        'test_code': (
            'const el = getEl("email-label");\n'
            'if (!el || !getText(el)) throw new Error("text");'
        ),
        'success_message': '#email-label describes the email field.',
        'failure_message': 'Add descriptive text inside #email-label.',
    },
    {
        'name': '24. #number-label has text',
        'description': 'Your #number-label should contain text that describes the input.',
        'test_code': (
            'const el = getEl("number-label");\n'
            'if (!el || !getText(el)) throw new Error("text");'
        ),
        'success_message': '#number-label describes the number field.',
        'failure_message': 'Add descriptive text inside #number-label.',
    },
    {
        'name': '25. #name-label inside #survey-form',
        'description': 'Your #name-label should be a descendant of #survey-form.',
        'test_code': (
            'if (!isDescendantOf("name-label", "survey-form")) throw new Error("descendant");'
        ),
        'success_message': '#name-label is inside the form.',
        'failure_message': 'Place #name-label inside #survey-form.',
    },
    {
        'name': '26. #email-label inside #survey-form',
        'description': 'Your #email-label should be a descendant of #survey-form.',
        'test_code': (
            'if (!isDescendantOf("email-label", "survey-form")) throw new Error("descendant");'
        ),
        'success_message': '#email-label is inside the form.',
        'failure_message': 'Place #email-label inside #survey-form.',
    },
    {
        'name': '27. #number-label inside #survey-form',
        'description': 'Your #number-label should be a descendant of #survey-form.',
        'test_code': (
            'if (!isDescendantOf("number-label", "survey-form")) throw new Error("descendant");'
        ),
        'success_message': '#number-label is inside the form.',
        'failure_message': 'Place #number-label inside #survey-form.',
    },
    {
        'name': '28. #name has placeholder',
        'description': 'Your #name should have a placeholder attribute and value.',
        'test_code': (
            'const el = getEl("name");\n'
            'if (!el || !el.hasAttribute("placeholder") || !el.getAttribute("placeholder")) '
            'throw new Error("placeholder");'
        ),
        'success_message': '#name has a placeholder.',
        'failure_message': 'Add a placeholder attribute to #name.',
    },
    {
        'name': '29. #email has placeholder',
        'description': 'Your #email should have a placeholder attribute and value.',
        'test_code': (
            'const el = getEl("email");\n'
            'if (!el || !el.hasAttribute("placeholder") || !el.getAttribute("placeholder")) '
            'throw new Error("placeholder");'
        ),
        'success_message': '#email has a placeholder.',
        'failure_message': 'Add a placeholder attribute to #email.',
    },
    {
        'name': '30. #number has placeholder',
        'description': 'Your #number should have a placeholder attribute and value.',
        'test_code': (
            'const el = getEl("number");\n'
            'if (!el || !el.hasAttribute("placeholder") || !el.getAttribute("placeholder")) '
            'throw new Error("placeholder");'
        ),
        'success_message': '#number has a placeholder.',
        'failure_message': 'Add a placeholder attribute to #number.',
    },
    {
        'name': '31. select#dropdown exists',
        'description': 'You should have a select field with an id of dropdown.',
        'test_code': (
            'const el = getEl("dropdown");\n'
            'if (!el || el.tagName.toLowerCase() !== "select") throw new Error("dropdown");'
        ),
        'success_message': 'select#dropdown is present.',
        'failure_message': 'Add a <select id="dropdown"> element.',
    },
    {
        'name': '32. #dropdown has 2+ options',
        'description': (
            'Your #dropdown should have at least two selectable (not disabled) option elements.'
        ),
        'test_code': (
            'const el = getEl("dropdown");\n'
            'if (!el) throw new Error("dropdown");\n'
            'const options = Array.from(el.querySelectorAll("option")).filter((o) => !o.disabled);\n'
            'if (options.length < 2) throw new Error("options");'
        ),
        'success_message': '#dropdown has at least two options.',
        'failure_message': 'Add at least two selectable <option> elements to #dropdown.',
    },
    {
        'name': '33. #dropdown inside #survey-form',
        'description': 'Your #dropdown should be a descendant of #survey-form.',
        'test_code': (
            'if (!isDescendantOf("dropdown", "survey-form")) throw new Error("descendant");'
        ),
        'success_message': '#dropdown is inside the form.',
        'failure_message': 'Place #dropdown inside #survey-form.',
    },
    {
        'name': '34. At least 2 radio inputs',
        'description': 'You should have at least two input elements with a type of radio.',
        'test_code': (
            'if (getDoc().querySelectorAll(\'input[type="radio"]\').length < 2) '
            'throw new Error("radios");'
        ),
        'success_message': 'At least two radio inputs exist.',
        'failure_message': 'Add at least two <input type="radio"> elements.',
    },
    {
        'name': '35. 2+ radios inside #survey-form',
        'description': (
            'You should have at least two radio buttons that are descendants of #survey-form.'
        ),
        'test_code': (
            'if (getFormRadios().length < 2) throw new Error("form-radios");'
        ),
        'success_message': 'At least two radio buttons are inside the form.',
        'failure_message': 'Place at least two radio buttons inside #survey-form.',
    },
    {
        'name': '36. All radios have value',
        'description': 'All your radio buttons should have a value attribute and value.',
        'test_code': (
            'const radios = getDoc().querySelectorAll(\'input[type="radio"]\');\n'
            'if (radios.length < 2) throw new Error("radios");\n'
            'for (const radio of radios) {\n'
            '  if (!radio.hasAttribute("value") || !radio.getAttribute("value")) '
            'throw new Error("value");\n'
            '}'
        ),
        'success_message': 'All radio buttons have a value.',
        'failure_message': 'Every radio button needs a non-empty value attribute.',
    },
    {
        'name': '37. All radios have name',
        'description': 'All your radio buttons should have a name attribute and value.',
        'test_code': (
            'const radios = getDoc().querySelectorAll(\'input[type="radio"]\');\n'
            'if (radios.length < 2) throw new Error("radios");\n'
            'for (const radio of radios) {\n'
            '  if (!radio.hasAttribute("name") || !radio.getAttribute("name")) '
            'throw new Error("name");\n'
            '}'
        ),
        'success_message': 'All radio buttons have a name.',
        'failure_message': 'Every radio button needs a non-empty name attribute.',
    },
    {
        'name': '38. Each radio group has 2+ buttons',
        'description': 'Every radio button group should have at least 2 radio buttons.',
        'test_code': (
            'const radios = getDoc().querySelectorAll(\'input[type="radio"]\');\n'
            'const groups = {};\n'
            'for (const radio of radios) {\n'
            '  const name = radio.getAttribute("name");\n'
            '  if (!name) throw new Error("name");\n'
            '  groups[name] = (groups[name] || 0) + 1;\n'
            '}\n'
            'const counts = Object.values(groups);\n'
            'if (!counts.length || counts.some((count) => count < 2)) throw new Error("group");'
        ),
        'success_message': 'Every radio group has at least two buttons.',
        'failure_message': 'Each radio group (same name) needs at least two buttons.',
    },
    {
        'name': '39. 2+ checkboxes inside #survey-form',
        'description': (
            'You should have at least two input elements with a type of checkbox '
            'that are descendants of #survey-form.'
        ),
        'test_code': (
            'if (getFormCheckboxes().length < 2) throw new Error("checkboxes");'
        ),
        'success_message': 'At least two checkboxes are inside the form.',
        'failure_message': 'Add at least two checkboxes inside #survey-form.',
    },
    {
        'name': '40. All checkboxes have value',
        'description': (
            'All your checkboxes inside #survey-form should have a value attribute and value.'
        ),
        'test_code': (
            'const boxes = getFormCheckboxes();\n'
            'if (boxes.length < 2) throw new Error("checkboxes");\n'
            'for (const box of boxes) {\n'
            '  if (!box.hasAttribute("value") || !box.getAttribute("value")) '
            'throw new Error("value");\n'
            '}'
        ),
        'success_message': 'All checkboxes have a value.',
        'failure_message': 'Every checkbox inside the form needs a non-empty value attribute.',
    },
    {
        'name': '41. textarea inside #survey-form',
        'description': (
            'You should have at least one textarea element that is a descendant of #survey-form.'
        ),
        'test_code': (
            'const form = getEl("survey-form");\n'
            'if (!form || !form.querySelector("textarea")) throw new Error("textarea");'
        ),
        'success_message': 'A textarea is inside the form.',
        'failure_message': 'Add a <textarea> inside #survey-form.',
    },
    {
        'name': '42. #submit exists',
        'description': 'You should have an input or button element with an id of submit.',
        'test_code': (
            'const el = getEl("submit");\n'
            'const tag = el ? el.tagName.toLowerCase() : "";\n'
            'if (!el || (tag !== "button" && tag !== "input")) throw new Error("submit");'
        ),
        'success_message': '#submit element is present.',
        'failure_message': 'Add a <button id="submit"> or <input id="submit"> element.',
    },
    {
        'name': '43. #submit type is submit',
        'description': 'Your #submit should have a type of submit.',
        'test_code': (
            'const el = getEl("submit");\n'
            'if (!submitTypeIsValid(el)) throw new Error("type");'
        ),
        'success_message': '#submit has type="submit".',
        'failure_message': 'Set type="submit" on your #submit button or input.',
    },
    {
        'name': '44. #submit inside #survey-form',
        'description': 'Your #submit should be a descendant of #survey-form.',
        'test_code': (
            'if (!isDescendantOf("submit", "survey-form")) throw new Error("descendant");'
        ),
        'success_message': '#submit is inside the form.',
        'failure_message': 'Place #submit inside #survey-form.',
    },
]
