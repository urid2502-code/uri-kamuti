// Render the print pages built by build_pdfs.py to A4 PDFs, with a page footer.
// usage: node tools/print/render.js <jobs.json>
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const job of jobs) {
    await page.goto('file://' + job.html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: job.pdf,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate:
        '<div dir="rtl" style="width:100%;font:8.5px Arial,sans-serif;color:#7a8086;padding:0 17mm;display:flex;justify-content:space-between">' +
        '<span>urIQ · מקבץ ' + job.set + '</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    });
  }
  await browser.close();
})();
