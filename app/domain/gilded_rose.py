# -*- coding: utf-8 -*-

SULFURAS = "Sulfuras, Hand of Ragnaros"
AGED_BRIE = "Aged Brie"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"

maxQuantity = 50
minQuantity = 0

def increase_quality(item, amount=1):
    if item.quality < maxQuantity:
        item.quality += amount


def decrease_quality(item, amount=1):
    if item.quality > minQuantity:
        item.quality -= amount

def decrease_sell_in(item):
    item.sell_in -= 1

def update_normal_item(item):
    decrease_quality(item)


def update_aged_brie(item):
    increase_quality(item)


def update_backstage(item):
    increase_quality(item)
    if item.sell_in < 11:
        increase_quality(item)
    if item.sell_in < 6:
        increase_quality(item)

def handle_expired_item(item):
    if item.name == AGED_BRIE:
        increase_quality(item)
    elif item.name == BACKSTAGE:
        item.quality = minQuantity
    elif item.name != SULFURAS:
        decrease_quality(item)


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:

            is_sulfuras = item.name == SULFURAS
            is_aged_brie = item.name == AGED_BRIE
            is_backstage = item.name == BACKSTAGE

            if is_sulfuras : 
                continue 
            
            if is_aged_brie:
                update_aged_brie(item)
            elif is_backstage:
                update_backstage(item)
            else : 
                update_normal_item(item)


            decrease_sell_in(item)

            if item.sell_in < 0:
                handle_expired_item(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
