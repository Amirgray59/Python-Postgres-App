import pytest
from kata.gilded_rose.after.gilded_rose import Item, GildedRose

def update_items(*items):
    app = GildedRose(list(items))
    app.update_quality()


def test_normal_item_degrades_by_one_before_sell_date():
    item = Item("Elixir of the Mongoose", sell_in=10, quality=20)

    update_items(item)

    assert item.sell_in == 9
    assert item.quality == 19


def test_normal_item_degrades_twice_as_fast_after_sell_date():
    item = Item("Elixir of the Mongoose", sell_in=0, quality=10)

    update_items(item)

    assert item.sell_in == -1
    assert item.quality == 8


def test_quality_never_negative():
    item = Item("Elixir of the Mongoose", sell_in=0, quality=0)

    update_items(item)

    assert item.quality == 0


def test_aged_brie_increases_in_quality():
    item = Item("Aged Brie", sell_in=10, quality=10)

    update_items(item)

    assert item.quality == 11


def test_aged_brie_quality_capped_at_50():
    item = Item("Aged Brie", sell_in=5, quality=50)

    update_items(item)

    assert item.quality == 50


def test_sulfuras_never_changes():
    item = Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)

    update_items(item)

    assert item.sell_in == 0
    assert item.quality == 80


@pytest.mark.parametrize(
    "sell_in,quality,expected_quality",
    [
        (15, 20, 21),
        (10, 20, 22),
        (5, 20, 23),
        (0, 20, 0),
    ],
)
def test_backstage_passes_behavior(sell_in, quality, expected_quality):
    item = Item(
        "Backstage passes to a TAFKAL80ETC concert",
        sell_in=sell_in,
        quality=quality,
    )

    update_items(item)

    assert item.quality == expected_quality