(function () {
  if (document.querySelector('.back-to-top')) return;
  var btn = document.createElement('button');
  btn.className = 'back-to-top';
  btn.setAttribute('aria-label', '回到顶部');
  btn.setAttribute('title', '回到顶部');
  btn.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 4l-8 8h5v8h6v-8h5z"/></svg>';
  document.body.appendChild(btn);

  var TH = Math.max(300, Math.round(window.innerHeight * 0.5));
  var ticking = false;
  function update() {
    if (window.pageYOffset > TH) { btn.classList.add('show'); }
    else { btn.classList.remove('show'); }
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  window.addEventListener('resize', function () { TH = Math.max(300, Math.round(window.innerHeight * 0.5)); update(); }, { passive: true });
  update();

  btn.addEventListener('click', function () {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });
})();
