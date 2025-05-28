const express = require("express");
const puppeteer = require("puppeteer");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());

app.get("/api/extract", async (req, res) => {
  const url = req.query.url;
  if (!url) return res.status(400).json({ error: "URL is required" });

  try {
    const browser = await puppeteer.launch({
      headless: "new",
      args: ["--no-sandbox", "--disable-setuid-sandbox"]
    });

    const page = await browser.newPage();

    await page.setUserAgent(
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    );

    await page.goto(url, { waitUntil: "networkidle2", timeout: 0 });

    // ページが完全に描画されるまで待機
    await page.waitForSelector("dl.blogDtlInner", { timeout: 15000 });

    const data = await page.evaluate(() => {
      const title = document.querySelector("dl.blogDtlInner dt")?.innerText.trim() || "";

      const rawHtml = document.querySelector("dl.blogDtlInner dd")?.innerHTML || "";
      const text = rawHtml
        .replace(/<br\s*\/?>/gi, "\n")
        .replace(/<[^>]+>/g, "")
        .trim();

      const image = document.querySelector("dl.blogDtlInner dd img")?.src || "";
      return { title, text, image };
    });

    await browser.close();
    return res.json({ ...data, url });
  } catch (err) {
    console.error("Extraction error:", err);
    return res.status(500).json({ error: "Failed to fetch or render page" });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
