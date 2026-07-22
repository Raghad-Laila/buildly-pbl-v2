import { testUsesHtmlCssWorkspace, shouldUseWorkspaceFileTests, getClientTestSourceCode, runClientTests } from './src/utils/testRunner.js'
import { linkResultsByIndex, linkResultsByTask } from './src/utils/testResultLinking.js'

function assert(cond, msg) {
  if (!cond) {
    console.error('FAIL:', msg)
    process.exit(1)
  }
}

assert(
  !testUsesHtmlCssWorkspace('const nav=buildNav(); if(!nav.includes("x")) throw 0'),
  'JS buildNav should not be workspace'
)
assert(
  testUsesHtmlCssWorkspace('if(!html.includes("gallery")) throw 0'),
  'html.includes is workspace'
)
assert(
  testUsesHtmlCssWorkspace('if(!css.includes(":hover")) throw 0'),
  'css.includes is workspace'
)
assert(testUsesHtmlCssWorkspace('if(!getEl("x")) throw 0'), 'getEl helper is workspace')
assert(
  !shouldUseWorkspaceFileTests('html', [
    { test_code: 'const n=buildNav(); if(!n.includes("a")) throw 0' },
  ]),
  'html project with JS tests should not force workspace suite'
)
assert(
  shouldUseWorkspaceFileTests('html', [{ test_code: 'if(!html.includes("a")) throw 0' }]),
  'html project with html tests uses workspace'
)

const workspace = {
  files: [
    { name: 'index.html', content: '<html></html>' },
    { name: 'style.css', content: '' },
    {
      name: 'script.js',
      content:
        'function buildNav(){ return "المشاريع التواصل"; } function buildHome(){ return "<h1>hi</h1>"; } function buildProjects(){ return "<ul><li>a</li><li>b</li></ul>"; }',
    },
  ],
}

const src = getClientTestSourceCode(workspace, 'html')
assert(src.includes('buildNav'), 'should read script.js not index.html')

const payload = runClientTests(
  '',
  [
    {
      id: 1,
      name: 'nav',
      test_code: 'const nav=buildNav(); if(!nav.includes("المشاريع")) throw new Error("nav");',
      success_message: 'ok',
      failure_message: 'fail',
    },
    {
      id: 2,
      name: 'gallery',
      test_code: 'if(!html.includes("html")) throw new Error("html");',
      success_message: 'ok',
      failure_message: 'fail',
    },
  ],
  { workspace, projectLanguage: 'html' }
)

assert(payload.results[0].passed, 'JS test should pass on html project: ' + payload.results[0].stderr)
assert(payload.results[1].passed, 'HTML test should pass in mixed suite: ' + payload.results[1].stderr)

const linked = linkResultsByIndex(
  [
    { title: 'Build Navigation Bar', description: 'nav links' },
    { title: 'Gallery section', description: 'gallery' },
  ],
  {
    results: [
      { id: 1, name: 'nav links check', passed: true },
      { id: 2, name: 'gallery markup', passed: false },
    ],
  }
)
assert(linked[0].testStatus === 'passed', 'fuzzy link story0')
assert(linked[1].testStatus === 'failed', 'fuzzy link story1')

const taskStories = [
  { id: 10, title: 'Story with many tests' },
  { id: 20, title: 'Story with no tests' },
]
const taskTests = [
  { id: 1, task: 10, name: 'a' },
  { id: 2, task: 10, name: 'b' },
  { id: 3, task: 10, name: 'c' },
  { id: 99, task: null, name: 'unlinked' },
]

const allPassedByTask = linkResultsByTask(taskStories, taskTests, {
  results: [
    { id: 1, passed: true },
    { id: 2, passed: true },
    { id: 3, passed: true },
    { id: 99, passed: false },
  ],
})
assert(allPassedByTask[0].testStatus === 'passed', 'all linked tests passed')
assert(allPassedByTask[1].testStatus === null, 'story with no linked tests')

const anyFailedByTask = linkResultsByTask(taskStories, taskTests, {
  results: [
    { id: 1, passed: true },
    { id: 2, passed: false },
    { id: 3, passed: true },
    { id: 99, passed: true },
  ],
})
assert(anyFailedByTask[0].testStatus === 'failed', 'any linked failure fails story')
assert(anyFailedByTask[1].testStatus === null, 'unlinked story stays null')

const missingResultByTask = linkResultsByTask(taskStories, taskTests, {
  results: [
    { id: 1, passed: true },
    { id: 3, passed: true },
  ],
})
assert(missingResultByTask[0].testStatus === null, 'missing linked result => null')

const unlinkedIgnored = linkResultsByTask(
  [{ id: 10, title: 'Only story' }],
  [
    { id: 1, task: 10, name: 'linked' },
    { id: 99, task: null, name: 'orphan' },
  ],
  {
    results: [
      { id: 1, passed: true },
      { id: 99, passed: false },
    ],
  }
)
assert(unlinkedIgnored[0].testStatus === 'passed', 'unlinked tests ignored for story status')

console.log('All frontend test-routing checks passed')
