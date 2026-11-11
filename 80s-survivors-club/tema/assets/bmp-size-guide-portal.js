// bmp-size-guide-portal.js — keeping the size guide reachable in a hostile DOM
//
// This module owns one job: the size guide stays openable no matter what the
// surrounding DOM does to it. Two independent reparenting routines serve that
// job, plus the config handoff that decides WHICH trigger candidate shows at
// all; they are described in turn below.
//
//   PART 1 — the DIALOG, moved out of the quick-add popup.
//   PART 2 — the TRIGGER, moved out of an unrenderable variant picker.
//   PART 3 — the CONFIG, read off the block's dialog element and
//            applied to the trigger candidates.
//
// ════ PART 1 — the dialog ═══════════════════════════════════════════════════
//
// WHAT: Keeps the "Size Guide" chart working from inside quick-add's popup by
// guaranteeing the size-guide dialog is a child of <body> — never a DOM
// descendant of the open quick-add dialog — and by removing whatever it
// adopted once that popup closes.
//
// WHY: quick-add clones the whole product page's [data-product-grid-content]
// into its own modal (assets/quick-add.js:112-127), so the size-guide block
// lands INSIDE the already-open quick-add dialog. Opening it there is broken
// two independent ways, and both are consequences of that descendancy:
//
//   1. Events. dialog.js:62-63 binds click/keydown on the dialog COMPONENT, so
//      a click or an Escape inside the nested dialog bubbles into the outer
//      quick-add component's handlers. isClickedOutside (utilities.js:395-401)
//      switches to a geometric hit-test when the event target is an
//      HTMLDialogElement, so a click on the inner dialog that lands outside the
//      quick-add dialog's rect reads as an outside-click on the OUTER one and
//      closes it; Escape closes both, running the outer's dialog.close() while
//      the inner is still open and leaving the document inert — the frozen
//      screen this bug was reported as.
//   2. Layout. `.quick-add-modal[open]` animates with
//      `modalSlideInTop … forwards` (snippets/quick-add-modal-styles.liquid:74-76),
//      whose final keyframe is `transform: translateY(0)` — a non-none
//      transform the fill mode holds forever — plus `overflow: hidden`
//      (`clip` on mobile). A modal <dialog> is position: fixed, so a
//      transformed ancestor becomes its containing block: the nested dialog
//      lays out inside the quick-add box instead of the viewport.
//
// Moving the node to <body> removes the descendancy and therefore both
// failures at once: no bubbling into the outer component's handlers, and no
// transformed ancestor. The two dialogs then simply stack in the top layer in
// showModal() order — the chart above the popup — and each one's own Escape /
// outside-click handler only sees its own events. Closing the chart returns
// focus to the trigger inside the popup; a second Escape closes the popup.
//
// The previous fix suppressed the trigger inside `.quick-add-modal` with CSS
// instead, which removed the feature from that surface rather than fixing it.
//
// Three resolution routes, in order:
//   1. A copy already outside the popup (the host PDP's own dialog block) wins,
//      and any stale in-popup duplicate of that id is dropped so the id stays
//      unique — the trigger resolves its target by id.
//   2. Desktop quick-add: adopt the copy quick-add cloned into the popup by
//      moving it to <body>. No network.
//   3. Mobile quick-add: updateQuickAddModal removes `.product-details`
//      (assets/quick-add.js:246) and the size-guide block renders inside it
//      (templates/product.json, product-details block_order), so there is no
//      copy to adopt — fetch the product page once per product and adopt the
//      dialog out of the parsed response.
//
// Resolution runs eagerly on quick-add's `dialog:open`, not on the trigger
// click: blocks/bmp-size-guide.liquid emits the trigger's reveal rule from a
// `{% style %}` INSIDE the dialog-component, so appending that node is also
// what reveals the trigger on the mobile route, and the click then has no
// latency. (That placement is load-bearing for route 3: the fetch adopts the
// `[data-bmp-size-guide-dialog]` element alone, and a `<style>` beside it would
// stay behind in the parse document.)
//
// Cost: two capture-phase document listeners. One extra product-page GET per
// product on the mobile route only — the same URL quick-add already fetched, so
// the HTTP cache usually serves it — memoized per URL for the page's lifetime.
//
// ════ PART 2 — the trigger ══════════════════════════════════════════════════
//
// WHAT: When a <variant-picker> is not rendered, the size-guide trigger inside
// it is moved out — to the picker's own parent, immediately before the picker —
// and moved back if the picker ever renders again.
//
// WHY: swatch apps commonly replace Horizon's native picker rather than
// integrate with it: they inject their own swatch UI as a sibling and set
// `display: none` INLINE on the <variant-picker>. The trigger is rendered by
// the contracted edit in snippets/variant-main-picker.liquid, inside the Size
// option's <legend> — i.e. inside the element that got hidden. It then measures
// 0x0 and there is no way to open the chart at all: the size guide is dead on
// every product page of such a store. The dialog is fine; only its opener is
// unreachable.
//
// CSS cannot fix this. A descendant of `display: none` cannot be shown again,
// at any specificity — the subtree generates no boxes. The node has to leave.
//
// Detection is deliberately generic — `checkVisibility()`, falling back to
// `getClientRects().length` — and never keys on any app's class names. The
// condition that matters is "the picker is not rendered", whoever caused it;
// keying on one vendor's markers would ship a fix that only works until the
// merchant installs a different app doing the same thing.
//
// Where it lands: the picker's own parent, immediately before the picker. On
// the confirmed structure that parent is the theme's own
// `div.group-block-content` (the swatch app's UI is the picker's preceding
// sibling inside it), so the trigger comes to rest directly under the app's
// size row — a theme-owned container, not the app's internals. That position is
// re-asserted on every pass rather than set once: the app injects its own UI
// immediately before the picker as well, and it can do so after the trigger has
// already moved there, which would otherwise strand the button above the swatch
// rows.
//
// Nothing moves on a store without such an app: a rendered picker keeps its
// trigger in the legend and the contracted `[ Size: 2XL … Size Guide ]` row is
// untouched. The relocated state carries its own class so its (very small)
// layout rule lives in the trigger snippet's stylesheet, not inline.
//
// No rewiring is needed after the move: the click handler below is a delegated
// document listener resolving with `target.closest(TRIGGER_SELECTOR)`, so the
// trigger works from anywhere in the document.
//
// Timing: the hide happens asynchronously, long after this module runs, and a
// variant change morphs the picker (which can re-inject a trigger inside it),
// so a MutationObserver drives a re-sync. It watches <html> for childList and
// for `style`/`class`/`hidden` attribute changes at any depth: an ancestor can
// be what got hidden, and the picker itself can be injected or replaced. The
// callback is O(1) — it only schedules one rAF-coalesced pass — and the pass
// itself walks `document.querySelectorAll('variant-picker')`, which is one or
// two elements. The pass is idempotent, so the mutations it causes settle on
// the next frame instead of looping.
//
// ════ PART 3 — the config ═══════════════════════════════════════════════════
//
// WHAT: exactly one value — the block's link text. It lives on the "BMP: Size
// guide" block, the trigger renders in the variant picker's legend, and Liquid
// exposes no sibling block's settings, so the block publishes it as
// data-bmp-size-guide-label on its dialog and this pass copies it onto the
// trigger for the same product, resolved by the dialog's per-product id (never
// another product's, which would decorate a button whose click resolves
// nothing).
//
// WHAT THIS IS NOT. The option name is not part of the handoff: it stays the
// theme setting `settings.bmp_size_guide_option`, because the server-side
// add-to-cart gate reads the same value from blocks/buy-buttons and
// blocks/accelerated-checkout, where no block's settings are reachable. That is
// what lets the trigger snippet gate itself server-side, so this module never
// decides WHETHER a trigger shows. Neither is the ICON: the block emits a rule
// for it — per product, in the same `{% style %}` that carries the reveal — or
// emits none, so it resolves at parse time with no JS. One mechanism per value
// — a second writer could only disagree with the first.
//
// The remaining write is change-guarded so the pass stays idempotent and the
// MutationObserver that schedules it cannot feed itself.
// Quick-add clones and variant-change morphs re-inject the server's undecorated
// trigger; the same observer that drives Part 2 re-runs this pass over it.

