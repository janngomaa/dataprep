import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]


    def parse(self, response):
        pnum = 1
        for quote in response.css('div.quote'):
            yield {
                'text': quote.xpath('//span/text()').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
            
            next_page = response.css('li.next a::attr(href)').extract_first()
            if next_page is not None and pnum < 10:
                yield response.follow(next_page, callback=self.parse)
            pnum = pnum + 1