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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import scrapy
# from urlparse import  parse

import os

class MyItem(Item):
    originalResponse = Field()
    param = Field()
    method = Field()
    value = Field()
    endpoint = Field()
    endpoints = Field()



class ExampleSpider(CrawlSpider):
    name = 'crawler_assignment'
    # start_urls = ['http://target.com/']
    # start_urls = ['http://target.com/sqli/javascript.html']
    custom_settings = {'REDRIRECT_ENABLED' : False }
    # start_urls = ['file:///home/cs5331/Desktop/A3/tutorial/tutorial/spiders/sample.html']


##########SELENIUM ##########


    browser = webdriver.Firefox(executable_path='./geckodriver')
    browser.get('http://target.com/sqli/javascript.html')
    form_val = browser.find_element_by_id('username')
    submit_query_btn = browser.find_element_by_id('submit')

    form_val.send_keys("hahhaa")
    submit_query_btn.click()
    browser.close()

##########SELENIUM ##########

    # rules = (Rule(LinkExtractor(),callback='parse_url', follow=True), )

    def parse_url(self, response):

        selector = Selector(response)
        item = MyItem()
        value = ''
        parsed = urlparse(response.url)
        endpoint_result = []

        cookies = response.headers.getlist('Set-Cookie')
        if cookies:
            item['method'] = 'Cookie'
        else:
            pass

        ### ALL THE GET URL #####
        all_links = response.xpath('*//a/@href').extract()

        if all_links:
            list_form = []

            for href in all_links:
                item = MyItem()
                request =  response.follow(url=href, callback=self.parse_url)



                get_request_url  = request.url
                query_get_url = urlparse(get_request_url).query
                get_params_for_get_url = parse_qs(query_get_url).keys()
                get_values_for_get_url = parse_qs(query_get_url).values()


                if (get_params_for_get_url):

                    endpoint = urlparse(get_request_url).path

                    param = get_params_for_get_url
                    method = "GET"
                    item['endpoint'] = endpoint
                    item['param'] = param
                    item['method'] = method
                    item['value'] = get_values_for_get_url
                    list_form.append(item)

                else:
                    return

        elif(response.css('form')):
            endpoint =parsed.path
            item['endpoint'] = endpoint
            param = ['']
            method = ['']
            value = ['']
            list_form =[]

            for form in (response.xpath('//form')):
                item = MyItem()
                endpoint =parsed.path
                item['endpoint'] = endpoint
                if (form.xpath('.//@method')):
                    method = form.xpath('.//@method')[0].extract()
                    item['method'] = method
                else:
                    item['method'] = 'GET'

                if (form.xpath('.//@action')):
                    actions = form.xpath('.//@action')[0].extract()
                    if (actions[0:5] != "https" and actions[0:5] != "http:"):
                        folder = endpoint.split('/')
                        folder = "/".join(folder[0:len(folder)-1])
                        actions = folder+"/"+actions
                    item['endpoint'] = actions
                else:
                    pass

                if(form.xpath('.//input')):
                    form_params = []
                    form_values = []
                    for form_inputs in form.xpath('.//input'):

                        if (form_inputs.xpath('.//@type').extract() ==[u'hidden']):

                            form_name = form_inputs.xpath('.//@name').extract()

                            form_name = form_name[0] + "_hiddenPEST"
                            form_value = form_inputs.xpath('.//@value').extract()
                            form_value = form_value[0]
                            form_params.append(form_name)
                            form_values.append(form_value)
                        elif (form_inputs.xpath('.//@type').extract() ==[u'text']):
                            form_name = form_inputs.xpath('.//@name').extract()[0] if form_inputs.xpath('.//@name').extract() else ''
                            form_value = form_inputs.xpath('.//@value').extract()[0] if form_inputs.xpath('.//@value').extract() else ''
                            form_params.append(form_name)
                            form_values.append(form_value)
                        else:
                            pass

                    item['param'] = form_params
                    item['value'] = form_values



                list_form.append(item)

        else:
            return


        yield{
            "endpoints": list_form
        }
