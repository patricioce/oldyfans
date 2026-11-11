/**
 * BMP Curated First
 *
 * Pins a product to position #1 of a collection grid via URL parameters, so a
 * Facebook/Meta ad can land the customer on a collection with the exact
 * clicked product (and variant) already first.
 *
 * Ported from an earlier Horizon 3.5.1 build of this feature to this
 * tree's Horizon 4.1.3 base. The 3.5.1 script was an
 * IIFE writing nothing to `window`; it is converted
 * here into a `bmp-*` ES module (module scope already keeps everything off
 * `window` — no wrapper needed) loaded from snippets/bmp-curated-first.liquid,
 * never patching core JS. The only global read is `window.Shopify.routes.root`
 * (storefront locale-root prefix for the fetches below) — nothing is written
 * to `window`.
 *
 * DOM contract verified against THIS tree's Horizon 4.1.3 collection markup
 * (sections/main-collection.liquid + snippets/product-grid.liquid +
 * snippets/product-card.liquid + snippets/card-gallery.liquid):
 *   <results-list>                              (custom element, unchanged)
 *     <ul ref="grid" class="product-grid ...">   (was a div in 3.5.1; the
 *                                                  [ref="grid"] selector still
 *                                                  resolves it either way)
 *       <li ref="cards[]" class="product-grid__item ..." data-page="N">
 *         <product-card class="product-card ...">
 *           <a class="product-card__link" href="{{ product.url }}">
 *           <div class="product-card__content ...">
 *             ...
 *             <div class="card-gallery ...">
 *               <a class="contents" href="{{ product.url }}">
 *                 <div class="product-media-container ..."><img ...></div>
 *
 * The card is NOT assumed to have only one anchor pointing at the product:
 * card-gallery.liquid renders its own `<a class="contents" href={{ product.url
 * }}>` over the image, separate from `a.product-card__link`. Every function
 * below that needs to touch "the product's link(s)" (variant deep-linking)
 * walks ALL `a[href*="/products/"]` inside the card and filters by handle
 * match (linkMatchesHandle), not just the primary link — see setVariantOnLinks.
 *
 * The standalone SRA fallback card (sections/bmp-curated-product-card.liquid,
 * fetched below when the pinned product isn't already in the grid) renders
 * its own card content directly rather than depending on the grid's
 * `content_for 'block'` mechanism (which has no configured child blocks
 * outside a template) — see that file's header comment.
 *
 * Pagination interop: assets/paginated-list.js derives the "previous page"
 * to fetch from `cards[0].dataset.page` (its `#getPage('previous')`). Moving
 * or inserting a card at the front of the grid therefore MUST stamp that
 * card's `data-page` from whatever card it displaced — moveToFront() does
 * this on every pin, for both the SRA-clone case and the moved-existing-card
 * case, so upward infinite scroll keeps resolving the correct page number.
 * The displaced card must be resolved by `[ref="cards[]"]`, never by
 * `firstElementChild`: the grid's first child on the storefront is the
 * sessionStorage grid-view <script>, not a card. See moveToFront()'s own
 * comment — that mistake made the stamp a no-op in production while still
 * working in the theme editor, where the script is not rendered.
 *
 * Duplicate handling: infinite scroll can later append the GENUINE
 * server-rendered card for the pinned product elsewhere in the grid (its
 * real page legitimately contains it), which would otherwise show the
 * product twice — once pinned, once in its natural position. The re-render
 * observer's pin() pass detects this (findOtherCardWithHandle) and prefers
 * the genuine card: it swaps to the front and the previously-pinned node
 * (clone or otherwise) is removed, rather than leaving both in the DOM.
 *
 * URL params (the param NAME is configurable; default "first"):
 *   first   - product handle OR a full/encoded product URL (FB deep link)
 *   variant - variant id to deep-link + display (optional; also parsed from
 *             the encoded URL when `first` is a full product URL)
 *
 * Config comes from the loader <script> tag's data-* attributes, emitted by
 * snippets/bmp-curated-first.liquid only when settings.bmp_curated_first_enabled
 * (default true — see that snippet's doc comment for the cost tradeoff).
 */

const cfg = readConfig();

if (cfg.enabled) {
  const params = new URLSearchParams(window.location.search);
  const firstParam = params.get(cfg.param);

  if (firstParam) {
    const parsed = parseFirstParam(firstParam, params.get('variant'));

    if (parsed.handle) {
      init(parsed, cfg);
    }
  }
}

// ---- config ------------------------------------------------------------

