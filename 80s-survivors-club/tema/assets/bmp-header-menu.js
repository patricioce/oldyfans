/**
 * BMP desktop nav dropdown behaviour.
 *
 * Drives the content-sized dropdown card rendered by
 * snippets/bmp-nav-dropdown.liquid: click to open, click again / outside click
 * / Escape / focus-out to close, opening one closes any other, and a
 * collapsible level-3 list per level-2 group.
 *
 * Loaded from snippets/bmp-globals.liquid as an ES module. Nothing is put on
 * `window`. Guarded by scripts/check-nav-dropdown.mjs (A8, A9).
 *
 * -- WHY DELEGATED DOCUMENT LISTENERS, NOT A CUSTOM ELEMENT -----------------
 *
 * The nodes this drives live inside the `data-hydration-key="header-menu"`
 * subtree. That subtree is re-rendered through the Section Rendering API right
 * after load (assets/section-hydration.js), diffed by assets/morph.js, and
 * re-rendered again on every theme-editor change; `overflow-list` also
 * re-slots items between the visible row and the "More" flyout on resize.
 * Listeners bound to specific nodes die on each of those. Delegated listeners
 * registered once on `document` need no re-initialisation at all, which is R5.
 *
 * That is also why v1.1.5's version needed a `window.__rbMegaMenuInitialized`
 * global: it bound per-node listeners from an inline `<script>` inside a
 * snippet rendered once per menu item (its bugs #5 and #9). There is nothing
 * here to guard — a module body runs once.
 *
 * ALL STATE LIVES IN DOM ATTRIBUTES (`aria-expanded` on the trigger,
 * `data-bmp-open` on a level-2 group, and — mirrored, computed from live DOM —
 * `aria-expanded` on the owning <header-menu>, see syncHeaderMenuExpanded). A morph that resets them merely closes
 * the panel, which is a safe resting state; there is no in-memory state to go
 * stale against the DOM.
 *
 * `shopify:section:load` is deliberately NOT listened for. It would be a
 * no-op: there is nothing to re-wire.
 *
 * -- THE FOCUS-THEN-CLICK HAZARD -------------------------------------------
 *
 * The BMP `<li>` keeps the stock `on:focus="/activate"` (decision D5 — it is
 * stock keyboard-open, and its `on:blur` twin is the established focus-out
 * dismissal). assets/component.js resolves that attribute through
 * `target.closest('[on\\:focus]')`, so focusing the trigger inside the `<li>`
 * really does reach core's `activate`, which sets `aria-expanded="true"`.
 *
 * A mouse press fires pointerdown -> focus -> click. So by the time a click
 * handler runs, core has ALREADY opened the panel, and a handler that toggles
 * from the live attribute would read "true" and close it: clicking would never
 * open. The fix is to record the state on `pointerdown`, BEFORE focus, and
 * toggle from that. Keyboard activation (Enter/Space) has no preceding
 * focus-open of its own and reports `event.detail === 0`, so it toggles from
 * live state instead.
 *
 * Both paths are pinned by regression tests ("should open on
 * click", "should close on a second click", "should open from the keyboard").
 */

/** Selector for a level-1 dropdown trigger. */
const TRIGGER = '.bmp-nav-trigger';

/** Selector for a level-2 expand control. */
const GROUP_TOGGLE = '.bmp-nav-group__toggle';

/** The BMP `<li>` wrapping a trigger and its panel. */
const ITEM = '.menu-list__list-item';

/** Rows inside an open panel that keyboard navigation walks, in visual order. */
const PANEL_ROWS =
  '.bmp-nav-panel__parent, .bmp-nav-group__link, .bmp-nav-group__toggle, .bmp-nav-group[data-bmp-open] .bmp-nav-group__item';

/** Viewport gutter the edge clamp keeps the card inside. */
const EDGE_MARGIN = 16;

/**
 * Expanded state of each trigger as it was BEFORE the focus that a mouse press
 * fires. Keyed weakly so a morphed-away trigger is collectable.
 * @type {WeakMap<Element, boolean>}
 */
const preFocusState = new WeakMap();

/** @param {EventTarget | null} target @returns {Element | null} */
const asElement = (target) => (target instanceof Element ? target : null);

