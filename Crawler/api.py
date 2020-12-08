from function import *
import requests
import json


def reply(type,oid,pn):
    url = "http://api.bilibili.com/x/v2/reply"
    params = {
        'type':type,
        'oid':oid,
        'ps':49,  #项目数
        'pn':pn,   #页码
    }
    cookie = BCookies()
    res = requests.get(url=url,params=params,cookies =cookie)
    data = json.loads(res.text)
    return data

def replyson(type,oid,root,pn,ps):
    url = "https://api.bilibili.com/x/v2/reply/reply"
    params = {
        'type':type,
        'oid':oid,
        'root':root, #父级rpid
        'ps':ps,  #项目数
        'pn':pn,   #页码
    }
    cookie = BCookies()
    res = requests.get(url=url,params=params,cookies =cookie)
    data = json.loads(res.text)
    return data