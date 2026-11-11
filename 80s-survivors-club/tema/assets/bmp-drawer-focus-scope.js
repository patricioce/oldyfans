// bmp-drawer-focus-scope.js - a NON-MODAL drawer must not trap focus.
//
// WHAT: releases the global focus trap whenever an open <theme-drawer> is
// showing a non-modal dialog, i.e. the >= 990px "squeeze" mode.
//
// WHY: core assets/theme-drawer.js opens the panel with panel.show() at
// >= 990px - a NON-modal dialog, so the rest of the page stays visible and
// interactive - and then installs a focus trap over it (theme-drawer.js:223,
// and again at :154 when the viewport crosses the breakpoint with the drawer
// open). assets/focus.js trapFocus() implements that trap as a CAPTURING
// `focusin` listener on document which calls first?.focus() whenever focus
// lands outside the container. So a press on any control outside the drawer
// has its focus yanked straight back into the drawer.
//
// For most of the page that is merely wrong; for the header navigation it is
// fatal. The yank is a blur out of the submenu whose relatedTarget sits
// outside the menu, so core HeaderMenu.deactivate() closes the submenu, and
// a closed submenu is marked `inert` (header-menu.js). The pressed control
// therefore stops being hit-testable BETWEEN mousedown and mouseup, mouseup
// retargets to an ancestor, and `click` fires on the nearest common ancestor
// instead of the control. Measured: pressing a submenu link dispatched click
// on div.page-wrapper, never on the <a>, so nothing navigated; pressing a
// level-2 group toggle collapsed the whole panel instead of expanding it.
//
// Trapping focus in a non-modal dialog is independently wrong: it leaves a
// keyboard user unable to Tab out of the drawer while the page beside it is
// fully visible, which is not the contract for a non-modal dialog. Modal mode
// (< 990px) is untouched - there showModal() makes the rest of the page
// genuinely inert and the NATIVE trap applies, which is correct.
//
// WHY A BMP MODULE AND NOT A CORE PATCH: assets/theme-drawer.js and
// assets/focus.js are Horizon core, held byte-identical to the pinned contract
// tag, and BMP-HOOK regions have no JavaScript comment form. The precedent is
// assets/bmp-dialog-close-guard.js, which drives core's public close methods
// without touching core; this module calls core's exported removeTrapFocus().

import { removeTrapFocus } from '@theme/focus';

/** Mirrors MODAL_BREAKPOINT in assets/theme-drawer.js: below this the drawer is modal. */
const MODAL_BREAKPOINT = 990;

const modalQuery = window.matchMedia(`(max-width: ${MODAL_BREAKPOINT - 1}px)`);

/**
 * @returns {boolean} Whether an open theme-drawer is showing a NON-modal panel.
 */
function hasOpenNonModalDrawer() {
  for (const drawer of document.querySelectorAll('theme-drawer[open]')) {
    const panel = drawer.querySelector('dialog');
    // :modal is the authority, not the breakpoint - the two disagree for one
    // frame while #onModalBreakpointChange re-opens the dialog in the new mode.
    if (panel instanceof HTMLDialogElement && panel.open && !panel.matches(':modal')) return true;
  }
  return false;
}

/**
 * Drops the trap if, and only if, a non-modal drawer is on screen.
 *
 * removeTrapFocus() is a no-op when nothing is trapped (it removes two
 * listeners), so calling this more often than strictly necessary is free.
 */
function releaseNonModalTrap() {
  if (hasOpenNonModalDrawer()) removeTrapFocus();
}

// theme-drawer.js dispatches DrawerOpenEvent AFTER trapFocus() and after the
// `open` attribute is set (theme-drawer.js:227-230), and the event bubbles, so
// a document listener sees a fully-settled drawer and can undo the trap.
document.addEventListener('theme-drawer:open', releaseNonModalTrap);

// Crossing the breakpoint with the drawer open re-installs the trap via
// #onModalBreakpointChange and dispatches NO event. Listener order across two
// distinct MediaQueryList objects is not something to rely on, so re-check on
// the next frame, once core's own handler has certainly run.
modalQuery.addEventListener('change', () => {
  requestAnimationFrame(releaseNonModalTrap);
});
