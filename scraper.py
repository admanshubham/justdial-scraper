from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ JustDial Scraper is running! Use /scrape?url=<JustDial URL>"

@app.route("/scrape", methods=["GET"])
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing ?url="}), 400

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # 🔹 Example: extract business names from JustDial listing
        business_names = [tag.get_text(strip=True) for tag in soup.select("a.rsNa")]

        return jsonify({
            "url": url,
            "count": len(business_names),
            "business_names": business_names
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
