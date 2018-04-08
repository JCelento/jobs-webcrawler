# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from jobs.items import JobsItem

class InfojobsSpider(scrapy.Spider):
    name = 'infojobs'
    allowed_domains = []
    start_urls = [
        'https://www.infojobs.com.br/empregos.aspx?Palabra=Desenvolvedor',
        'https://www.infojobs.com.br/empregos.aspx?Palabra=Programador',
        ''.join('https://www.infojobs.com.br/empregos.aspx?Palabra=analista%20de%20sistemas'.split())
    ]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('li > a.lnkNext::attr(href)',)),
             callback="parse",
             follow=True),)

    def parse(self, response):
       item_links = response.css('.vagaTitle::attr(href)').extract()
       for a in item_links:
        yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        jobTitle = response.css('.header-content-left> h1::text').extract()[0].strip()
        company = response.css('.header-name::text').extract()[0]
        location = response.css('.liLocation> span::text').extract()[0]
        jobSummary = response.css('.descriptionItems *::text').extract()
        salary = response.css('.liSalary> span::text').extract()[0]

        print('Got item...', response.url)
        
        item = JobsItem()
        item['jobTitle'] = jobTitle
        item['company'] = company
        item['location'] = location
        item['jobSummary'] = jobSummary
        item['url'] = response.url
        item['salary'] = salary
        yield item