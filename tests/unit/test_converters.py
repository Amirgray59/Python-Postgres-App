
def test_user_tuple_to_dict():
    user_tuple = (1, "amir", "amir@example.com")
    user_dict = {"id": 1, "name": "amir", "email": "amir@example.com"}
    assert dict(zip(["id", "name", "email"], user_tuple)) == user_dict

def test_item_tuple_to_dict():
    item_tuple = (1, "item1", 10, 5, 1)
    item_dict = {"id": 1, "name": "item1", "sell_in": 10, "quality": 5, "owner_id": 1}
    assert dict(zip(["id","name","sell_in","quality","owner_id"], item_tuple)) == item_dict
