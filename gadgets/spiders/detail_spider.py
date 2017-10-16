import scrapy
import redis
import json
import re
from gadgets.items import GadgetsItem 


rc = redis.Redis(host='127.0.0.1')

class DetailSpider(scrapy.Spider):
    name = "detail"
    allowed_domains = ["gadgets.ndtv.com"]
    start_urls = json.loads(rc.get("mobile_url_list"))
     
    def parse(self, response):
        title = response.xpath('//span[@id="ContentPlaceHolder1_FullstoryCtrl_Stitle"]/text()').extract()[0]
        mainPic = response.xpath('//div[@class="fullstoryImage"]/img/@src').extract()[0] 
        highlights = response.xpath('//ul[@class="newins_lhs_highlights"]/li/text()').extract()
        drop_tags = re.compile(r'<[^>]+>',re.S)
        desc = response.xpath('//div[@class="content_text row description"]/p').extract()[0]
        desc = drop_tags.sub('', desc)
        yield GadgetsItem(title=title, mainPic=mainPic, highlights=highlights, desc=desc)
        print "========================", title, "========================"
        print mainPic
