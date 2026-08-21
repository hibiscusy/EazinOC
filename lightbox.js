(function () {
  var grids = document.querySelectorAll('.diary-img-grid');
  if (!grids.length) return;

  var lb = document.createElement('div'); lb.className = 'img-lightbox';
  var im = document.createElement('img'); im.className = 'lb-img';
  var prev = document.createElement('button'); prev.className = 'lb-nav lb-prev'; prev.setAttribute('aria-label', '上一张'); prev.innerHTML = '&#10094;';
  var next = document.createElement('button'); next.className = 'lb-nav lb-next'; next.setAttribute('aria-label', '下一张'); next.innerHTML = '&#10095;';
  var cnt = document.createElement('div'); cnt.className = 'lb-count';
  var closeBtn = document.createElement('button'); closeBtn.className = 'lb-close'; closeBtn.setAttribute('aria-label', '关闭'); closeBtn.innerHTML = '&times;';
  lb.appendChild(im); lb.appendChild(prev); lb.appendChild(next); lb.appendChild(cnt); lb.appendChild(closeBtn);
  document.body.appendChild(lb);

  var curGrid = null, curIdx = -1, swiped = false;
  function show() {
    if (!curGrid) return;
    var list = curGrid._imgs;
    if (curIdx < 0 || curIdx >= list.length) return;
    var img = list[curIdx];
    im.src = img.currentSrc || img.src; im.alt = img.alt;
    cnt.textContent = (curIdx + 1) + ' / ' + list.length;
    prev.classList.toggle('disabled', curIdx === 0);
    next.classList.toggle('disabled', curIdx === list.length - 1);
  }
  function openLB(grid, imgEl) {
    curGrid = grid;
    var list = grid._imgs;
    curIdx = list.indexOf(imgEl);
    if (curIdx < 0) curIdx = 0;
    lb.classList.add('open');
    show();
  }
  function go(d) {
    if (!curGrid) return;
    var list = curGrid._imgs;
    var ni = curIdx + d;
    if (ni < 0 || ni >= list.length) return;
    curIdx = ni; show();
  }
  function closeLB() { lb.classList.remove('open'); curGrid = null; curIdx = -1; }

  grids.forEach(function (grid) {
    grid.addEventListener('click', function (e) {
      var t = e.target;
      if (t && t.tagName === 'IMG') { openLB(grid, t); }
    });
  });
  lb.addEventListener('click', function (e) {
    if (swiped) { swiped = false; return; }
    if (e.target === lb || e.target === im || e.target === closeBtn) { closeLB(); }
  });
  prev.addEventListener('click', function (e) { e.stopPropagation(); go(-1); });
  next.addEventListener('click', function (e) { e.stopPropagation(); go(1); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') { closeLB(); }
    else if (e.key === 'ArrowLeft') { go(-1); }
    else if (e.key === 'ArrowRight') { go(1); }
  });
  var sx = 0, sy = 0, tracking = false;
  lb.addEventListener('touchstart', function (e) { var t = e.changedTouches[0]; sx = t.clientX; sy = t.clientY; tracking = true; swiped = false; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (!tracking) return; tracking = false;
    var t = e.changedTouches[0]; var dx = t.clientX - sx, dy = t.clientY - sy;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) { swiped = true; go(dx < 0 ? 1 : -1); setTimeout(function () { swiped = false; }, 350); }
  }, { passive: true });

  function colCount() {
    var w = window.innerWidth;
    if (w <= 560) return 2;
    if (w <= 900) return 3;
    return 4;
  }
  function build(grid) {
    var imgs = grid._imgs || (grid._imgs = Array.prototype.slice.call(grid.querySelectorAll('img')));
    if (!imgs.length) return;
    var n = colCount();
    grid.classList.add('masonry');
    grid.innerHTML = '';
    var cols = [];
    for (var i = 0; i < n; i++) { var c = document.createElement('div'); c.className = 'mg-col'; grid.appendChild(c); cols.push({ el: c, h: 0 }); }
    imgs.forEach(function (img) {
      var min = cols[0];
      for (var i = 1; i < cols.length; i++) { if (cols[i].h < min.h) min = cols[i]; }
      min.el.appendChild(img);
      var w = parseFloat(img.getAttribute('width')) || 1;
      var h = parseFloat(img.getAttribute('height')) || 1;
      min.h += h / w;
    });
  }
  grids.forEach(build);

  var lastCols = colCount();
  function onBreakpoint() {
    var n = colCount();
    if (n === lastCols) return;
    lastCols = n;
    grids.forEach(build);
  }
  if (window.matchMedia) {
    var mqs = ['(max-width:560px)', '(max-width:900px)'];
    mqs.forEach(function (q) {
      var m = window.matchMedia(q);
      if (m.addEventListener) m.addEventListener('change', onBreakpoint);
      else if (m.addListener) m.addListener(onBreakpoint);
    });
  }
})();
