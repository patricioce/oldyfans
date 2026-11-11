/**
 * Announcement first-surviving-slide fallback.
 *
 * Feature-scoped module: loaded only from
 * snippets/bmp-countdown.liquid, mode: 'fallback', at the render site of a
 * block whose own countdown state is 'hidden' (blocks/_announcement.liquid's
 * BMP-HOOK:announcement-countdown-hide / -hide-close removes that block's
 * <slideshow-slide> from the DOM entirely). It never loads at any default
 * state, so the default render stays byte-identical to stock.
 *
 * WHY THIS EXISTS: native `block_index` (blocks/_announcement.liquid's own
 * `section.blocks | find_index: 'id', block.id`) is computed over EVERY
 * configured block, whether or not it will actually render — a sibling
 * block's own resolved countdown state is unreadable from inside another
 * block's render pass in Horizon's theme-block architecture (measured live,
 * 2026-08-13; see scripts/check-announcement-countdown.mjs's A6 comment).
 * So when an earlier block is server-skipped this way, no later block's
 * find_index is guaranteed to be 0, and none of the surviving slides is
 * guaranteed to carry native aria-hidden="false" — stock's own
 * `[aria-hidden='true'] { opacity: 0; visibility: hidden }` rule then hides
 * every slide left on the page.
 *
 * A CSS-only fix for this shipped briefly and was reverted: it forced a
 * slide visually visible without touching its aria-hidden="true" attribute,
 * which broke stock's aria-hidden/visibility pairing and made a covering
 * link keyboard-focusable while still hidden from assistive tech (axe-core
 * aria-hidden-focus, WCAG 4.1.2 — stock does not have this defect). Only
 * the attribute itself fixes it correctly, so this module writes it.
 *
 * BEHAVIOR: runs once, at load. For each `.announcement-bar__slides`
 * container with no slide already carrying `aria-hidden="false"`, sets it
 * on the first surviving slide. Does nothing when a slide already has it
 * (the common case — native find_index landed on 0 for someone). Native
 * `assets/announcement-bar.js` takes over `aria-hidden` from the first
 * autoplay tick or user interaction onward; this module runs once per
 * document load and does not re-touch the attribute afterwards, so it
 * cannot fight the component for control. `type="module"` scripts execute
 * once the document is parsed (defer semantics) and the browser's module
 * map runs a given URL's top-level code exactly once no matter how many
 * `<script type="module" src="...">` tags reference it, so this is safe to
 * emit from more than one hidden block on the same page.
 *
 * KNOWN LIMITATION, deliberate:
 * "runs once per document load" is also a ceiling. Because the browser's
 * module map runs a given URL's top-level code at most once per document,
 * and because the only load site is inside this block's own render output,
 * the correction does NOT re-apply after an in-place theme-editor section
 * re-render. Storefront is unaffected -- nothing re-renders this section
 * there. In the editor the symptom is a bounded blank preview that
 * self-heals at the next autoplay tick, because the condition that makes
 * this fallback necessary at all (>= 2 configured blocks, so that one can
 * be server-skipped while another survives) is exactly the condition that
 * turns autoplay on at sections/header-announcements.liquid:19-22, where
 * `speed` is 2 to 10 seconds and defaults to 5. Making this re-runnable
 * would mean a custom element whose connectedCallback does the sweep; that
 * is more machinery than an editor-only, self-healing symptom warrants for
 * v1.
 */
(() => {
  document.querySelectorAll('.announcement-bar__slides').forEach((slides) => {
    if (slides.querySelector('.announcement-bar__slide[aria-hidden="false"]')) return;
    const first = slides.querySelector('.announcement-bar__slide');
    if (first) first.setAttribute('aria-hidden', 'false');
  });
})();