/** @param {Element} el @returns {boolean} */
const isExpanded = (el) => el.getAttribute('aria-expanded') === 'true';

/** @returns {HTMLElement | null} */
const headerComponent = () => /** @type {HTMLElement | null} */ (document.querySelector('#header-component'));

/**
 * True when the item has been re-slotted into the "More" flyout.
 *
 * Inside the flyout the dropdown is CORE's to drive, not ours, and this module
 * leaves every level-1 trigger there alone. Two measured reasons:
 *
 *  1. Core already owns `aria-expanded` on those triggers. Opening the flyout
 *     calls core's `activate`, which sets the FIRST overflowed item's
 *     `aria-expanded` to true (`#getFirstOverflowMenuItem`) so its submenu fills
 *     the flyout's right column. On this store that item IS a BMP dropdown, so a
 *     click handler toggling from that state read "already open" and closed it —
 *     clicking an overflowed dropdown did nothing at all.
 *  2. Core's activate still opens the panel there (aria-expanded lands on this
 *     trigger via `#expandableFor`'s no-disclosure fallback, and core clears the
 *     panel's `inert`). The REVEAL, though, needs one BMP rule since 4.1.4:
 *     core's flyout CSS now keys on `.menu-list__disclosure[aria-expanded]`,
 *     which this markup deliberately lacks — assets/bmp-styles.css carries the
 *     mirrored rule keyed on the BMP trigger (nav dropdown group).
 *
 * The level-2 accordion is NOT skipped in overflow — level-3 has to stay
 * operable there too, and nothing in core competes for `data-bmp-open`.
 *
 * @param {Element} item
 */
const inOverflow = (item) => item.getAttribute('slot') === 'overflow' || Boolean(item.closest('[slot="overflow"]'));


/**
 * Keep the card inside the viewport by translating it left when its right edge
 * would overrun. v1.1.5 never clamped at all; a card under the last menu item
 * simply ran off the page.
 *
 * A translate rather than switching to `right: 0`, because the panel's own
 * `left: 0` is what expresses R1's left-edge alignment, and R1 is only asserted
 * for items that do not need clamping.
 * @param {HTMLElement} panel
 */
function clampToViewport(panel) {
  panel.style.removeProperty('--bmp-nav-shift');
  const rect = panel.getBoundingClientRect();
  const overhang = Math.round(rect.right - (window.innerWidth - EDGE_MARGIN));
  if (overhang <= 0) return;
  // Never push the left edge past the opposite gutter — a card wider than the
  // viewport should stay left-aligned and let its own max-width handle it.
  const shift = Math.min(overhang, Math.max(0, Math.round(rect.left - EDGE_MARGIN)));
  if (shift > 0) panel.style.setProperty('--bmp-nav-shift', `${-shift}px`);
}

/**
 * Reset the two custom properties core's `activate` wrote for the full-width
 * band, but ONLY when nothing else in the header is still open.
 *
 * NOTE: the underlay's own collapse is handled entirely in CSS, by a `:has()`
 * rule in assets/bmp-styles.css that reads the live `aria-expanded` of a
 * non-overflow trigger. This module deliberately writes no flag for it — an
 * earlier version did, and it went stale whenever core reassigned its active
 * item behind the module's back (open a card, hover "More"). See that rule's
 * comment.
 *
 * Necessary because core's `#deactivate` early-returns unless the item is still
 * its own `#state.activeItem` (assets/header-menu.js:416 in 4.1.4), so a BMP close often
 * never reaches it and `--full-open-header-height` stays at panel + header
 * height. `.header__underlay-open` is sized from that property, so without this
 * the card closes and leaves a tall empty band painted across the page.
 *
 * The guard matters: zeroing these while the "More" flyout is open would
 * collapse the band the flyout genuinely needs.
 */
function releaseHeaderHeight() {
  const header = headerComponent();
  if (!header) return;
  // Two open-signals to respect: aria-haspopup catches the "More" trigger and
  // any BMP trigger; the disclosure selector catches a NATIVE 4.1.4 item, whose
  // open state lives on its dedicated disclosure button (no aria-haspopup).
  if (header.querySelector('[aria-expanded="true"][aria-haspopup], .menu-list__disclosure[aria-expanded="true"]')) return;
  header.style.setProperty('--submenu-height', '0px');
  header.style.setProperty('--full-open-header-height', '0px');
}

