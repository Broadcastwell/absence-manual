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
})();
