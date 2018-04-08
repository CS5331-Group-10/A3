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
    response = Field()
    resquest = Field()
    cookies = Field()
    meta = Field()
    raw_html = Field()



class ExampleSpider(CrawlSpider):
    name = 'crawler_assignment'
    start_urls = ['http://target.com']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True), )

    def parse_url(self, response):
        item = MyItem()
        item['originalResponse'] = response.url
        parsed = urlparse(response.url)

        soup = BeautifulSoup(response.text, 'html.parser').findAll('input')

        yield {
            "url": response.url,
            "query": parsed.query,
            "endpoint": parsed.path,
            "response": response.headers,
            "cookies":response.headers.getlist('Set-Cookie'),
            "request": response.request,
            "meta": response.meta,
            "raw_html": response.text


            # session.cookies.get_dict()

        }
        # return item