/**
 * Keep the owning <header-menu>'s own aria-expanded in step with reality.
 *
 * Core writes that attribute from activate/deactivate, but those only run when
 * focus moves — and macOS Safari does not focus a button on pointer click, so a
 * BMP click-open can happen with core never involved. The 4.1.4 transparent-
 * header selectors key on `header-menu[aria-expanded='true']`
 * (sections/header.liquid), so without this write a transparent header reverts
 * to transparent the moment the pointer leaves the trigger for the open card.
 * Until 4.1.3 those selectors read `.menu-list__link[aria-expanded='true']` —
 * the BMP trigger itself — which is why this write did not exist before.
 *
 * Computed from live DOM state rather than toggled, with the same two open
 * signals releaseHeaderHeight respects, so a still-open native, overflow or
 * sibling item keeps the attribute true when this card closes.
 * @param {HTMLElement} trigger
 */
function syncHeaderMenuExpanded(trigger) {
  const headerMenu = trigger.closest('header-menu');
  if (!headerMenu) return;
  const anyOpen = headerMenu.querySelector(
    '[aria-expanded="true"][aria-haspopup], .menu-list__disclosure[aria-expanded="true"]'
  );
  headerMenu.setAttribute('aria-expanded', String(Boolean(anyOpen)));
}

/**
 * Collapse every level-2 group in an item.
 *
 * Called on every close path, and NOT gated on the trigger's state. An
 * expanded group leaves a second `aria-expanded="true"` inside the `<li>`, and
 * core's reveal rule is `:has([aria-expanded='true'])` across the whole item —
 * so a group left open behind a closed trigger used to keep the card painted
 * and unrecoverable. assets/bmp-styles.css now hides the panel unless the
 * TRIGGER is expanded, which fixes the painting; this keeps the DOM state
 * honest so a reopen starts from the server-rendered state.
 * @param {Element | null | undefined} item
 */
function collapseGroups(item) {
  item?.querySelectorAll('[data-bmp-nav-group][data-bmp-open]').forEach((group) => {
    group.removeAttribute('data-bmp-open');
    group.querySelector(GROUP_TOGGLE)?.setAttribute('aria-expanded', 'false');
  });
}

/** True when the item is in any kind of open state — trigger OR a group. */
const isItemOpen = (item) => {
  const trigger = item.querySelector(TRIGGER);
  return Boolean(
    (trigger && isExpanded(trigger)) || item.querySelector('[data-bmp-nav-group][data-bmp-open]')
  );
};

/** @param {HTMLElement} trigger */
function close(trigger) {
  const item = trigger.closest(ITEM);
  trigger.setAttribute('aria-expanded', 'false');

  const panel = item?.querySelector('.bmp-nav-panel');
  if (panel instanceof HTMLElement) {
    panel.style.removeProperty('--bmp-nav-shift');
    // Mirror core's deactivate (4.1.4): a collapsed submenu is `inert`, which
    // keeps its links out of the tab order and lets the header row-elevation
    // rule (`:has(.menu-list__submenu:not([inert]))`) release the row.
    panel.inert = true;
  }

  collapseGroups(item);
  syncHeaderMenuExpanded(trigger);
  releaseHeaderHeight();
}

/**
 * Close an item whatever state it is in, including the case where core has
 * already set the trigger to false but a level-2 group is still open. Every
 * dismissal path routes through this rather than through a scan for expanded
 * TRIGGERS, which by construction cannot see an item core closed behind our back.
 * @param {Element} item
 */
function closeItem(item) {
  const trigger = item.querySelector(TRIGGER);
  if (trigger instanceof HTMLElement) close(trigger);
  else collapseGroups(item);
}

/** Every non-overflow BMP item currently in an open state. @returns {Element[]} */
const openItems = () =>
  [...document.querySelectorAll('.bmp-nav-item')].filter((item) => !inOverflow(item) && isItemOpen(item));

