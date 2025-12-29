try : 
    from app.api.handlers import update_items_handler
except ModuleNotFoundError : 
    from api.handler import update_items_handler

if __name__ == "__main__":
    sample = [
        {"name": "Aged Brie", "sell_in": 2, "quality": 0}
    ]

    print(update_items_handler(sample))