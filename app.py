from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Render from Flask!"

@app.route("/extract", methods=["GET"])
def extract():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.content, "html.parser")

        title = soup.select_one("dl.blogDtlInner dt")
        image = soup.select_one("dl.blogDtlInner dd img")
        text_raw = soup.select_one("dl.blogDtlInner dd")

        return jsonify({
            "title": title.text.strip() if title else "",
            "image": image["src"] if image else "",
            "text": text_raw.get_text(separator="\n").strip() if text_raw else "",
            "url": url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
