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
        content = response.xpath('//div[@id="center_content_div"]/div/p')
        content_list = []
        for c in content:
            if c.xpath(".//span/img"):
                img_src = c.xpath(".//span/img/@src").extract()[0]
                img_info = {"type" : "img", "val" : img_src}
                content_list.append(img_info)
            else:
                if c.xpath(".//text()").extract():
                    text = c.xpath(".//text()").extract()[0]
                    text = drop_tags.sub('', text) 
                    text_info = {"type" : "text", "val" : text} 
                    content_list.append(text_info)
        review = response.xpath('//div[@class="pw_detail"]/div/ul/li')
        review_info = {"rating" : {}, "good" : [], "bad" : []}
        for r in review:
            key = r.xpath(".//span/text()").extract()[0]
            text = r.xpath(".//i").extract()[0]
            m = re.search(r"rating(.*?)\"", text)
            if m:
                val = m.group(1)
            review_info["rating"][key] = val
        good = response.xpath('//div[@class="pd_quality"]/ul[@class="good"]/li/text()').extract()[1:]
        bad = response.xpath('//div[@class="pd_quality"]/ul[@class="bad"]/li/text()').extract()[1:] 
        review_info["good"] = good
        review_info["bad"] = bad
        keySpecs = {}
        keySpecs_info = response.xpath('//div[@class="pw_detail"]/div[@class="pd_cont"]/div[@class="pd_colmn"]')
   
        for k in keySpecs_info:
            key = k.xpath(".//h4/text()").extract()[0]
            val = k.xpath(".//span/text()").extract()[0]
            keySpecs[key] = val
            
        yield GadgetsItem(title=title, mainPic=mainPic, highlights=highlights, desc=desc, content=content_list, review=review_info, keySpecs=keySpecs)
        print "========================", title, "========================"
        print mainPic
