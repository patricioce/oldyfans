/**
 * PDP title auto-fit custom element.
 *
 * Feature-scoped module: loaded only from
 * snippets/bmp-title-fit.liquid, at the render site of a product-title block
 * whose auto-fit engaged (bmp_title_autofit on, real product, title 1-48
 * characters). The one-line commitment itself is CSS
 * (bmp-title-fit[data-bmp-fit] applies white-space: nowrap from first paint,
 * assets/bmp-styles.css) — this element only shrinks the font inside that
 * committed line box, never grows it, and pins the measured line-height so
 * the box height cannot move when the glyphs change size (webfont swap
 * included: font-display is swap everywhere, so document.fonts.ready
 * re-measures after the real face arrives).
 *
 * Measurement contract: available width comes from the nearest ancestor that
 * generates a box (the wrapper itself, the stock <a class="contents"> and the
 * global-style <div class="bmp-card-global-title"> are all display: contents;
 * .text-block is width: fit-content in stock form and must never be the
 * yardstick — its width follows the text, which would feed back). Needed
 * width is measured with a Range over the title text, which reports
 * FRACTIONAL width; scrollWidth is integer-rounded and leaves the last glyph
 * shaved against the clip edge. Writes go to the wrapper only (two custom properties +
 * data-bmp-fit-ready), with an equality guard so re-runs are free.
 */
// The solve targets `available - SLACK` rather than `available`. Aiming at the
// exact box edge leaves the last glyph flush against the clip, and the widths
// this element can read (Range rects, scrollWidth) come back QUANTISED to
// whole pixels on the PDP, so a sub-pixel overshoot is not even measurable —
// measured: text 367px inside a 366px box, unchanged by further correction
// passes. Two pixels of slack absorbs that rounding in one pass; at a 32px
// title that is ~0.5% of the size, which is invisible, and it only ever makes
// the text smaller, never clipped.
const SLACK = 2;

