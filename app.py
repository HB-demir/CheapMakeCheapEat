from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from malzeme_resim_scraper import get_recipe_data

app = Flask(__name__, template_folder="templates")
CORS(app)

CACHE_FILE = "cache/recipes_cache.json"

# 📦 Cache’e veri yaz
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

# ♻️ Cache’den veri oku
def load_from_cache(meal):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        result = cache.get(meal)
        if result:
            app.logger.info("♻️ Cache hit for '%s'", meal)
        return result
    return None

# 🏠 Ana sayfa
@app.route("/")
def index():
    return render_template("index.html")

# 🍽️ Yemek hesaplama
@app.route("/calculate", methods=["POST"])
def calculate_meal():
    payload = request.get_json(force=True)
    app.logger.info("📨 Gelen JSON: %s", payload)

    meal = payload.get("mealName") or payload.get("meal") or ""
    if not meal:
        return jsonify({"error": "Meal name is required"}), 400

    cached = load_from_cache(meal)
    if cached:
        return jsonify(cached)

    try:
        recipe = get_recipe_data(meal)
        app.logger.info("📥 get_recipe_data sonucu: %s", recipe)
    except Exception as e:
        app.logger.error("🔥 get_recipe_data HATASI: %s", str(e))
        return jsonify({"error": "Tarif verisi alınamadı."}), 500

    if not recipe or not isinstance(recipe, dict) or "meal" not in recipe:
        return jsonify({"error": "Yemek bulunamadı veya veri eksik"}), 404

    result = {
        "meal": recipe["meal"],
        "image": recipe["image"],
        "ingredients": recipe["ingredients"]
    }

    save_to_cache(meal, result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