/** @param {HTMLElement} trigger */
function open(trigger) {
  const mine = trigger.closest(ITEM);
  // Close by ITEM, not by expanded trigger: opening a sibling is one of the
  // routes where core has already set the other trigger to false, so a scan for
  // expanded triggers would not see it and its expanded group would survive.
  for (const other of openItems()) {
    if (other !== mine) closeItem(other);
  }

  const item = trigger.closest(ITEM);
  trigger.setAttribute('aria-expanded', 'true');

  const panel = item?.querySelector('.bmp-nav-panel');
  if (panel instanceof HTMLElement) {
    // Core's focus-driven activate already cleared `inert` on every pointer
    // open (focus precedes click); clearing it here too covers the paths that
    // never re-focus the trigger and makes a core-set `inert` (blur-close)
    // impossible to inherit into an open card.
    panel.inert = false;
    clampToViewport(panel);
  }
  syncHeaderMenuExpanded(trigger);
}

/** @param {HTMLElement} trigger @param {boolean} shouldOpen */
const setOpen = (trigger, shouldOpen) => (shouldOpen ? open(trigger) : close(trigger));

/**
 * Move focus to the trigger WITHOUT core re-opening the panel.
 *
 * R6 requires Escape to close the card and return focus to the trigger. Doing
 * that naively does not work, and the failure is invisible unless focus happened
 * to be on the trigger already:
 *
 *   keydown Escape (on a group toggle)   aria-expanded=true
 *   focusout from the toggle             aria-expanded=false   <- close() ran
 *   focusin on the trigger               aria-expanded=true    <- core REOPENED
 *
 * Two core behaviours combine. Moving focus off the toggle to the trigger is a
 * blur whose relatedTarget is NOT inside the panel (the trigger is the panel's
 * sibling), so none of core's `deactivate` guards match and it clears its own
 * `#state.activeItem`. The very next focus event therefore no longer hits
 * `activate`'s `item == activeItem` early return, and core opens the panel again
 * — one tick after this module closed it.
 *
 * So the focus attribute is lifted for exactly the duration of the focus() call.
 * assets/component.js resolves the handler by reading `on:focus` off
 * `target.closest('[on:focus]')` AT DISPATCH TIME, and focus() dispatches
 * synchronously, so removing the attribute suppresses precisely this one
 * activation and nothing else. The attribute is restored in a `finally`, so a
 * throw cannot leave the item permanently unable to open from the keyboard.
 *
 * This touches a core ATTRIBUTE at runtime, never the core file — the markup in
 * snippets/bmp-nav-dropdown.liquid still ships `on:focus="/activate"`, which is
 * what decision D5 preserves and what gate A4 asserts.
 *
 * Only the Escape path needs this. ArrowUp also returns focus to the trigger,
 * but there the panel is meant to stay open, so a re-activation is harmless.
 *
 * @param {HTMLElement} trigger
 */
function focusTriggerWithoutReopening(trigger) {
  const item = trigger.closest(ITEM);
  const value = item?.getAttribute('on:focus') ?? null;
  if (item && value !== null) item.removeAttribute('on:focus');
  try {
    trigger.focus();
  } finally {
    if (item && value !== null) item.setAttribute('on:focus', value);
  }
}

// ---------------------------------------------------------------------------
// pointerdown — capture the pre-focus state, and dismiss on an outside press
// ---------------------------------------------------------------------------

document.addEventListener(
  'pointerdown',
  (event) => {
    const target = asElement(event.target);
    if (!target) return;

    const trigger = target.closest(TRIGGER);
    if (trigger) {
      // Inside the "More" flyout the trigger is core's; see `inOverflow`.
      const item = trigger.closest(ITEM);
      if (item && inOverflow(item)) return;
      // Read BEFORE the focus this press is about to fire, which core turns
      // into an open. See the header comment.
      preFocusState.set(trigger, isExpanded(trigger));
      return;
    }

    // A press anywhere else dismisses any open card it did not land inside.
    // Explicit rather than leaning on the incidental blur: a press
    // on non-focusable page furniture does not always move focus.
    for (const item of openItems()) {
      if (!item.contains(target)) closeItem(item);
    }
  },
  { capture: true }
);

// ---------------------------------------------------------------------------
// mousedown — keep a press on the card's own surface from blurring the trigger
// ---------------------------------------------------------------------------