if (!customElements.get('bmp-title-fit')) {
  class BmpTitleFit extends HTMLElement {
    #animationFrame = 0;
    #abortController = new AbortController();
    #resizeObserver = new ResizeObserver(() => this.#scheduleFit());
    #mutationObserver = new MutationObserver(() => this.#scheduleFit());
    #appliedSize = '';

    connectedCallback() {
      if (!this.hasAttribute('data-bmp-fit')) return;
      this.#connectObservers();
      this.#scheduleFit();
    }

    disconnectedCallback() {
      this.#disconnectObservers();
    }

    get #target() {
      const textBlock = this.querySelector('.text-block');
      const target = textBlock?.firstElementChild;
      return target instanceof HTMLElement ? target : null;
    }

    get #container() {
      let node = this.parentElement;
      while (node && getComputedStyle(node).display === 'contents') {
        node = node.parentElement;
      }
      return node;
    }

    #connectObservers() {
      this.#disconnectObservers();
      this.#abortController = new AbortController();

      const container = this.#container;
      if (container) this.#resizeObserver.observe(container);

      // Observe the WRAPPER, not the current title node: a morph or a Section
      // Rendering update can REPLACE that node rather than mutate its text,
      // which would strand an observer bound to the detached one. Watching
      // `this` is safe because the fit writes only to this element's inline
      // style and its data-bmp-fit-ready attribute, and neither `attributes`
      // nor style mutations are observed here.
      this.#mutationObserver.observe(this, {
        characterData: true,
        childList: true,
        subtree: true,
      });

      const fontsReady = document.fonts?.ready;
      if (fontsReady) {
        const { signal } = this.#abortController;
        void fontsReady.then(() => {
          if (!signal.aborted) this.#scheduleFit();
        });
      }
    }

    #disconnectObservers() {
      this.#abortController.abort();
      this.#resizeObserver.disconnect();
      this.#mutationObserver.disconnect();

      if (this.#animationFrame) {
        cancelAnimationFrame(this.#animationFrame);
        this.#animationFrame = 0;
      }
    }

    #scheduleFit = () => {
      if (this.#animationFrame) return;

      this.#animationFrame = requestAnimationFrame(() => {
        this.#animationFrame = 0;
        this.#fit();
      });
    };

    #availableWidth() {
      const container = this.#container;
      if (!container) return 0;

      const style = getComputedStyle(container);
      return container.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    }

    /**
     * Sub-pixel text width. scrollWidth/clientWidth are INTEGER-rounded, so a
     * solve driven by them converges to "within a pixel or two" and can leave
     * the last glyph shaved against the clip edge (measured: 368 vs 366 at a
     * 366px column). A Range over the text reports fractional width, which is
     * what the solve needs.
     */
    #textWidth(target) {
      const range = document.createRange();
      range.selectNodeContents(target);
      const width = range.getBoundingClientRect().width;
      range.detach?.();
      return width || target.scrollWidth;
    }

    #fit() {
      const target = this.#target;
      if (!target) return;

      const available = this.#availableWidth();
      if (available <= 0) return;

      // Measure at the base (configured) size: dropping the ready attribute
      // disables the fit rule, so the reads below see the merchant's size —
      // including the per-device mobile size when that rule is active.
      const wasReady = this.hasAttribute('data-bmp-fit-ready');
      this.removeAttribute('data-bmp-fit-ready');

      const baseSize = parseFloat(getComputedStyle(target).fontSize);
      const baseLineHeight = target.getBoundingClientRect().height;
      if (!baseSize || !baseLineHeight) {
        // Nothing measurable (element hidden at this moment). Restore whatever
        // fit was already applied rather than leaving the title un-fitted
        // inside a box that still clips it.
        if (wasReady) this.setAttribute('data-bmp-fit-ready', '');
        return;
      }

      // Shrink-only, no minimum: the Liquid 48-character gate is what keeps
      // this from ever producing unreadable text.
      let size = baseSize;
      let needed = this.#textWidth(target);

      // The box that actually CLIPS is the title element's own, which can be a
      // pixel narrower than the container's content box (max-inline-size from
      // snippets/text.liquid, fractional layout). Solving against the
      // container alone therefore leaves the last glyph a pixel over the clip
      // edge — measured on the PDP at a 366px column. Clamp to the target box,
      // but ONLY when that box is not itself text-driven: with a fit-content
      // ancestor the box tracks the text, and clamping to it would chase its
      // own tail on every pass.
      const boxWidth = target.getBoundingClientRect().width;
      const textDriven = boxWidth >= needed - 0.5;
      const limit = textDriven || boxWidth <= 0 ? available : Math.min(available, boxWidth);
      const room = Math.max(1, limit - SLACK);

      if (needed > room) {
        // floor, never round: the solve must not overshoot upward.
        size = Math.max(1, Math.floor(baseSize * (room / needed) * 100) / 100);
      }

      this.style.setProperty('--bmp-title-fit-lh', `${baseLineHeight}px`);
      this.#apply(size);
      this.setAttribute('data-bmp-fit-ready', '');

      // Font rendering is not perfectly proportional (same caveat as core's
      // jumbo-text.js) and hinting quantises stem widths, so one proportional
      // pass can still overflow. Correct with a bounded loop, each pass capped
      // by the previous result so this can only ever shrink.
      for (let pass = 0; pass < 3 && size < baseSize; pass += 1) {
        needed = this.#textWidth(target);
        if (needed <= room) break;
        const next = Math.max(1, Math.floor(size * (room / needed) * 100) / 100);
        if (next >= size) break;
        size = next;
        this.#apply(size);
      }
    }

    #apply(size) {
      const value = `${size}px`;
      if (value === this.#appliedSize) return;
      this.style.setProperty('--bmp-title-fit-size', value);
      this.#appliedSize = value;
    }
  }

  customElements.define('bmp-title-fit', BmpTitleFit);
}
