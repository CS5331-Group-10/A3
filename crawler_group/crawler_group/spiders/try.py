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
import time


import os

class MyItem(Item):
    originalResponse = Field()
    param = Field()
    method = Field()
    value = Field()
    endpoint = Field()
    endpoints = Field()

class ExampleSpider(CrawlSpider):
    name = 'crawler_assignment_3'
    # start_urls = ['http://ec2-54-254-145-200.ap-southeast-1.compute.amazonaws.com:8080/']
    browser = webdriver.Firefox(executable_path='./geckodriver')
    browser.get('http://ec2-54-254-145-200.ap-southeast-1.compute.amazonaws.com:8081/')
    form_name = browser.find_element_by_name('username')
    form_password = browser.find_element_by_name('password')
    submit_query_btn = browser.find_element_by_xpath("//input[@value='Submit']")
    form_name.send_keys("morty")
    form_password.send_keys("QNKCDZO")
    # submit_query_btn.click().then(function(){
    #     webdriver.sleep(5);
    # })
    submit_query_btn.click();
    time.sleep(2);

    url_next_page = browser.find_element_by_link_text('Come on in.')

    url_next_page.click()
    # url_next_page.click().then(function(){
    #     console.log("weeee")
    # })
    current_url_to_continue =  browser.current_url
    print current_url_to_continue
    links = browser.find_elements_by_xpath("//a[@href]")
    for elem in links:
        print elem.get_attribute("href")
        # browser.get(elem.get_attribute("href"))
        # inner_link = browser.find_elements_by_xpath("//a[@href]")
        # for inner in inner_link:
        #     print inner.get_attribute("href")
    # print links
    # for link in links:
    #     print link.text
        # links.click()
        # other_urls = browser.current_url
        # print other_urls
    # links = browser.find_elements_by_css_selector('a')
    # print links
    browser.close()
    # for link_url in links:

    # start_urls = ['http://ec2-54-254-145-200.ap-southeast-1.compute.amazonaws.com:8081/secretclub.php']


##### Set scrapy rules to extract link ==> after which parse_url function will be run ####
    # rules = (Rule(LinkExtractor(),callback='parse_url', follow=True), )

    # def parse_url(self, response):
    #     selector = Selector(response)
    #     item = MyItem()
    #     value = ''
    #     parsed = urlparse(response.url)
    #
    #     endpoint_result = []
    #     #### Identify presence of cookies #####
    #     cookies = response.headers.getlist('Set-Cookie')
    #     if cookies:
    #         item['method'] = 'Cookie'
    #     else:
    #         pass
    #
    #     ##### Within each page, identify if there is presence of any href ####
    #     all_links = response.xpath('*//a/@href').extract()
    #     print all_links
    #     if all_links:
    #         list_form = []
    #
    #         for a in all_links:
    #
    #             item = MyItem()
    #             ### For those pages with href, we do a request again to hit the url
    #             # request =  response.follow(url=href, callback=self.parse_url)
    #             get_request_url  = response.url +a
    #
    #             ### Parsing of url query parameters to get the keys and values ####
    #             query_get_url = urlparse(get_request_url).query
    #             get_params_for_get_url = parse_qs(query_get_url).keys()
    #             get_values_for_get_url = parse_qs(query_get_url).values()
    #
    #
    #             if (get_params_for_get_url):
    #
    #                 endpoint = urlparse(get_request_url).path
    #
    #                 param = get_params_for_get_url
    #                 method = "GET"
    #                 item['endpoint'] = endpoint
    #                 item['param'] = param
    #                 item['method'] = method
    #                 item['value'] = get_values_for_get_url
    #                 list_form.append(item)
    #
    #             else:
    #                 return
    #
    #
    #         #### Identify presence of Form ==> not just limited to POST but also GET method ####
    #     elif(response.css('form')):
    #         endpoint =parsed.path
    #         item['endpoint'] = endpoint
    #         param = ['']
    #         method = ['']
    #         value = ['']
    #         list_form =[]
    #
    #         for form in (response.xpath('//form')):
    #             item = MyItem()
    #             endpoint =parsed.path
    #             item['endpoint'] = endpoint
    #             ### Extract method from form ###
    #             if (form.xpath('.//@method')):
    #                 method = form.xpath('.//@method')[0].extract()
    #                 item['method'] = method
    #             else:
    #                 item['method'] = 'GET'
    #             ### Extract action from form ###
    #             if (form.xpath('.//@action')):
    #                 actions = form.xpath('.//@action')[0].extract()
    #                 ### Special handling of action attribute to include folder directory ###
    #                 if (actions[0:5] != "https" and actions[0:5] != "http:"):
    #                     folder = endpoint.split('/')
    #                     folder = "/".join(folder[0:len(folder)-1])
    #                     actions = folder+"/"+actions
    #                 ### If actions present, endpoint will be set to where the form action points to ###
    #                 item['endpoint'] = actions
    #             else:
    #                 pass
    #             ### Extract input from form useful for exploits ####
    #             if(form.xpath('.//input')):
    #                 form_params = []
    #                 form_values = []
    #                 for form_inputs in form.xpath('.//input'):
    #                     ### Extract hidden inputs in the form ####
    #                     if (form_inputs.xpath('.//@type').extract() ==[u'hidden']):
    #                         ### Name attribute and Value attribute from the inputs attribute of the form
    #                         ### are useful for attacks ####
    #                         form_name = form_inputs.xpath('.//@name').extract()
    #
    #                         form_name = form_name[0] + "_hiddenPEST"
    #                         form_value = form_inputs.xpath('.//@value').extract()
    #                         form_value = form_value[0]
    #                         form_params.append(form_name)
    #                         form_values.append(form_value)
    #                     elif (form_inputs.xpath('.//@type').extract() ==[u'text']):
    #                         form_name = form_inputs.xpath('.//@name').extract()[0] if form_inputs.xpath('.//@name').extract() else ''
    #                         form_value = form_inputs.xpath('.//@value').extract()[0] if form_inputs.xpath('.//@value').extract() else ''
    #                         form_params.append(form_name)
    #                         form_values.append(form_value)
    #                     else:
    #                         pass
    #
    #                 item['param'] = form_params
    #                 item['value'] = form_values
    #
    #
    #
    #             list_form.append(item)
    #
    #     else:
    #         return
    #
    #
    #     # yield{
    #     #     "endpoints": list_form
    #     # }
