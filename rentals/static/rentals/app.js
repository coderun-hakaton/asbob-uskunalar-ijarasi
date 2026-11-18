(() => {
  const grid = document.getElementById('toolsGrid');
  const overlay = document.getElementById('modalOverlay');
  const form = document.getElementById('rentalForm');
  const daysInput = document.getElementById('daysInput');
  const nameInput = document.getElementById('nameInput');
  const totalPrice = document.getElementById('totalPrice');
  const searchInput = document.getElementById('toolSearch');
  const noResults = document.getElementById('noResults');

  if (!grid || !overlay || !form) return;

  let dailyPrice = 0;
  let activeFilter = 'all';
  let lastFocusedElement = null;

  const formatPrice = (value) => String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');

  const updateTotal = () => {
    const days = Number(daysInput.value);
    totalPrice.textContent = Number.isInteger(days) && days >= 1 && days <= 7
      ? formatPrice(days * dailyPrice)
      : '0';
  };

  const openModal = (button) => {
    lastFocusedElement = document.activeElement;
    dailyPrice = Number(button.dataset.toolPrice);
    document.getElementById('modalToolId').textContent = button.dataset.toolCode;
    document.getElementById('modalToolName').textContent = button.dataset.toolName;
    document.getElementById('modalToolDesc').textContent = button.dataset.toolDescription;
    document.getElementById('modalToolPrice').textContent = formatPrice(dailyPrice);
    form.action = button.dataset.rentUrl;
    daysInput.value = '1';
    nameInput.value = '';
    updateTotal();
    overlay.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
    nameInput.focus();
  };

  const closeModal = () => {
    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');
    if (lastFocusedElement) lastFocusedElement.focus();
  };

  const applyFilters = () => {
    const query = searchInput.value.trim().toLocaleLowerCase();
    let visibleCount = 0;
    grid.querySelectorAll('.tool-card').forEach((card) => {
      const categoryMatches = activeFilter === 'all' || card.dataset.category === activeFilter;
      const searchMatches = card.dataset.search.toLocaleLowerCase().includes(query);
      const visible = categoryMatches && searchMatches;
      card.hidden = !visible;
      if (visible) visibleCount += 1;
    });
    noResults.classList.toggle('hidden', visibleCount > 0);
  };

  grid.addEventListener('click', (event) => {
    const button = event.target.closest('[data-rent-url]');
    if (button) openModal(button);
  });

  document.getElementById('closeModalBtn').addEventListener('click', closeModal);
  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) closeModal();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && overlay.classList.contains('is-open')) closeModal();
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      searchInput.focus();
    }
  });
  daysInput.addEventListener('input', updateTotal);
  searchInput.addEventListener('input', applyFilters);
  document.querySelectorAll('[data-filter]').forEach((button) => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.filter;
      document.querySelectorAll('[data-filter]').forEach((chip) => {
        const selected = chip === button;
        chip.classList.toggle('is-active', selected);
        chip.setAttribute('aria-pressed', String(selected));
      });
      applyFilters();
    });
  });

  if (document.body.dataset.openRental === 'true') {
    const modalToolId = document.getElementById('modalToolId');
    const modalToolName = document.getElementById('modalToolName');
    const modalToolDesc = document.getElementById('modalToolDesc');
    const button = grid.querySelector(`[data-tool-code="${CSS.escape(modalToolId.textContent)}"]`);
    if (button) {
      dailyPrice = Number(button.dataset.toolPrice);
      modalToolId.textContent = button.dataset.toolCode;
      modalToolName.textContent = button.dataset.toolName;
      modalToolDesc.textContent = button.dataset.toolDescription;
      document.getElementById('modalToolPrice').textContent = formatPrice(dailyPrice);
      form.action = button.dataset.rentUrl;
      updateTotal();
      overlay.classList.add('is-open');
      overlay.setAttribute('aria-hidden', 'false');
      document.body.classList.add('modal-open');
      nameInput.focus();
    }
  }
})();
