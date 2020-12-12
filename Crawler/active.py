"""
@author: NGWORKS-夏姬八彻
@contact: wl@ngworks.com
@version: 0.a1
@file: active2.py
@time: 2020/12/11   20:12
@detail: 【异步重写】通过传入的dynamic_id_list，批量获取、保存动态详情，下版本解决代理ip问题。
"""

import aiohttp,requests,asyncio,redis,json,time,sqlite3
from DB import *
from fuc import *
from requests.auth import HTTPBasicAuth

#全局变量
info_list = []
imglist = []

#API
def dynamic_history_new(dynamic_id,cookie,request_type):
    url = [
        "http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_history",
        "http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new",

    ]
    uid = cookie['DedeUserID']
    # proxy_dict = proxydict()
    # proxies = {
    #     'http':proxy_dict
    # }
    # proxy_auth = HTTPBasicAuth('NGWORKSPCI', 'b784262f85')
    params = [{'uid':uid,'type_list':268435455,'offset_dynamic_id':dynamic_id},{'uid':uid,'type_list':268435455,'current_dynamic_id':dynamic_id}]
    res = requests.get(url = url[request_type],params = params[request_type],cookies = cookie)
    data = json.loads(res.text)
    return data

#API
async def fetch(session,cookie,params,url_type,proxy_dict):
    url_list = [
        "http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail",       #获取动态详情
    ]
    url = url_list[url_type]
    proxy_auth = aiohttp.BasicAuth('NGWORKSPCI', 'b784262f85')
    async with session.get(url = url,params = params,cookies = cookie,proxy = proxy_dict,proxy_auth=proxy_auth) as response:
        res = await response.json()
        if res['code'] != 0:
            raise ValueError("api")
            print("代理ip被封禁，回调请求并更换ip")
            proxy_dict = proxydict()
            fetch(session,cookie,params,url_type,proxy_dict)

        dynamic_id = res['data']['card']['desc']['dynamic_id']
        type_orgin = res['data']['card']['desc']['type']
        rid = res['data']['card']['desc']['rid']
        dynamic_type( type_orgin , dynamic_id , rid ,res)
        
#动态分类器
def dynamic_type( type_orgin , dynamic_id , rid ,detail):
    ctime = detail['data']['card']['desc']['timestamp']
    data = json.loads(detail['data']['card']['card'])
    try:
        uid = detail['data']['card']['desc']['user_profile']['info']['uid']
        host = detail['data']['card']['desc']['user_profile']['info']['uname']
    except Exception:
        orgin_id = 0
        uid = 0
        host = "未知用户"
        
    orgin_id = 0
    if type_orgin == 1:
        oid = dynamic_id
        type = 17
        orgin_id = detail['data']['card']['desc']['orig_dy_id']

        description = data['item']['content']
    elif type_orgin == 2:
        oid = rid
        type = 11
        imgsrc = []
        pictureslist = data['item']['pictures']
        pictures_count = data['item']['pictures_count']
        i = 0
        while pictures_count > i:
            img = pictureslist[i]['img_src']
            pictures = img
            imgsrc.append(pictures)
            i+=1
        imglist.append((dynamic_id,oid,pictures_count,str(imgsrc)))
        description = data['item']['description']

    elif type_orgin == 4:
        oid = dynamic_id
        type = 17
        description = data['item']['content']

    elif type_orgin == 8:
        oid = rid
        type = 1
        description  = data['title']
        desc = data['desc']
    elif type_orgin == 64:
        oid = rid
        type = 12
        description  = str(data['title'])
    elif type_orgin == 4300:
        oid = rid
        type = 17
    elif type_orgin == 4200:
        pass
    elif type_orgin == 512:
        oid = rid
        type = 1
        description  = data['apiSeasonInfo']['title']
        host = "bilibili番剧"
    else:
        raise ValueError("不支持的动态类型")
    z_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))  #时间戳转换
    data = (dynamic_id,oid,orgin_id,type,description,host,uid,ctime,z_time)
    info_list.append(data)

    return oid,type

#抓取动态列表
def get_new_dynamic(dynamic_id,cookie):
    uid = cookie['DedeUserID']
    dynamic_id_list = []
    data1 = dynamic_history_new(dynamic_id,cookie,1)
    if data1['code'] != 0:
        print(data1['code'])
        raise ValueError("api出错")
    try:
        new_num = data1['data']['new_num']
        i = 0
        new_num = len(data1['data']['cards'])
    except Exception:
        raise ValueError("没有新动态")
    
    while i < new_num:
        dynamic_id_str = data1['data']['cards'][i]['desc']['dynamic_id']
        dynamic_id_list.append(dynamic_id_str)
        i+=1 
    if new_num > 19:
        try:
            listok = False
            while True:
                dynamic_id_last = dynamic_id_list[-1]
                data2 = dynamic_history_new(dynamic_id_last,cookie,0)
                i = 0
                new_num2 = len(data2['data']['cards'])
                while i < new_num2:
                    dynamic_id_str = data2['data']['cards'][i]['desc']['dynamic_id']
                    if int(dynamic_id_str) == int(dynamic_id):
                        print("找到了")
                        raise ValueError("找到了")
                    dynamic_id_list.append(dynamic_id_str)
                    i+=1
        except Exception:
            pass
    print(dynamic_id_list)
    return dynamic_id_list

#发请求，给task列表里添加
async def dynamic_detail(dynamic_id_list ,cookie):
    #connector=aiohttp.TCPConnector(verify_ssl=False),trust_env=True
    async with aiohttp.ClientSession() as session:
        proxy_dict = proxydict()
        tasks = [asyncio.create_task(fetch(session,cookie,{'dynamic_id':dynamic_id},0,str(proxy_dict))) for dynamic_id in dynamic_id_list]
        done,pending = await asyncio.wait(tasks)


#跑起来
def main(dynamic_id,cookie):
    dynamic_id_list = dynamic_id
    result = dynamic_detail(dynamic_id_list,cookie)
    #执行协程函数创建的协程对象时，协程函数内部的代码不会被执行，必须通过事件循环
    loop = asyncio.get_event_loop()
    loop.run_until_complete(result)

#提供参数，保存数据
def get_new_dynamic_all():
    try:
        cookie = Cookies()
        with SqliteDB('dynamic.db') as db:   
            sql = '''select * from inf where key = '%s' ''' % "dynamic_id" 
            query_set = db.execute(sql).fetchall()
            if len(query_set) > 0:
                dynamic_id = query_set[0][1]
            else:
                dynamic_id = input("储存中动态id失效，请指定新的起始id：")
            
            data = get_new_dynamic(dynamic_id,cookie)
            new_dynamic_id_db = data[0]
            main(data,cookie)
            tuple_info_list = tuple(info_list)
            tuple_imglist = tuple(imglist)

            db.execute("UPDATE inf SET value=? WHERE key=?", (new_dynamic_id_db,"dynamic_id")) 

            db.connection.executemany("INSERT INTO dynamic_host values(?,?,?,?,?,?,?,?,?)", tuple_info_list)

            db.connection.executemany("INSERT INTO dynamic_img values(?,?,?,?)", tuple_imglist)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    get_new_dynamic_all()
