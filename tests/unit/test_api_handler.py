from app.api.handler import update_items_handler


def test_update_items_handler_increases_aged_brie():
    data = [{"name": "Aged Brie", "sell_in": 2, "quality": 0}]

    result = update_items_handler(data)

    assert result[0]["quality"] == 1


def test_update_items_handler_normal_item():
    data = [
        {"name": "Elixir of the Mongoose", "sell_in": 5, "quality": 7}
    ]

    result = update_items_handler(data)

    assert result == [
        {"name": "Elixir of the Mongoose", "sell_in": 4, "quality": 6}
    ]


def test_update_items_handler_aged_brie_increases_quality():
    data = [
        {"name": "Aged Brie", "sell_in": 2, "quality": 0}
    ]

    result = update_items_handler(data)

    assert result[0]["quality"] == 1
    assert result[0]["sell_in"] == 1


def test_update_items_handler_backstage_standard_increase():
    data = [
        {
            "name": "Backstage passes to a TAFKAL80ETC concert",
            "sell_in": 15,
            "quality": 20,
        }
    ]

    result = update_items_handler(data)

    assert result[0]["quality"] == 21


def test_update_items_handler_backstage_near_concert():
    data = [
        {
            "name": "Backstage passes to a TAFKAL80ETC concert",
            "sell_in": 5,
            "quality": 20,
        }
    ]

    result = update_items_handler(data)

    assert result[0]["quality"] == 23
    assert result[0]["sell_in"] == 4

def test_update_items_handler_sulfuras_unchanged():
    data = [
        {
            "name": "Sulfuras, Hand of Ragnaros",
            "sell_in": 0,
            "quality": 80,
        }
    ]

    result = update_items_handler(data)

    assert result == data


# Negative tests 
def test_update_items_handler_quality_never_negative():
    data = [
        {"name": "Elixir of the Mongoose", "sell_in": 0, "quality": 0}
    ]

    result = update_items_handler(data)

    assert result[0]["quality"] == 0

def test_update_items_handler_backstage_after_concert():
    data = [
        {
            "name": "Backstage passes to a TAFKAL80ETC concert",
            "sell_in": 0,
            "quality": 30,
        }
    ]

    result = update_items_handler(data)

    assert result[0]["quality"] == 0
def test_update_items_handler_empty_input():
    result = update_items_handler([])

    assert result == []


def test_update_items_handler_quality_capped_at_50():
    data = [
        {"name": "Aged Brie", "sell_in": 1, "quality": 50}
    ]

    result = update_items_handler(data)

    assert result[0]["quality"] == 50