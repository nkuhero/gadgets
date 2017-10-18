#coding=utf-8
import web
import json
import urllib2
import time
import datetime
import redis



urls = (
    '/gadgets/list', 'list',
    '/gadgets/info', 'info',
)


rc = redis.Redis(host='127.0.0.1')

class list:
    def GET(self):
        li = rc.get("gadgets_mobile_list")
        li = json.loads(li)
        return json.dumps(li)


class info:
    def GET(self):
        i =  web.input()
        id = i.id 
        li = rc.get(id)
        li = json.loads(li)
        return json.dumps(li)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