/** Elements that legitimately take focus when pressed. */
const FOCUSABLE = 'a[href], button, input, select, textarea, summary, [tabindex]:not([tabindex="-1"])';

/**
 * A press on the card's non-interactive surface must not close the card.
 *
 * Pressing a non-focusable node moves focus to <body>, which fires the `<li>`'s
 * stock `on:blur="/deactivate"` and lets CORE close the panel — measured with a
 * real mouse click on the card's block padding: activeElement became BODY and
 * the card closed. This module's own focusout ignores a null relatedTarget
 * (see below), but that alone cannot help, because the close comes from core.
 *
 * The dead surface is smaller than it looks — the rows are full-bleed, so their
 * 16px gutters are inside the links — but the card's ~11px block padding and
 * the gap between a group's link and its toggle are real, and a near-miss on a
 * toggle dismissing the whole panel is a bad affordance.
 *
 * Suppressing the default action of `mousedown` is the standard fix: it keeps
 * focus where it is, so core never sees a blur, while the subsequent `click`
 * still fires normally. Deliberately NOT done on `pointerdown` — preventing
 * that does not stop the compatibility `mousedown` that actually moves focus.
 * Scoped to presses on non-focusable targets inside a BMP panel, so links, the
 * group toggles and the trigger all keep native focus behaviour.
 */
document.addEventListener('mousedown', (event) => {
  const target = asElement(event.target);
  const panel = target?.closest('.bmp-nav-panel');
  if (!panel) return;
  const item = panel.closest(ITEM);
  if (item && inOverflow(item)) return;
  if (target?.closest(FOCUSABLE)) return;
  event.preventDefault();
});

// ---------------------------------------------------------------------------
// click — toggle the panel, and toggle a level-2 group
// ---------------------------------------------------------------------------

document.addEventListener('click', (event) => {
  const target = asElement(event.target);
  if (!target) return;

  const groupToggle = target.closest(GROUP_TOGGLE);
  if (groupToggle instanceof HTMLElement) {
    const group = groupToggle.closest('[data-bmp-nav-group]');
    if (!group) return;
    // Groups are independent: opening one leaves its siblings alone, matching
    // v1.1.5's own accordion.
    const willOpen = !group.hasAttribute('data-bmp-open');
    group.toggleAttribute('data-bmp-open', willOpen);
    groupToggle.setAttribute('aria-expanded', String(willOpen));
    return;
  }

  const trigger = target.closest(TRIGGER);
  if (!(trigger instanceof HTMLElement)) return;

  // Inside the "More" flyout the trigger is core's; see `inOverflow`.
  const triggerItem = trigger.closest(ITEM);
  if (triggerItem && inOverflow(triggerItem)) return;

  // `detail === 0` means the click was synthesised by Enter/Space on the
  // button rather than produced by a pointer, so no focus-open preceded it and
  // the live attribute is trustworthy. A mouse press must use the state
  // recorded on pointerdown instead.
  const wasOpen = event.detail === 0 ? isExpanded(trigger) : (preFocusState.get(trigger) ?? isExpanded(trigger));
  preFocusState.delete(trigger);

  setOpen(trigger, !wasOpen);
});

// ---------------------------------------------------------------------------
// keydown — Escape, and arrow/Home/End traversal of the open panel (R6)
// ---------------------------------------------------------------------------

