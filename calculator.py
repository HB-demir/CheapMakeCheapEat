# calculator.py 
from fractions import Fraction
from typing import Tuple

# Birim + Malzeme yoğunluklarına göre (gram cinsinden)
unit_material_to_gram = {
    ("yemek kaşığı", "şeker"): 20,
    ("yemek kaşığı", "zeytinyağı"): 13,
    ("yemek kaşığı", "un"): 8,
    ("yemek kaşığı", "salça"): 15,
    ("tatlı kaşığı", "tuz"): 5,
    ("çay kaşığı", "tuz"): 3,
    ("çay kaşığı", "karabiber"): 2,
    ("su bardağı", "pirinç"): 160,
    ("su bardağı", "süt"): 200,
    ("su bardağı", "un"): 120,
    ("avuç", "ceviz"): 30,
    ("avuç", "ıspanak"): 20,
    ("adet", "yumurta"): 60,
    ("adet", "domates"): 120,
    ("dilim", "ekmek"): 35,
    ("paket", "kabartma tozu"): 10,
    ("ml", "sıvı"): 1,
    ("litre", "sıvı"): 1000,
    ("gram", "herşey"): 1,
    ("gr", "herşey"): 1,
    ("kg", "herşey"): 1000,
    ("kase", "yoğurt"): 150,
    ("tutam", "maydanoz"): 1,
    ("çimdik", "tuz"): 0.5,
    ("küçük", "soğan"): 70,
    ("büyük", "soğan"): 150
}

def parse_quantity(qty_str: str) -> float:
    """"1/2", "2.5" gibi stringleri float'a çevirir."""
    try:
        if '/' in qty_str:
            return float(Fraction(qty_str.strip()))
        return float(qty_str.strip())
    except:
        return 1.0

def calculate_price(amount_str: str, unit: str, material: str, price_per_kg: float) -> float:
    """
    Ölçü + Malzeme'yi gram'a çevirip doğru orantı ile fiyat hesaplar.
    Eğer eşleşme bulunamazsa ValueError fırlatır.
    """
    unit = unit.strip().lower()
    material = material.strip().lower()
    amount = parse_quantity(amount_str)

    key: Tuple[str, str] = (unit, material)
    fallback_key: Tuple[str, str] = (unit, "herşey")

    if key in unit_material_to_gram:
        gram = unit_material_to_gram[key] * amount
    elif fallback_key in unit_material_to_gram:
        gram = unit_material_to_gram[fallback_key] * amount
    else:
        raise ValueError(f"Tanımsız ölçü birimi ve malzeme çifti: {key}")

    kg = gram / 1000
    return round(kg * price_per_kg, 2)

# Örnek kullanımlar (backend testleri yapılırken silinebilir)
if __name__ == "__main__":
    print(calculate_price("1/4", "yemek kaşığı", "zeytinyağı", 130))  # 0.42 TL
    print(calculate_price("2", "avuç", "ıspanak", 60))                # 2.4 TL
    print(calculate_price("1", "paket", "kabartma tozu", 400))        # 4.0 TL
