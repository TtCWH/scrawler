# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import requests
import os
from yoga.items import YogaItem
from scrapy.utils.project import get_project_settings

class YogaPipeline(object):
    def process_item(self, item, spider):
        settings=get_project_settings()
        url=item['url']
        content=requests.get(url,headers=settings['DEFAULT_REQUEST_HEADERS']).content
        if not os.path.exists(spider.result_dir):
        	os.mkdir(spider.result_dir)
        with open('{}/{}.{}'.format(spider.result_dir,item['title'],'jpg'),'wb') as f:
        	f.write(content)
        return item
