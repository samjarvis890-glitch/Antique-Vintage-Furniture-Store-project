/**
 * MAISON RELIQUE — EDITORIAL ANTIQUE & VINTAGE FURNITURE STORE
 * JAVASCRIPT MASTER INTERACTION MODULE
 */

(function () {
  'use strict';

  // --- 1. DOM REFERENCES ---
  const htmlEl = document.documentElement;
  const bodyEl = document.body;

  // Toggles
  const themeToggles = document.querySelectorAll('.theme-toggle-btn');
  const rtlToggles = document.querySelectorAll('.rtl-toggle-btn');

  // Navigation & Dropdowns
  const dropdownWrappers = document.querySelectorAll('.nav-dropdown-wrapper');
  const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const mobileDrawer = document.getElementById('mobile-drawer');
  const drawerBackdrop = document.getElementById('drawer-backdrop');
  const drawerCloseBtn = document.getElementById('drawer-close-btn');
  const drawerNavLinks = document.querySelectorAll('.drawer-nav-link:not(.drawer-submenu-toggle), .drawer-sublink, .drawer-actions a');
  const drawerSubmenuToggles = document.querySelectorAll('.drawer-submenu-toggle');

  // Modal (Book a Viewing)
  const viewingModal = document.getElementById('viewing-modal');
  const modalBackdrop = document.getElementById('modal-backdrop');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const openViewingButtons = document.querySelectorAll('[data-action="open-viewing-modal"]');
  const viewingForm = document.getElementById('viewing-booking-form');
  const modalSuccessMsg = document.getElementById('modal-success-state');

  // Modal (Client Login)
  const loginModal = document.getElementById('login-modal');
  const loginModalBackdrop = document.getElementById('login-modal-backdrop');
  const loginModalCloseBtn = document.getElementById('login-modal-close-btn');
  const openLoginButtons = document.querySelectorAll('[data-action="open-login-modal"], .nav-login-btn');
  const loginForm = document.getElementById('login-form');
  const loginSuccessMsg = document.getElementById('login-success-state');

  // Sections for Scroll Spy
  const sections = document.querySelectorAll('section[id]');
  const desktopNavLinks = document.querySelectorAll('.desktop-nav .nav-link');

  // --- 2. THEME CONTROLLER (LIGHT / DARK) ---
  const STORAGE_KEY_THEME = 'maison_relique_theme';

  function initTheme() {
    const savedTheme = localStorage.getItem(STORAGE_KEY_THEME);
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme ? savedTheme : (prefersDark ? 'dark' : 'light');

    setTheme(initialTheme);
  }

  function setTheme(theme) {
    if (theme === 'dark') {
      htmlEl.setAttribute('data-theme', 'dark');
      updateThemeButtons(true);
    } else {
      htmlEl.removeAttribute('data-theme');
      updateThemeButtons(false);
    }
    localStorage.setItem(STORAGE_KEY_THEME, theme);
  }

  function toggleTheme() {
    const isDark = htmlEl.getAttribute('data-theme') === 'dark';
    setTheme(isDark ? 'light' : 'dark');
  }

  function updateThemeButtons(isDark) {
    // Dynamic Favicon Update
    const faviconLink = document.querySelector('link[rel="icon"]');
    if (faviconLink) {
      faviconLink.setAttribute('href', isDark ? 'assets/icons/favicon-dark.svg' : 'assets/icons/favicon.svg');
    }

    themeToggles.forEach(btn => {
      const sunIcon = btn.querySelector('.icon-sun');
      const moonIcon = btn.querySelector('.icon-moon');
      const label = btn.querySelector('.theme-btn-label');

      if (sunIcon && moonIcon) {
        if (isDark) {
          sunIcon.style.display = 'block';
          moonIcon.style.display = 'none';
        } else {
          sunIcon.style.display = 'none';
          moonIcon.style.display = 'block';
        }
      }
      if (label) {
        label.textContent = isDark ? 'Light Mode' : 'Dark Mode';
      }
      btn.setAttribute('aria-label', isDark ? 'Switch to Light Theme' : 'Switch to Dark Theme');
    });
  }

  themeToggles.forEach(btn => {
    btn.addEventListener('click', toggleTheme);
  });

  // --- 3. RTL / LTR CONTROLLER ---
  const STORAGE_KEY_RTL = 'maison_relique_dir';

  function initDirection() {
    const savedDir = localStorage.getItem(STORAGE_KEY_RTL) || 'ltr';
    setDirection(savedDir);
  }

  function setDirection(dir) {
    htmlEl.setAttribute('dir', dir);
    localStorage.setItem(STORAGE_KEY_RTL, dir);
    updateRtlButtons(dir === 'rtl');
  }

  function toggleDirection() {
    const currentDir = htmlEl.getAttribute('dir') || 'ltr';
    setDirection(currentDir === 'rtl' ? 'ltr' : 'rtl');
  }

  function updateRtlButtons(isRtl) {
    rtlToggles.forEach(btn => {
      const label = btn.querySelector('.rtl-btn-label');
      if (label) {
        label.textContent = isRtl ? 'LTR View' : 'RTL View';
      }
      btn.setAttribute('aria-label', isRtl ? 'Switch to Left to Right' : 'Switch to Right to Left');
    });
  }

  rtlToggles.forEach(btn => {
    btn.addEventListener('click', toggleDirection);
  });

  // --- 4. DESKTOP ACCESSIBLE DROPDOWNS ---
  function closeAllDropdowns() {
    dropdownWrappers.forEach(wrapper => {
      const toggle = wrapper.querySelector('.dropdown-toggle');
      const menu = wrapper.querySelector('.dropdown-menu');
      if (toggle) toggle.setAttribute('aria-expanded', 'false');
      if (menu) menu.classList.remove('show');
    });
  }

  dropdownToggles.forEach(toggle => {
    // Mouse click
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      const parent = this.closest('.nav-dropdown-wrapper');
      const menu = parent.querySelector('.dropdown-menu');
      const isExpanded = this.getAttribute('aria-expanded') === 'true';

      closeAllDropdowns();

      if (!isExpanded) {
        this.setAttribute('aria-expanded', 'true');
        if (menu) menu.classList.add('show');
      }
    });

    // Keyboard support: Enter & Space
    toggle.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        this.click();
      }
    });
  });

  // Close desktop dropdowns on click outside
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-dropdown-wrapper')) {
      closeAllDropdowns();
    }
  });

  // --- 5. MOBILE & TABLET DRAWER NAVIGATION ---
  function openDrawer() {
    if (!mobileDrawer || !drawerBackdrop) return;
    mobileDrawer.classList.add('active');
    drawerBackdrop.classList.add('active');
    if (hamburgerBtn) {
      hamburgerBtn.classList.add('active');
      hamburgerBtn.setAttribute('aria-expanded', 'true');
    }
    bodyEl.style.overflow = 'hidden';

    const firstInteractive = mobileDrawer.querySelector('button, a');
    if (firstInteractive) firstInteractive.focus();
  }

  function closeDrawer() {
    if (!mobileDrawer || !drawerBackdrop) return;
    mobileDrawer.classList.remove('active');
    drawerBackdrop.classList.remove('active');
    if (hamburgerBtn) {
      hamburgerBtn.classList.remove('active');
      hamburgerBtn.setAttribute('aria-expanded', 'false');
    }
    bodyEl.style.overflow = '';
  }

  if (hamburgerBtn) {
    hamburgerBtn.addEventListener('click', function () {
      const isOpen = mobileDrawer.classList.contains('active');
      if (isOpen) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });
  }

  if (drawerCloseBtn) {
    drawerCloseBtn.addEventListener('click', closeDrawer);
  }

  if (drawerBackdrop) {
    drawerBackdrop.addEventListener('click', closeDrawer);
  }

  drawerNavLinks.forEach(link => {
    link.addEventListener('click', function () {
      closeDrawer();
    });
  });

  // Drawer Submenus Accordion
  drawerSubmenuToggles.forEach(toggle => {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      const parent = this.closest('.drawer-nav-item');
      const submenu = parent.querySelector('.drawer-submenu');
      const isExpanded = this.classList.contains('expanded');

      if (isExpanded) {
        this.classList.remove('expanded');
        if (submenu) submenu.classList.remove('open');
        this.setAttribute('aria-expanded', 'false');
      } else {
        this.classList.add('expanded');
        if (submenu) submenu.classList.add('open');
        this.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // --- 6. PRIVATE VIEWING BOOKING MODAL ---
  function openModal() {
    if (!viewingModal || !modalBackdrop) return;
    closeDrawer();
    modalBackdrop.classList.add('active');
    viewingModal.classList.add('active');
    bodyEl.style.overflow = 'hidden';

    const firstInput = viewingModal.querySelector('input, select');
    if (firstInput) firstInput.focus();
  }

  function closeModal() {
    if (!modalBackdrop || !viewingModal) return;
    modalBackdrop.classList.remove('active');
    viewingModal.classList.remove('active');
    bodyEl.style.overflow = '';

    setTimeout(() => {
      if (viewingForm && modalSuccessMsg) {
        viewingForm.style.display = 'block';
        modalSuccessMsg.style.display = 'none';
        viewingForm.reset();
      }
    }, 400);
  }

  openViewingButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      openModal();
    });
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeModal);
  }

  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', function (e) {
      if (e.target === modalBackdrop) {
        closeModal();
      }
    });
  }

  if (viewingForm) {
    viewingForm.addEventListener('submit', function (e) {
      e.preventDefault();
      viewingForm.style.display = 'none';
      if (modalSuccessMsg) {
        modalSuccessMsg.style.display = 'block';
      }
    });
  }

  // --- 6B. CLIENT LOGIN MODAL ---
  function openLoginModal() {
    if (!loginModal || !loginModalBackdrop) return;
    closeDrawer();
    closeModal();
    loginModalBackdrop.classList.add('active');
    loginModal.classList.add('active');
    bodyEl.style.overflow = 'hidden';

    const firstInput = loginModal.querySelector('input');
    if (firstInput) firstInput.focus();
  }

  function closeLoginModal() {
    if (!loginModalBackdrop || !loginModal) return;
    loginModalBackdrop.classList.remove('active');
    loginModal.classList.remove('active');
    bodyEl.style.overflow = '';

    setTimeout(() => {
      if (loginForm && loginSuccessMsg) {
        loginForm.style.display = 'block';
        loginSuccessMsg.style.display = 'none';
        loginForm.reset();
      }
    }, 400);
  }

  openLoginButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      openLoginModal();
    });
  });

  if (loginModalCloseBtn) {
    loginModalCloseBtn.addEventListener('click', closeLoginModal);
  }

  if (loginModalBackdrop) {
    loginModalBackdrop.addEventListener('click', function (e) {
      if (e.target === loginModalBackdrop) {
        closeLoginModal();
      }
    });
  }

  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      e.preventDefault();
      loginForm.style.display = 'none';
      if (loginSuccessMsg) {
        loginSuccessMsg.style.display = 'block';
      }
    });
  }

  // --- 7. KEYBOARD ESCAPE HANDLER ---
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.keyCode === 27) {
      if (loginModal && loginModal.classList.contains('active')) {
        closeLoginModal();
      } else if (viewingModal && viewingModal.classList.contains('active')) {
        closeModal();
      } else if (mobileDrawer && mobileDrawer.classList.contains('active')) {
        closeDrawer();
      } else if (document.getElementById('mobile-filter-drawer') && document.getElementById('mobile-filter-drawer').classList.contains('active')) {
        closeFilterDrawer();
      } else {
        closeAllDropdowns();
      }
    }
  });

  // --- 8. ACTIVE SCROLL SPY ---
  function updateActiveNav() {
    const scrollPos = window.scrollY + 140;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        desktopNavLinks.forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          } else if (link.getAttribute('href') && link.getAttribute('href').startsWith('#')) {
            link.classList.remove('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', updateActiveNav, { passive: true });

  // --- 9. COLLECTION FILTER & SORT CONTROLLER ---
  const collectionGrid = document.getElementById('collection-grid-container');
  const filterCatSelect = document.getElementById('filter-category');
  const filterEraSelect = document.getElementById('filter-era');
  const filterMatSelect = document.getElementById('filter-material');
  const filterSortSelect = document.getElementById('filter-sort');
  const filterResetBtn = document.getElementById('filter-clear-btn');
  const emptyResetBtn = document.getElementById('empty-state-reset-btn');
  const productCountDisplay = document.getElementById('product-count-display');
  const emptyState = document.getElementById('collection-empty-state');

  // Mobile Filter Drawer References
  const mobileFilterDrawer = document.getElementById('mobile-filter-drawer');
  const filterBackdrop = document.getElementById('filter-backdrop');
  const mobileFilterTriggerBtn = document.getElementById('mobile-filter-trigger-btn');
  const filterDrawerCloseBtn = document.getElementById('filter-drawer-close-btn');
  const mobileFilterApplyBtn = document.getElementById('mobile-filter-apply-btn');
  const mobileFilterClearBtn = document.getElementById('mobile-filter-clear-btn');
  const filterPillButtons = document.querySelectorAll('.filter-pill-btn');

  let activeFilters = {
    category: 'all',
    era: 'all',
    material: 'all',
    sort: 'featured'
  };

  function openFilterDrawer() {
    if (!mobileFilterDrawer || !filterBackdrop) return;
    mobileFilterDrawer.classList.add('active');
    filterBackdrop.classList.add('active');
    bodyEl.style.overflow = 'hidden';
  }

  function closeFilterDrawer() {
    if (!mobileFilterDrawer || !filterBackdrop) return;
    mobileFilterDrawer.classList.remove('active');
    filterBackdrop.classList.remove('active');
    bodyEl.style.overflow = '';
  }

  function applyCollectionFilters() {
    if (!collectionGrid) return;
    const cards = Array.from(collectionGrid.querySelectorAll('.collection-card'));
    let visibleCount = 0;

    cards.forEach(card => {
      const cardCat = card.getAttribute('data-category');
      const cardEra = card.getAttribute('data-era');
      const cardMat = card.getAttribute('data-material');

      const matchesCat = activeFilters.category === 'all' || cardCat === activeFilters.category;
      const matchesEra = activeFilters.era === 'all' || cardEra === activeFilters.era;
      const matchesMat = activeFilters.material === 'all' || cardMat === activeFilters.material;

      if (matchesCat && matchesEra && matchesMat) {
        card.style.display = 'flex';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    // Sort visible cards
    const sortedCards = cards.filter(c => c.style.display !== 'none');
    if (activeFilters.sort === 'title-az') {
      sortedCards.sort((a, b) => a.getAttribute('data-title').localeCompare(b.getAttribute('data-title')));
    } else if (activeFilters.sort === 'newest') {
      sortedCards.sort((a, b) => parseInt(b.getAttribute('data-order'), 10) - parseInt(a.getAttribute('data-order'), 10));
    } else {
      // featured
      sortedCards.sort((a, b) => parseInt(a.getAttribute('data-order'), 10) - parseInt(b.getAttribute('data-order'), 10));
    }

    sortedCards.forEach(card => {
      collectionGrid.appendChild(card);
    });

    // Update Product Count
    if (productCountDisplay) {
      productCountDisplay.textContent = `Showing ${visibleCount} Pieces`;
    }

    // Toggle Empty State
    if (emptyState) {
      if (visibleCount === 0) {
        emptyState.style.display = 'block';
        collectionGrid.appendChild(emptyState);
      } else {
        emptyState.style.display = 'none';
      }
    }

    // Sync Controls UI
    syncFilterUI();
  }

  function syncFilterUI() {
    if (filterCatSelect) filterCatSelect.value = activeFilters.category;
    if (filterEraSelect) filterEraSelect.value = activeFilters.era;
    if (filterMatSelect) filterMatSelect.value = activeFilters.material;
    if (filterSortSelect) filterSortSelect.value = activeFilters.sort;

    // Sync Mobile Pills
    filterPillButtons.forEach(btn => {
      const group = btn.closest('[data-filter-group]').getAttribute('data-filter-group');
      const val = btn.getAttribute('data-value');
      if (activeFilters[group] === val) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  function resetAllFilters() {
    activeFilters = {
      category: 'all',
      era: 'all',
      material: 'all',
      sort: 'featured'
    };
    applyCollectionFilters();
  }

  // Bind desktop filter changes
  if (filterCatSelect) {
    filterCatSelect.addEventListener('change', function () {
      activeFilters.category = this.value;
      applyCollectionFilters();
    });
  }

  if (filterEraSelect) {
    filterEraSelect.addEventListener('change', function () {
      activeFilters.era = this.value;
      applyCollectionFilters();
    });
  }

  if (filterMatSelect) {
    filterMatSelect.addEventListener('change', function () {
      activeFilters.material = this.value;
      applyCollectionFilters();
    });
  }

  if (filterSortSelect) {
    filterSortSelect.addEventListener('change', function () {
      activeFilters.sort = this.value;
      applyCollectionFilters();
    });
  }

  if (filterResetBtn) {
    filterResetBtn.addEventListener('click', resetAllFilters);
  }

  if (emptyResetBtn) {
    emptyResetBtn.addEventListener('click', resetAllFilters);
  }

  // Mobile drawer trigger
  if (mobileFilterTriggerBtn) {
    mobileFilterTriggerBtn.addEventListener('click', openFilterDrawer);
  }

  if (filterDrawerCloseBtn) {
    filterDrawerCloseBtn.addEventListener('click', closeFilterDrawer);
  }

  if (filterBackdrop) {
    filterBackdrop.addEventListener('click', closeFilterDrawer);
  }

  // Mobile pills selection
  filterPillButtons.forEach(btn => {
    btn.addEventListener('click', function () {
      const group = this.closest('[data-filter-group]').getAttribute('data-filter-group');
      const val = this.getAttribute('data-value');
      activeFilters[group] = val;
      const groupButtons = this.parentElement.querySelectorAll('.filter-pill-btn');
      groupButtons.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
    });
  });

  if (mobileFilterApplyBtn) {
    mobileFilterApplyBtn.addEventListener('click', function () {
      applyCollectionFilters();
      closeFilterDrawer();
    });
  }

  if (mobileFilterClearBtn) {
    mobileFilterClearBtn.addEventListener('click', function () {
      resetAllFilters();
    });
  }

  // Category Index clicks (Section 4)
  const categoryRowItems = document.querySelectorAll('.category-row-item');
  categoryRowItems.forEach(item => {
    item.addEventListener('click', function () {
      const targetCat = this.getAttribute('data-category-target');
      if (targetCat) {
        activeFilters.category = targetCat;
        applyCollectionFilters();
        const selectionSection = document.getElementById('selection');
        if (selectionSection) {
          selectionSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
    item.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.click();
      }
    });
  });

  // Era Index clicks (Section 5)
  const eraTimelineNodes = document.querySelectorAll('.era-timeline-node');
  eraTimelineNodes.forEach(node => {
    node.addEventListener('click', function () {
      const targetEra = this.getAttribute('data-era-target');
      if (targetEra) {
        activeFilters.era = targetEra;
        applyCollectionFilters();
        const selectionSection = document.getElementById('selection');
        if (selectionSection) {
          selectionSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
    node.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.click();
      }
    });
  });

  // Scale Guide quick links (Section 3)
  const scaleFilterLinks = document.querySelectorAll('[data-filter-scale]');
  scaleFilterLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      const scaleCat = this.getAttribute('data-filter-scale');
      if (scaleCat) {
        activeFilters.category = scaleCat;
        applyCollectionFilters();
        const selectionSection = document.getElementById('selection');
        if (selectionSection) {
          selectionSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });

  // --- 10. PRODUCT DETAIL PAGE DATA CONTROLLER ---
  const PRODUCT_DATA = {
    '01': {
      title: 'Georgian Mahogany Writing Table',
      eraLabel: 'Georgian · Circa 1780',
      eraValue: 'georgian',
      summary: 'A refined writing table with a balanced silhouette, cockbeaded twin frieze drawers, and naturally aged timber with original brass drop handles.',
      image: 'assets/images/collection/products/product-01.jpg',
      period: 'Georgian (1714 – 1837) · England',
      material: 'Solid Cuban Mahogany, Hand-Cast Brass',
      dimensions: 'Height: 76cm · Width: 122cm · Depth: 64cm',
      scale: 'Medium (Study / Library / Salon)',
      condition: 'Conserved in-house. Original patina and joinery preserved. Traditional beeswax luster.'
    },
    '02': {
      title: 'French Oak Provincial Armoire',
      eraLabel: 'Victorian · Circa 1865',
      eraValue: 'victorian',
      summary: 'Hand-hewn mortise and tenon joinery, carved serpentine crown, and original forged iron espagnolette locking mechanism with natural wax finish.',
      image: 'assets/images/collection/products/product-02.jpg',
      period: 'Victorian (1837 – 1901) · Provence, France',
      material: 'Aged French Oak & Forged Iron',
      dimensions: 'Height: 198cm · Width: 135cm · Depth: 58cm',
      scale: 'Room-Scale (Grand Hall / Dining / Master Suite)',
      condition: 'Complete historic conservation. Original hand-forged hinges and locks intact.'
    },
    '03': {
      title: 'Art Deco Sculptural Club Chair',
      eraLabel: 'Art Deco · Circa 1934',
      eraValue: 'art-deco',
      summary: 'Sweeping continuous walnut armrests cradling a deeply cushioned seat, newly restored in dense unbleached heritage bouclé.',
      image: 'assets/images/collection/products/product-03.jpg',
      period: 'Art Deco (1920 – 1939) · Paris, France',
      material: 'Bent Walnut & Unbleached Bouclé',
      dimensions: 'Height: 78cm · Width: 86cm · Depth: 82cm',
      scale: 'Medium (Salon / Reading Corner / Living Room)',
      condition: 'Fully conserved frame. Reupholstered with traditional horsehair and natural bouclé.'
    },
    '04': {
      title: 'Edwardian Glazed Library Bookcase',
      eraLabel: 'Edwardian · Circa 1908',
      eraValue: 'edwardian',
      summary: 'Astragal geometric glazed twin doors revealing adjustable timber shelving, set upon a moulded bracket plinth with subtle brass key escutcheons.',
      image: 'assets/images/collection/products/product-04.jpg',
      period: 'Edwardian (1901 – 1910) · England',
      material: 'Figured Mahogany & Crown Glass',
      dimensions: 'Height: 185cm · Width: 110cm · Depth: 42cm',
      scale: 'Large (Library / Study / Wall Elevation)',
      condition: 'Original wavy cylinder glass intact. Cleaned and hand-waxed with antique beeswax.'
    },
    '05': {
      title: 'Scandinavian Teak Sideboard Credenza',
      eraLabel: 'Mid-Century · Circa 1958',
      eraValue: 'mid-century',
      summary: 'Low-profile architectural silhouette with seamless sliding tambour doors, sculpted recessed solid teak handles, and brass-capped tapered splayed legs.',
      image: 'assets/images/collection/products/product-05.jpg',
      period: 'Mid-Century (1945 – 1970) · Denmark',
      material: 'Burmese Teak & Solid Brass',
      dimensions: 'Height: 74cm · Width: 180cm · Depth: 46cm',
      scale: 'Large (Dining Room / Living Room / Media Elevation)',
      condition: 'Hand-rubbed natural teak oil finish. Tambour roll mechanism smoothly tuned.'
    },
    '06': {
      title: 'Regency Twin-Pedestal Dining Table',
      eraLabel: 'Georgian / Regency · Circa 1815',
      eraValue: 'georgian',
      summary: 'Deeply figured flame mahogany top with reeded edge, supported by twin turned columns on tripod sabre legs terminating in cast brass paw casters.',
      image: 'assets/images/collection/products/product-06.jpg',
      period: 'Regency / Late Georgian (1811 – 1820) · England',
      material: 'Flame Mahogany & Cast Brass',
      dimensions: 'Height: 75cm · Width: 210cm · Depth: 105cm',
      scale: 'Room-Scale (Dining Hall / Entertaining)',
      condition: 'French-polished surface preserving antique character. Brass casters polished and secured.'
    },
    '07': {
      title: 'Art Deco Brass Cheval Mirror',
      eraLabel: 'Art Deco · Circa 1930',
      eraValue: 'art-deco',
      summary: 'Arched architectural frame featuring stepped geometric crown motifs, pivoting brass side stays, and heavy hand-polished brass base with gentle patina.',
      image: 'assets/images/collection/products/product-07.jpg',
      period: 'Art Deco (1920 – 1939) · Belgium',
      material: 'Solid Antique Brass & Heavy Beveled Plate Glass',
      dimensions: 'Height: 165cm · Width: 54cm · Depth: 48cm',
      scale: 'Small (Dressing Room / Foyer / Bedroom)',
      condition: 'Original beveled mirror plate with subtle historic silvering. Brass frame stabilized.'
    },
    '08': {
      title: 'Mid-Century Walnut Partner Desk',
      eraLabel: 'Mid-Century · Circa 1962',
      eraValue: 'mid-century',
      summary: 'Floating desktop design with double drawer pedestals, solid walnut bookmatched grain, and slender brass linear pull accents.',
      image: 'assets/images/collection/products/product-08.jpg',
      period: 'Mid-Century (1945 – 1970) · United States',
      material: 'American Walnut & Brushed Brass Hardware',
      dimensions: 'Height: 76cm · Width: 152cm · Depth: 84cm',
      scale: 'Large (Executive Office / Architectural Study)',
      condition: 'Original factory joinery inspected and leveled. Hard-wax oil finish applied.'
    },
    '09': {
      title: 'Victorian Deep-Tufted Salon Settee',
      eraLabel: 'Victorian · Circa 1885',
      eraValue: 'victorian',
      summary: 'Serpentine carved walnut cresting rail over deep diamond-buttoned mohair velvet upholstery with turned cabriole legs on brass porcelain casters.',
      image: 'assets/images/collection/products/product-09.jpg',
      period: 'Victorian (1837 – 1901) · England',
      material: 'Carved Walnut & Olive Mohair Velvet',
      dimensions: 'Height: 88cm · Width: 148cm · Depth: 76cm',
      scale: 'Medium (Salon / Bay Window / Reception Room)',
      condition: 'Traditional coil springing retied with jute webbing. Luxurious antique mohair velvet.'
    }
  };

  function initProductDetailPage() {
    const urlParams = new URLSearchParams(window.location.search);
    const pieceId = urlParams.get('id') || '01';
    const piece = PRODUCT_DATA[pieceId];

    if (!piece) return;

    const elTitle = document.getElementById('detail-title');
    const elBreadcrumb = document.getElementById('breadcrumb-current-piece');
    const elEra = document.getElementById('detail-era-label');
    const elSummary = document.getElementById('detail-summary');
    const elImage = document.getElementById('detail-image');
    const elPeriod = document.getElementById('detail-spec-period');
    const elMaterial = document.getElementById('detail-spec-material');
    const elDimensions = document.getElementById('detail-spec-dimensions');
    const elScale = document.getElementById('detail-spec-scale');
    const elCondition = document.getElementById('detail-spec-condition');
    const selectEraModal = document.getElementById('viewing-era');

    if (elTitle) elTitle.textContent = piece.title;
    if (elBreadcrumb) elBreadcrumb.textContent = piece.title;
    if (elEra) elEra.textContent = piece.eraLabel;
    if (elSummary) elSummary.textContent = piece.summary;
    if (elImage) {
      elImage.setAttribute('src', piece.image);
      elImage.setAttribute('alt', piece.title);
    }
    if (elPeriod) elPeriod.textContent = piece.period;
    if (elMaterial) elMaterial.textContent = piece.material;
    if (elDimensions) elDimensions.textContent = piece.dimensions;
    if (elScale) elScale.textContent = piece.scale;
    if (elCondition) elCondition.textContent = piece.condition;

    if (selectEraModal && piece.eraValue) {
      selectEraModal.value = piece.eraValue;
    }

    // Dynamic CTA links on product detail
    const enquireBtn = document.getElementById('detail-enquire-btn');
    const viewingBtn = document.getElementById('detail-viewing-btn');
    const restorationBtn = document.getElementById('detail-restoration-btn');
    const encodedTitle = encodeURIComponent(piece.title);

    if (enquireBtn) {
      enquireBtn.setAttribute('href', `contact.html?type=collection&piece=${encodedTitle}#enquiry`);
    }
    if (viewingBtn) {
      viewingBtn.setAttribute('href', `contact.html?type=viewing&piece=${encodedTitle}#enquiry`);
    }
    if (restorationBtn) {
      restorationBtn.setAttribute('href', `contact.html?type=restoration&piece=${encodedTitle}#enquiry`);
    }

    document.title = `${piece.title} — MAISON RELIQUE`;
  }

  // --- 11. CONTACT PAGE URL PARAMETERS & SCROLL CONTROLLER ---
  function initContactPageParams() {
    const contactForm = document.getElementById('contact-enquiry-form');
    if (!contactForm) return;

    const urlParams = new URLSearchParams(window.location.search);
    const typeParam = urlParams.get('type');
    const pieceParam = urlParams.get('piece');

    const typeSelect = document.getElementById('contact-type');
    const pieceInput = document.getElementById('contact-piece');
    const msgTextarea = document.getElementById('contact-message');

    // Handle Preselected Enquiry Type
    if (typeParam && typeSelect) {
      const normalizedType = typeParam.toLowerCase();
      // Match option values or text
      for (let i = 0; i < typeSelect.options.length; i++) {
        const opt = typeSelect.options[i];
        if (opt.value.toLowerCase() === normalizedType ||
            (normalizedType === 'collection' && (opt.value === 'acquisition' || opt.value === 'collection')) ||
            (normalizedType === 'acquisition' && (opt.value === 'acquisition' || opt.value === 'collection'))) {
          typeSelect.selectedIndex = i;
          break;
        }
      }
    }

    // Handle Piece Reference and Message Prefill
    if (pieceParam) {
      const decodedPiece = decodeURIComponent(pieceParam).trim();
      if (pieceInput) {
        pieceInput.value = decodedPiece;
      }
      if (typeSelect && (!typeParam || typeParam === 'collection' || typeParam === 'acquisition')) {
        for (let i = 0; i < typeSelect.options.length; i++) {
          if (typeSelect.options[i].value === 'acquisition' || typeSelect.options[i].value === 'collection') {
            typeSelect.selectedIndex = i;
            break;
          }
        }
      }
      if (msgTextarea && !msgTextarea.value.trim()) {
        msgTextarea.value = `I am interested in: ${decodedPiece}. Please provide condition details, high-resolution photography, and acquisition arrangements.`;
      }
    }

    // Smooth scroll to #enquiry if present in hash
    if (window.location.hash === '#enquiry') {
      const enquirySec = document.getElementById('enquiry');
      if (enquirySec) {
        setTimeout(() => {
          enquirySec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
      }
    }
  }

  // --- 12. INITIALIZATION ON DOM READY ---
  document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    initDirection();
    updateActiveNav();
    if (collectionGrid) {
      applyCollectionFilters();
    }
    if (document.getElementById('detail-title')) {
      initProductDetailPage();
    }
    if (document.getElementById('contact-enquiry-form')) {
      initContactPageParams();
    }
  });

})();

