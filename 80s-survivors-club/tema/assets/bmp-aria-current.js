// bmp-aria-current.js — a11y-slideshow-aria
// (named outside the bmp-slideshow* asset namespace: it is an ARIA normalizer,
//  not a slideshow reimplementation — the slideshow ships no bespoke bmp JS.)
//
// WHAT: Keeps the slideshow pagination dots / thumbnails using the VALID
// `aria-current` attribute instead of the invalid `aria-selected`.
//
// WHY: Horizon's `snippets/slideshow-controls.liquid` markup and
// `assets/slideshow.js` mark the active dot/thumbnail with `aria-selected`,
// which is only valid on roles in the listbox/grid/tab families — on a plain
// <button> it is invalid ARIA (axe `aria-allowed-attr`, WCAG 4.1.2) and screen
// readers ignore the state. The BMP layer renames it to `aria-current` in the
// snippet markup (BMP-HOOK:a11y-slideshow-aria) and styles the active state on
// `aria-current` in bmp-styles.css.
//
// The active state is also updated at runtime by the core `slideshow.js`
// controller (and the zoom dialog / predictive carousel reuse the same control
// markup), which still calls `setAttribute('aria-selected', …)` on every slide
// change. Editing those core JS files is not permitted (BMP keeps Horizon core
// JS byte-identical). So this small, self-contained module mirrors any
// runtime-applied `aria-selected` onto `aria-current` and strips the invalid
// attribute — scoped to <slideshow-controls> control buttons only, so the
// predictive-search listbox (where `aria-selected` IS valid) is never touched.
//
// Cost: one MutationObserver per <slideshow-controls> element, watching only the
// `aria-selected` attribute on its control buttons. No layout work, no polling.

(() => {
  const CONTROL_SELECTOR = '.slideshow-control';

  /** Move an invalid aria-selected onto a valid aria-current on one button. */
  function normalize(button) {
    if (!button || !button.hasAttribute('aria-selected')) return;
    const value = button.getAttribute('aria-selected');
    button.setAttribute('aria-current', value);
    button.removeAttribute('aria-selected');
  }

  /** Normalize every control button inside a <slideshow-controls> element. */
  function normalizeAll(root) {
    root.querySelectorAll(CONTROL_SELECTOR).forEach(normalize);
  }

  /** Observe a <slideshow-controls> so runtime aria-selected writes are fixed. */
  function observe(controls) {
    if (controls.dataset.bmpAriaObserved === 'true') return;
    controls.dataset.bmpAriaObserved = 'true';

    normalizeAll(controls);

    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.attributeName !== 'aria-selected') continue;
        const target = mutation.target;
        if (target instanceof Element && target.matches(CONTROL_SELECTOR)) {
          normalize(target);
        }
      }
    });

    observer.observe(controls, {
      subtree: true,
      attributes: true,
      attributeFilter: ['aria-selected'],
    });
  }

  function init() {
    document.querySelectorAll('slideshow-controls').forEach(observe);
  }

  // Catch slideshow-controls added later (quick-add modal, zoom dialog, AJAX
  // section renders) without observing the whole document for everything.
  const rootObserver = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) {
        if (!(node instanceof Element)) continue;
        if (node.matches?.('slideshow-controls')) observe(node);
        node.querySelectorAll?.('slideshow-controls').forEach(observe);
      }
    }
  });

  // Defer the initial sweep AND the documentElement subtree observer install to
  // idle. This is post-paint a11y (aria-selected -> aria-current only matters
  // once a user changes a slide), and installing a whole-document MutationObserver
  // during the load task adds avoidable main-thread cost while hydration is
  // mutating the DOM. (BMP-HOOK:perf-defer)
  const startup = () => {
    init();
    rootObserver.observe(document.documentElement, { childList: true, subtree: true });
  };
  // Bound the wait so a pathologically never-idle page still installs the
  // a11y normalizer; fall back to a near-immediate macrotask where rIC is absent.
  const onIdle = window.requestIdleCallback
    ? (cb) => window.requestIdleCallback(cb, { timeout: 2000 })
    : (cb) => setTimeout(cb, 1);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => onIdle(startup), { once: true });
  } else {
    onIdle(startup);
  }
})();
