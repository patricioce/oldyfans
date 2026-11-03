/* =====================================================================
   OldyFans — Mini cart estilo Sloth Hiking Club (complemento del CSS)
   ---------------------------------------------------------------------
   Agrega al cajón del carrito del tema:
     · "Order subtotal (N items)" y "You're saving $X" (ahorro vs. precio tachado)
     · Botón "Secure checkout" + link "View / edit cart" + nota al pie
     · Carrusel "Pairs great with" con recomendaciones de Shopify
   El tema vuelve a dibujar el cajón cada vez que cambia el carrito; este
   script lo detecta y vuelve a aplicar todo.
   ===================================================================== */
(() => {
  'use strict';

  /* ---------- Textos (editables) ---------- */
  const TEXT = {
    subtotal: 'Order subtotal',
    item: 'item',
    items: 'items',
    saving: 'You’re saving',
    checkout: 'Secure checkout',
    viewCart: 'View / edit cart',
    note: 'Made to order · Money-back guarantee · Real people on email',
    recsTitle: 'Pairs great with',
    from: 'From',
    prev: 'Previous recommendations',
    next: 'More recommendations',
  };
  const RECS_LIMIT = 8;

  const ROOT = '.cart-drawer__inner';
  const ARROW = '<svg viewBox="0 0 10 6" aria-hidden="true" focusable="false"><path fill="currentColor" fill-rule="evenodd" d="M9.354.646a.5.5 0 0 0-.708 0L5 4.293 1.354.646a.5.5 0 0 0-.708.708l4 4a.5.5 0 0 0 .708 0l4-4a.5.5 0 0 0 0-.708" clip-rule="evenodd"/></svg>';

  const currency = (window.Shopify && Shopify.currency && Shopify.currency.active) || 'USD';
  const fmt = new Intl.NumberFormat('en-US', { style: 'currency', currency });
  const money = (cents) => fmt.format((cents || 0) / 100);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const root = window.Shopify && Shopify.routes && Shopify.routes.root ? Shopify.routes.root : '/';

  let cart = null;
  let cartSig = '';
  let loading = null;
  const productCache = new Map();   // handle -> product.js
  const recsCache = new Map();      // product_id -> products[]

  /* ---------- Datos ---------- */
  async function getProduct(handle) {
    if (!productCache.has(handle)) {
      productCache.set(handle, fetch(`${root}products/${handle}.js`).then((r) => (r.ok ? r.json() : null)).catch(() => null));
    }
    return productCache.get(handle);
  }

  async function getRecs(productId) {
    if (!recsCache.has(productId)) {
      recsCache.set(productId, fetch(`${root}recommendations/products.json?product_id=${productId}&limit=${RECS_LIMIT + 4}&intent=related`)
        .then((r) => (r.ok ? r.json() : { products: [] }))
        .then((d) => d.products || [])
        .catch(() => []));
    }
    return recsCache.get(productId);
  }

  async function savingsFor(c) {
    let saved = 0;
    await Promise.all(c.items.map(async (it) => {
      const p = await getProduct(it.handle);
      const v = p && p.variants.find((x) => x.id === it.variant_id);
      const compare = v && v.compare_at_price;
      if (compare && compare > it.final_price) saved += (compare - it.final_price) * it.quantity;
      else if (it.original_price > it.final_price) saved += (it.original_price - it.final_price) * it.quantity;
    }));
    return saved + (c.cart_level_discount_applications || []).reduce((s, d) => s + (d.total_allocated_amount || 0), 0);
  }

  function domSignature(inner) {
    return [...inner.querySelectorAll('.cart-items__table-row')]
      .map((r) => `${r.dataset.key}:${(r.querySelector('input[name="updates[]"]') || {}).value}`)
      .join('|');
  }

  async function refresh(inner) {
    const sig = domSignature(inner);
    if (sig === cartSig && cart) return;
    cartSig = sig;
    if (!loading) {
      loading = fetch(`${root}cart.js`).then((r) => r.json()).finally(() => { loading = null; });
    }
    try {
      cart = await loading;
      cart.ofcSaved = await savingsFor(cart);
    } catch (e) { return; }
    schedule();
  }

  /* ---------- Armado ---------- */
  function cleanVariants(inner) {
    inner.querySelectorAll('.cart-items__variant dd').forEach((dd) => {
      const t = dd.textContent.replace(/ /g, ' ').replace(/,\s*$/, '').trim();
      if (dd.textContent !== t) dd.textContent = t;
    });
  }

  function totals(inner) {
    const label = inner.querySelector('.cart-totals__total-label');
    const total = inner.querySelector('.cart-totals__total');
    if (!label || !total) return;
    const count = cart ? cart.item_count : inner.querySelectorAll('.cart-items__table-row').length;
    const html = `${TEXT.subtotal} <span class="ofc-count">(${count} ${count === 1 ? TEXT.item : TEXT.items})</span>`;
    if (label.innerHTML !== html) label.innerHTML = html;

    const value = inner.querySelector('.cart-totals__total-value');
    if (value && cart) {
      const v = money(cart.total_price);
      if (value.textContent.trim() !== v) value.textContent = v;
    }

    let sav = inner.querySelector('.ofc-savings');
    const saved = cart ? cart.ofcSaved : 0;
    if (saved > 0) {
      if (!sav) {
        sav = document.createElement('p');
        sav.className = 'ofc-savings';
        total.insertAdjacentElement('afterend', sav);
      }
      const t = `${TEXT.saving} ${money(saved)}`;
      if (sav.textContent !== t) sav.textContent = t;
    } else if (sav) sav.remove();
  }

  function ctas(inner) {
    const btn = inner.querySelector('.cart__checkout-button');
    if (!btn) return;
    const txt = btn.querySelector('.button-text') || btn;
    if (txt.textContent.trim() !== TEXT.checkout) txt.textContent = TEXT.checkout;
    const wrap = btn.closest('.cart__ctas') || btn.parentElement;
    if (!wrap.querySelector('.ofc-view-cart')) {
      const a = document.createElement('a');
      a.className = 'ofc-view-cart';
      a.href = `${root}cart`;
      a.textContent = TEXT.viewCart;
      wrap.appendChild(a);
    }
    if (!wrap.nextElementSibling || !wrap.nextElementSibling.classList.contains('ofc-note')) {
      const p = document.createElement('p');
      p.className = 'ofc-note';
      p.textContent = TEXT.note;
      wrap.insertAdjacentElement('afterend', p);
    }
  }

  function recsMarkup(list) {
    const cards = list.map((p) => {
      // Misma imagen servida desde el dominio de la tienda (/cdn/shop/files/…), como el resto del tema
      const src = (p.featured_image || '').replace(/^(https?:)?\/\/cdn\.shopify\.com\/s\/files\/[\d/]+\/files\//, `${root}cdn/shop/files/`);
      const img = src ? `${src}${src.includes('?') ? '&' : '?'}width=600` : '';
      const price = `${p.price_varies ? `${TEXT.from} ` : ''}${money(p.price)}`;
      const compare = p.compare_at_price && p.compare_at_price > p.price
        ? `<s><span class="visually-hidden">Regular price</span>${money(p.compare_at_price)}</s>` : '';
      return `<li class="ofc-card">
          <a class="ofc-card__image" href="${esc(p.url)}" tabindex="-1" aria-hidden="true">${img ? `<img src="${esc(img)}" alt="" width="600" height="600" loading="lazy">` : ''}</a>
          <a class="ofc-card__title" href="${esc(p.url)}">${esc(p.title)}</a>
          <div class="ofc-card__price"><span>${price}</span>${compare}</div>
        </li>`;
    }).join('');
    return `<div class="ofc-recs__header">
        <h3>${esc(TEXT.recsTitle)}</h3>
        <div class="ofc-recs__controls">
          <button type="button" data-dir="-1" aria-label="${esc(TEXT.prev)}" disabled><span style="display:grid;transform:rotate(90deg)">${ARROW}</span></button>
          <button type="button" data-dir="1" aria-label="${esc(TEXT.next)}"><span style="display:grid;transform:rotate(-90deg)">${ARROW}</span></button>
        </div>
      </div>
      <ul class="ofc-recs__rail" role="list">${cards}</ul>`;
  }

  function wireRail(section) {
    const rail = section.querySelector('.ofc-recs__rail');
    const [prev, next] = section.querySelectorAll('.ofc-recs__controls button');
    const update = () => {
      prev.disabled = rail.scrollLeft <= 2;
      next.disabled = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 2;
    };
    section.querySelectorAll('.ofc-recs__controls button').forEach((b) => {
      b.addEventListener('click', () => rail.scrollBy({ left: Number(b.dataset.dir) * rail.clientWidth, behavior: 'smooth' }));
    });
    rail.addEventListener('scroll', update, { passive: true });
    requestAnimationFrame(update);
  }

  let recsKey = '';
  let recsHTML = '';
  async function buildRecs() {
    if (!cart || !cart.items.length) { recsKey = ''; recsHTML = ''; return; }
    const key = cart.items.map((i) => i.product_id).join(',');
    if (key === recsKey) return;
    recsKey = key;
    const inCart = new Set(cart.items.map((i) => i.product_id));
    const list = (await getRecs(cart.items[0].product_id)).filter((p) => !inCart.has(p.id) && p.available).slice(0, RECS_LIMIT);
    recsHTML = list.length ? recsMarkup(list) : '';
    document.querySelectorAll('.ofc-recs').forEach((s) => s.remove());
    schedule();
  }

  function recs(inner) {
    const host = inner.querySelector('.cart-drawer__items');
    const items = host && host.querySelector('.cart-items__wrapper');
    let section = inner.querySelector('.ofc-recs');
    if (!recsHTML || !items) { if (section) section.remove(); return; }
    if (section && section.dataset.key === recsKey && section.previousElementSibling === items) return;
    if (section) section.remove();
    section = document.createElement('section');
    section.className = 'ofc-recs';
    section.dataset.key = recsKey;
    section.setAttribute('aria-label', TEXT.recsTitle);
    section.innerHTML = recsHTML;
    items.insertAdjacentElement('afterend', section);
    wireRail(section);
  }

  function apply() {
    const inner = document.querySelector(ROOT);
    if (!inner || !inner.querySelector('.cart-items__table-row')) return;
    cleanVariants(inner);
    totals(inner);
    ctas(inner);
    recs(inner);
    refresh(inner).then(buildRecs);
  }

  /* ---------- Re-aplicar cuando el tema redibuja el cajón ---------- */
  let queued = false;
  function schedule() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      observer.disconnect();
      try { apply(); } finally { observe(); }
    });
  }
  const observer = new MutationObserver(schedule);
  function observe() {
    const inner = document.querySelector(ROOT);
    observer.observe(inner ? inner.closest('dialog') || inner : document.body, { childList: true, subtree: true, characterData: true });
  }

  document.addEventListener('cart:update', () => { cartSig = ''; schedule(); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => { observe(); schedule(); });
  else { observe(); schedule(); }
})();
