#爬回复的包，实例化Reply()
"""
@author: NGWORKS-夏姬八彻
@contact: wl@ngworks.com
@version: 0.a1
@file: reply.py
@time: 2020/12/11   20:12
@detail: 爬回复。
"""
import time,asyncio,requests,json,math,aiohttp
from fuc import *
from DB import *
from active import *

class Reply(object):
    '用来爬回复的\n(参数一:评论区类型 ,参数二:评论区id ,参数三:起始页 ,参数四:终止页)\n参数二、三非必填，默认抓取全部。'
    def __init__(self,type,oid,StartPage = 1 ,EndPage = None):
        '定义的公共属性'
        print('开始')
        # api的地址
        self.url_list = [
            "http://api.bilibili.com/x/v2/reply",       #根评论
            "http://api.bilibili.com/x/v2/reply/reply"  #回复
        ]
        # 预请求算出page
        self.page = math.ceil((requests.get(url = self.url_list[0] , params = {'type':type,'oid':oid,'ps':49,'pn':1} ,cookies = Cookies()).json()['data']['page']['count'])/49)
        self.type = type
        self.oid = oid
        self.StartPage = StartPage
        self.EndPage = EndPage
        self.reply_host_list = []
        self.reply_reply_list = []

    def manage(self):
        '异步管理器'
        result = self.reply_API_taska()
        # 建立事件循环
        loop = asyncio.get_event_loop()
        loop.run_until_complete(result)
    
    async def reply_API_taska(self):
        '创建taska列表'
        async with aiohttp.ClientSession() as session:
            self.session = session
            if self.EndPage != None:
                if self.EndPage > self.page:
                    pass
                else:
                    self.page = self.EndPage
            if self.page != 0:
                self.test_list = range(self.StartPage,self.page + 1)
                print(self.page)
                tasks = [asyncio.create_task(self.reply_API(tp,0))for tp in self.test_list]
                await asyncio.wait(tasks)
                self.exit()
            else:
                print("没有动态")

    async def reply_API(self,pn,typ,root = '0'):
        'taska列表的模板，也就是aiohttp请求的函数'
        print("发请求")
        params = [{'type':self.type,'oid':self.oid,'ps':49,'pn':pn},{'type':self.type,'oid':self.oid,'root':root,'ps':20,'pn':pn}]
        async with self.session.get(url = self.url_list[typ] ,params = params[typ],cookies = Cookies()) as response:
            data = await response.json()
        if typ == 0:
            print(str(pn))
            try:
                count = len(data['data']['replies'])   #判断有无评论
            except Exception:
                raise ValueError('没有评论')
            i = 0
            while i < count:
                rpid = data['data']['replies'][i]['rpid']                    #评论根id
                message = data['data']['replies'][i]['content']['message']   #消息
                uname = data['data']['replies'][i]['member']['uname']        #用户名
                uid = data['data']['replies'][i]['member']['mid']            #uid
                like = data['data']['replies'][i]['like']                    #点赞
                ctime = data['data']['replies'][i]['ctime']
                z_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))  #时间戳转换
                level = data['data']['replies'][i]['member']['level_info']['current_level']
                self.reply_host_list.append((1,self.oid,0,rpid,message,uname,uid,ctime,z_time))
                # str_data =  "1" + " |" + str(self.oid) + " |" + " - " + " |" + str(rpid) + " |" + repr(str(message)) + " |" + str(uname) + " |" + str(uid) + " |" + str(level) + " |" + str(like) + " |" + str(z_time)
                # print(str_data)

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
                        self.reply_reply_list.append((0,self.oid,root,rrpid,rmessage,runame,ruid,rctime,rz_time))
                        #rstr_data =   "0" + " |" + str(self.oid) + " |" + str(root) + " |" + str(rrpid) + " |" + repr(str(rmessage)) + " |" + str(runame) + " |" + str(ruid) + " |" + str(level) + " |" + str(rlike) + " |" + str(rz_time)
                        #print(rstr_data)               
                        j+=1
                else:
                    page = range(1,math.ceil(rcount/20) + 1)
                    tasks = [asyncio.create_task(self.reply_API(tp,1,rpid))for tp in page]
                    await asyncio.wait(tasks)
                i+=1
        else:
            count = len(data['data']['replies'])
            p = 0
            repliesson = data['data']['replies']

            while p < count:
                rootson = repliesson[p]['root']
                rpidson = repliesson[p]['rpid']
                messageson = repliesson[p]['content']['message']
                unameson = repliesson[p]['member']['uname']
                uidson = repliesson[p]['member']['mid']
                likeson = repliesson[p]['like']
                timeson = repliesson[p]['ctime']
                z_time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeson))
                level = repliesson[p]['member']['level_info']['current_level']
                self.reply_reply_list.append((0,self.oid,rootson,rpidson,messageson,unameson,uidson,timeson,z_time2))
                # son_str = "0" + " |" + str(self.oid) + " |" + str(rootson) + " |" +str(rpidson) + " |" + repr(str(messageson)) + " |" + str(unameson) +  " |" + str(uidson) + " |" + str(level) + " |" + str(likeson) + " |" + str(z_time2)
                # print(son_str)
                p+=1
        print("完成")

    def exit(self):
        self.DATA = tuple(set(tuple(self.reply_host_list) + tuple(self.reply_reply_list)))
        with SqliteDB('dynamic.db') as db:
            db.connection.executemany("INSERT INTO dynamic_reply values(?,?,?,?,?,?,?,?,?)", self.DATA)
        print("任务完成")     


if __name__ == "__main__":    
    datali = get_new_dynamic_all()
    if len(datali) != 0:
        for ifo in datali:
            Reply(ifo[1],ifo[0]).manage()
    
