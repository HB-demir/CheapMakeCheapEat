# scraper-service/app.py

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
import time

from malzeme_resim_scraper import get_recipe_data
from en_ucuz_fiyat import get_cheapest_price_from_market

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
CORS(app)

CACHE_FILE = "cache/recipes_cache.json"

def save_to_cache(meal, data):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    cache[meal] = data
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    app.logger.info("✅ Cached result for '%s'", meal)

def load_from_cache(meal):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        result = cache.get(meal)
        if result:
            app.logger.info("♻️ Cache hit for '%s'", meal)
        return result
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate_meal():
    data = request.get_json(force=True)
    app.logger.info("📨 Incoming JSON: %s", data)
    meal = data.get("mealName") or data.get("meal") or ""
    if not meal:
        return jsonify({"error": "Meal name is required"}), 400

    # 1) Cache kontrolü
    cached = load_from_cache(meal)
    if cached:
        return jsonify(cached)

    # 2) Scrape tarif ve malzemeleri çek
    recipe = get_recipe_data(meal)
    if "error" in recipe:
        app.logger.error("❌ Scraper error: %s", recipe["error"])
        return jsonify({"error": recipe["error"]}), 500

    # 3) Her malzeme için en ucuz fiyatı al
    result = {
        "meal": recipe["meal"],
        "image": recipe["image"],
        "ingredients": [],
        "prices": {},
        "total_cost": 0
    }
    total = 0
    for ing in recipe["ingredients"]:
        fiyat_data = get_cheapest_price_from_market(ing)
        # fiyat_data ya float/int ya da {'error': ...} ya da {'price': float}
        price = None
        if isinstance(fiyat_data, dict):
            price = fiyat_data.get("price")
        elif isinstance(fiyat_data, (int, float)):
            price = fiyat_data

        if price is None:
            app.logger.warning("⚠️ Fiyat bulunamadı: %s", ing)
            continue

        result["ingredients"].append(ing)
        result["prices"][ing] = round(price, 2)
        total += price
        time.sleep(0.5)  # isteğe bağlı: servisi yormamak için bekle

    result["total_cost"] = round(total, 2)

    # 4) Cache’e kaydet ve dön
    save_to_cache(meal, result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
