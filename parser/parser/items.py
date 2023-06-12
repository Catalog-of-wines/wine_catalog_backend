# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WineItem(scrapy.Item):
    kind = scrapy.Field()
    name = scrapy.Field()
    color = scrapy.Field()
    wine_type = scrapy.Field()
    brand = scrapy.Field()
    capacity = scrapy.Field()
    in_box = scrapy.Field()
    package = scrapy.Field()
    alcohol_percentage = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    producer = scrapy.Field()
    glass = scrapy.Field()
    temperature = scrapy.Field()
    gastronomic_combination = scrapy.Field()
    grape = scrapy.Field()
    vintage = scrapy.Field()
    decantation = scrapy.Field()
    diameter = scrapy.Field()
    supplier = scrapy.Field()
    image_url = scrapy.Field()
    small_image_url = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
