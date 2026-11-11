// bmp-dialog-close-guard.js - a native dialog close request must not
// strand the scroll lock.
//
// WHAT: two document-level listeners that make a NATIVE <dialog> close request
// (the Android back button) take the owning component's own close path, and,
// when nothing can stop that close, at least release the scroll lock.
//
// WHY: core assets/dialog.js acquires the lock in showDialog() (lockScroll,
// dialog.js:57) and only releases it in closeDialog() (unlockScroll,
// dialog.js:93). Core assets/theme-drawer.js does the same across open()
// (theme-drawer.js:219) and #closeDialog() (theme-drawer.js:320). Plenty of
// routes reach those release paths - Escape, the close button, an outside
// click, toggleDialog(), a resize past the component's width bounds. The one
// route that reaches NEITHER of them is the native close request.
//
// The Android back button is a CLOSE REQUEST. Chrome routes it through
// CloseWatcher straight to the native dialog close: a `cancel` event, then
// close(). No keydown fires, so dialog.js's #handleKeyDown and
// theme-drawer.js's #onKeyDown never run, so neither component's close method
// runs, so unlockScroll() never runs. `scroll-lock` stays on <html> and
// `html[scroll-lock] { overflow: hidden }` (base.css:43) freezes the page for
// the rest of the session. Desktop Escape was never affected: both components
// preventDefault() the keydown, which suppresses the close request outright.
// That asymmetry is why the bug was mobile-only.
//
// Repairing the CANCEL path (listener 1) rather than only unlocking also fixes
// two consequences of the same gap, because the component's full close path
// runs: the exit animation and scroll restore happen, and DialogCloseEvent
// (`dialog:close`) fires. That event is consumed by quick-add's stay-visible
// toggle (quick-add.js:147) and the size-guide portal teardown
// (bmp-size-guide-portal.js:286), both of which went stale on the native path.
//
// Scope that claim to the cancel path only. On the non-cancelable path
// (listener 2) the dialog is already closed by the time we see it, so
// DialogComponent.closeDialog() early-returns on `!dialog.open` (dialog.js:73)
// and `dialog:close` does not fire at all. Dispatching it ourselves would make
// every consumer run twice on the normal path, which is the worse trade.
//
// Not a consumer, despite appearances: drag-zoom-wrapper.js:59 listens for
// DialogCloseEvent on `window` in the bubble phase, but dialog.js:167 constructs
// it with no options, so it does not bubble and that listener can never fire.
// It was already dead in core and this module does not revive it.
//
// WHY A BMP MODULE AND NOT A CORE PATCH: assets/dialog.js and
// assets/theme-drawer.js are Horizon core, held byte-identical to the pinned
// contract tag — and the layer's core-asset exception class is closed. The precedent is assets/bmp-card-hover.js, which
// drives core's public previewVariant() / resetVariant() without touching
// assets/product-card.js; this module does the same with core's public
// closeDialog() / close().
//
// Both listeners use capture: true because `cancel` and `close` do NOT bubble.
// A capture listener on document still sees them on the way down to the target.

import { unlockScroll } from '@theme/utilities';

document.addEventListener('cancel', handleCancel, { capture: true });
document.addEventListener('close', handleClose, { capture: true });

/**
 * Listener 1, the primary fix. Turns a native close request into the owning
 * component's own close, so the whole close path runs: exit animation,
 * unlockScroll(), scroll restore, and the dialog:close event.
 *
 * The HTMLDialogElement check narrows the type for resolveOwnerClose() and
 * states the intent. It is not what keeps us off <input type="file">'s own
 * `cancel` event: the spec fires that one non-cancelable, and an unowned
 * element returns null from resolveOwnerClose() and bails below anyway, both
 * of which happen before any preventDefault().
 *
 * @param {Event} event - The dialog's `cancel` event.
 */
function handleCancel(event) {
  const dialog = event.target;
  if (!(dialog instanceof HTMLDialogElement)) return;

  const closeOwner = resolveOwnerClose(dialog);
  if (!closeOwner) return;

  // Per spec a close watcher is only cancelable once per user activation, so
  // `cancel` can arrive non-cancelable and the dialog then closes whatever we
  // do. preventDefault() on a non-cancelable event has no effect, so do not
  // pretend it does: let the native close happen and let handleClose catch it.
  if (!event.cancelable) return;

  event.preventDefault();
  closeOwner();
}

