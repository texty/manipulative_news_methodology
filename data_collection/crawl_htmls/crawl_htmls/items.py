# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RaResult(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    real_url = scrapy.Field()
    ra_title = scrapy.Field()
    ra_summary = scrapy.Field()
    rss_id = scrapy.Field()
    fbfeeds_id = scrapy.Field()
    page_links = scrapy.Field()
    pass