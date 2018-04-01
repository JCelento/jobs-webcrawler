# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from jobs.items import JobsItem

class IndeedSpider(CrawlSpider):
    name = 'indeed'
    allowed_domains = []
    start_urls = [
        'https://www.indeed.com.br/empregos-de-desenvolvedor',
        'https://www.indeed.com.br/empregos-de-analista-de-sistemas',
        'https://www.indeed.com.br/empregos-de-programador'
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pagination',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
       item_links = response.css('.jobtitle::attr(href)').extract()
       for a in item_links:
        yield scrapy.Request("http://indeed.com.br"+ a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        jobTitle = response.css('.jobtitle> font::text').extract()[0].strip()
        company = response.css('.company::text').extract()[0]
        location = response.css('.location::text').extract()[0]
        jobSummary = response.css('.summary *::text').extract()

        print('Got item...', response.url)
        
        item = JobsItem()
        item['jobTitle'] = jobTitle
        item['company'] = company
        item['location'] = location
        item['jobSummary'] = jobSummary
        item['url'] = response.url
        yield item