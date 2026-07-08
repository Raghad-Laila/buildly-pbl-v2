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
`.trim()

export function runHtmlWorkspaceTest(html, css, testCode) {
  const runner = new Function('html', 'css', `${HTML_TEST_HELPERS}\n${testCode || ''}`)
  runner(html, css)
}
