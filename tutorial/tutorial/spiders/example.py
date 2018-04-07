# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from tutorial.items import TutorialItem
from scrapy.http import Request



class ExampleSpider(scrapy.Spider):
    name = 'crawler_assignment'
    allowed_domains = ['target.com/']
    start_urls = ['http://target.com/']

    def parse(self, response):
        hxs =  Selector(response=response)
        visited_links = []
        # links = hxs.path('//a/@href').extract()
        links = hxs.xpath('//a/@href').extract()
        link_validator = re.compile("^(?:http|https)")
        for link in links:
            if link_validator.match(link) and not link in visited_links:
                visited_links.append(link)
                yield Request(link,self.parse)
            else:
                full_url = response.urljoin(link)
                visited_links.append(full_url)
                yield Request(full_url, self.parse)