document.addEventListener('keydown', (event) => {
  const target = asElement(event.target);
  if (!target) return;

  const item = target.closest(ITEM);
  const trigger = /** @type {HTMLElement | null} */ (item?.querySelector(TRIGGER) ?? null);
  if (!trigger) return;
  // Inside the "More" flyout the trigger is core's; see `inOverflow`.
  if (item && inOverflow(item)) return;

  if (event.key === 'Escape') {
    if (!isItemOpen(item)) return;
    closeItem(item);
    // R6: focus must come back to the trigger, not be dropped on a hidden node
    // — but without core re-opening the panel on that very focus event. See
    // focusTriggerWithoutReopening.
    focusTriggerWithoutReopening(trigger);
    event.stopPropagation();
    return;
  }

  if (!['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) return;

  const onTrigger = target === trigger;

  // ArrowDown on a closed trigger opens it, the standard menu-button gesture.
  if (onTrigger && !isExpanded(trigger)) {
    if (event.key !== 'ArrowDown') return;
    open(trigger);
    event.preventDefault();
    focusRow(item, 0);
    return;
  }
  if (!isExpanded(trigger)) return;

  const rows = /** @type {HTMLElement[]} */ ([...(item?.querySelectorAll(PANEL_ROWS) ?? [])]);
  if (!rows.length) return;

  const current = rows.indexOf(/** @type {HTMLElement} */ (target));
  let next;
  if (event.key === 'Home') next = 0;
  else if (event.key === 'End') next = rows.length - 1;
  else if (event.key === 'ArrowDown') next = onTrigger ? 0 : Math.min(current + 1, rows.length - 1);
  else if (current <= 0) {
    // ArrowUp from the first row returns to the trigger rather than trapping.
    trigger.focus();
    event.preventDefault();
    return;
  } else next = current - 1;

  rows[next]?.focus();
  event.preventDefault();
});

/**
 * Focus the nth row of an item's panel after a layout pass, so a row inside a
 * group that just expanded is focusable by the time we reach for it.
 * @param {Element | null | undefined} item
 * @param {number} index
 */
function focusRow(item, index) {
  requestAnimationFrame(() => {
    const rows = /** @type {HTMLElement[]} */ ([...(item?.querySelectorAll(PANEL_ROWS) ?? [])]);
    rows[index]?.focus();
  });
}

// ---------------------------------------------------------------------------
// focusout — dismiss when focus leaves the item entirely
// ---------------------------------------------------------------------------

document.addEventListener('focusout', (event) => {
  const target = asElement(event.target);
  const item = target?.closest(ITEM);
  if (!item || !item.classList.contains('bmp-nav-item')) return;
  // Inside the "More" flyout the trigger is core's; see `inOverflow`.
  if (inOverflow(item)) return;

  // Deliberately NOT gated on the trigger still being expanded. Core's blur
  // handler is a capture-phase document listener, so by the time this
  // bubble-phase handler runs core has often ALREADY set aria-expanded="false"
  // (assets/header-menu.js). Gating on it made this handler bail on exactly the
  // flow that needed it — Tab out of a card with a level-2 group expanded —
  // leaving that group open behind a closed trigger, which kept the card
  // painted and stranded DOM state a later reopen inherited.
  if (!isItemOpen(item)) return;

  const next = asElement(/** @type {FocusEvent} */ (event).relatedTarget);

  // A null relatedTarget is NOT a dismissal signal. A real mousedown on any
  // non-focusable node clears focus to <body>, and this card is mostly
  // non-focusable surface — 16px row gutters, the card's block padding, the gap
  // in a group's title row — so closing on null dismissed the whole panel when
  // the shopper merely near-missed a toggle. Press-outside dismissal is already
  // covered completely by the pointerdown handler above, so ignoring null
  // loses nothing.
  if (!next || item.contains(next)) return;
  closeItem(item);
});

// ---------------------------------------------------------------------------
// Edge clamp on the paths that do not go through open()
// ---------------------------------------------------------------------------

/** Clamp the panel of every open item. */
function clampOpenPanels() {
  for (const item of openItems()) {
    const panel = item.querySelector('.bmp-nav-panel');
    if (panel instanceof HTMLElement) clampToViewport(panel);
  }
}

// Core opens the panel on FOCUS, without this module's open() ever running
// (that is stock keyboard behaviour, kept by decision D5). Tabbing to a
// right-hand child-bearing item therefore reached an unclamped card. Inert on
// a store whose only dropdown is the first menu item, but one menu change away
// from a card hanging off the viewport.
document.addEventListener('focusin', (event) => {
  const target = asElement(event.target);
  const trigger = target?.closest(TRIGGER);
  if (!(trigger instanceof HTMLElement)) return;
  const item = trigger.closest(ITEM);
  if (!item || inOverflow(item)) return;
  const panel = item.querySelector('.bmp-nav-panel');
  // requestAnimationFrame so core's own focus handling has laid the panel out.
  if (panel instanceof HTMLElement) requestAnimationFrame(() => clampToViewport(panel));
});

// A resize while a card is open changes the available room, and the shift is a
// pixel value that does not track it.
window.addEventListener('resize', clampOpenPanels);
