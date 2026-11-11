import { Component } from '@theme/component';
import { morph } from '@theme/morph';
import { StandardEvents } from '@shopify/events';

/**
 * Keeps the product-label overlay in sync with the selected variant.
 *
 * Mirrors assets/product-price.js: listen for StandardEvents.productSelect on
 * the closest scope, await the event's promise, and swap in the freshly
 * server-rendered markup. All label logic lives in
 * snippets/bmp-product-labels.liquid — this element does no computation of its
 * own, so there is exactly one source of truth.
 *
 * Scope selection matters. On the product page the event bubbles to the
 * section. Inside a product card it is dispatched on the card itself
 * (assets/product-card.js:200) and then continues up to the section, so a PDP
 * element listening on the section would also see card events. The
 * card-originated guard below is the same one product-price.js:40 uses.
 *
 * Children are morphed rather than the element itself, so the context and
 * position classes on the wrapper survive. That matters because a card's
 * fetched HTML is the PRODUCT PAGE, whose element carries
 * `bmp-product-labels--pdp`; morphing the whole element would swap a card's
 * inset scale to the product page's.
 */
class BmpProductLabels extends Component {
  #scope = null;

  connectedCallback() {
    super.connectedCallback();
    this.#scope = this.closest('product-card') ?? this.closest('.shopify-section, dialog');
    if (!this.#scope) return;
    this.#scope.addEventListener(StandardEvents.productSelect, this.#handleProductSelect);
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    this.#scope?.removeEventListener(StandardEvents.productSelect, this.#handleProductSelect);
    this.#scope = null;
  }

  /**
   * @param {Event & { promise?: Promise<{ detail?: { html?: Document } }> }} event
   */
  #handleProductSelect = (event) => {
    // A card-originated event must not update a product-page overlay that
    // happens to share the section. Same guard as product-price.js:40.
    const insideCard = this.closest('product-card') != null;
    if (!insideCard && event.target instanceof Element && event.target.closest('product-card')) return;

    event.promise
      ?.then(({ detail }) => {
        const html = detail?.html;
        if (!html) return;

        const next = html.querySelector('bmp-product-labels');
        if (!next) return;

        // Morph children only — keep this element's own context/position
        // classes. See the class comment for why.
        morph(this, this.#withOwnAttributes(next));
      })
      .catch((error) => {
        if (error?.name !== 'AbortError') console.warn('[bmp-product-labels] event promise rejected:', error);
      });
  };

  /**
   * Returns a copy of the incoming element carrying THIS element's class,
   * style and data attributes, so morph updates only the pills.
   * @param {Element} incoming
   * @returns {Element}
   */
  #withOwnAttributes(incoming) {
    const clone = /** @type {Element} */ (incoming.cloneNode(true));
    for (const attr of Array.from(clone.attributes)) clone.removeAttribute(attr.name);
    for (const attr of Array.from(this.attributes)) clone.setAttribute(attr.name, attr.value);
    return clone;
  }
}

if (!customElements.get('bmp-product-labels')) {
  customElements.define('bmp-product-labels', BmpProductLabels);
}
