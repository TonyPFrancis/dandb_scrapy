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