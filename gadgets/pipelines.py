# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
import json

class GadgetsPipeline(object):


    def __init__(self):
        self.rc = redis.Redis(host='127.0.0.1')

    def process_item(self, item, spider):
        gagets_mobile_list = json.loads(self.rc.get("gadgets_mobile_list"))
        if item["title"] not in gagets_mobile_list:
            gagets_mobile_list.append([item["title"], hash(item["title"])])
            self.rc.set("gadgets_mobile_list", json.dumps(gagets_mobile_list))
        self.rc.set(hash(item["title"]), json.dumps(dict(item))) 
        return item




