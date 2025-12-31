
try : 
    from app.domain.gilded_rose import GildedRose, Item
except ModuleNotFoundError : 
    from domain.gilded_rose import GildedRose, Item
    

def update_items_handler(items_data: list[dict]) -> list[dict]:
    items = [
        Item(
            name=data["name"],
            sell_in=data["sell_in"],
            quality=data["quality"],
        )
        for data in items_data
    ]

    app = GildedRose(items)
    app.update_quality()

    return [
        {
            "name": item.name,
            "sell_in": item.sell_in,
            "quality": item.quality,
        }
        for item in items
    ]