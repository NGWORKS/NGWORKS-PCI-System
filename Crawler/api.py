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

def dynamic_new(dynamic_id):
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new"
    cookie = BCookies()
    uid = cookie['DedeUserID']
    params = {
        'uid':uid,
        'type_list':268435455,
        'current_dynamic_id':dynamic_id
    }
    res = requests.get(url=url,params=params,cookies =cookie)
    data = json.loads(res.text)
    return data

def dynamic_history(dynamic_id):
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_history"
    cookie = BCookies()
    uid = cookie['DedeUserID']
    params = {
        'uid':uid,
        'type_list':268435455,
        'offset_dynamic_id':dynamic_id
    }
    res = requests.get(url=url,params=params,cookies =cookie)
    data = json.loads(res.text)
    return data

def get_dynamic_detail(sid):
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail"
    params = {
        'dynamic_id':sid
    }
    cookie = BCookies()
    res = requests.get(url=url,params=params,cookies =cookie)
    data = json.loads(res.text)
    return data

def mov_info(aid):
    url = "http://api.bilibili.com/x/web-interface/view"
    params = {
        'aid':id
    }
    cookie = BCookies()
    res = requests.get(url=url,params=params,cookies =cookie)
    data = json.loads(res.text)
    return data