/**
 * Listener 2, the last-resort net for the non-cancelable case above. Releases
 * the lock, then asks the owner to finish its own teardown.
 *
 * The owner call is not redundant with the unlock. Releasing the lock alone is
 * enough for a DialogComponent, whose closeDialog() early-returns here anyway
 * (dialog.js:73, the dialog is already closed). It is NOT enough for a
 * ThemeDrawer: without it #closeDialog() never runs, so `<theme-drawer open>`
 * stays set (removed at theme-drawer.js:317) and DrawerCloseEvent never fires.
 * cart-drawer.js:69 gates auto-open on `!this.#themeDrawer?.isOpen`, so a
 * stranded attribute means adding to cart silently opens nothing, and
 * Shopify.actions.openCart cannot recover it either - open() takes the
 * already-open branch into #bringToFront(), which skips showModal() while
 * panel.open is false (theme-drawer.js:254). The drawer stays invisible until
 * a reload.
 *
 * Safe on the normal close path: #closeDialog() removes the `open` attribute
 * (theme-drawer.js:317) before panel.close() (331) and clears #isClosing (350)
 * with no await in between, so this queued task always finds isOpen false and
 * early-returns at theme-drawer.js:308. panel.close() on an already-closed
 * dialog is a spec no-op that fires no event, so there is no loop either.
 *
 * It deliberately does NOT dispatch dialog:close. On the normal path the
 * component fires that event itself, and a second dispatch from here would make
 * every consumer run twice; listener 1 is what keeps it firing exactly once.
 * unlockScroll() is safe to double-run, being a Set.delete (utilities.js:385),
 * so ordering against the component's own unlock does not matter.
 *
 * @param {Event} event - The dialog's `close` event.
 */
function handleClose(event) {
  const dialog = event.target;
  if (!(dialog instanceof HTMLDialogElement)) return;

  // NON-OBVIOUS, DO NOT "SIMPLIFY" THIS AWAY: theme-drawer.js legitimately
  // calls panel.close() and then immediately panel.showModal(), at THREE sites -
  // when the viewport crosses the 990px breakpoint with the drawer open
  // (theme-drawer.js:145-150), when raising this drawer above the stack
  // (theme-drawer.js:254-257), and when restacking a nested dialog
  // (theme-drawer.js:296-297). All three reopen synchronously. The `close` event
  // is queued as a task, so by the time this handler runs the dialog is already
  // open again. Without this bail we would release the lock underneath a live
  // modal, which is the same frozen page from the opposite direction.
  // Covered by a regression test as the drawer-mode-swap
  // case.
  if (dialog.open) return;

  unlockScroll(dialog);
  resolveOwnerClose(dialog)?.();
}

/**
 * Resolves the component that owns a dialog, matching on the REF so a nested
 * dialog can never drive its parent component's close. `refs` is a public
 * instance field on Component (component.js:45).
 *
 * @param {HTMLDialogElement} dialog - The dialog that received the close request.
 * @returns {(() => void) | null} The owner's close call, or null if unowned.
 */
function resolveOwnerClose(dialog) {
  for (let element = dialog.parentElement; element; element = element.parentElement) {
    const owner = /** @type {any} */ (element);
    const refs = /** @type {{ dialog?: Element, panel?: Element } | undefined} */ (owner.refs);
    if (!refs) continue;

    // DialogComponent family: quick-add, search modal, size guide, zoom,
    // popup-link, and everything else that extends it.
    if (refs.dialog === dialog && typeof owner.closeDialog === 'function') {
      return () => owner.closeDialog();
    }

    // ThemeDrawer: cart drawer, filters drawer, chat drawer, all modal below
    // 990px. close() is public and already guarded internally by #isClosing
    // (theme-drawer.js:363), so a duplicate call is a no-op.
    if (refs.panel === dialog && typeof owner.close === 'function') {
      return () => owner.close();
    }
  }

  return null;
}
