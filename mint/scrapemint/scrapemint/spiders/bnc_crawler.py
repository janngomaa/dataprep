# -*- coding: utf-8 -*-
import scrapy


class MintSpider(scrapy.Spider):
    name = 'bnc_crawler'
    allowed_domains = ['bnc.ca']
    start_urls = ['https://bvi.bnc.ca/auth/Login']

    def parse(self, response):
        print('********************    BEGIN CRAWLING ...')
        
        return scrapy.FormRequest.from_response(response, \
                                                formdata={'username': '', \
                                                          'password': ''},\
                                                callback=self.after_login \
                                               )

    def after_login(self, response):
        if b'Error while logging in' in response.body:
            self.logger.error("Login failed!")
        else:
            self.logger.info("Login succeeded!")
            scrapy.Request(url="https://bvi.bnc.ca/bnc/page?" \
                           "BPPC=BPPC18040320460863592566" \
                           "&aliasDispatcher=masterCardEntryPoint" \
                           "&cAliasDispatcher=masterCardMsgDisplay", \
                           callback=self.parse_data)
            #item = SampleItem()
            #item["quote"] = response.css(".text").extract()
            #item["author"] = response.css(".author").extract()
            #return item
    def parse_data(self, response):
        self.logger.info("Parsing Data .... from %s!" %response.url)
        