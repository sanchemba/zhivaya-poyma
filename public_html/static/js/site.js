console.log("site loaded");

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