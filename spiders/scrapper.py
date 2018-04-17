from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from urlparse import urlparse
from bs4 import BeautifulSoup
import requests
from scrapy.selector import Selector
import re

import os

class MyItem(Item):
    originalResponse = Field()
    url= Field()
    endpoint = Field()
    get_params = Field()
    post_params = Field()
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

    # start_urls = ['file:///home/cs5331/Desktop/A3/tutorial/tutorial/spiders/sample.html']

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



        ### See if there is a GET request ###
        get_post_value = []
        request = response.request
        get_params = parsed.query
        if (get_params or 'GET' in value):
            get_post_value.append('GET')
            if ('POST' in value):
                get_post_value.append('POST')
            else:
                pass
        elif ('POST' in value):
            get_post_value.append('POST')
        else:
            pass

        methods = response.xpath('//form//@method').extract()
        ##handling post_params:
        post_params = response.xpath('//form//input//@name').extract()
        # print "yay"
        # print len(post_params)

        ##handling input params:
        if get_params :
            get_params.split('=')
        else:
            pass

        if (get_params and 'GET' not in methods):
            methods.append('GET')


        else:
            pass


        # if(response.css('form')):
        #     # for i in len(response.css('form')):
        #     # for i in
        #     # print response.css('form')
        #     value = response.css('form')[0].extract()
        #     form_values['form'] = value
        #     form_values['action'] = response.xpath('//form//@action').extract()
        #     form_values['form_method'] = response.xpath('//form//@method').extract()
        #     form_values['method'] = methods
        #     form_values['inputs'] = {'name': response.xpath('//form/input/@name').extract(), 'value': response.xpath('//form/input/@value').extract()}
        #     forms.append(form_values)
        # else:
        #     value = ''

        forms = []
        if(response.css('form')):
            # print len(response.css('form').extract())
            for i in range(len(response.css('form').extract())):

                form_values = {}


                value = response.css('form')[i].extract()
                action = response.xpath('//form//@action')[i].extract() if response.xpath('//form//@action') else ''
                method = response.xpath('//form[position()=0]').extract() if response.xpath('//form//@method') else ''


                inputs={}
                for j in range(len(response.xpath('//form/input/@name').extract())):


                    inputs_name = response.xpath('//form/input/@name')[j].extract() if response.xpath('//form/input/@name') else ''
                    inputs_value = response.xpath('//form/input/@value')[j].extract() if response.xpath('//form/input/@value') else ''
                    inputs[inputs_name] = inputs_value




                form_values['form'] = value
                form_values['action'] = action
                form_values['form_method'] = method
                form_values['overall_method'] = methods
                form_values['inputs'] = inputs
                # form_values['inputs'] = {'name': inputs_name if inputs_name else '', 'value': inputs_value if inputs_value else ''}
                forms.append(form_values)
        else:
            value = ''

        yield {
            "endpoint": parsed.path,
            "forms": forms,
            "url": response.url,
            "get_params": parsed.query,
            "post_params": post_params,
            "headers": response.headers,
            "cookies":response.headers.getlist('Set-Cookie'),
            "request": response.request,
            "get_post": methods,
            "meta": response.meta,
            "input_post_params": value

        }
