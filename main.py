import json
import os
import time
from malzeme_resim_scraper import get_recipe_data
from en_ucuz_fiyat import get_cheapest_price_from_market

# 🚨 Docker'da kalıcı olması için bu klasöre bağlayacağız:
CACHE_FILE = "cache/recipes_cache.json"

# 📥 JSON cache'e yaz
def save_to_cache(meal, data):
    os.makedirs("cache", exist_ok=True)  # klasör yoksa oluştur
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    else:
        cache = {}

    cache[meal] = data

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

# 📤 JSON cache'den oku
def load_from_cache(meal):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        return cache.get(meal)
    return None

if __name__ == "__main__":
    meal = input("🍽️ Tarif adı girin: ")

    cached = load_from_cache(meal)
    if cached:
        print(f"\n✅ '{meal}' önceden bulunmuş (cache'den).")
        print(f"📷 Görsel: {cached['image']}")
        for ing, fiyat in zip(cached['ingredients'], cached['prices']):
            print(f"🔍 {ing} → {fiyat} TL")
        print(f"\n💰 Toplam maliyet: {cached['total']} TL")
        exit()

    # Eğer cache'de yoksa yeni veriler çek
    recipe = get_recipe_data(meal)
    if "error" in recipe:
        print("❌ Tarif alınamadı:", recipe["error"])
        exit()

    print(f"\n📷 Görsel: {recipe['image']}")
    print("\n📋 Malzemeler ve Fiyatlar:\n")

    ingredients = []
    prices = []
    total = 0

    for item in recipe["ingredients"]:
        print(f"🔍 {item} → ", end="")
        fiyat = get_cheapest_price_from_market(item)

        if isinstance(fiyat, dict) and "error" in fiyat:
            print(f"❌ {fiyat['error']}")
            continue

        if isinstance(fiyat, (float, int)):
            print(f"{fiyat} TL")
            ingredients.append(item)
            prices.append(fiyat)
            total += fiyat
        else:
            print("⚠️ Fiyat alınamadı.")

        time.sleep(2)

    print(f"\n💰 Toplam maliyet: {round(total, 2)} TL")

    # Cache'e kaydet
    save_to_cache(meal, {
        "meal": recipe["meal"],
        "image": recipe["image"],
        "ingredients": ingredients,
        "prices": prices,
        "total": round(total, 2)
    })

