#!/bin/sh
scrapy runspider scrapper.py -t json -o - > "result.json"
