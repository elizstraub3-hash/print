const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(900);
  await p.pdf({ path: process.argv[3], width: '210mm', height: '297mm', printBackground: true });
  await b.close();
})();
