# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from aliscraper.items import AliscraperItem

import hashlib


class AliCrawlerSpider(CrawlSpider):
    name = 'ali_crawler'
    allowed_domains = ['aliexpress.com']
    start_urls = ['https://www.aliexpress.com/category/200003482/dresses.html']

    rules = (
        Rule(LinkExtractor(allow=['\/item\/']), 
             callback='parse_item', 
             follow=True),
    )

    def parse_item(self, response):
        aliItem = AliscraperItem()
                                  
        aliItem['id'] = hashlib.md5(bytes(str(response.url),"ascii")).hexdigest()
        aliItem['url'] = response.url
        aliItem['price'] = response.xpath('//*[@id="j-sku-price"]/text()').extract()
        aliItem['shippingCompany'] = response.xpath('//*[@id="j-shipping-company"]/text()').extract()
 
        return aliItem
