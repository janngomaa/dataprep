# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyupwPipeline(object):
    def open_spider(self, spider):
        self.file = open('upm.jl', 'w')

    def close_spider(self, spider):
        self.file.close()
        #Insert into param table
        
    def process_item(self, item, spider):
        if not item['title'] is None:
            item['title'] = 'TOTOTOTOT'
            '''
            item['merchant'] = self.helper.cleanHtml(item['merchant'])
            item['merchantLocation'] = self.helper.cleanHtml(item['merchantLocation'])
            
            item['dealOptMessages'] = list(filter(lambda x: len(x)>0, \
                                                  map(self.helper.cleanHtml, item['dealOptMessages'])))
            item['dealOptPrices'] = list(filter(lambda x: len(x)>0, \
                                                    map(self.helper.cleanHtml, item['dealOptPrices'])))

            
            item['dealTiming'] = self.helper.cleanHtml(item['dealTiming'])
            item['dealRatingValue'] = self.helper.cleanHtml(item['dealRatingValue']) + '%'
            '''
            
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
            return item
        else:
            raise DropItem("Missing title in %s" % item)
           
       
    def cleanHtml(self, html):
        return str(html).replace('\n', '').strip()