function readConfig() {
  const el = document.querySelector('script[data-bmp-curated-first]');
  const d = (el && el.dataset) || {};
  return {
    enabled: el != null,
    param: d.param || 'first',
    swapImage: d.swapImage !== 'false',
  };
}

// ---- storefront routing ---------------------------------------------------

/** Storefront locale-root prefix (e.g. "/en-ca/"), always trailing-slashed. */
function shopifyRoot() {
  const root = (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';
  return root.charAt(root.length - 1) === '/' ? root : root + '/';
}

// ---- param parsing -------------------------------------------------------

/**
 * `first` may be a plain handle or a full/encoded product URL. Also extracts
 * the variant from the encoded URL when not passed separately.
 *
 * Decoding note: `firstParam` comes from `URLSearchParams#get()`, which
 * already percent-decodes its value once — so it is normally plain text
 * here (a handle, or an already-decoded `https://...` URL) and needs NO
 * further decoding. Some ad-link generators double-encode the deep-link URL
 * before appending it to the query string, so it can arrive still
 * percent-escaped (e.g. `https%3A%2F%2F...`); we decode ONE additional time
 * ONLY when the value doesn't already look like a URL, and only ever act on
 * the result if THAT decode reveals one. This is deliberately not
 * unconditional: a handle containing a literal `%` (e.g. "50%-off-sale") is
 * not valid percent-encoding, and calling decodeURIComponent on it
 * unconditionally throws — guarded here with try/catch, and skipped
 * entirely for the common case where firstParam already reads as a URL.
 */
function parseFirstParam(firstParam, fallbackVariant) {
  let handle = firstParam;
  let variant = fallbackVariant || null;

  let candidate = firstParam;
  if (!/^https?:\/\//.test(candidate)) {
    try {
      const maybeDecoded = decodeURIComponent(candidate);
      if (/^https?:\/\//.test(maybeDecoded)) candidate = maybeDecoded;
    } catch (e) {
      // Not valid percent-encoding (e.g. a handle with a literal "%") —
      // candidate stays as the raw value and falls through to the plain-
      // handle path below.
    }
  }

  if (/^https?:\/\//.test(candidate)) {
    try {
      // Full/encoded product URL (FB deep link): pull the handle from /products/<handle>.
      const url = new URL(candidate);
      const parts = url.pathname.split('/');
      const idx = parts.indexOf('products');
      handle = idx !== -1 && parts[idx + 1] ? parts[idx + 1] : '';
      if (!variant) variant = new URLSearchParams(url.search).get('variant');
    } catch (e) {
      // Malformed URL — fall through and treat firstParam as a plain handle.
    }
  }

  handle = (handle || '').split('?')[0].split('#')[0].split('/').pop() || '';
  // Variant ids are always integers; strip anything else (defuse param pollution).
  variant = (variant || '').replace(/[^0-9]/g, '') || null;
  return { handle, variant };
}

// ---- grid helpers ---------------------------------------------------------

function getGrid() {
  const list = document.querySelector('results-list');
  if (!list) return null;
  return list.querySelector('[ref="grid"]') || list.querySelector('.product-grid');
}

function getCards(grid) {
  return Array.prototype.slice.call(grid.querySelectorAll(':scope > [ref="cards[]"]'));
}

/** Does this card's product link point at the given handle? */
function cardMatchesHandle(card, handle) {
  const links = card.querySelectorAll('a[href*="/products/"]');
  for (let i = 0; i < links.length; i++) {
    if (linkMatchesHandle(links[i].getAttribute('href'), handle)) return true;
  }
  return false;
}

function linkMatchesHandle(href, handle) {
  if (!href) return false;
  const marker = '/products/' + handle;
  const at = href.indexOf(marker);
  if (at === -1) return false;
  // Guard against prefix collisions ("shirt" matching "shirt-blue"):
  // the char after the handle must end the path segment.
  const next = href.charAt(at + marker.length);
  return next === '' || next === '?' || next === '#' || next === '/';
}

function findCardByHandle(grid, handle) {
  const cards = getCards(grid);
  for (let i = 0; i < cards.length; i++) {
    if (cardMatchesHandle(cards[i], handle)) return cards[i];
  }
  return null;
}

/** Find a card matching `handle` other than `exclude` (duplicate detection). */
function findOtherCardWithHandle(grid, exclude, handle) {
  const cards = getCards(grid);
  for (let i = 0; i < cards.length; i++) {
    if (cards[i] !== exclude && cardMatchesHandle(cards[i], handle)) return cards[i];
  }
  return null;
}

// ---- pinning ---------------------------------------------------------------

/** Per-pin runtime state: shared by pin() and the re-render observer. */
function createState() {
  // `failed` latches an unresolvable handle: without it, every mutation frame
  // re-issues the Section Rendering API fetch for a handle that will never
  // resolve. `inflight` covers the round trip BEFORE `failed` (or
  // `cachedCard`) can latch anything: without it, a mutation arriving while
  // fetch #1 is still in the air (a third-party swatch/review/badge app is
  // the usual source) re-enters pin() and fires fetch #2, #3, ... one per
  // animation frame until the first response lands.
  return { pinning: false, cachedCard: null, rafId: 0, variantImageSrc: null, failed: false, inflight: false };
}

function init(parsed, cfg) {
  const state = createState();
  pin(parsed, cfg, state);
  observeReRenders(parsed, cfg, state);
}

function pin(parsed, cfg, state) {
  // The pin retires as soon as the shopper filters or sorts.
  //
  // `parsed` is captured once at module load, but assets/facets.js:86-96 does
  // `url.search = ''` and rebuilds the URL from the form only, so `?first=` is
  // WIPED on any filter or sort change. The facets re-render morphs
  // <results-list> in place, so this module's observer is never detached and
  // pin() runs again — which used to re-insert the pinned product into a
  // result set that excludes it (filter to "Blue", get 8 matching products,
  // and the red variant sits at #1 anyway with the count reading 8 next to 9
  // visible cards).
  //
  // Re-reading the param here is self-consistent: the moment facets strips it,
  // the pin retires on its own, no event wiring and no observer teardown. The
  // product call behind it — the ad intent owns the landing, the first explicit
  // user action ends it — also covers sort deliberately: a pin that outranks
  // "Price: low to high" is not a pin to the shopper, it is a broken sort.
  if (!new URLSearchParams(window.location.search).get(cfg.param)) return;

  const grid = getGrid();
  if (!grid || state.pinning) return;

  const firstCard = grid.querySelector(':scope > [ref="cards[]"]');
  if (firstCard && cardMatchesHandle(firstCard, parsed.handle)) {
    // Already pinned. Infinite scroll can later append the GENUINE
    // server-rendered card for the same product elsewhere in the grid (its
    // real page legitimately contains it), which would otherwise duplicate
    // it alongside whatever we pinned. Prefer the genuine card: swap it to
    // the front and drop what was there before.
    const duplicate = findOtherCardWithHandle(grid, firstCard, parsed.handle);
    if (duplicate) {
      state.pinning = true;
      try {
        // Read the displaced page BEFORE the remove — moveToFront would
        // otherwise resolve the second <li> as the displaced card.
        const pageHint = firstCard.dataset.page;
        firstCard.remove();
        moveToFront(grid, duplicate, pageHint);
        if (parsed.variant) applyVariant(duplicate, parsed, cfg, state);
      } finally {
        state.pinning = false;
      }
      return;
    }
    if (parsed.variant) applyVariant(firstCard, parsed, cfg, state);
    return;
  }

  state.pinning = true;
  try {
    const existing = findCardByHandle(grid, parsed.handle);
    if (existing) {
      // Already-in-grid path: swap slots rather than splice, so only two boxes
      // move instead of every card between position 1 and k. See swapToFront.
      swapToFront(grid, existing);
      if (parsed.variant) applyVariant(existing, parsed, cfg, state);
    } else if (state.cachedCard) {
      const clone = state.cachedCard.cloneNode(true);
      adoptSiblingLayout(grid, clone);
      prioritizePinnedImage(clone);
      moveToFront(grid, clone);
      if (parsed.variant) applyVariant(clone, parsed, cfg, state);
    } else if (!state.failed && !state.inflight) {
      fetchAndPin(grid, parsed, cfg, state);
    }
  } finally {
    state.pinning = false;
  }
}

/**
 * Move `card` to the front of the grid, stamping its `data-page` from the card
 * it displaces so assets/paginated-list.js (`#getPage('previous')`, reading
 * `cards[0].dataset.page`) keeps deriving the correct "previous page" to fetch
 * after the pin. Covers both the SRA-clone case (a brand-new node with no real
 * page of its own) and the moved-existing-card case (the card already had a
 * page — intentionally overwritten to match its new position #1, since page
 * numbers describe grid position for this consumer, not the product's origin).
 *
 * The displaced card is resolved with `:scope > [ref="cards[]"]`, NOT
 * `firstElementChild`. snippets/product-grid.liquid:141-166 renders the
 * sessionStorage grid-view <script> as the first child of <ul ref="grid">
 * (opened at :128-137, before `{{ children }}` at :168) under
 * `{% unless request.design_mode %}`. <script> is a script-supporting element,
 * so the parser keeps it there and it stays in the DOM after executing —
 * meaning on the storefront `firstElementChild` was that SCRIPT, its
 * `dataset.page` was undefined, and the stamp never ran. Note the inversion
 * that hid this: in the theme editor the script is absent, so the stamp DID
 * fire and editor testing could never reproduce it. It was also wrong in the
 * other direction — once `paginated-list.js:234` `grid.prepend(...)` had run,
 * `firstElementChild` was a real <li> and the stamp fired with the WRONG page.
 *
 * `pageHint` exists for the duplicate branch in pin(), which removes the
 * previously-pinned first card before calling this. The page has to be read
 * off that card BEFORE it is removed, or this lands on the second <li>.
 */
function moveToFront(grid, card, pageHint) {
  const displaced = grid.querySelector(':scope > [ref="cards[]"]');
  if (displaced === card) return;
  const page = pageHint != null ? pageHint : displaced && displaced.dataset.page;
  if (page != null) card.dataset.page = page;
  grid.insertBefore(card, displaced || grid.firstElementChild);
}

/**
 * Swap `card` with the grid's current first card instead of splicing it in.
 *
 * Layout-shift control for the common case (the pinned product is already in
 * the visited grid). `moveToFront`'s `insertBefore` renumbers every slot
 * between 1 and k, so the browser re-lays-out that whole run of the flow grid;
 * a swap moves exactly two boxes and leaves slots 2..k-1 where they are.
 *
 * `data-page` follows the SLOT, not the card, matching the convention
 * moveToFront already uses: page numbers describe grid position for
 * assets/paginated-list.js, not the product's origin. Exchanging the two
 * cards' pages therefore keeps the sequence monotonic, which is what
 * `#getPage('previous')` (reads `cards[0]`) and `#getPage('next')` (reads the
 * last card) depend on.
 *
 * Only helps the already-in-grid path. The SRA path still inserts a brand-new
 * node and shifts everything after it — inherent to a client-side pin, and the
 * reason a server-side pin remains the complete answer.
 */
function swapToFront(grid, card) {
  const first = grid.querySelector(':scope > [ref="cards[]"]');
  if (!first || first === card) return false;
  const after = card.nextSibling;
  const firstPage = first.dataset.page;
  const cardPage = card.dataset.page;
  grid.insertBefore(card, first);
  grid.insertBefore(first, after);
  if (firstPage != null) card.dataset.page = firstPage;
  if (cardPage != null) first.dataset.page = cardPage;
  return true;
}

/**
 * Copy the layout contract off a sibling server-rendered card onto an
 * SRA-fetched clone.
 *
 * Three of Horizon's card layout inputs are custom properties that only ever
 * exist as INLINE styles on the real cards — `--gallery-aspect-ratio`
 * (card-gallery.liquid:91), `--product-media-fit` + the `media-fit` class
 * (:123,134) and `--product-card-gap` (product-card.liquid:106) — so a clone
 * that omits them renders at the wrong aspect ratio, without the crop, and
 * with a collapsed gap. sections/bmp-curated-product-card.liquid hardcodes the
 * values templates/collection.json ships today, which keeps the card correct
 * standalone; copying from a live sibling on top of that keeps it correct when
 * the merchant changes those settings. When the grid has no sibling to copy
 * from (empty or fully-filtered results) the inline defaults stand alone.
 *
 * Only `class` and `style` are copied — never refs, ids or data attributes,
 * which are per-card identity.
 *
 * The card-global-style carrier is the one input this node-to-node
 * copy cannot express, because it is an ANCESTOR of .product-card__content
 * rather than the element itself. The section emits it unconditionally,
 * mirroring templates/collection.json; this function only has to take it away
 * again when the live cards say the toggle is off. It UNWRAPS rather than
 * dropping the class: the div is layout-inert only while
 * `.bmp-card-global-card { display: contents }` applies to it, and a bare
 * block div between the grid item and <product-card> would break the
 * `:is(.product-grid__item, .resource-list__item) .product-card { height: 100% }`
 * equal-height rule — a percentage height against an auto-height parent.
 */
function adoptSiblingLayout(grid, card) {
  const sibling = grid.querySelector(':scope > [ref="cards[]"]');
  if (!sibling || sibling === card) return;
  const selectors = ['.product-card__content', '.card-gallery', '.product-media-container'];
  for (let i = 0; i < selectors.length; i++) {
    const from = sibling.querySelector(selectors[i]);
    const to = card.querySelector(selectors[i]);
    if (!from || !to) continue;
    const className = from.getAttribute('class');
    if (className) to.setAttribute('class', className);
    const style = from.getAttribute('style');
    if (style) to.setAttribute('style', style);
  }
  const carrier = card.querySelector('.bmp-card-global-card');
  if (carrier && !sibling.querySelector('.bmp-card-global-card')) {
    while (carrier.firstChild) carrier.parentNode.insertBefore(carrier.firstChild, carrier);
    carrier.parentNode.removeChild(carrier);
  }
}

/**
 * Mark the pinned card's image as high priority before it enters the document.
 *
 * The card is grid slot #1 on an ad landing, so it is the LCP candidate — but
 * it arrives late by construction (deferred module + Section Rendering API
 * round trip) while every server-rendered sibling was already eager from
 * card-gallery.liquid:112-118. Setting this before insertion means the fetch
 * starts at high priority the moment the node is connected, rather than
 * queueing behind whatever the browser is already doing.
 */
function prioritizePinnedImage(card) {
  // Same selector chain as swapImage(): target the card's primary/featured
  // image specifically, not "the first img in the card". Bare querySelector('img')
  // happens to be correct for today's SRA card because the gallery image is its
  // only image, but it would silently retarget the moment the card gains an icon
  // or a badge image above the gallery.
  const img =
    card.querySelector('.card-gallery img') ||
    card.querySelector('.product-media-container img') ||
    card.querySelector('img');
  if (!img) return;
  img.setAttribute('loading', 'eager');
  img.setAttribute('fetchpriority', 'high');
}

/** Fetch a standalone card via the Section Rendering API and pin it. */
function fetchAndPin(grid, parsed, cfg, state) {
  // Marked BEFORE the fetch starts, not after it settles: a mutation frame
  // that lands mid-round-trip must see this and skip re-fetching (see
  // createState's comment). Cleared once state.cachedCard is populated below,
  // since the cachedCard branch in pin() takes over from there.
  state.inflight = true;
  const url = shopifyRoot() + 'products/' + parsed.handle + '?section_id=bmp-curated-product-card';
  fetch(url)
    .then((res) => {
      if (!res.ok) throw new Error('Section returned ' + res.status);
      return res.text();
    })
    .then((html) => {
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const card = doc.querySelector('[ref="cards[]"]') || doc.querySelector('.product-grid__item');
      if (!card) throw new Error('No card in rendered section');
      if (!cardMatchesHandle(card, parsed.handle)) {
        // A nil-product render (unknown handle, HTTP 200) produces a card with an
        // empty href. Caching it made cardMatchesHandle() unsatisfiable forever, so
        // pin() re-inserted a clone every frame. Treat any non-matching render as a
        // failed lookup.
        throw new Error('Rendered card does not match handle ' + parsed.handle);
      }
      state.cachedCard = card.cloneNode(true);
      state.inflight = false;

      // Re-check it isn't already there (a re-render may have added it meanwhile).
      const liveGrid = getGrid();
      if (!liveGrid || findCardByHandle(liveGrid, parsed.handle)) {
        if (liveGrid) pin(parsed, cfg, state);
        return;
      }
      state.pinning = true;
      try {
        const node = state.cachedCard.cloneNode(true);
        adoptSiblingLayout(liveGrid, node);
        prioritizePinnedImage(node);
        moveToFront(liveGrid, node);
        if (parsed.variant) applyVariant(node, parsed, cfg, state);
      } finally {
        state.pinning = false;
      }
    })
    .catch((err) => {
      state.failed = true;
      state.inflight = false;
      if (window.console) console.warn('[bmp-curated-first] could not pin product:', err.message);
    });
}

// ---- variant deep-link + image swap ---------------------------------------

function applyVariant(card, parsed, cfg, state) {
  if (!parsed.variant) return;
  setVariantOnLinks(card, parsed.handle, parsed.variant);
  if (!cfg.swapImage) return;
  // Re-use the resolved variant image across re-render re-pins (no repeat fetch).
  if (state.variantImageSrc) {
    swapImage(card, state.variantImageSrc);
  } else {
    swapVariantImage(card, parsed.handle, parsed.variant, state);
  }
}

/**
 * Point EVERY anchor inside the card that links to this product (replace or
 * append `variant=`) at the chosen variant — not just the primary
 * `a.product-card__link`. card-gallery.liquid renders its own
 * `<a class="contents" href={{ product.url }}>` over the image, separate
 * from the primary link, so clicking the image would otherwise land on the
 * default variant. Anchors are matched by handle (linkMatchesHandle), so
 * app-injected links to OTHER products (e.g. swatch/quick-add cross-sells)
 * stay untouched.
 */
function setVariantOnLinks(card, handle, variantId) {
  const links = card.querySelectorAll('a[href*="/products/"]');
  for (let i = 0; i < links.length; i++) {
    const link = links[i];
    const href = link.getAttribute('href');
    if (!href || !linkMatchesHandle(href, handle)) continue;
    link.setAttribute('href', withVariantParam(href, variantId));
  }
}

/** Set/replace the `variant` query param on `href` using the URL API. */
function withVariantParam(href, variantId) {
  try {
    const url = new URL(href, window.location.origin);
    url.searchParams.set('variant', variantId);
    return url.pathname + url.search + url.hash;
  } catch (e) {
    return href;
  }
}

/** Look up the variant's featured image, cache it, and swap the card's main image. */
function swapVariantImage(card, handle, variantId, state) {
  fetch(shopifyRoot() + 'products/' + handle + '.js')
    .then((res) => {
      if (!res.ok) throw new Error('product.js ' + res.status);
      return res.json();
    })
    .then((product) => {
      const idNum = parseInt(variantId, 10);
      let variant = null;
      for (let i = 0; i < product.variants.length; i++) {
        if (product.variants[i].id === idNum) {
          variant = product.variants[i];
          break;
        }
      }
      if (!variant || !variant.featured_image || !variant.featured_image.src) return;
      state.variantImageSrc = variant.featured_image.src;
      swapImage(card, state.variantImageSrc);
    })
    .catch(() => {
      // non-fatal: the card still works, just shows the default image
    });
}

/**
 * Swap only the card's primary/featured image (never the hover/carousel slides),
 * rebuilding srcset on the theme's width ladder and keeping the native sizes attr.
 * Query-param handling uses the URL API (not string surgery) so an existing
 * `?v=...&other=...` src neither leaves a dangling `&` after stripping `v`
 * nor gets a second `?` appended when the width param is added.
 */
function swapImage(card, imageSrc) {
  if (card.dataset.bmpVariantSwapped === imageSrc) return;
  const img =
    card.querySelector('.card-gallery img') ||
    card.querySelector('.product-media-container img') ||
    card.querySelector('img');
  if (!img) return;

  let base;
  try {
    base = new URL(imageSrc, window.location.href);
  } catch (e) {
    return; // Not a rewritable URL — leave the existing image alone.
  }
  base.searchParams.delete('v');

  const widths = [240, 352, 480, 640, 832, 1200, 1600, 1920];
  img.setAttribute('src', resizeSrc(base, 640));
  img.setAttribute('srcset', widths.map((w) => resizeSrc(base, w) + ' ' + w + 'w').join(', '));
  img.removeAttribute('data-src');
  card.dataset.bmpVariantSwapped = imageSrc;
}

/** Clone `base` and set its `width` param — never mutates the shared base URL. */
function resizeSrc(base, width) {
  const url = new URL(base.href);
  url.searchParams.set('width', String(width));
  return url.toString();
}

// ---- re-render survival -----------------------------------------------------

function observeReRenders(parsed, cfg, state) {
  // Subtree on <results-list> (not just the grid) is deliberate: filter/sort
  // and infinite-scroll pagination (assets/results-list.js extends the core
  // PaginatedList component) replace or extend the [ref="grid"] element's
  // contents, so a grid-scoped observer would miss that and lose the pin.
  // Every mutation is coalesced into one pin() per animation frame via rafId.
  // Even when already pinned, pin() re-scans the grid once (duplicate
  // detection, see findOtherCardWithHandle) before re-asserting the variant —
  // still O(cards) per animation frame, not per mutation, which also wins the
  // race against a swatch app / quick-add re-rendering the card link back to
  // its default variant.
  const list = document.querySelector('results-list');
  if (!list || typeof MutationObserver === 'undefined') return;
  const observer = new MutationObserver(() => {
    if (state.pinning || state.rafId) return;
    state.rafId = window.requestAnimationFrame(() => {
      state.rafId = 0;
      pin(parsed, cfg, state);
    });
  });
  observer.observe(list, { childList: true, subtree: true });
}
