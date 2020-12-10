#active.py 动态管理
from api import *
from function import *
from reply import * 
import redis
import math
import sqlite3


def get_new_dynamic(dynamic_id):
    cookie = BCookies()
    uid = cookie['DedeUserID']
    dynamic_id_list = []
    data1 = dynamic_new(dynamic_id)
    new_num = data1['data']['new_num']
    i = 0
    if new_num == 0:
        raise ValueError("没有新动态")
    elif new_num <= 20:
        while i < new_num:
            rid_str = data1['data']['cards'][i]['desc']['rid']
            dynamic_id_str = data1['data']['cards'][i]['desc']['dynamic_id']
            type = data1['data']['cards'][i]['desc']['type']
            dynamic_id_list.append({"dynamic_id":dynamic_id_str,"rid":rid_str,"type":type})
            i+=1 
        now_new_dynamic_id = dynamic_id_list[0]['dynamic_id']
    else:
        j = 0
        listok = False
        while i < 20:
            dynamic_id_str = data1['data']['cards'][i]['desc']['dynamic_id']
            rid_str = data1['data']['cards'][i]['desc']['rid']
            type = data1['data']['cards'][i]['desc']['type']
            dynamic_id_list.append({"dynamic_id":dynamic_id_str,"rid":rid_str,"type":type})
            i+=1
        now_count = new_num - 20
        page = math.ceil(now_count/20)
        while j < page:
            dynamic_id_last = dynamic_id_list[-1]['dynamic_id']
            data2 = dynamic_history(dynamic_id_last)
            i = 0
            while i < 19:
                dynamic_id_str = data2['data']['cards'][i]['desc']['dynamic_id']
                rid_str = data1['data']['cards'][i]['desc']['rid']
                type = data1['data']['cards'][i]['desc']['type']
                if int(dynamic_id_str) == int(dynamic_id):
                    listok = True
                    break
                dynamic_id_list.append({"dynamic_id":dynamic_id_str,"rid":rid_str,"type":type})
                i+=1
            if listok:
                break
            j+=1
    ttl = 60*60*24*30
    conn = sqlite3.connect('dynamic.db')
    curson = conn.cursor()
    Val = str(dynamic_id_list[0]['dynamic_id'])
    curson.execute("UPDATE inf SET value=? WHERE key=?", (Val,"dynamic_id")) 
    conn.commit()
    curson.close()
    conn.close() 
    return dynamic_id_list

def get_new_dynamic_all():
    try:
        conn = sqlite3.connect('dynamic.db')
        curson = conn.cursor()
        sql = '''select * from inf where key = '%s' ''' % "dynamic_id"     
        curson.execute(sql)     
        res = curson.fetchall()     
        if len(res) > 0:
            print(res)
            dynamic_id = res[0][1]
            print(dynamic_id)
        else:
            dynamic_id = input("储存动态id失效，请指定新的起始id：")
        conn.commit()
        curson.close()
        conn.close()
        
        data = get_new_dynamic(dynamic_id)

        count = len(data)

        i = 0
        while i < int(count):

            number = data[i]
            dynamic_id = number['dynamic_id']
            detail = get_dynamic_detail(dynamic_id)
            rid = detail['data']['card']['desc']['rid']

            dynamic_id = detail['data']['card']['desc']['dynamic_id']
            type_orgin = detail['data']['card']['desc']['type']
            res2 = dynamic_type( type_orgin , dynamic_id , rid ,detail)
            type = res2[1]
            oid = res2[0]

            getreply_all(type,oid)
            i+=1
    except Exception as e:
        print(e)
        
    
