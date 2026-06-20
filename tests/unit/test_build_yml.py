import xml.etree.ElementTree as ET
from datetime import datetime

from feed_task import CATEGORIES, PRODUCTS, build_yml


def test_build_yml_valid_xml():
    """Проверяем, что результат является валидным XML."""
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )

    # Не должно возникать исключений при парсинге
    root = ET.fromstring(result)
    assert root.tag == "yml_catalog"
    assert root.attrib["date"] == "2026-06-18 12:00"


def test_build_yml_product_filtering():
    """Проверяем, что в фид попали только правильные товары (101, 102, 107)."""
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )
    root = ET.fromstring(result)

    offers = root.findall(".//offer")
    assert len(offers) == 3

    offer_ids = [offer.attrib["id"] for offer in offers]
    assert offer_ids == ["101", "102", "107"]


def test_build_yml_categories_filtering():
    """Проверяем, что в фид попали только категории отфильтрованных товаров (1, 2)."""
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )
    root = ET.fromstring(result)

    categories = root.findall(".//category")
    assert len(categories) == 2

    cat_ids = [cat.attrib["id"] for cat in categories]
    assert cat_ids == ["1", "2"]


def test_build_yml_available_attribute():
    """Проверяем атрибут available (true если stock > 0, иначе false)."""
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )
    root = ET.fromstring(result)

    offer_101 = root.find(".//offer[@id='101']")
    assert offer_101.attrib["available"] == "true"

    offer_102 = root.find(".//offer[@id='102']")
    assert offer_102.attrib["available"] == "false"

    offer_107 = root.find(".//offer[@id='107']")
    assert offer_107.attrib["available"] == "true"


def test_build_yml_price_format():
    """Проверяем форматирование цены (точка, два знака)."""
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )
    root = ET.fromstring(result)

    assert root.find(".//offer[@id='101']/price").text == "490.00"
    assert root.find(".//offer[@id='102']/price").text == "1500.00"
    assert root.find(".//offer[@id='107']/price").text == "700.50"


def test_build_yml_old_price():
    """Проверяем логику вывода старой цены."""
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )
    root = ET.fromstring(result)

    # У 101 старая цена больше новой, должна быть
    assert root.find(".//offer[@id='101']/oldprice").text == "590.00"

    # У 102 старая цена меньше новой, не должно быть
    assert root.find(".//offer[@id='102']/oldprice") is None

    # У 107 нет старой цены
    assert root.find(".//offer[@id='107']/oldprice") is None


def test_build_yml_description():
    """Проверяем, что пустое описание не выводится."""
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )
    root = ET.fromstring(result)

    # У 101 есть описание
    assert root.find(".//offer[@id='101']/description").text is not None

    # У 107 описание пустое, тега быть не должно
    assert root.find(".//offer[@id='107']/description") is None


def test_build_yml_escaping():
    """Проверяем, что специальные символы корректно экранируются."""
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )
    root = ET.fromstring(result)

    name_element = root.find(".//offer[@id='101']/name")
    assert name_element.text == 'Чай "Лес & травы" <сбор №1>'
