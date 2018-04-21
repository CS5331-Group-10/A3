from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from urlparse import urlparse
from urlparse import parse_qs
# import urllib
# from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from scrapy.selector import Selector
import re
# import scrapy
# from urlparse import  parse

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
    get_url = Field()



class ExampleSpider(CrawlSpider):
    name = 'crawler_assignment'
    start_urls = ['http://target.com']
    custom_settings = {'REDRIRECT_ENABLED' : False }
    # start_urls = ['file:///home/cs5331/Desktop/A3/tutorial/tutorial/spiders/sample.html']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True), )


    def parse_url(self, response):
        selector = Selector(response)
        item = MyItem()
        value = ''
        item['originalResponse'] = response.url
        # print "hahhaha"
        # print response
        parsed = urlparse(response.url)


        ### ALL THE GET URL #####
        all_links = response.xpath('*//a/@href').extract()
        # print all_links
        if all_links:


            for href in all_links:
                request =  response.follow(url=href, callback=self.parse_url)

                # request.meta['from'] = response.url

                get_request_url  = request.url
                query_get_url = urlparse(get_request_url).query
                get_params_for_get_url = parse_qs(query_get_url).keys()



                if (get_params_for_get_url):
                    # print "INSIDE"

                    print get_request_url
                    print get_params_for_get_url


                else:
                    pass
            # print "WTH"

        else:

            # print "KNS"



        # Handle action methods ###
            actions = response.xpath('//form//@action/text').extract()


            ## HANDLING GET_PARAMS FROM CURRENT RESPONSE.URL
            query = urlparse(response.url).query
            get_params = parse_qs(query).keys()
            ### TO BE REMOVED

            ### See if there is a GET request ###
            get_post_value = []
            request = response.request

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
                "post_params": post_params,
                "headers": response.headers,
                "cookies":response.headers.getlist('Set-Cookie'),
                "request": response.request,
                "get_post": methods,
                "meta": response.meta,
                "input_post_params": value
                # "get_url" : get_url,
                # "get_params": get_params_for_get_url

            }
