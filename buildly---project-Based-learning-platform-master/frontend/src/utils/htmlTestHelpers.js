export const HTML_TEST_HELPERS = `
function htmlHasStructure() {
  if (!/<!doctype\\s+html>/i.test(html)) return false;
  if (!/<html[\\s>]/i.test(html)) return false;
  if (!/<head[\\s>]/i.test(html)) return false;
  if (!/<body[\\s>]/i.test(html)) return false;
  if (!/<meta[^>]+charset\\s*=/i.test(html)) return false;
  if (!/<\\/body>/i.test(html)) return false;
  if (!/<\\/html>/i.test(html)) return false;
  return true;
}

function htmlHasTagContent(tag, ...parts) {
  const pattern = new RegExp('<' + tag + '[^>]*>[\\\\s\\\\S]*?<\\\\/' + tag + '>', 'i');
  const match = html.match(pattern);
  if (!match) return false;
  const content = match[0];
  return parts.every((part) => content.includes(part));
}

function htmlHasText(...parts) {
  return parts.every((part) => html.includes(part));
}

// One parsed document per Check Code run. Re-parsing on every getEl/getDoc
// put child/parent in different trees, so Node.contains() always failed
// (isDescendantOf and any cross-element DOM check).
let _parsedDoc = null;
let _parsedHtml = null;

function getDoc() {
  if (_parsedDoc && _parsedHtml === html) {
    return _parsedDoc;
  }
  const parser = new DOMParser();
  _parsedDoc = parser.parseFromString(html, 'text/html');
  _parsedHtml = html;
  return _parsedDoc;
}

function getEl(id) {
  return getDoc().getElementById(id);
}

function getText(el) {
  if (!el) return '';
  return (el.textContent || '').trim();
}

function isDescendantOf(childId, parentId) {
  const doc = getDoc();
  const child = doc.getElementById(childId);
  const parent = doc.getElementById(parentId);
  if (!child || !parent) return false;
  return parent.contains(child);
}

function getFormInputs(type, formId) {
  const form = getEl(formId || 'survey-form');
  if (!form) return [];
  return Array.from(form.querySelectorAll('input[type="' + type + '"]'));
}

function getFormRadios(formId) {
  const form = getEl(formId || 'survey-form');
  if (!form) return [];
  return Array.from(form.querySelectorAll('input[type="radio"]'));
}

function getFormCheckboxes(formId) {
  const form = getEl(formId || 'survey-form');
  if (!form) return [];
  return Array.from(form.querySelectorAll('input[type="checkbox"]'));
}

function hasNumericAttr(el, attr) {
  if (!el || !el.hasAttribute(attr)) return false;
  const value = el.getAttribute(attr);
  return value !== '' && !isNaN(Number(value));
}

function submitTypeIsValid(el) {
  if (!el) return false;
  const tag = el.tagName.toLowerCase();
  if (tag === 'input') return el.getAttribute('type') === 'submit';
  if (tag === 'button') {
    const type = el.getAttribute('type') || 'submit';
    return type === 'submit';
  }
  return false;
}

function normalizeCss(cssText) {
  return (cssText || '').replace(/\\/\\*[\\s\\S]*?\\*\\//g, '').replace(/\\s+/g, ' ').trim();
}

function cssBlocks(cssText) {
  const normalized = normalizeCss(cssText);
  const blocks = [];
  const regex = /([^{]+)\\{([^}]+)\\}/g;
  let match = regex.exec(normalized);
  while (match) {
    blocks.push({ selector: match[1].trim(), body: match[2].trim() });
    match = regex.exec(normalized);
  }
  return blocks;
}

function selectorMatches(ruleSelector, targetSelector) {
  const targets = ruleSelector.split(',').map((part) => part.trim());
  const normalizedTarget = targetSelector.replace(/\\s+/g, '');
  return targets.some((part) => {
    const normalizedPart = part.replace(/\\s+/g, '');
    return (
      normalizedPart === normalizedTarget ||
      normalizedPart.endsWith(normalizedTarget) ||
      normalizedPart.includes(normalizedTarget)
    );
  });
}

function cssHasDeclaration(selector, property, expectedValue) {
  const blocks = cssBlocks(css);
  const propertyName = property.toLowerCase();

  for (const block of blocks) {
    if (!selectorMatches(block.selector, selector)) continue;

    const declarations = block.body.split(';').map((item) => item.trim()).filter(Boolean);
    for (const declaration of declarations) {
      const colonIndex = declaration.indexOf(':');
      if (colonIndex === -1) continue;

      const key = declaration.slice(0, colonIndex).trim().toLowerCase();
      const value = declaration.slice(colonIndex + 1).trim().toLowerCase().replace(/\\s+/g, ' ');

      if (key !== propertyName) continue;
      if (!expectedValue) return true;
      if (value === String(expectedValue).toLowerCase()) return true;
      if (value.includes(String(expectedValue).toLowerCase())) return true;
    }
  }

  return false;
}

function cssHasAttributeSelector(fragment) {
  return normalizeCss(css).includes(fragment);
}

function cssAttrRuleHasProperty(attrFragment, property, valueFragment) {
  const blocks = cssBlocks(css);

  for (const block of blocks) {
    if (!block.selector.includes('[') || !block.selector.includes(attrFragment)) continue;

    const body = block.body.toLowerCase();
    if (property && !body.includes(property.toLowerCase())) continue;
    if (valueFragment && !body.includes(valueFragment.toLowerCase())) continue;
    return true;
  }

  return false;
}

function cardHasInlineSize(card) {
  const style = (card.getAttribute('style') || '').toLowerCase();
  return style.includes('width') && style.includes('height');
}

function cssHasRowAttrSelector(className) {
  const blocks = cssBlocks(css);
  const exactPatterns = [
    '[class="' + className + '"]',
    '[class~="' + className + '"]',
    '[class*="' + className + '"]',
  ];

  return blocks.some((block) => {
    if (!block.selector.includes('tr')) return false;
    return exactPatterns.some((pattern) => block.selector.includes(pattern));
  });
}

function getTableBodyRows() {
  const table = getDoc().querySelector('table');
  if (!table) return [];
  return Array.from(table.querySelectorAll('tbody tr'));
}

function getTableHeadings() {
  const table = getDoc().querySelector('table');
  if (!table) return [];
  return Array.from(table.querySelectorAll('thead tr th')).map((th) => getText(th));
}
`.trim()

export function runHtmlWorkspaceTest(html, css, testCode) {
  const runner = new Function('html', 'css', `${HTML_TEST_HELPERS}\n${testCode || ''}`)
  runner(html, css)
}
