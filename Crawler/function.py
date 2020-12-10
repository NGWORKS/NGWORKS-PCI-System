import redis
import json
import requests
import sqlite3
import time

# 获取存在redis中的cookie
def BCookies():
    try:
        redis_b = redis.StrictRedis(host='localhost', port=6379, db=2)
    except Exception:
        raise ValueError("Redis连接错误")

    try:
        DedeUserID = redis_b.get('DedeUserID')
        DedeUserID__ckMd5 = redis_b.get('DedeUserID__ckMd5')
        SESSDATA = redis_b.get('SESSDATA')
        bili_jct = redis_b.get('bili_jct')
        sid = redis_b.get('sid')
        #redis中拿出的数据是bytes，要转str,人都傻了，草
        data = {
            'DedeUserID':DedeUserID.decode() ,
            'DedeUserID__ckMd5':DedeUserID__ckMd5.decode() ,
            'SESSDATA':SESSDATA.decode() ,
            'bili_jct':bili_jct.decode() ,
            'sid':sid.decode() ,
            }
        return data
    except Exception:
        raise ValueError("登录过期，请重新登录")


#AV-BV互转
def b_a(x):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF' #码表
    tr = {} #反查码表
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6] #位置编码表
    xor = 177451812 #固定异或值
    add = 8728348608 #固定加法值
    def bv2av(x):       #bv - av
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        return (r - add) ^ xor
    def av2bv(x):       #av - bv
        x = (x ^ xor) + add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]] = table[x // 58 ** i % 58]
        return ''. join(r)
    try:
        data = av2bv(x)
    except Exception:
        print("是BV号")
        data = bv2av(x)
    return data

#数据库操作
def dynamic_host_DATA(dynamic_id,oid,orgin_id,type,description,host,uid,time,z_time):
    conn = sqlite3.connect('dynamic.db')
    curson = conn.cursor()
    sql = '''select * from dynamic_host where dynamic_id = '%s' ''' % dynamic_id     
    curson.execute(sql)     
    res = curson.fetchall()     
    if len(res) > 0:
        pass
    else:
        curson.execute("INSERT INTO dynamic_host values(?,?,?,?,?,?,?,?,?)", (dynamic_id,oid,orgin_id,type,repr(str(description)),str(host),uid,time,z_time))
    conn.commit()
    curson.close()
    conn.close()

def dynamic_img_DATA(dynamic_id,oid,count,img):
    conn = sqlite3.connect('dynamic.db')
    curson = conn.cursor()
    sql = '''select * from dynamic_img where dynamic_id = '%s' ''' % dynamic_id     
    curson.execute(sql)     
    res = curson.fetchall()     
    if len(res) > 0:
        pass
    else:
        curson.execute("INSERT INTO dynamic_img values(?,?,?,?)", (dynamic_id,oid,count,img))
    conn.commit()
    curson.close()
    conn.close()

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
        print('>>含有分享内容')
        oid = dynamic_id
        type = 17
        orgin_id = detail['data']['card']['desc']['orig_dy_id']

        description = data['item']['content']
    elif type_orgin == 2:
        print('>>图片动态')
        imglist = []
        oid = rid
        type = 11
        pictureslist = data['item']['pictures']
        pictures_count = data['item']['pictures_count']
        i = 0
        while pictures_count > i:
            img = pictureslist[i]['img_src']
            pictures = img
            imglist.append(pictures)
            i+=1
        description = data['item']['description']
        dynamic_img_DATA(dynamic_id,oid,pictures_count,repr(str(imglist)))

    elif type_orgin == 4:

        print('>>文字动态')
        oid = dynamic_id
        type = 17
        description = data['item']['content']

    elif type_orgin == 8:

        print('>>投稿视频')
        oid = rid
        type = 1
        print(oid)
        description  = data['title']
        desc = data['desc']
    elif type_orgin == 64:

        print('>>投稿专栏')
        oid = rid
        type = 12
        description  = str(data['title'])
    elif type_orgin == 4300:

        print('>>收藏夹')
        oid = rid
        type = 17
    elif type_orgin == 4200:
        print('>>直播间')

    elif type_orgin == 512:
        print('>>番剧')
        oid = rid
        type = 1
        description  = data['apiSeasonInfo']['title']
        host = "bilibili番剧"
    else:
        raise ValueError("不支持的动态类型")
    z_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))  #时间戳转换
    dynamic_host_DATA(dynamic_id,oid,orgin_id,type,description,host,uid,ctime,z_time)
    return oid,type

