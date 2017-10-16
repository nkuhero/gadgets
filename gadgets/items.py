# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GadgetsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    mainPic = scrapy.Field()
    highlights = scrapy.Field()
    desc = scrapy.Field()

