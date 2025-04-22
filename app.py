from flask import Flask, request, jsonify
from malzeme_resim_scraper import get_recipe_data
from en_ucuz_fiyat import get_cheapest_price_from_market
import time

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_meal_cost():
    data = request.json
    meal_name = data.get("mealName")

    if not meal_name:
        return jsonify({"error": "Meal name is required"}), 400

    recipe = get_recipe_data(meal_name)
    if "error" in recipe:
        return jsonify({"error": recipe["error"]}), 404

    ingredients = []
    prices = []
    total = 0

    for item in recipe["ingredients"]:
        price = get_cheapest_price_from_market(item)
        if isinstance(price, dict) and "error" in price:
            continue
        if isinstance(price, (float, int)):
            ingredients.append(item)
            prices.append(price)
            total += price
        time.sleep(1)

    return jsonify({
        "meal": recipe["meal"],
        "image": recipe["image"],
        "ingredients": ingredients,
        "prices": dict(zip(ingredients, prices)),
        "total_cost": round(total, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
