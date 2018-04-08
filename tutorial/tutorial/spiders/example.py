from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from urlparse import urlparse
from bs4 import BeautifulSoup
import requests
from scrapy.selector import Selector

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



class ExampleSpider(CrawlSpider):
    name = 'crawler_assignment'
    start_urls = ['http://target.com']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True), )

    def parse_url(self, response):
        selector = Selector(response)
        item = MyItem()
        item['originalResponse'] = response.url
        parsed = urlparse(response.url)

        soup = BeautifulSoup(response.text, 'html.parser').findAll('input')

        yield {
            "url": response.url,
            "query": parsed.query,
            "endpoint": parsed.path,
            "headers": response.headers,
            "cookies":response.headers.getlist('Set-Cookie'),
            "request": response.request,
            "meta": response.meta,
            "input_post_params": response.css('input')[0].extract()


        }
        # return item
