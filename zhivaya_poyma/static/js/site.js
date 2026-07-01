//console.log("site loaded");

// этот блок для параллакса
(function () {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  if (reduceMotion.matches) return;

  const updateParallax = () => {
    root.style.setProperty('--scroll', window.scrollY);
  };

  updateParallax();
  window.addEventListener('scroll', updateParallax, { passive: true });
})();

// этот блок для раскрывающегося меню в мобильном отображении
document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.querySelector('.mobile-menu-toggle');
  const menu = document.querySelector('.mobile-menu');

  if (!toggle || !menu) return;

  toggle.addEventListener('click', function () {
    const isOpen = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!isOpen));
    menu.hidden = isOpen;
    menu.classList.toggle('is-open', !isOpen);
  });

  menu.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      toggle.setAttribute('aria-expanded', 'false');
      menu.hidden = true;
      menu.classList.remove('is-open');
    });
  });
});
