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
from scrapy_splash import SplashRequest
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
    start_urls = ['http://target.com/']
    custom_settings = {'REDRIRECT_ENABLED' : False }
    # start_urls = ['file:///home/cs5331/Desktop/A3/tutorial/tutorial/spiders/sample.html']
    def start_requests(self):
        for url in self.start_urls:
            # yield SplashRequest(url, args={'wait': 0.5})
            yield SplashRequest(url, dont_process_response=True, args={'wait': 0.5})


    rules = (Rule(LinkExtractor(),  callback='parse_url',process_request = 'start_requests' , follow=True), )
    # rules = (Rule(LinkExtractor(),callback='parse_url', follow=True), )


    def splash_request(self, request):
        yield SplashRequest(url=request.url, dont_process_response=True, args={'wait': 0.5}, meta={'real_url': request.url})

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
        # print all_links
        if all_links:
            list_form = []

            for href in all_links:
                item = MyItem()
                request =  response.follow(url=href, callback=self.parse_url)

                # request.meta['from'] = response.url

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

            # print "WTH"
            # item = list_get

        elif(response.css('form')):
            endpoint =parsed.path
            item['endpoint'] = endpoint
            param = ['']
            method = ['']
            value = ['']
            list_form =[]
            # print response.xpath('//form')
            for form in (response.xpath('//form')):
                item = MyItem()
                endpoint =parsed.path
                item['endpoint'] = endpoint
                if (form.xpath('.//@method')):
                    method = form.xpath('.//@method')[0].extract()
                    item['method'] = method
                else:
                    item['method'] = 'GET'
                # for form_method in form.xpath('.//@method'):
                #     method = form_method.extract()
                #     item['method'] = method
                # Handle action methods ###
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
                        # print form_inputs.xpath('.//@type').extract()
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

                # if (form.xpath('.//input//@name')):
                #     post_params = form.xpath('.//input//@name').extract()
                #     param = post_params
                #     item['param'] = param
                # else:
                #     item['param'] = ['']
                # if (form.xpath('.//input/@value')):
                #     value = form.xpath('.//input/@value').extract()
                #     item['value'] = value
                # else:
                #     item['value'] = ['']



                list_form.append(item)
            # item = list_form
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
            "endpoints": list_form
        }
        # yield SplashRequest(
        #     'http://target.com/',
        #     endpoint='sqli/javascript.html',
        #     # args={'js_source': 'document.title="My Title";'},
        # )
##################SCRAPY SPLASH ##################################
        # yield SplashRequest(url, self.parse_result,
        #     args={
        #         # optional; parameters passed to Splash HTTP API
        #         'wait': 0.5,
        #
        #         # 'url' is prefilled from request url
        #         # 'http_method' is set to 'POST' for POST requests
        #         # 'body' is set to request body for POST requests
        #     },
        #     endpoint='javascript.html', # optional; default is render.html
        #     # splash_url='<url>',     # optional; overrides SPLASH_URL
        #     slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
        # )








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
