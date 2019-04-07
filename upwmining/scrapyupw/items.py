# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyupwItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    AreaHierarchie = scrapy.Field()
    ProjectType = scrapy.Field()
    ProjectPricingType = scrapy.Field()
    ProjectBudget = scrapy.Field()
    RequiredExpertiseLevel = scrapy.Field()
    StartDate = scrapy.Field()
    Posted = scrapy.Field()
    Client = scrapy.Field()
    relatedSkills = scrapy.Field()
    activityOnJob  = scrapy.Field()
    tecTimeExtract = scrapy.Field()
    batchId = scrapy.Field()
