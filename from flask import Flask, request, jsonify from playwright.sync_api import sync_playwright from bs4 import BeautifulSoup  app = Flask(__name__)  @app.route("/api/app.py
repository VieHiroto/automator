from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/api/extract")
def extract():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")

            title = page.locator("dl.blogDtlInner dt").inner_text(timeout=5000)
            content_html = page.locator("dl.blogDtlInner dd").inner_html(timeout=5000)
            image = page.locator("dl.blogDtlInner dd img").get_attribute("src")

            soup = BeautifulSoup(content_html, "html.parser")
            for br in soup.find_all("br"):
                br.replace_with("\n")
            text = soup.get_text().strip()

            browser.close()

            return jsonify({
                "title": title,
                "text": text,
                "image": image,
                "url": url
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
