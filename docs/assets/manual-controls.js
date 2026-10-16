/* Local chapter and search controls. The shared site menu is separate. */
(function () {
  var search = document.querySelector('[data-md-component="search"]');
  var searchButton = document.querySelector('[data-manual-toggle="__search"]');
  var searchToggle = document.getElementById('__search');
  document.querySelectorAll('[data-manual-toggle]').forEach(function (button) {
    var input = document.getElementById(button.dataset.manualToggle);
    if (!input) return;
    function sync() {
      button.setAttribute('aria-expanded', String(input.checked));
      if (input !== searchToggle || !search) return;
      if (input.checked) { var query = search.querySelector('[data-md-component="search-query"]'); if (query) query.focus(); }
      else if (search.contains(document.activeElement) && searchButton) searchButton.focus();
    }
    button.addEventListener('click', function () {
      input.checked = !input.checked;
      input.dispatchEvent(new Event('change', {bubbles:true}));
    });
    input.addEventListener('change', sync);
    button.setAttribute('aria-expanded', String(input.checked));
  });
  if (!search || !searchToggle) return;
  search.setAttribute('aria-label', 'Search the Absence Manual');
  function close(event) {
    if (event) event.preventDefault();
    searchToggle.checked = false;
    searchToggle.dispatchEvent(new Event('change', {bubbles:true}));
    if (searchButton) searchButton.focus();
  }
  search.querySelectorAll('label[for="__search"]').forEach(function (label) {
    label.addEventListener('click', close);
    if (label.classList.contains('md-search__icon')) {
      label.setAttribute('role', 'button');
      label.setAttribute('tabindex', '0');
      label.setAttribute('aria-label', 'Close search');
      label.addEventListener('keydown', function (event) { if (event.key === 'Enter' || event.key === ' ') close(event); });
    }
  });
  search.addEventListener('keydown', function (event) { if (event.key === 'Escape' && searchToggle.checked) close(event); });
})();
