
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_real_ingredients_from_site(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    time.sleep(3)  # Sayfanın tam yüklenmesi için bekle

    try:
        element = driver.find_element("css selector", ".recipe-materials")
        full_text = element.get_attribute("innerText")  # 🧠 Bu en sağlam yöntem
    except Exception as e:
        driver.quit()
        return {"error": f"Malzemeler alınamadı: {e}"}

    driver.quit()

    # Her satırı ayıkla
    ingredients = [line.strip() for line in full_text.split("\n") if line.strip()]
    return ingredients

# Örnek kullanım

url = "https://www.nefisyemektarifleri.com/video/yumusacik-pogaca/"
result = get_real_ingredients_from_site(url)

if isinstance(result, dict) and "error" in result:
    print("❌", result["error"])
else:
    print("✅ Gerçek Malzemeler (kaynak: nefisyemektarifleri.com):")
    for item in result:
        print(" -", item)
