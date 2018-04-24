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
from selenium.webdriver.firefox.options import Options
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



##########SELENIUM ##########
    #http://target.com/sqli/javascript2.html
    #http://target.com/sqli/javascript3.html
    #http://target.com/sqli/dynamic.php
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=options, executable_path='./geckodriver')
    url = 'http://target.com/serverside/rfi.php'
    browser.get(url)

    all_links = browser.find_elements_by_xpath('*//a')
    print all_links
    if all_links:
        list_form = []

        for href in all_links:
            item = MyItem()
            ### For those pages with href, we do a request again to hit the url
            request =  response.follow(url=href, callback=self.parse_url)
            get_request_url  = request.url
            ### Parsing of url query parameters to get the keys and values ####
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
                pass

    # value= browser.find_elements_by_xpath('//form//input')
    # print value
    # for input in value:
    #     #print attribute name of each input element
    #     print input.get_attribute('name')
    # print value
    # browser.close()
    # browser = webdriver.Firefox(executable_path='./geckodriver')
    # value = browser.get('http://target.com/sqli/dynamic.php')
    # result = parse_url(self, value)
    # print result
    # print "hahahhahahahh"
    # form_val = browser.find_element_by_id('username')
    # submit_query_btn = browser.find_element_by_id('submit')
    #
    # form_val.send_keys("hahhaa")
    # submit_query_btn.click()
    # browser.close()

##########SELENIUM ##########
