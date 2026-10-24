(function () {
  'use strict';

  var themeToggle = document.getElementById('theme-toggle');
  var modal = document.getElementById('work-modal');
  var modalClose = modal.querySelector('.modal-close');
  var backToTop = document.getElementById('back-to-top');
  var worksDataEl = document.getElementById('works-data');
  var worksData = worksDataEl ? JSON.parse(worksDataEl.textContent) : [];

  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

  function getPreferredTheme() {
    var stored = localStorage.getItem('theme');
    if (stored) return stored;
    return prefersDark.matches ? 'dark' : 'light';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  setTheme(getPreferredTheme());

  themeToggle.addEventListener('click', function () {
    var current = document.documentElement.getAttribute('data-theme');
    setTheme(current === 'dark' ? 'light' : 'dark');
  });

  function openModal(index) {
    var work = worksData[index];
    if (!work) return;

    var imgWrapper = document.getElementById('modal-image-wrapper');
    var imgEl = modal.querySelector('.modal-image');
    if (work.image) {
      imgEl.src = work.image;
      imgEl.alt = work.title;
      imgWrapper.style.display = '';
    } else {
      imgWrapper.style.display = 'none';
    }

    modal.querySelector('.modal-title').textContent = work.title;
    modal.querySelector('.modal-description').textContent = work.detail;

    var tagsContainer = modal.querySelector('.modal-tags');
    tagsContainer.innerHTML = '';
    work.tags.forEach(function (tag) {
      var span = document.createElement('span');
      span.className = 'tag';
      span.textContent = tag;
      tagsContainer.appendChild(span);
    });

    var linksContainer = modal.querySelector('.modal-links');
    linksContainer.innerHTML = '';
    work.links.forEach(function (link) {
      var a = document.createElement('a');
      a.href = link.url;
      a.className = 'modal-link';
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.innerHTML = '<i data-feather="external-link"></i> ' + link.label;
      linksContainer.appendChild(a);
    });

    var listContainer = modal.querySelector('.modal-participation');
    listContainer.innerHTML = '';
    if (work.participation && work.participation.length) {
      listContainer.style.display = '';
      work.participation.forEach(function (p) {
        var a = document.createElement('a');
        a.href = p.url;
        a.className = 'participation-item';
        a.target = '_blank';
        a.rel = 'noopener noreferrer';

        var badge = document.createElement('span');
        badge.className = 'participation-badge ' + (p.type === 'pr' ? 'badge-pr' : 'badge-issue');
        badge.textContent = p.type === 'pr' ? 'PR' : 'Issue';

        var title = document.createElement('span');
        title.className = 'participation-title';
        title.textContent = p.title;

        var state = document.createElement('span');
        state.className = 'participation-state';
        state.textContent = p.state;
        if (p.state === 'merged' || p.state === 'closed') {
          state.classList.add('state-done');
        }

        var date = document.createElement('span');
        date.className = 'participation-date';
        date.textContent = (p.date || '').slice(0, 10);

        a.appendChild(badge);
        a.appendChild(title);
        a.appendChild(state);
        a.appendChild(date);
        listContainer.appendChild(a);
      });
    } else {
      listContainer.style.display = 'none';
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    feather.replace();
  }

  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  document.querySelectorAll('.work-card').forEach(function (card) {
    card.addEventListener('click', function () {
      openModal(parseInt(this.dataset.index));
    });
  });

  modalClose.addEventListener('click', closeModal);

  modal.addEventListener('click', function (e) {
    if (e.target === this) closeModal();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });

  window.addEventListener('scroll', function () {
    if (window.scrollY > 300) {
      backToTop.classList.add('visible');
    } else {
      backToTop.classList.remove('visible');
    }
  });

  backToTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  feather.replace();
})();
