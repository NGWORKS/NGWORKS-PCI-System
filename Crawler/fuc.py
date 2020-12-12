"""
@author: NGWORKS-夏姬八彻
@contact: wl@ngworks.com
@version: 0.a1
@file: fuc.py
@time: 2020/12/12   22:39
@detail: 常用的函数。
"""
import redis,json,requests
#获取新的代理ip
def proxydict():
    url = "http://httpapi.91vps.com/api/getips?num=1&proxyType=http&dataType=json&username=NGWORKSPCI&po=A16077452933228028&auth=key&key=b784262f85"
    res = requests.get(url=url).json()
    ip = res['data'][0]['connip']
    port = res['data'][0]['port']
    ip_src = "http://" + str(ip) + ":" + str(port)
    data = ip_src
    print(res)
    return data

#代理ip池（返回一定数量的代理ip）

#cookie
def Cookies():
    try:
        redis_b = redis.StrictRedis(host = 'localhost', port = 6379, db = 2)
    except Exception:
        raise IOError("Redis连接错误")

    try:
        print("获取cookie")
        DedeUserID = redis_b.get('DedeUserID')
        DedeUserID__ckMd5 = redis_b.get('DedeUserID__ckMd5')
        SESSDATA = redis_b.get('SESSDATA')
        bili_jct = redis_b.get('bili_jct')
        sid = redis_b.get('sid')
        #redis中拿出的数据是bytes，要decode,人都傻了，草
        data = {
            'DedeUserID':DedeUserID.decode() ,
            'DedeUserID__ckMd5':DedeUserID__ckMd5.decode() ,
            'SESSDATA':SESSDATA.decode() ,
            'bili_jct':bili_jct.decode() ,
            'sid':sid.decode() ,
            }
        return data
    except Exception:
        raise LookupError("登录过期，请重新登录")

#cookie池（返回一定数量的B站cookie）