from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

def slugify(turkish_text):
    mapping = {
        "ç": "c", "Ç": "c",
        "ğ": "g", "Ğ": "g",
        "ı": "i", "İ": "i",
        "ö": "o", "Ö": "o",
        "ş": "s", "Ş": "s",
        "ü": "u", "Ü": "u"
    }
    for turkish, ascii_char in mapping.items():
        turkish_text = turkish_text.replace(turkish, ascii_char)
    turkish_text = turkish_text.lower()
    turkish_text = re.sub(r'[^a-z0-9\s-]', '', turkish_text)
    turkish_text = turkish_text.replace(" ", "-")
    return turkish_text.strip("-")

def get_real_ingredients_from_site(meal_name):
    slug = slugify(meal_name)
    url = f"https://www.nefisyemektarifleri.com/{slug}/"
    print(f"🔗 URL: {url}")

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)

        # Malzeme kısmı birden fazla şekilde olabilir
        possible_selectors = [
            ".recipe-materials",
            ".recipe-materials-inner",
            ".recipe-material-content",
            ".recipe-content"
        ]

        element = None
        for selector in possible_selectors:
            try:
                element = driver.find_element("css selector", selector)
                if element and element.get_attribute("innerText").strip():
                    break
            except:
                continue

        if not element:
            return {"error": "Hiçbir malzeme alanı bulunamadı."}

        full_text = element.get_attribute("innerText")
        ingredients = [line.strip() for line in full_text.split("\n") if line.strip()]

        return {
            "meal": meal_name,
            "url": url,
            "ingredients": ingredients
        }

    except Exception as e:
        return {"error": f"Hata oluştu: {e}"}
    finally:
        driver.quit()

# Test
meal_input = input("Yemek adı girin: ")  # Örnek: anne köftesi
result = get_real_ingredients_from_site(meal_input)

if "error" in result:
    print("❌", result["error"])
else:
    print(f"\n✅ {result['meal']} Tarifi (Kaynak: {result['url']})")
    for item in result['ingredients']:
        print(" -", item)
