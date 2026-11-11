/* Chapter navigation on brand pages (STEP 3.3 B117, site tests D0071 and D0072). Escape closes the open
   chapter drawer and returns focus to its Chapters button, and each chapter-navigation section reports
   whether it is open. assets/manual-controls.js keeps its reviewed bytes for the 45 registered pages.
   No storage, no request, no cookie. */
(function () {
  var drawer = document.getElementById('__drawer');
  var button = document.querySelector('[data-manual-toggle="__drawer"]');
  if (drawer) {
    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape' || !drawer.checked) return;
      drawer.checked = false;
      drawer.dispatchEvent(new Event('change', { bubbles: true }));
      if (button) button.focus();
    });
  }
  document.querySelectorAll('input.md-nav__toggle[id]').forEach(function (input) {
    var nav = document.querySelector('nav.md-nav[aria-labelledby="' + input.id + '_label"]');
    if (!nav) return;
    function sync() { nav.setAttribute('aria-expanded', String(input.checked)); }
    input.addEventListener('change', sync);
    sync();
  });
  /* Wide screens (STEP 3.3 B126, art round 2 point 7): the chapter list scrolls in its own column. An item
     either edge of the column would cut is hidden until it fits, so the list never shows half an item; a
     focused item is never hidden. Once the page has loaded (Material has then scrolled the current page's
     item into view), an item cut at the top is brought fully into view, so the first view starts on a
     whole item. Scripts off, Material draws the whole list with no inner scroll. */
  var column = document.querySelector('.md-sidebar--primary .md-sidebar__scrollwrap');
  var wide = typeof window !== 'undefined' && window.matchMedia ? window.matchMedia('(min-width: 76.25em)') : null;
  if (!column || !wide) return;
  var frame = 0;
  function shown(link) {
    return !link.checkVisibility || link.checkVisibility({ opacityProperty: true, visibilityProperty: true });
  }
  function edges() {
    var box = column.getBoundingClientRect();
    var found = { top: box.top, bottom: box.bottom, head: null, tail: null };
    var links = column.querySelectorAll('.md-nav__link');
    for (var i = 0; i < links.length; i += 1) {
      var item = links[i].getBoundingClientRect();
      if (!item.height || item.bottom <= box.top || !shown(links[i])) continue;
      if (item.top < box.top) { found.head = { link: links[i], top: item.top, bottom: item.bottom }; continue; }
      if (item.bottom <= box.bottom) continue;
      if (item.top < box.bottom) found.tail = { link: links[i], top: item.top, bottom: item.bottom };
      break;
    }
    return found;
  }
  function open(cut) { return cut && !cut.link.contains(document.activeElement); }
  function trim() {
    frame = 0;
    var head = 0, tail = 0;
    if (wide.matches) {
      var e = edges();
      if (open(e.head)) head = Math.ceil(e.head.bottom - e.top);
      if (open(e.tail)) tail = Math.ceil(e.bottom - e.tail.top);
    }
    column.style.clipPath = head || tail ? 'inset(' + head + 'px 0 ' + tail + 'px 0)' : '';
  }
  function later() { if (!frame) frame = window.requestAnimationFrame(trim); }
  function settle() {
    if (wide.matches) {
      var e = edges();
      if (e.head) column.scrollTop -= Math.ceil(e.top - e.head.top);
    }
    later();
  }
  column.addEventListener('scroll', later, { passive: true });
  column.addEventListener('focusin', later);
  window.addEventListener('scroll', later, { passive: true });
  window.addEventListener('resize', later);
  // Material scrolls the current item into view on an animation frame after the document is ready.
  window.addEventListener('load', function () {
    window.requestAnimationFrame(function () { window.requestAnimationFrame(settle); });
  });
  if (window.ResizeObserver) new window.ResizeObserver(later).observe(column);
  later();
})();
