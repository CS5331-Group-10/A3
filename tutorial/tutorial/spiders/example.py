from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from urlparse import urlparse
from bs4 import BeautifulSoup


class MyItem(Item):
    originalResponse = Field()
    url= Field()
    endpoint = Field()
    query = Field()

class ExampleSpider(CrawlSpider):
    name = 'crawler_assignment'
    start_urls = ['http://target.com']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True), )

    def parse_url(self, response):
        item = MyItem()
        item['originalResponse'] = response.url
        parsed = urlparse(response.url)

        soup = BeautifulSoup(response.text, 'lxml')
        yield {
            "url": response.url,
            "query": parsed.query,
            "endpoint": parsed.path
        }
        # return item
