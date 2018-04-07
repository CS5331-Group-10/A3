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
        links_h1 = hxs.xpath("//h1").extract()
        print links_h1
