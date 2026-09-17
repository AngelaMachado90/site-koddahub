const test = require('node:test');
const assert = require('node:assert/strict');
const social = require('../public/assets/js/blog-social.js');

function storage() {
  const values = new Map();
  return { getItem: (key) => values.get(key) ?? null, setItem: (key, value) => values.set(key, value) };
}

test('one increment per browser session and a new session increments', () => {
  const first = storage();
  assert.equal(social.shouldIncrement(first, 'artigo-teste'), true);
  assert.equal(social.shouldIncrement(first, 'artigo-teste'), false);
  assert.equal(social.shouldIncrement(storage(), 'artigo-teste'), true);
});

test('formats public views with pt-BR locale', () => {
  assert.equal(social.formatViews(12580), '12.580');
});

test('loads the total and keeps endpoint failure non-blocking', async () => {
  const value = { textContent: '' };
  const label = { textContent: '' };
  const element = {
    dataset: { articleSlug: 'artigo-teste', endpoint: '/api/blog/views' }, hidden: false,
    querySelector: (selector) => selector === '.article-view-value' ? value : label
  };
  let request;
  const root = {
    sessionStorage: storage(),
    fetch: async (url, options) => { request = { url, options }; return { ok: true, json: async () => ({ success: true, article_slug: 'artigo-teste', views: 1234 }) }; },
    setTimeout: () => 1, clearTimeout: () => {}, AbortController
  };
  await social.loadViews(root, element);
  assert.equal(request.url, '/api/blog/views');
  assert.deepEqual(JSON.parse(request.options.body), { slug: 'artigo-teste', increment: true });
  assert.equal(value.textContent, '1.234');
  assert.equal(label.textContent, 'visualizações');

  root.fetch = async () => { throw new Error('offline'); };
  await social.loadViews(root, element);
  assert.equal(element.hidden, true);
});

test('Web Share uses canonical and fallback links remain valid', async () => {
  const native = { hidden: true, addEventListener: (name, callback) => { native.click = callback; } };
  const copy = { addEventListener: () => {} };
  const feedback = { textContent: '' };
  const links = [
    { dataset: { shareUrl: 'https://wa.me/?text={title}%0A{url}' }, href: '' },
    { dataset: { shareUrl: 'https://www.linkedin.com/sharing/share-offsite/?url={url}' }, href: '' }
  ];
  const share = {
    dataset: { shareTitle: 'Título real', shareText: 'Texto real' },
    querySelector: (selector) => ({ '[data-native-share]': native, '[data-copy-link]': copy, '[data-share-feedback]': feedback }[selector]),
    querySelectorAll: () => links
  };
  let payload;
  const root = {
    document: { title: 'Fallback', location: { href: 'https://example.test/fallback' }, querySelector: () => ({ href: 'https://koddahub.com.br/blog/artigo/' }) },
    navigator: { share: async (value) => { payload = value; } },
    setTimeout: () => 1
  };
  social.initShare(root, share);
  assert.equal(native.hidden, false);
  await native.click();
  assert.deepEqual(payload, { title: 'Título real', text: 'Texto real', url: 'https://koddahub.com.br/blog/artigo/' });
  assert.match(links[0].href, /^https:\/\/wa\.me\/\?text=/);
  assert.match(links[1].href, /linkedin\.com\/sharing\/share-offsite\/\?url=/);
});

test('native share stays hidden when Web Share API is unavailable', () => {
  const native = { hidden: true, addEventListener: () => {} };
  const share = {
    dataset: {},
    querySelector: (selector) => selector === '[data-native-share]' ? native : null,
    querySelectorAll: () => []
  };
  social.initShare({ document: { title: 'Artigo', location: { href: 'https://example.test' }, querySelector: () => null }, navigator: {} }, share);
  assert.equal(native.hidden, true);
});
