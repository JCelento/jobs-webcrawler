# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

class IndeedSpider(CrawlSpider):
    name = 'indeed'
    allowed_domains = ['www.indeed.com.br']
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
       item_links = response.css('.jobtitle > .turnstileLink::attr(href)').extract()
       for a in item_links:
        yield scrapy.Request(a, callback=self.parse_detail_page)
