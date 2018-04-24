#!/bin/sh
scrapy runspider example.py -t json -o - > "../result.json"
# scrapy crawl scrapper
