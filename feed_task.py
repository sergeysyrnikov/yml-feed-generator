import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Dict, List

CATEGORIES = [
    {
        "id": 1,
        "name": "Чай",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Посуда",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Подарочные наборы",
        "is_active": False,
    },
]


PRODUCTS = [
    {
        "id": 101,
        "name": 'Чай "Лес & травы" <сбор №1>',
        "slug": "les-i-travy",
        "category_id": 1,
        "price": "490.00",
        "old_price": "590.00",
        "stock": 12,
        "description": "Вкус: мята & чабрец > классический чай",
        "image_url": "https://example.test/media/tea-101.jpg",
        "is_active": True,
    },
    {
        "id": 102,
        "name": "Чайник стеклянный",
        "slug": "glass-teapot",
        "category_id": 2,
        "price": "1500.00",
        "old_price": "1400.00",
        "stock": 0,
        "description": "Стеклянный чайник объёмом 800 мл",
        "image_url": "https://example.test/media/teapot-102.jpg",
        "is_active": True,
    },
    {
        "id": 103,
        "name": "Скрытый товар",
        "slug": "hidden-product",
        "category_id": 1,
        "price": "350.00",
        "old_price": None,
        "stock": 5,
        "description": "Товар отключён администратором",
        "image_url": "https://example.test/media/product-103.jpg",
        "is_active": False,
    },
    {
        "id": 104,
        "name": "Пробник чая",
        "slug": "tea-sample",
        "category_id": 1,
        "price": "0.00",
        "old_price": None,
        "stock": 30,
        "description": "Бесплатный пробник",
        "image_url": "https://example.test/media/product-104.jpg",
        "is_active": True,
    },
    {
        "id": 105,
        "name": "Чашка фарфоровая",
        "slug": "porcelain-cup",
        "category_id": 2,
        "price": "700.00",
        "old_price": "900.00",
        "stock": 4,
        "description": "Фарфоровая чашка",
        "image_url": None,
        "is_active": True,
    },
    {
        "id": 106,
        "name": "Подарочный набор",
        "slug": "gift-set",
        "category_id": 3,
        "price": "2500.00",
        "old_price": "3000.00",
        "stock": 2,
        "description": "Товар находится в неактивной категории",
        "image_url": "https://example.test/media/product-106.jpg",
        "is_active": True,
    },
    {
        "id": 107,
        "name": "Чай улун молочный",
        "slug": "milk-oolong",
        "category_id": 1,
        "price": "700.50",
        "old_price": None,
        "stock": 3,
        "description": "",
        "image_url": "https://example.test/media/product-107.jpg",
        "is_active": True,
    },
]


def build_yml(
    products: List[Dict[str, Any]], categories: List[Dict[str, Any]], generated_at: datetime
) -> str:  # noqa: C901
    # 1. Подготавливаем словарь категорий для быстрого доступа
    cat_map = {c["id"]: c for c in categories}

    # 2. Фильтруем товары по правилам
    valid_products = []
    for p in products:
        # Товар активен
        if not p.get("is_active"):
            continue

        # Категория активна
        cat = cat_map.get(p.get("category_id"))
        if not cat or not cat.get("is_active"):
            continue

        # Название не пустое
        if not p.get("name"):
            continue

        # Цена больше нуля
        try:
            price = float(p.get("price", 0))
        except (ValueError, TypeError):
            continue
        if price <= 0:
            continue

        # Ссылка на изображение начинается с http:// или https://
        img = p.get("image_url")
        if not img or not (img.startswith("http://") or img.startswith("https://")):
            continue

        valid_products.append((p, price))

    # 3. Сортируем товары по идентификатору
    valid_products.sort(key=lambda x: x[0]["id"])

    # 4. Собираем только те категории, которые используются в отфильтрованных товарах
    used_cat_ids = sorted(list(set(p["category_id"] for p, _ in valid_products)))

    # 5. Формируем XML-дерево
    date_str = generated_at.strftime("%Y-%m-%d %H:%M")
    root = ET.Element("yml_catalog", date=date_str)
    shop = ET.SubElement(root, "shop")

    ET.SubElement(shop, "name").text = "Test Shop"
    ET.SubElement(shop, "company").text = "Test Company"
    ET.SubElement(shop, "url").text = "https://example.test"

    currencies = ET.SubElement(shop, "currencies")
    ET.SubElement(currencies, "currency", id="RUB", rate="1")

    categories_el = ET.SubElement(shop, "categories")
    for cat_id in used_cat_ids:
        cat = cat_map[cat_id]
        cat_el = ET.SubElement(categories_el, "category", id=str(cat_id))
        cat_el.text = cat["name"]

    offers_el = ET.SubElement(shop, "offers")
    for p, price in valid_products:
        available_str = "true" if p.get("stock", 0) > 0 else "false"
        offer_el = ET.SubElement(offers_el, "offer", id=str(p["id"]), available=available_str)

        ET.SubElement(offer_el, "url").text = f"https://example.test/products/{p['slug']}/"
        ET.SubElement(offer_el, "price").text = f"{price:.2f}"

        old_price_raw = p.get("old_price")
        if old_price_raw:
            try:
                old_price = float(old_price_raw)
                if old_price > 0 and old_price > price:
                    ET.SubElement(offer_el, "oldprice").text = f"{old_price:.2f}"
            except (ValueError, TypeError):
                pass

        ET.SubElement(offer_el, "currencyId").text = "RUB"
        ET.SubElement(offer_el, "categoryId").text = str(p["category_id"])
        ET.SubElement(offer_el, "picture").text = p["image_url"]
        ET.SubElement(offer_el, "name").text = p["name"]

        desc = p.get("description")
        if desc:
            ET.SubElement(offer_el, "description").text = desc

    # 6. Конвертируем в строку
    xml_bytes = ET.tostring(root, encoding="UTF-8", xml_declaration=True)
    xml_str = str(xml_bytes.decode("utf-8"))

    # ElementTree может использовать одинарные кавычки в декларации,
    # заменяем на двойные для строгого соответствия формату YML
    if xml_str.startswith("<?xml version='1.0' encoding='UTF-8'?>"):
        xml_str = xml_str.replace(
            "<?xml version='1.0' encoding='UTF-8'?>", '<?xml version="1.0" encoding="UTF-8"?>', 1
        )

    return xml_str


if __name__ == "__main__":
    import sys

    # Настройка вывода для корректного отображения кириллицы в консоли Windows
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )

    print(result)
