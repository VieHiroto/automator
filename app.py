from flask import request, jsonify
import requests
from bs4 import BeautifulSoup

@app.route("/extract", methods=["GET"])
def extract_blog():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.select_one("dl.blogDtlInner dt")
        image = soup.select_one("dl.blogDtlInner dd img")
        text_html = soup.select_one("dl.blogDtlInner dd")

        # 整形
        title = title.get_text(strip=True) if title else ""
        image_url = image["src"] if image else ""
        text = text_html.decode_contents().replace("<br>", "\n").replace("<br/>", "\n") if text_html else ""
        soup_text = BeautifulSoup(text, "html.parser").get_text(strip=True)

        return jsonify({
            "title": title,
            "text": soup_text,
            "image": image_url,
            "url": url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
