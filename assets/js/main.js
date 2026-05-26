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

    var imgEl = modal.querySelector('.modal-image');
    imgEl.src = work.image;
    imgEl.alt = work.title;
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

  document.querySelectorAll('.card-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
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