(() => {
  const TRIGGER_SELECTOR = '.bmp-size-guide__trigger';
  const DIALOG_SELECTOR = '[data-bmp-size-guide-dialog]';
  const CONFIG_SELECTOR = '[data-bmp-size-guide-config]';
  const QUICK_ADD_MODAL_SELECTOR = '.quick-add-modal';
  const QUICK_ADD_DIALOG_ID = 'quick-add-dialog';
  const PICKER_SELECTOR = 'variant-picker';
  const RELOCATED_CLASS = 'bmp-size-guide__trigger--relocated';

  /**
   * Parsed size-guide dialogs keyed by the product URL they were fetched from.
   * Stores the node from the detached parse document and hands out clones, so
   * releasing an adopted copy never empties the cache.
   * @type {Map<string, Promise<Element | null>>}
   */
  const fetchedDialogs = new Map();

  /**
   * Dialogs this module moved (or fetched) into <body> for the popup, and must
   * take back out when that popup closes. A host page's own dialog block is
   * never in here.
   * @type {Set<Element>}
   */
  const adoptedDialogs = new Set();

  /**
   * In-flight resolutions keyed by dialog id, so the eager resolve on
   * quick-add's open and a click that lands before it settles share ONE result.
   * Without this, the fetch route (whose await is long enough to lose the race)
   * would append two clones of the same id.
   * @type {Map<string, Promise<Element | null>>}
   */
  const resolvingDialogs = new Map();

  /** Whether the quick-add popup is currently open (route 3's staleness check). */
  let quickAddOpen = false;

  /** @param {string} productId */
  const dialogIdFor = (productId) => `bmp-size-guide-dialog-${productId}`;

  /**
   * Every node in the document carrying this id. Deliberately not
   * getElementById: quick-add's clone can duplicate an id, and the duplicate is
   * exactly what needs finding.
   * @param {string} id
   * @returns {Element[]}
   */
  function nodesWithId(id) {
    return Array.from(document.querySelectorAll(`${DIALOG_SELECTOR}[id="${CSS.escape(id)}"]`));
  }

  /**
   * Move a dialog to <body> and remember to release it on popup close.
   * @param {Element} node
   * @returns {Element}
   */
  function adopt(node) {
    document.body.append(node);
    adoptedDialogs.add(node);
    return node;
  }

  /**
   * Fetch a product page once and return a fresh clone of its size-guide dialog.
   * @param {string | undefined} url
   * @param {string} id
   * @returns {Promise<Element | null>}
   */
  async function fetchDialog(url, id) {
    if (!url) return null;

    let pending = fetchedDialogs.get(url);
    if (!pending) {
      pending = (async () => {
        const response = await fetch(url);
        if (!response.ok) return null;
        const parsed = new DOMParser().parseFromString(await response.text(), 'text/html');
        return parsed.querySelector(`${DIALOG_SELECTOR}[id="${CSS.escape(id)}"]`);
      })().catch(() => null);
      fetchedDialogs.set(url, pending);
    }

    const found = await pending;
    return found ? /** @type {Element} */ (found.cloneNode(true)) : null;
  }

  /**
   * Resolve the one dialog node a trigger should open, guaranteeing it is not
   * inside the quick-add popup. Concurrent calls for the same product share one
   * resolution.
   * @param {HTMLElement} trigger
   * @returns {Promise<Element | null>}
   */
  function resolveDialog(trigger) {
    const productId = trigger.dataset.bmpSizeGuideProduct;
    if (!productId) return Promise.resolve(null);

    const id = dialogIdFor(productId);

    const inFlight = resolvingDialogs.get(id);
    if (inFlight) return inFlight;

    const pending = resolve(trigger, id).finally(() => resolvingDialogs.delete(id));
    resolvingDialogs.set(id, pending);
    return pending;
  }

  /**
   * @param {HTMLElement} trigger
   * @param {string} id
   * @returns {Promise<Element | null>}
   */
  async function resolve(trigger, id) {
    const existing = nodesWithId(id);

    // Route 1 — a copy already lives outside the popup. showModal() promotes it
    // to the top layer, which lifts the inertness the open popup put it under,
    // so it opens correctly from in there. Drop in-popup duplicates: the
    // trigger resolves by id and a duplicate id makes that ambiguous. Also
    // self-heals a variant-change morph re-injecting a copy into the popup.
    const outsidePopup = existing.find((node) => !node.closest(QUICK_ADD_MODAL_SELECTOR));
    if (outsidePopup) {
      for (const node of existing) {
        if (node !== outsidePopup) node.remove();
      }
      return outsidePopup;
    }

    // Route 2 — adopt quick-add's clone out of the popup.
    const insidePopup = existing[0];
    if (insidePopup) return adopt(insidePopup);

    // Route 3 — mobile: nothing to adopt, fetch it. Only ever reached from a
    // popup trigger (a host page whose template lacks the block keeps its
    // trigger hidden), so a popup that closed mid-fetch means the result is
    // stale: adopting it anyway would leave an orphan in <body> that no
    // dialog:close releases — and the orphan carries its own reveal rule, so
    // that product's trigger would light up wherever it turns up next with the
    // chart detached from the popup that was supposed to own it.
    const fetched = await fetchDialog(trigger.dataset.bmpSizeGuideUrl, id);
    if (!fetched || !quickAddOpen) return null;
    return adopt(fetched);
  }

  /**
   * Open a resolved dialog through its own component API (focus trap, Escape,
   * scroll lock all stay Horizon's).
   * @param {Element} node
   */
  async function openDialog(node) {
    await customElements.whenDefined('dialog-component');
    customElements.upgrade(node);

    const component = /** @type {Element & { showDialog?: () => void }} */ (node);
    if (typeof component.showDialog !== 'function') return;
    component.showDialog();
  }

  /**
   * Take an adopted dialog back out of <body>.
   *
   * Closes through closeDialog() first when it is open, and awaits it, so
   * Horizon runs its own teardown on an attached node: unlockScroll(dialog),
   * the scroll-position restore, and DialogCloseEvent. Detaching an open dialog
   * instead leans on pruneDisconnectedScrollLockOwners (utilities.js:344-350),
   * which does eventually drop the stale scroll-lock owner via the
   * documentElement MutationObserver — but skips the scroll restore and the
   * close event, and leaves focus wherever the removed subtree had it.
   * @param {Element} node
   */
  async function release(node) {
    const component = /** @type {Element & { closeDialog?: () => Promise<void> }} */ (node);
    const dialog = node.querySelector('dialog');

    if (dialog?.open && typeof component.closeDialog === 'function') {
      await component.closeDialog();
    }

    node.remove();
  }

  /** @param {Event} event */
  function handleTriggerClick(event) {
    const target = event.target;
    if (!(target instanceof Element)) return;

    const trigger = /** @type {HTMLElement | null} */ (target.closest(TRIGGER_SELECTOR));
    if (!trigger) return;

    event.preventDefault();
    resolveDialog(trigger).then((node) => {
      if (node) openDialog(node);
    });
  }

  /**
   * Quick-add fires `dialog:open` after its content is morphed in, so every
   * cloned trigger is already present here.
   * @param {Event} event
   */
  function handleQuickAddOpen(event) {
    const modal = event.target;
    if (!(modal instanceof Element) || modal.id !== QUICK_ADD_DIALOG_ID) return;

    quickAddOpen = true;

    // No pre-filter here on purpose. The guard this replaced inferred "this
    // product has no size-guide block" from ".product-details present && no
    // dialog in the clone", which is only true while the block sits inside
    // .product-details — and the block has presets, so a merchant may place it
    // anywhere `closest.product` resolves. It was needed while the server
    // rendered one trigger candidate per option legend; with the option gate
    // back on the server, a modal only holds a trigger for a product that
    // actually has the configured option, which is the same set of resolves
    // this module performed before the config handoff existed.
    for (const trigger of modal.querySelectorAll(TRIGGER_SELECTOR)) {
      resolveDialog(/** @type {HTMLElement} */ (trigger));
    }
  }

  /** @param {Event} event */
  function handleQuickAddClose(event) {
    const modal = event.target;
    if (!(modal instanceof Element) || modal.id !== QUICK_ADD_DIALOG_ID) return;

    quickAddOpen = false;

    for (const node of adoptedDialogs) release(node);
    adoptedDialogs.clear();
  }

  // ── PART 2 — relocating the trigger out of an unrenderable picker ──────────

  /**
   * The trigger this module moved out of each picker, so a later pass can put
   * it back, and so a morph that re-injects a trigger inside the picker can be
   * deduped against it. Keyed weakly: a picker replaced wholesale by a section
   * render takes its entry with it.
   * @type {WeakMap<Element, HTMLElement>}
   */
  const relocatedTriggers = new WeakMap();

  /**
   * Where each relocated trigger came from, so reverting restores its exact
   * position in the legend rather than guessing one.
   * @type {WeakMap<HTMLElement, { parent: Element, next: Node | null }>}
   */
  const triggerOrigins = new WeakMap();

  /** @type {number | null} */
  let scheduledSync = null;

  /**
   * Whether an element is actually rendered. checkVisibility() with default
   * options answers exactly the question that matters — does this element
   * generate boxes — including when the `display: none` sits on an ancestor.
   * getClientRects() is the fallback for engines without it.
   * @param {Element} el
   * @returns {boolean}
   */
  function isRendered(el) {
    if (typeof el.checkVisibility === 'function') return el.checkVisibility();
    return el.getClientRects().length > 0;
  }

  /**
   * Move a trigger out of its picker, remembering where it came from.
   * @param {Element} picker
   * @param {HTMLElement} trigger
   */
  function relocate(picker, trigger) {
    const host = picker.parentElement;
    if (!host || !trigger.parentElement) return;

    triggerOrigins.set(trigger, { parent: trigger.parentElement, next: trigger.nextSibling });
    trigger.classList.add(RELOCATED_CLASS);
    host.insertBefore(trigger, picker);
    relocatedTriggers.set(picker, trigger);
  }

  /**
   * Put a relocated trigger back where it came from, now that its picker
   * renders again. If a morph already re-injected one inside the picker, the
   * relocated copy is simply dropped — the in-picker one is the fresher node.
   * @param {Element} picker
   * @param {HTMLElement} trigger
   */
  function restore(picker, trigger) {
    relocatedTriggers.delete(picker);
    trigger.classList.remove(RELOCATED_CLASS);

    const origin = triggerOrigins.get(trigger);
    triggerOrigins.delete(trigger);

    if (picker.querySelector(TRIGGER_SELECTOR) || !origin || !picker.contains(origin.parent)) {
      trigger.remove();
      return;
    }

    const next = origin.next?.parentNode === origin.parent ? origin.next : null;
    origin.parent.insertBefore(trigger, next);
  }

  /**
   * Bring one picker's trigger to the reachable side. Idempotent: called again
   * with nothing to do it mutates nothing, which is what keeps the
   * MutationObserver that calls it from feeding itself.
   * @param {Element} picker
   */
  function syncPicker(picker) {
    // A picker inside a closed <dialog> is unrendered because the dialog is
    // shut, not because anything hid it — quick-add's own markup before it
    // opens. Relocating there would move the trigger to a sibling that is just
    // as closed, and the open handler re-syncs anyway.
    if (picker.closest('dialog:not([open])')) return;

    const previous = relocatedTriggers.get(picker);
    const relocated = previous?.isConnected && !picker.contains(previous) ? previous : null;
    if (previous && !relocated) relocatedTriggers.delete(picker);

    if (isRendered(picker)) {
      if (relocated) restore(picker, relocated);
      return;
    }

    // Position is re-asserted, not set once. The app injects its own swatch UI
    // immediately before the picker too, and it can do so AFTER this module has
    // already moved the trigger there — which would leave the button stranded
    // above the swatch rows instead of under them. Re-seating it costs one DOM
    // move per intruder and settles as soon as the app stops inserting; the
    // check below is what keeps that from being a move every frame.
    if (relocated && picker.previousElementSibling !== relocated) {
      picker.parentElement?.insertBefore(relocated, picker);
      return;
    }

    const inside = /** @type {HTMLElement | null} */ (picker.querySelector(TRIGGER_SELECTOR));
    if (!inside) return;

    // Only act once THIS trigger's own product has a dialog on the page.
    // Without one the trigger is hidden by the block's missing per-product
    // reveal rule — legitimately, because the merchant never placed the
    // size-guide block on that product's template — and relocating it would
    // move an element that stays invisible. Per product rather than
    // "any dialog anywhere", which is what the reveal itself now keys on: a
    // PDP carrying a featured-product section for a second product would
    // otherwise relocate the second product's trigger on the strength of the
    // first product's dialog.
    const productId = inside.dataset.bmpSizeGuideProduct;
    if (!productId || nodesWithId(dialogIdFor(productId)).length === 0) return;

    // A trigger inside the picker while one is already relocated means a morph
    // re-injected it (variant change). The fresh node wins — its data
    // attributes are the ones matching the newly selected variant — and the
    // stale relocated copy goes, so the document never holds two.
    if (relocated) relocated.remove();
    relocate(picker, inside);
  }

  // ── PART 3 — applying the block's config to the trigger candidates ─────────

  /**
   * Apply the size-guide block's link text to the trigger for the SAME product,
   * and nothing else. The option name is not part of this handoff: the trigger
   * is gated server-side on `settings.bmp_size_guide_option`, so a trigger that
   * exists is already the right one, in the right legend. This pass only
   * decorates it.
   *
   * A trigger with no config element keeps exactly what the server rendered:
   * the shipped default label. That state is reachable — the product has the
   * configured option on a template with no size-guide block — and it is also
   * invisible, which is a property of the REVEAL, not of this pass.
   *
   * That is worth stating precisely, because it was false until the per-product
   * reveal landed. The reveal used to be `body:has([data-bmp-size-guide-dialog])`,
   * per DOCUMENT, while the trigger's target is per product: a page holding ANY
   * size-guide dialog revealed every trigger on it — reachable through
   * sections/featured-product-information.liquid and featured-product.liquid,
   * which render a variant picker for a merchant-chosen second product, and
   * through a quick-add whose adopted dialog lands in <body>. Those triggers
   * were visible, undecorated, and their click resolved nothing. The reveal is
   * now emitted per product by blocks/bmp-size-guide.liquid, from a
   * `{% style %}` inside the dialog-component, so "no config element for this
   * product" and "no trigger for this product" are once again the same fact.
   *
   * Deliberately NO cross-product fallback: lending product A's label to
   * product B's trigger would decorate a button whose click resolves nothing.
   * Duplicate ids (a quick-add clone before adoption) are harmless — both
   * copies carry identical config values.
   *
   * One `querySelectorAll` per pass, not one per trigger: this runs from a
   * `subtree: true, attributes: true` observer on `<html>`, so it re-runs on
   * every mutation batch on every page of the store, and the per-trigger form
   * walked the whole document once for each option legend.
   *
   * Change-guarded writes keep the pass idempotent for the MutationObserver.
   */
  function applyTriggerConfigs() {
    const triggers = /** @type {NodeListOf<HTMLElement>} */ (
      document.querySelectorAll(TRIGGER_SELECTOR)
    );
    if (!triggers.length) return;

    /** @type {Map<string, HTMLElement>} */
    const configs = new Map();
    for (const el of /** @type {NodeListOf<HTMLElement>} */ (
      document.querySelectorAll(CONFIG_SELECTOR)
    )) {
      if (el.id) configs.set(el.id, el);
    }

    for (const trigger of triggers) {
      const productId = trigger.dataset.bmpSizeGuideProduct;
      const config = productId ? configs.get(dialogIdFor(productId)) : undefined;
      if (!config) continue;

      // Label only. The icon is resolved entirely by the per-product rule the
      // block emits next to this element, so nothing here touches it — one
      // mechanism, not two that can disagree.
      // That also removes the write this pass had to change-guard: `hidden`
      // reflects through setAttribute, which enqueues a mutation record even
      // for an unchanged value, and 'hidden' is in this module's own
      // attributeFilter, so an unguarded write re-scheduled the pass every
      // frame forever on any page whose icon toggle was off.
      const label = trigger.querySelector('.bmp-size-guide__trigger-label');
      const text = config.dataset.bmpSizeGuideLabel ?? '';
      if (label && text && label.textContent !== text) label.textContent = text;
    }
  }

  function syncAll() {
    scheduledSync = null;
    applyTriggerConfigs();
    for (const picker of document.querySelectorAll(PICKER_SELECTOR)) syncPicker(picker);
  }

  /** Coalesce every mutation batch in a frame into one pass. */
  function scheduleSync() {
    if (scheduledSync !== null) return;
    scheduledSync = requestAnimationFrame(syncAll);
  }

  document.addEventListener('click', handleTriggerClick);

  // DialogOpenEvent / DialogCloseEvent are non-bubbling CustomEvents dispatched
  // on the dialog component (dialog.js), so these must be capture-phase
  // document listeners — which also means they work regardless of when
  // snippets/quick-add-modal.liquid's element enters the DOM.
  document.addEventListener('dialog:open', handleQuickAddOpen, true);
  document.addEventListener('dialog:close', handleQuickAddClose, true);

  // Part 2's and Part 3's shared driver. One observer, one target: <html>.
  // childList catches a picker being injected, morphed or replaced (and
  // catches the swatch app inserting its own UI, the size-guide dialog being
  // appended, and a morph re-injecting raw trigger candidates); the attribute
  // filter catches the picker — or any ancestor of it — being hidden.
  // Anything broader would not be cheaper: the callback does no DOM work, and
  // the pass it schedules reads a handful of elements.
  new MutationObserver(scheduleSync).observe(document.documentElement, {
    subtree: true,
    childList: true,
    attributes: true,
    attributeFilter: [
      'style',
      'class',
      'hidden',
      // `open` is in here for <dialog>/<details>: a picker inside one goes
      // from unrendered to rendered with no childList or style change at all.
      'open',
      // The label: the theme editor's live preview morphs a settings change
      // onto the EXISTING dialog element — no childList mutation — and the
      // trigger's text must follow it. The icon needs no entry here: it is a
      // rule in the block's own `{% style %}`, and the editor morphs that
      // element's text along with everything else, which the style engine
      // picks up on its own.
      'data-bmp-size-guide-label',
    ],
  });

  scheduleSync();
})();
