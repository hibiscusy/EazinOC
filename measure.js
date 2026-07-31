const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
  await page.goto('http://127.0.0.1:8123/OC%E5%AE%87%E5%AE%99-%E4%BA%BA%E7%89%A9%E6%97%B6%E9%97%B4%E7%BA%BF-%E8%92%B2%E7%86%A0%E6%98%9F.html', { waitUntil: 'networkidle' });
  const data = await page.evaluate(() => {
    const r = (sel) => { const e = document.querySelector(sel); const b = e.getBoundingClientRect(); return { top: b.top, bottom: b.bottom, height: b.height }; };
    const intro = r('.intro');
    const pyx = r('#r-pyx');
    const firstOC = r('#r-jx');
    return { intro, pyx, firstOC };
  });
  const topGap = data.pyx.top - data.intro.bottom;
  const bottomGap = data.firstOC.top - data.pyx.bottom;
  console.log('intro.bottom=', data.intro.bottom.toFixed(1), 'pyx.top=', data.pyx.top.toFixed(1), '=> TOP gap=', topGap.toFixed(1));
  console.log('pyx.bottom=', data.pyx.bottom.toFixed(1), 'firstOC.top=', data.firstOC.top.toFixed(1), '=> BOTTOM gap=', bottomGap.toFixed(1));
  console.log('DIFF=', (bottomGap - topGap).toFixed(1));
  await browser.close();
})();
