from flask import Flask, request, jsonify, redirect
from database import Database
from shortener import Shortener

app = Flask(__name__)
db = Database()
shortener = Shortener()

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to URL Shortener API ",
        "endpoints": {
            "POST /shorten": "Shorten a URL",
            "GET /<short_code>": "Redirect to original URL",
            "GET /stats/<short_code>": "Get click analytics"
        }
    })

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Please provide a URL"}), 400

    original_url = data["url"]
    custom_code  = data.get("custom_code")  

    if not original_url.startswith(("http://", "https://")):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    if custom_code:
        if db.code_exists(custom_code):
            return jsonify({"error": "Custom code already taken!"}), 409
        short_code = custom_code
    else:
        short_code = shortener.generate_code()
        while db.code_exists(short_code):
            short_code = shortener.generate_code()

    db.save_url(short_code, original_url)

    return jsonify({
        "original_url": original_url,
        "short_code":   short_code,
        "short_url":    f"http://localhost:5000/{short_code}",
        "message":      "URL shortened successfully! "
    }), 201

@app.route("/<short_code>")
def redirect_url(short_code):
    url_data = db.get_url(short_code)

    if not url_data:
        return jsonify({"error": "Short URL not found!"}), 404

    db.track_click(short_code)

    return redirect(url_data["original_url"])

@app.route("/stats/<short_code>")
def get_stats(short_code):
    url_data = db.get_url(short_code)

    if not url_data:
        return jsonify({"error": "Short URL not found!"}), 404

    clicks = db.get_clicks(short_code)

    return jsonify({
        "short_code":   short_code,
        "short_url":    f"http://localhost:5000/{short_code}",
        "original_url": url_data["original_url"],
        "total_clicks": url_data["clicks"],
        "created_at":   url_data["created_at"],
        "click_history": clicks
    })

@app.route("/all")
def list_all():
    all_urls = db.get_all_urls()
    return jsonify({
        "total_urls": len(all_urls),
        "urls": all_urls
    })

if __name__ == "__main__":
    print("🚀 URL Shortener running at http://localhost:5000")
    app.run(debug=True)
