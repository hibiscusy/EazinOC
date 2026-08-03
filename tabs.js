/* 公共 tab 切换 —— 适用于所有含 .tabs 的页面（度漪/谶等）
 * 结构约定：
 *   .tabs[role=tablist] > button.tab-btn[data-tab=xxx][role=tab][aria-controls=tab-xxx]
 *   同一容器（section）内的 .tab-panel#tab-xxx[role=tabpanel]
 * 点击按钮：切换 active、维护 aria-selected、按 #tab-<tab> 显隐对应面板。
 */
(function () {
  function setup(tabs) {
    if (!tabs || tabs.dataset.ready) return;
    tabs.dataset.ready = '1';
    tabs.addEventListener('click', function (e) {
      var btn = e.target.closest('.tab-btn');
      if (!btn || !tabs.contains(btn)) return;
      var tab = btn.getAttribute('data-tab');
      if (!tab) return;
      tabs.querySelectorAll('.tab-btn').forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('active', on);
        if (b.hasAttribute('aria-selected')) {
          b.setAttribute('aria-selected', on ? 'true' : 'false');
        }
      });
      var scope = tabs.parentElement;
      scope.querySelectorAll('.tab-panel').forEach(function (p) {
        p.hidden = p.id !== 'tab-' + tab;
      });
    });
  }
  document.querySelectorAll('.tabs').forEach(setup);
})();
