from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from urlparse import urlparse
from bs4 import BeautifulSoup
import requests
from scrapy.selector import Selector
import re

class MyItem(Item):
    originalResponse = Field()
    url= Field()
    endpoint = Field()
    query = Field()
    headers = Field()
    resquest = Field()
    cookies = Field()
    meta = Field()
    raw_html = Field()
    input_post_params = Field()
    html_url = Field()
    get_post = Field()
    action_url = Field()
    forms = Field()



class ExampleSpider(CrawlSpider):
    name = 'crawler_assignment'
    start_urls = ['http://target.com']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True), )


    def parse_url(self, response):
        selector = Selector(response)
        item = MyItem()
        value = ''
        item['originalResponse'] = response.url
        parsed = urlparse(response.url)
        # if 'html' in response.url:
        #     yield{
        #         html_url : response.url
        #     }
        # soup = BeautifulSoup(response.text, 'html.parser').findAll('input')

        # if(response.css('input')):
        #     value = response.css('form')[0].extract()
        #
        # else:
        #     value = ''

        form_values = {}
        if(response.css('form')):
            # print response.css('form')
            value = response.css('form')[0].extract()
            form_values['form'] = value
            form_values['action'] = response.xpath('//form//@action').extract()
            form_values['method'] = response.xpath('//form//@method').extract()
            form_values['inputs'] = {'name': response.xpath('//form/input/@name').extract(), 'value': response.xpath('//form/input/@value').extract()}
        else:
            value = ''

        ### See if there is a GET request ###
        get_post_value = []
        request = response.request
        query = parsed.query
        if (query or 'GET' in value):
            get_post_value.append('GET')
            if ('POST' in value):
                get_post_value.append('POST')
            else:
                pass
        elif ('POST' in value):
            get_post_value.append('POST')
        else:
            pass

        yield {
            "endpoint": parsed.path,
            "forms": form_values,
            "url": response.url,
            "query": parsed.query,
            "headers": response.headers,
            "cookies":response.headers.getlist('Set-Cookie'),
            "request": response.request,
            "get_post": get_post_value,
            "meta": response.meta,
            "input_post_params": value

        }
