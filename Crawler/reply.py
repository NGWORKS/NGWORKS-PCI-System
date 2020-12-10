#reply.py  回复评论抓取
from api import *
from function import *

import time
import asyncio

'''
遍历评论
type       评论区类型
oid        评论区oid
StartPage  起始页
EndPage    结束页
例如：getreply(17,457347621130311478,1,500)
'''
#数据库操作
def dynamic_reply_DATA(type,dynamic_id,root_id,rid,reply,host,uid,time,ztime):
    conn = sqlite3.connect('dynamic.db')
    curson = conn.cursor()
    sql = '''select * from dynamic_reply where rid = '%s' ''' % rid    
    curson.execute(sql)     
    res = curson.fetchall()   
    if len(res) > 0:
        pass
    else:
        curson.execute("INSERT INTO dynamic_reply values(?,?,?,?,?,?,?,?,?)", (type,dynamic_id,root_id,rid,reply,host,uid,time,ztime))
    conn.commit()
    curson.close()
    conn.close()

def getreply(type,oid,StartPage,EndPage):
    try:
        # srclist = "PL" + str(oid) + ".txt"
        while True:
            try:
                data = reply(type,str(oid),StartPage)     #预先请求
            except Exception:
                raise ValueError("接口请求错误")  #跳出报错

            if data['code'] != 0:
                print(data['code'])
                print(oid)
                print(type)
                raise ValueError("评论区爬取1" + data['messag'])    #跳出报错

            try:
                count = len(data['data']['replies'])   #判断有无评论
            except Exception:
                break                 #没有就跳出
            i = 0
            while i < count:            #遍历评论根

                rpid = data['data']['replies'][i]['rpid']                    #评论根id
                message = data['data']['replies'][i]['content']['message']   #消息
                uname = data['data']['replies'][i]['member']['uname']        #用户名
                uid = data['data']['replies'][i]['member']['mid']            #uid
                like = data['data']['replies'][i]['like']                    #点赞
                ctime = data['data']['replies'][i]['ctime']
                z_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))  #时间戳转换
                level = data['data']['replies'][i]['member']['level_info']['current_level']

                dynamic_reply_DATA(1,oid,0,rpid,repr(str(message)),str(uname),uid,ctime,z_time)
                # str_data =  "1" + " |" + str(oid) + " |" + " - " + " |" + str(rpid) + " |" + repr(str(message)) + " |" + str(uname) + " |" + str(uid) + " |" + str(level) + " |" + str(like) + " |" + str(z_time)
                # txt = open(srclist, 'a',encoding='utf-8')
                # txt.write(str_data+'\n')
                # txt.close()
                
                rcount = data['data']['replies'][i]['rcount']
                try:
                    sonrcount = len(data['data']['replies'][i]['replies'])  #判断replies的长度
                except Exception:
                    i+=1
                    continue

                data3 = data['data']['replies'][i]['replies']
                
                j = 0
                if rcount <= 3:
                    while j < sonrcount:    #拿出自带的最多3个回复
                        root = rpid
                        rrpid = data3[j]['rpid']
                        rmessage = data3[j]['content']['message']
                        runame = data3[j]['member']['uname']
                        ruid = data3[j]['member']['mid']
                        rlike = data3[j]['like']                    #点赞
                        rctime = data3[j]['ctime']
                        rz_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(rctime))  #时间戳转换
                        level = data3[j]['member']['level_info']['current_level']
                        dynamic_reply_DATA(0,oid,root,rrpid,repr(str(rmessage)),str(runame),ruid,rctime,rz_time)
                        # rstr_data =   "0" + " |" + str(oid) + " |" + str(root) + " |" + str(rrpid) + " |" + repr(str(rmessage)) + " |" + str(runame) + " |" + str(ruid) + " |" + str(level) + " |" + str(rlike) + " |" + str(rz_time)
                                        
                        # txt = open(srclist, 'a',encoding='utf-8')
                        # txt.write(str(rstr_data)+'\n')
                        # txt.close()
                        j+=1
                    
                if rcount > 3:       #比3个多时
                    k = 1
                    while True:

                        try:
                            data2 = replyson(type,oid,rpid,k,20)  
                        except Exception:
                            raise ValueError("接口请求错误")

                        if data2['code'] != 0 :
                            raise ValueError(str(data2['message']))
                        
                        try:
                            count2 = len(data2['data']['replies'])
                        except Exception:
                            break
                        p = 0
                        repliesson = data2['data']['replies']

                        while p < count2:
                            rootson = repliesson[p]['root']
                            rpidson = repliesson[p]['rpid']
                            messageson = repliesson[p]['content']['message']
                            unameson = repliesson[p]['member']['uname']
                            uidson = repliesson[p]['member']['mid']
                            likeson = repliesson[p]['like']
                            timeson = repliesson[p]['ctime']
                            z_time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeson))
                            level = repliesson[p]['member']['level_info']['current_level']

                            dynamic_reply_DATA(0,oid,str(rootson),str(rpidson),repr(str(messageson)),str(unameson),str(uidson),str(timeson),z_time2)
                            # son_str = "0" + " |" + str(oid) + " |" + str(rootson) + " |" +str(rpidson) + " |" + repr(str(messageson)) + " |" + str(unameson) +  " |" + str(uidson) + " |" + str(level) + " |" + str(likeson) + " |" + str(z_time2)

                            # txt = open(srclist, 'a',encoding='utf-8')
                            # txt.write(son_str+'\n')
                            # txt.close()
                            p+=1
                        k+=1
                i+=1

            num = data['data']['page']['num']

            if num == EndPage:        #当前页面等于终止页时跳出循环
                print("任务完成")
                break
            StartPage+=1

    except Exception as e:
        raise ValueError(e)


'''   
判断id
id     链接上的id
type   类型，见文档
'''
def getreply_all(type,oid):
    StartPage = 1
    EndPage = 99999999
    getreply(type,oid,StartPage,EndPage)

def reply_host_info(id,type):
    if type == 1:  #是视频
        res = mov_info(id)
        title = res['data']['title']
        desc = res['data']['desc']
        ctime = res['data']['ctime']
    






        







