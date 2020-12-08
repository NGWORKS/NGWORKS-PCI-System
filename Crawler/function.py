import redis

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
    