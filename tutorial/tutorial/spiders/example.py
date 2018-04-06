# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'crawler example'
    allowed_domains = ['http://target.com/']
    start_urls = ['http://target.com/']

    def parse(self, response):
        pass
