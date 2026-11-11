/**
 * bmp-card-hover.js — drives the product-card hover image swap.
 *
 * Applies the hover-target map snippets/bmp-card-hover.liquid computes
 * server-side (see that file's header) by calling core's own PUBLIC
 * previewVariant()/resetVariant() (assets/product-card.js:466,599) — this
 * module does NO target computation, no media-order logic, no variant math.
 * It only reads the data-bmp-hover-map attribute it is handed and calls
 * core. Never patches core JS.
 *
 * Delegated listeners on `document`, not per-card wiring: cards render on
 * collection, search, home and recommendation surfaces, and more are added
 * later by infinite scroll, filter morphs and quick-add re-renders — none of
 * which this module observes directly, so delegation is the only way to
 * cover cards that don't exist yet. `pointerover`/`pointerout` are used
 * instead of `pointerenter`/`pointerleave` because the latter do not bubble
 * and so cannot be delegated from `document`.
 *
 * Self-gating: snippets/bmp-card-hover.liquid only emits `data-bmp-hover`
 * (the attribute HOVER_SELECTOR matches on) at a non-'zoom'
 * settings.bmp_card_hover_effect, so this module is a complete no-op on the
 * default theme even though snippets/bmp-globals.liquid only loads it at all
 * for the 'second_image'/'next_variant' settings values.
 *
 * Mouse-only, mirroring core previewImage()'s own guard
 * (assets/product-card.js:480) — touch keeps stock tap-to-navigate behavior.
 */

const HOVER_SELECTOR = '.card-gallery[data-bmp-hover]';
const ACTIVE_MODES = ['second_image', 'next_variant'];

document.addEventListener('pointerover', handlePointerOver);
document.addEventListener('pointerout', handlePointerOut);

/**
 * @param {PointerEvent} event
 */
function handlePointerOver(event) {
  const resolved = resolveEventTarget(event);
  if (!resolved) return;
  const { card, gallery } = resolved;

  const map = parseHoverMap(gallery.dataset.bmpHoverMap);
  const visibleId = getVisibleSlideId(gallery);
  const targetId = resolveTargetId(map, getSwatchMediaId(card), visibleId);
  if (targetId == null) return;

  // Required guard: a product whose target happens to already be the
  // visible slide (e.g. featured_media == the mapped target) must not
  // "flip" to the image already on screen — that is a visible no-op flicker.
  if (targetId === visibleId) return;

  card.previewVariant(targetId);
}

/**
 * @param {PointerEvent} event
 */
function handlePointerOut(event) {
  const resolved = resolveEventTarget(event);
  if (!resolved) return;

  resolved.card.resetVariant();
}

/**
 * Shared gate for both listeners: mouse only, inside a gated gallery and a
 * product-card, in an active mode, and the pointer move must be
 * entering/leaving the gallery itself rather than crossing a child element
 * inside it (this is what stops the flip retriggering as the pointer crosses
 * the image, swatches, badges, etc.).
 * @param {PointerEvent} event
 * @returns {{ card: Element, gallery: Element } | null}
 */
function resolveEventTarget(event) {
  if (event.pointerType !== 'mouse') return null;

  const gallery = event.target.closest?.(HOVER_SELECTOR);
  if (!gallery) return null;

  const related = event.relatedTarget;
  if (related instanceof Node && gallery.contains(related)) return null;

  const card = gallery.closest('product-card');
  if (!card) return null;

  if (!ACTIVE_MODES.includes(gallery.dataset.bmpHover)) return null;

  return { card, gallery };
}

/**
 * Parses the `base:target,base:target,…` map format
 * snippets/bmp-card-hover.liquid emits. `base` may be a media id or the
 * literal key `default`. An empty string is a legitimate value that snippet
 * deliberately emits (e.g. no swatches, no next-variant pairs) and must
 * no-op cleanly, not be treated as an error.
 * @param {string | undefined} raw
 * @returns {Record<string, string>}
 */
function parseHoverMap(raw) {
  // Object.create(null): resolveTargetId tests membership with `in`, which
  // walks the prototype chain — a plain {} would resolve a base of
  // "constructor"/"toString"/etc. to an inherited property that was never in
  // the attribute. Media ids are server-generated integers so this isn't
  // reachable today, but the map must not carry a prototype regardless.
  /** @type {Record<string, string>} */
  const map = Object.create(null);
  if (!raw) return map;

  for (const pair of raw.split(',')) {
    const [base, target] = pair.split(':');
    if (!base || !target) continue;
    map[base] = target;
  }
  return map;
}

/**
 * Resolves the hover target for the current pointer, trying candidates in
 * order — the checked swatch's media id, else the currently visible slide's
 * id, else the literal key `default` — and taking the target of the FIRST
 * candidate that actually HAS AN ENTRY in the map. This is not "the first
 * candidate that is a non-empty string": a product with no variant-attached
 * media emits a map whose ONLY key is `default`, and the visible slide's id
 * is a perfectly good non-empty string that simply isn't a key in that map —
 * it must be skipped in favor of `default`, not returned as a dead end.
 * `default` is a literal string key the Liquid snippet emits, never a media
 * id, so it is always tried last regardless of emptiness. Returns undefined
 * when none of the three candidates has an entry.
 * @param {Record<string, string>} map
 * @param {string | undefined} swatchMediaId
 * @param {string | undefined} visibleSlideId
 * @returns {string | undefined}
 */
function resolveTargetId(map, swatchMediaId, visibleSlideId) {
  for (const id of [swatchMediaId, visibleSlideId, 'default']) {
    if (id && id in map) return map[id];
  }
  return undefined;
}

/**
 * The checked swatch's media id — the same source core's own
 * #updateVariantImages() reads (assets/product-card.js:419).
 * @param {Element} card
 * @returns {string | undefined}
 */
function getSwatchMediaId(card) {
  return card.variantPicker?.selectedOption?.dataset?.optionMediaId;
}

/**
 * The slide currently shown in the gallery's slideshow.
 *
 * Primary source is the slideshow component's own synchronous `current`
 * index into its own `slides` getter (both public API — assets/slideshow.js
 * :412 get, :420 set, :819 get slides) — `select()` updates `current` inline
 * (assets/slideshow.js:301), so reading it is never stale.
 *
 * The `aria-hidden="false"` attribute query is kept only as a fallback (no
 * `slideshow-component` found, e.g. the single-media card-gallery branch
 * that renders no slideshow at all). It is NOT reliable as the primary
 * source: `select()` stamps the NEW slide `aria-hidden="false"` immediately
 * (assets/slideshow.js:295), but the OLD slide is only reset to `"true"`
 * later, in the deferred IntersectionObserver batch
 * (assets/slideshow.js:930-938, inside `scheduler.schedule()`). Between
 * those two points more than one slide can carry `aria-hidden="false"`, and
 * `querySelector` would return whichever comes first in DOM order — the
 * stale slide, not the current one.
 * @param {Element} gallery
 * @returns {string | undefined}
 */
function getVisibleSlideId(gallery) {
  const slideshow = gallery.querySelector('slideshow-component');
  const currentSlide = slideshow?.slides?.[slideshow.current];
  const currentId = currentSlide?.getAttribute('slide-id');
  if (currentId) return currentId;

  return gallery.querySelector('slideshow-slide[aria-hidden="false"]')?.getAttribute('slide-id') ?? undefined;
}
