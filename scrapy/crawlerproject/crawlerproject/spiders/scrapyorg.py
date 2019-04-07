# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlerproject.items import CrawlerprojectItem


class ScrapyorgSpider(CrawlSpider):
    name = 'scrapyorg'
    #allowed_domains = ['scrapy.org']
    
    def start_requests(self):
        urls = [
            'https://doc.scrapy.org/en/latest/topics/items.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    


    def parse(self, response):
        item = CrawlerprojectItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        pages = response.xpath("/html/body/div[1]/nav/div/div[2]/ul[1]/li")
        for p in pages:
            item["file_urls"] = 'https://doc.scrapy.org/en/latest/' + str(p.xpath("a/@href").extract_first()).replace('../', '')
            item["title"] = p.xpath("a/text()").extract_first()
            print(item)
            yield item

   
