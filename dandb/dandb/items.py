# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class DandbItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    business_url = Field()
    business_name = Field()
    street = Field()
    city = Field()
    state = Field()
    zip = Field()
    phone = Field()
    url = Field()
    email = Field()
    founded = Field()
    incorporated = Field()
    revenue = Field()
    employee = Field()
    industries = Field()
    contacts = Field()
