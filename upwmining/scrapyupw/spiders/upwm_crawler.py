# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyupw.items import JobItem
import datetime

import hashlib
from cryptography.fernet import Fernet


class UpwmSpider(CrawlSpider):
    name = 'upwm_crawler'
    upwmKey = b'BTcjnu5BY4YjcEv--QxGBO_EAR1QRS16vlBz6KdrJSc='
    
    upwm_domain = Fernet(upwmKey).decrypt(b'gAAAAABa1UJA8Y7ttvD92reNs4oXdazSYSuC8RLxgFC3txjpi-'\
                                           b'IIok0X8uzMRK_Fj-B7HWsmYYWh7M1UPycWeMQnPzWz_oW2GQ==')
    
    upwm_url = Fernet(upwmKey).decrypt(b'gAAAAABasa0ROZgnQGxyzS9Ddqv9TuiXZm0xPl-J1TZ7H4fqkIScoTZ'\
                                       b'hRzBt57mKqvAp_KK5OqKAjdeWWXBvLJg6B9lBFf5BmHKqeotwh_kg1r'\
                                       b'YWtjRsPggR-tvGPfbTGl2Bi5wriB-P')
    
    allowed_domains = [upwm_domain.decode("utf-8")]
    start_urls = [upwm_url.decode("utf-8")]


    BATCH_ID = "upw_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f_%z")

    rules = (
        Rule(
            LinkExtractor(
                allow=(['\/jobs\/job\/', '\/jobs\/browse\/']),
                deny=(['\/login']),
                canonicalize=False,
                unique=True,
            ),
            callback='parse_job', 
            follow=True
        ),
    )

    def parse_job(self, response):
        job_id = ''
        try:
            job_id = str(response.url).split("_")[1][:-1]
        except:
            pass
        if len(job_id) > 1:
            job = JobItem()
            #job['id'] = hashlib.md5(bytes(str(response.url),"ascii")).hexdigest()
            job['url'] = response.url
            job['title'] = response.xpath('//*[@id="layout"]/div[2]/div[1]/div/h1/text()').extract_first()
            #job['AreaHierarchie'] = ' >> '.join(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]/header/a/text()').extract())
            ##job['ProjectType'] = ''.join(response.xpath('//*[@id="form"]/li[3]/text()').extract())
            
            job['ProjectPricingType'] = response\
            .xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]/header/div/div[1]/div[2]/p/strong/text()').extract_first('')

            job['ProjectBudget'] = response\
            .xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]/header/div/div[2]/div/div[2]/p/strong/text()').extract_first('')

            #Extractein Required Experience Level 

            job['RequiredExpertiseLevel'] = {'Symbol':''.join(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]/header/div'\
                                                                              '/div[position() < 5]/div[1]/text()')
                                                               .extract()).replace('\n', '').strip(), 
                                             'Level':''.join(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]/header/div'\
                                                                            '/div[position() > 1 and position() < 5]/div[2]/p'\
                                                                            '/strong/text()')
                                                               .extract()).replace('\n', '').strip(), 
                                             'Detail':''.join(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]/header/div'\
                                                                             '/div[position() > 1 and position() < 5]/div[2]/small/text()')
                                                               .extract()).replace('\n', '').strip(),
                                            }


            job['StartDate'] = ''

            job['Posted'] = ''.join(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]/'\
                                                   'section[1]/span/small/span/text()').extract()).replace('\n', '').strip()

            job['Client'] = {'RatingValue': response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                           '/aside/div[2]/div/div/span[2]/span[1]/text()').extract_first(''),
                             'RatingCount': response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                           '/aside/div[2]/div/div/span[2]/span[2]/text()').extract_first(''),
                             'clientCountry': response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                             '/aside/p[2]/strong/text()').extract_first(''),
                             'clientCity': '|'.join(str(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                          '/aside/p[2]/span/text()').extract_first('')).split('\n')),
                             'numberOfPostedJobs': str(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                                  '/aside/p[3]/strong/text()').extract_first('')).replace('\n', '').strip(),
                             'hiringRates': str(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                          '/aside/p[3]/span/text()').extract_first('')).replace('\n', '').strip(),
                             'totalAmountSpent': str(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]/aside/p[4]'\
                                                                    '/strong/span/@ng-bind').extract_first('')).replace('\n', '').strip(),
                             'hiringStatistics': str(response.xpath('///*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                                '/aside/p[4]/span/text()').extract_first('')).replace('\n', '').strip(),
                             'avgRatePaid': str(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                           '/aside/p[5]/strong/text()[1]').extract_first('')).replace('\n', '').strip(),
                             'totalHoursSpent': str(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                               '/aside/p[5]/span/text()').extract_first('')).replace('\n', '').strip(),
                             'memberSince': str(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[2]'\
                                                           '/aside/small/text()').extract_first('')).replace('\n', '').strip(),
                            }


            job['relatedSkills'] = response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]/section[2]/div/@data-ng-init').extract()
            job['activityOnJob'] = {'submittedProposalRange' : ''.join(response.xpath('//*[@id="layout"]/div[2]/div[2]'\
                                                                                      '/div/div[1]/section[position() < 5]/div/div/p[1]'\
                                                                                      '/text()').extract()).replace('\n', '').strip(),
                                    'interviewing': ''.join(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]'\
                                                                           '/section[position() < 5]/div/div/p[2]/text()')\
                                                            .extract()).replace('\n', '').strip(),
                                    'invitesSent': ''.join(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]'\
                                                                  '/section[position() < 5]/div/div/p[3]/text()')\
                                                           .extract()).replace('\n', '').strip(),
                                    'unAnsweredInvites': ''.join(response.xpath('//*[@id="layout"]/div[2]/div[2]/div/div[1]'\
                                                                                '/section[position() < 5]/div/div/p[4]/text()')\
                                                                 .extract()).replace('\n', '').strip(),
                                   }
            job['tecTimeExtract']: datetime.datetime.now()
            job['batchId']: self.BATCH_ID

            yield job
