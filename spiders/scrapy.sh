#!/bin/sh
scrapy runspider scrapper_selenium.py -t json -o - > "../result.json"
