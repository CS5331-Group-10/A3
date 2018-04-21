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
    param = Field()
    method = Field()
    value = Field()
    endpoint = Field()
    endpoints = Field()
    # url= Field()
    # get_params = Field()
    # post_params = Field()
    # headers = Field()
    # resquest = Field()
    # cookies = Field()
    # meta = Field()
    # raw_html = Field()
    # input_post_params = Field()
    # html_url = Field()
    # get_post = Field()
    # action_url = Field()
    # forms = Field()
    # get_url = Field()
    # endpoint_result = Field()


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
        # item['originalResponse'] = response.url
        # print "hahhaha"
        # print response
        parsed = urlparse(response.url)
        endpoint_result = []

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

                    # print "IN GET"
                    # print response
                    # print "IN GET DONE"
                    # print get_request_url
                    # print get_params_for_get_url
                    endpoint = urlparse(get_request_url).path

                    param = get_params_for_get_url
                    method = "GET"
                    item['endpoint'] = endpoint
                    item['param'] = param
                    item['method'] = method
                    # return item
                    # endpoint_result.append(
                    #     {
                    #     'endpoint' : endpoint,
                    #     'param' : param,
                    #     'method' : method
                    #     }
                    # )

                    # yield{
                    #      "endpoint": endpoint,
                    #     "param": param,
                    #     "get_post" : method
                    # }
                else:
                    return
            # print "WTH"

        elif(response.css('form')):
            endpoint =parsed.path
            item['endpoint'] = endpoint
            param = ''
            method = ''
            value = ''
            list_form =[]
            # print response.xpath('//form')
            for form in (response.xpath('//form')):

                for form_method in form.xpath('.//@method'):
                    method = form_method.extract()
                    item['method'] = method
                # Handle action methods ###
                if (form.xpath('.//@action')):
                    actions = form.xpath('.//@action')[0].extract()
                    endpoint = actions
                    item['endpoint'] = endpoint
                else:
                    pass


                if (form.xpath('.//input//@name')):
                    post_params = form.xpath('.//input//@name').extract()
                    param = post_params
                    item['param'] = param
                else:
                    item['param'] = ''
                if (form.xpath('.//input/@value')):
                    value = form.xpath('.//input/@value').extract()
                    item['value'] = value
                else:
                    item['value'] = ''



                list_form.append(item)
            item = list_form
            # return list_form
                # print item
                # return list_form
                # endpoint_result.append({
                #     'endpoint' : endpoint,
                #     'param' : param,
                #     'method' : form_method_type,
                #     'value' : value
                #     }
                # )


            #
            #
            # ## HANDLING GET_PARAMS FROM CURRENT RESPONSE.URL
            # query = urlparse(response.url).query
            # get_params = parse_qs(query).keys()
            # ### TO BE REMOVED
            #
            # ### See if there is a GET request ###
            # get_post_value = []
            # request = response.request
            #
            # if (get_params or 'GET' in value):
            #     get_post_value.append('GET')
            #     if ('POST' in value):
            #         get_post_value.append('POST')
            #     else:
            #         pass
            # elif ('POST' in value):
            #     get_post_value.append('POST')
            # else:
            #     pass
            #
            # methods = response.xpath('//form//@method').extract()
            #
            # ##handling post_params:
            # post_params = response.xpath('//form//input//@name').extract()
            #
            #
            # if (get_params and 'GET' not in methods):
            #     methods.append('GET')
            #
            #
            # else:
            #     pass
            #



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

            # forms = []
            # if(response.css('form')):
            #     # print len(response.css('form').extract())
            #     for i in range(len(response.css('form').extract())):
            #
            #         form_values = {}
            #
            #
            #         value = response.css('form')[i].extract()
            #         action = response.xpath('//form//@action')[i].extract() if response.xpath('//form//@action') else ''
            #         method = response.xpath('//form[position()=0]').extract() if response.xpath('//form//@method') else ''
            #
            #
            #         inputs={}
            #         for j in range(len(response.xpath('//form/input/@name').extract())):
            #
            #
            #             inputs_name = response.xpath('//form/input/@name')[j].extract() if response.xpath('//form/input/@name') else ''
            #             inputs_value = response.xpath('//form/input/@value')[j].extract() if response.xpath('//form/input/@value') else ''
            #             inputs[inputs_name] = inputs_value
            #
            #
            #
            #         #
            #         # form_values['form'] = value
            #         # form_values['action'] = action
            #         # form_values['form_method'] = method
            #         # form_values['overall_method'] = methods
            #         # form_values['inputs'] = inputs
            #         # form_values['inputs'] = {'name': inputs_name if inputs_name else '', 'value': inputs_value if inputs_value else ''}
            #         forms.append(form_values)
            # else:
            #     value = ''

            ### PARAMS #########


            # yield{
            #      "endpoint": endpoint,
            #     "param": param,
            #     "get_post" : method
            # }
        else:
            # endpoint = ""
            # param = ""
            # method = ""

            return


            # print "in ELSE"
            # print response
            # print "in end of  ELSE"



            ####################
            # yield {
            #     "endpoint": parsed.path,
            #     "forms": forms,
            #     "url": response.url,
            #     "post_params": post_params,
            #     "headers": response.headers,
            #     "cookies":response.headers.getlist('Set-Cookie'),
            #     "request": response.request,
            #     "get_post": methods,
            #     "meta": response.meta,
            #     "input_post_params": value
            #     # "get_url" : get_url,
            #     # "get_params": get_params_for_get_url
            #
            # }
        yield{
            "endpoints": item
        }

        # yield {
        #     "endpoint_result" : endpoint_result
        #     # "endpoint": endpoint,
        #     # "param": param,
        #     # "get_post" : method
        #
        #     # "param": param
        #     # "endpoint": parsed.path
        #     # "forms": forms,
        #     # "url": response.url,
        #     # "post_params": post_params,
        #     # "headers": response.headers,
        #     # "cookies":response.headers.getlist('Set-Cookie'),
        #     # "request": response.request,
        #     # "get_post": methods,
        #     # "meta": response.meta,
        #     # "input_post_params": value
        #
        #     # "get_url" : get_url,
        #     # "get_params": get_params_for_get_url
        #
        # }
