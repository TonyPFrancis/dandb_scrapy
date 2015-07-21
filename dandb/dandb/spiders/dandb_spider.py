# -*- coding: utf-8 -*-
from apt.utils import get_maintenance_end_date
import re
import requests
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urlparse import urlparse, urljoin, parse_qs
from scrapy.selector import Selector
from time import sleep
import urllib
from dandb.items import DandbItem
from scrapy.http import Request
from dateutil import rrule, parser
from dateutil import relativedelta
from datetime import timedelta, datetime
from scrapy.log import ScrapyFileLogObserver
from scrapy import log
from scrapy.shell import inspect_response
import time
import json

class DandbSpider(Spider):
    name = 'dandb'
    start_urls = ['https://www.dandb.com', ]
    allowed_domains = ['dandb.com', ]
    TIMEZONE = ''
    BASE_URL = 'https://www.dandb.com'
    HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'}

    def __init__(self, name=None, **kwargs):
        ScrapyFileLogObserver(open("spider.log", 'w'), level=log.INFO).start()
        ScrapyFileLogObserver(open("spider_error.log", 'w'), level=log.ERROR).start()
        super(DandbSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        sel = Selector(response)

        search_url = 'https://www.dandb.com/businessdirectory/search/?keyword=Enter+business+name%2C+phone%2C+or+DUNS'
        yield Request(url=search_url, headers=self.HEADERS, callback=self.parse_search)

    def parse_search(self, response):
        sel = Selector(response)

        HEADERS = self.HEADERS
        HEADERS['Cookie'] = response.headers['Set-Cookie']

        BUSINESS_LINKS_XPATH = '//div[@class="result_sec"]/a[@data-rank]/@href'

        business_links = sel.xpath('//div[@class="result_sec"]/a[@data-rank]/@href').extract()
        if business_links:
            for business_link in business_links:
                business_link = (business_link if business_link.startswith('http') else self.BASE_URL+business_link) if business_link else ''
                sleep(5)
                yield Request(url=business_link, dont_filter=True, headers=HEADERS, callback=self.parse_business)
        else:
            return

    def parse_business(self, response):
        sel = Selector(response)

        BUSINESS_NAME_XPATH = '//section[@class="midd_sec"]/section[@class="box basic_info_box"]//h3/text()'
        STREET_XPATH = '//section[@class="midd_sec"]/section[@class="box basic_info_box"]//p[@class="address"]/span[@class="address_street"]/text()'
        CITY_XPATH = '//section[@class="midd_sec"]/section[@class="box basic_info_box"]//p[@class="address"]/span[@class="address_city"]/text()'
        STATE_XPATH = '//section[@class="midd_sec"]/section[@class="box basic_info_box"]//p[@class="address"]/span[@class="address_state"]/text()'
        ZIP_XPATH = '//section[@class="midd_sec"]/section[@class="box basic_info_box"]//p[@class="address"]/span[@class="address_zip"]/text()'
        PHONE_XPATH = '//section[@class="midd_sec"]/section[@class="box basic_info_box"]//a[@class="tel"]/text()'
        URL_XPATH = '//section[@class="midd_sec"]/section[@class="box basic_info_box"]//a[@class="web"]/@href'
        EMAIL_XPATH = '//section[@class="midd_sec"]/section[@class="box basic_info_box"]//a[starts-with(@href,"mailto:")]/@href'
        FOUNDED_XPATH = '//section[@class="midd_sec"]/section[@class="box"]//ul[@class="list "]/li[contains(text(),"Founded")]/span/text()'
        INCORPORATED_XPATH = '//section[@class="midd_sec"]/section[@class="box"]//ul[@class="list "]/li[contains(text(),"Incorporated")]/span/text()'
        REVENUE_XPATH = '//section[@class="midd_sec"]/section[@class="box"]//ul[@class="list "]/li[contains(text(),"Revenue")]/span/text()'
        EMPLOYEE_XPATH = '//section[@class="midd_sec"]/section[@class="box"]//ul[@class="list "]/li[contains(text(),"Employee Count")]/span/text()'
        INDUSTRIES_XPATH = '//section[@class="midd_sec"]/section[@class="box"]//ul[@class="list "]/li[contains(text(),"Industries")]/span/text()'
        CONTACT_XPATH = '//section[@class="midd_sec"]/section[@class="box"]//ul[@class="list "]/li[contains(text(),"Contacts")]/span/text()'

        business_url = response.url
        business_name = sel.xpath(BUSINESS_NAME_XPATH).extract()
        business_name = business_name[0].strip() if business_name else ''
        street = sel.xpath(STREET_XPATH).extract()
        street = street[0].strip() if street else ''
        city = sel.xpath(CITY_XPATH).extract()
        city = city[0].strip() if city else ''
        state = sel.xpath(STATE_XPATH).extract()
        state = state[0].strip() if state else ''
        zip = sel.xpath(ZIP_XPATH).extract()
        zip = zip[0].strip() if zip else ''
        phone = sel.xpath(PHONE_XPATH).extract()
        phone = phone[0].strip() if phone else ''
        url = sel.xpath(URL_XPATH).extract()
        url = url[0].strip() if url else ''
        email = sel.xpath(EMAIL_XPATH).extract()
        email = email[0].lstrip('mailto:').strip() if email else ''
        founded = sel.xpath(FOUNDED_XPATH).extract()
        founded = founded[0].strip() if founded else ''
        incorporated = sel.xpath(INCORPORATED_XPATH).extract()
        incorporated = incorporated[0].strip() if incorporated else ''
        revenue = sel.xpath(REVENUE_XPATH).extract()
        revenue = revenue[0].strip() if revenue else ''
        employee = sel.xpath(EMPLOYEE_XPATH).extract()
        employee = employee[0].strip() if employee else ''
        industries = sel.xpath(INDUSTRIES_XPATH).extract()
        industries = industries[0].strip() if industries else ''
