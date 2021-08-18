# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YichewangItem(scrapy.Item):
    # define the fields for your item here like:
    letter=scrapy.Field()
    brand_name=scrapy.Field()
    logo=scrapy.Field()
    car_name=scrapy.Field()
    type_name=scrapy.Field()
    type=scrapy.Field()
    data_id=scrapy.Field()
    new_page=scrapy.Field()
    sort=scrapy.Field()


