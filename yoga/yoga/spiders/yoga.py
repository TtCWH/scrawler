# -*- coding: utf-8 -*-
import time
import json
import scrapy
from scrapy.shell import inspect_response
from yoga.items import YogaItem
from yoga.pipelines import YogaPipeline
_META_VERSION = 'v1.0'


class YogaSpider(scrapy.Spider):
    name = "yoga"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {
            'yoga.pipelines.YogaPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        reqs = []
        url = 'http://www.jpmsg.com/meinv/tieshenyundongku.html'
        reqs.append(scrapy.Request(url))
        self.logger.info('total {}'.format(len(reqs)))
        return reqs

    def parse(self, response):
        # inspect_response(response, self)
        # self.logger.info('now {}'.format(response.meta['index']))
        for url in response.xpath(
                './/div[@class="presently_li"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_info)

    def parse_info(self, response):
        # inspect_response(response, self)
        self.logger.info('now {}'.format(response.url))
        info=response.xpath('.//div[@id="MyContent"]//img')
        for i in range(len(info)):
            elem=info[i]
            item=YogaItem()
            item['url']=elem.xpath('./@src').extract_first()
            item['title']=elem.xpath('./@alt').extract_first()+str(i)
            yield item
