# calculator.py 
from fractions import Fraction

# Sade birim → gram dönüşüm tablosu (her malzeme için ortak kabul)
unit_to_gram = {
    "su bardağı": 200,
    "yemek kaşığı": 15,
    "tatlı kaşığı": 10,
    "çay kaşığı": 5,
    "ml": 1,
    "litre": 1000,
    "gram": 1,
    "gr": 1,
    "kg": 1000,
    "adet": 100,
    "paket": 250,
    "tutam": 1,
    "avuç": 25,
    "çimdik": 0.5,
    "dilim": 30,
    "kase": 150,
    "küçük": 70,
    "büyük": 150
}

def parse_quantity(qty_str: str) -> float:
    try:
        if '/' in qty_str:
            return float(Fraction(qty_str.strip()))
        return float(qty_str.strip())
    except:
        return 1.0

def calculate_price(amount_str: str, unit: str, price_per_kg: float) -> float:
    unit = unit.strip().lower()
    amount = parse_quantity(amount_str)

    if unit not in unit_to_gram:
        raise ValueError(f"Bilinmeyen ölçü birimi: {unit}")

    gram = unit_to_gram[unit] * amount
    kg = gram / 1000
    return round(kg * price_per_kg, 2)

# Örnek kullanımlar
if __name__ == "__main__":
    print(calculate_price("1/4", "yemek kaşığı", 130))  # 0.49 TL
    print(calculate_price("2", "avuç", 60))             # 3.0 TL
    print(calculate_price("1", "paket", 400))           # 100.0 TL

