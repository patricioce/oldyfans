(function () {
  // Menú del celular
  var burger = document.getElementById("burger");
  var sheet = document.getElementById("sheet");
  var path = document.getElementById("burger-path");
  function setMenu(open) {
    sheet.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", open);
    burger.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    path.setAttribute("d", open ? "M6 6l12 12M18 6L6 18" : "M4 8h16M4 16h16");
  }
  if (burger && sheet) {
    burger.addEventListener("click", function () { setMenu(!sheet.classList.contains("open")); });
    sheet.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  }

  // Botones de copiar
  document.querySelectorAll(".copy").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var el = document.getElementById(btn.dataset.copy);
      var done = function () { btn.textContent = "Copiado"; btn.classList.add("ok"); setTimeout(function () { btn.textContent = "Copiar"; btn.classList.remove("ok"); }, 1800); };
      var fallback = function () { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); };
      try { navigator.clipboard.writeText(el.textContent.trim()).then(done, fallback); } catch (e) { fallback(); }
    });
  });

  // Mostrar más opiniones
  var moreBtn = document.getElementById("more-reviews");
  if (moreBtn) {
    moreBtn.addEventListener("click", function () {
      var open = moreBtn.getAttribute("aria-expanded") !== "true";
      document.querySelectorAll(".more-review").forEach(function (r) { r.hidden = !open; });
      moreBtn.setAttribute("aria-expanded", open);
      moreBtn.textContent = open ? "Ver menos" : "Ver más opiniones";
    });
  }
})();
