from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from urlparse import urlparse
from bs4 import BeautifulSoup
import requests


class MyItem(Item):
    originalResponse = Field()
    url= Field()
    endpoint = Field()
    query = Field()
    rawHtml = Field()
    requestCookies = Field()
    


class MySpider(CrawlSpider):
    name = 'target.com'
    start_urls = ['http://target.com']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True), )
    
    def parse_url(self, response):
        item = MyItem()
        item['originalResponse'] = response.url
        #parsed = urlparse(response.url)
        #item['url'] = parsed.netloc
        #item['endpoint'] = parsed.path
        #item['query'] = parsed.query
	
        request = requests.get(response.url)
        soup = BeautifulSoup(request.text)   
        for input in soup.find_all('input'):
           if input['type'] =='submit':
              continue
           item['rawHtml'] = input.get('name')
        return item


