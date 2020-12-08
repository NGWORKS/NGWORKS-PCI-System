# NGWORKS心理危机干预系统
NGWORKS Psychological Crisis Intervention System
# 警告[WARNING]：本文档会关联部分有关抑郁症群体活动的“树洞”，如果你没有充足的专业知识储备，请不要擅自干预，因为你不知道你是否会给他们带来二次伤害，请你求助更加专业人士来做。请务必记着。

## 1.1 什么是NGWORKS心理危机干预系统

自杀是导致全球高疾病负担的一个重要因素。一项全球自杀数据显示，2016年全球自杀死亡人数为81.7万人，1990～2016年全球自杀死亡总数增加了6.7%。据WHO发布的《2018世界卫生统计报告》，在中国，每年每10万人中约9.7人死于自杀。

尽管有自杀倾向者很少寻求帮助，但已有研究表明产生自杀意念的人群在行为及言语表达上存在特定形式。早期识别自杀风险并进行自杀干预有利于降低自杀死亡率。

随着网络社交平台的发展，人们借助网络表达观点的意愿越来越强烈，很多抑郁症患者在萌发自杀意念时也往往通过社交平台表达自身真实想法，这种现象基于渴望得到他人关注和挽回的
心理需求。

本项目主要基于哔哩哔哩社区功能，通过自然语言处理技术，通过理解在“树洞”评论区的评论，对其中潜在的抑郁症患者行为进行**监控**、**评估**、**预警**、**干预**的系统
**也就是说，这个项目分为四大模块：**
* 对所有评论区数据的收集
* 识别“树洞”评论区
* 对需要监控的对象进行监控
* 响应与干预
## 1.2 谁应该阅读这个文档
* 对这个项目感兴趣的人
    > 欢迎吃瓜
* 开发者
    > 有一定的开发能力
* 热心的普通人
    > 志愿者
* 有专业医学知识的人
    > 总之很强就对了，~~快教教我~~
# 概述
这一章节会对本项目有一个具体的规划，对一些名词进行解释，同时也会讲讲实现的方法与要做的事情。
## 2.1 什么是“树洞”
> “树洞”一词来源于古代童话故事《皇帝长了驴耳朵》，借指诉说不能告人的秘密的地方。  

**抑郁症患者自杀死亡后，他们的个人空间通常会成为其他抑郁症患者特别是有自杀倾向的人吐露心声的“树洞”。**

本人目前密切监控的“树洞”有两个：
* [琉科Ryuko“树洞”](https://t.bilibili.com/457347621130311478),目前有1655条数据
  > B站up主、武工大学生、画师；于2020年11月19日凌晨3时许跳楼自杀死亡
* [Neuuuuu“树洞”](https://www.bilibili.com/video/av1712033)，目前有92041条数据
  > B站up主、唱见；于2014年11月29日中午12时许燃炭自杀死亡

非常**不建议**看到这里的朋友跑去留言，谢谢

两个“树洞”的形成时间差具较大，影响范围也尽不相同，各具代表性。**可以这么推测，任何一个已经逝去的up主的页面，凡是带有评论区的地方，都是一个“树洞”**  

*其实这件事情应该平台去做的，现代任何的社区平台都应该及时的把“心理危机干预”如同“内容安全”一样常态化。*

## 2.2 实现方案
### 2.2.1 查找，发掘树洞
通过海量数据的爬取，人工的发掘，来找到“树洞”

找到“树洞”后，可以通过爬虫爬取评论区

我是通过下面两个api实现：
```
获取根评论[GET] http://api.bilibili.com/x/v2/reply
```
|字段名称       |字段说明         |类型            |必填            |备注     |
| -------------|:--------------:|:--------------:|:--------------:| ------:|
|type|评论区类型|字符串|Y|-|
|oid|评论区id|字符串|Y|-|
|ps|一页展示多少根评论|字符串|Y|最大49|
|pn|获取指定页的评论|字符串|Y|-|

上面这个API获取的数据中会**默认携带三条针对根评论的回复**，如果这个评论下的回复大于3，请再使用下面这个API请求：

```
获取指定评论[GET] https://api.bilibili.com/x/v2/reply/reply
```
|字段名称       |字段说明         |类型            |必填            |备注     |
| -------------|:--------------:|:--------------:|:--------------:| ------:|
|type|评论区类型|字符串|Y|-|
|oid|评论区id|字符串|Y|-|
|root|父级rid|字符串|Y|-|
|ps|一页的项目数|字符串|Y|最大20|
|pn|获取指定页的评论|字符串|Y|-|

详细内容可以见这个项目：[bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)

**我通过自建接口，实现了方便的封装：**
```
下载目标评论区所有评论 [GET]  【上线后公开】/api/bilibili/pinglun
```
**请求参数：**

|字段名称       |字段说明         |类型            |必填            |备注     |
| -------------|:--------------:|:--------------:|:--------------:| ------:|
|type|评论区类型|字符串|Y|-|
|id|评论区id|字符串|Y|-|
|APPid|appid|字符串|Y|我下发的appid|
|Signature|签名|字符串|Y|-|

**type 字段:**
|字段名称       |字段说明         |类型            |必填            |备注     |
| -------------|:--------------:|:--------------:|:--------------:| ------:|
|1|视频|字符串|Y|-|
|2|动态|字符串|Y|-|

**id 字段：**

视频内容的**AV号与BV号均可**，动态即为**动态的Dynamic id**
```
2020年3月23日，B站全面取消了Av号，故Av号的寻找方式在这不做赘述。

BV号：位于视频链接的末尾，以BV开头的字符串
例如：https://www.bilibili.com/video/BV1Li4y157ts

Dynamic id:位于动态链接末尾，巴拉巴拉吧的一长串
例如：https://t.bilibili.com/457347621130311478
```

**Signature 字段：**

* 前面两个请求参数加上**当前Unix时间戳（毫秒）**按照下面的示例拼接成字符串
    ```
    <type>&<id>&<Unix时间戳（毫秒）>
    2&457347621130311478&1607359540000
    ```
* 按照**RFC2104**的定义，计算待签名字符串的HMAC值，**使用的Key为我下发的Appkey**。
* 将按照**Base64**编码规则把上面的HMAC值编码成字符串，即得到签名值。
* 将计算得到的签名加到请求的Signature字段。

**通过正确的请求参数时会得到下示的返回：**
```
{
    "code": 0,
    "msg": "请求成功",
    "origin": {
        "oid": "457347621130311478",
        "type": 17,
        "typemsg": "文字动态",
        "count": 831,
        "acount": 1658,
        "info": {
            "dynamic_id": "457347621130311478",
            "rid": "457347621130311478",
            "description": "使用魔法的方式是与元素沟通，比如自爆术的咒语就是辱骂火元素",
            "time": "2020-11-14 11:02:21",
            "ctime": 1605322941,
            "owner": "琉科Ryuko",
            "uid": 9989545,
            "view": 131419,
            "like": 1190,
            "repost": 254,
            "url": "https://t.bilibili.com/457347621130311478",
            "orign": [],
            "img": []
        }
    },
    "data": {
        "get": 1657,
        "msg": "完成，实际抓取1657条评论,B站标称1658条评论",
        "url": "http://127.0.0.1:8000/static/PL457347621130311478.txt"
    }
}
```
data中的url即为该评论区所有评论的文本文件下载地址。

**得到的文本文件的数据处理：**
```
键 |类型 |评论区id |上级id |评论id |内容 |昵称 |UID |等级 |赞 |发表时间
1 |1 |457347621130311478 | -  |3788648426 |'晚上好，在异世界不要再给自己太多的压力，照顾好自己。[拥抱]' |Erio_0173 |14782169 |5 |0 |2020-12-07 18:29:51
2 |1 |457347621130311478 | -  |3786956471 |'早上草，前辈\n今天又是周一\n感觉永远都睡不醒5555\n一起fighting吧\n\n早上草～' |NIN-kidu |410720184 |4 |2 |2020-12-07 06:31:02
3 |1 |457347621130311478 | -  |3786717445 |'晚安' |别问一问就是白嫖 |256153880 |4 |0 |2020-12-07 01:21:39
...
...
```
下载的文本文件会包含一个自增的键和评论的主要数据

**服务器主动进行数据更新的规则：**
* 服务器会每2分钟对“树洞”的评论区的评论进行一次扫描，并且根据数据库中记录的上次最新评论的时间戳与rid进行比较，当现有评论的时间戳大于这个时间戳时，服务器就会爬取大于该时间戳的评论，直到爬取到等于，或者小于这个时间戳的评论，当有相等时间戳时，程序才会判断rid。上述操作执行完毕后，数据库会更新用于下次的时间戳与rid。
    > 这个策略只能发现根评论的更新，**通过时间戳判断是为了防止评论被删除**。
* 服务器每天凌晨会全面抓取一次“树洞”评论。

## 2.2.2 分类，评估
**程序通过6～10级高自杀风险人群进行自杀风险分级（根据自杀方式的确定性和时间紧迫性[1]）：**
> [1]这个性质下面会有个树图详细的说明

* 10级：自杀可能**正在进行**中
* 9级：自杀**方式已确定**，近日内**可能进行**
* 8级：自杀方式**已在计划中**，自杀日期**大体确定**
* 7级：自杀方式**已确定**，自杀**日期未明**
* 6级：自杀**已在计划中**
* 5级：**强烈**的自杀**愿望**，自杀**方式未明**
* 4级：自杀**愿望已表达**，具体**方式和计划未明**
* 3级：**强烈的生存痛苦**，未见自杀愿望表达
* 2级：**生存痛苦已明确表达**，未见自杀愿望表达
* 1级：生存痛苦**有所表达**，未见自杀愿望表达
* 0级：未见任何生存痛苦表达

**通常在树洞下通过简单的关键词筛选，就能非常快捷的找到体现不同风险程度的人：**

这些数据时间跨度大，都符合上方基于对于目的与方法的特征

|键            |类型            |评论id           |内容            |发表时间 |
| -------------|:--------------:|:--------------:|:--------------:| ------:|
|365|1|******|<font color='RED'>up主，今天板子还是没焊出来，最近想起在一个七成是女生的学校里依然没有小姐姐接受我，果然还是**我太差劲了**吧。\n这两天感冒了，应该是因为这次开学一直没吃晚饭的原因，提抗力下降了吧，嗓子好疼，收音机焊不出来我宁可让病毒**把我带走**。\n快期末了，宿舍抽屉里那把**刀**，我去年休学期间花了好多钱才买到的，**非常锋利**，我这次也一定不会再找错位置了，我还带了我之前开的那些**药**，量是很多的，等我**出发**一定可以顺利**到达**你那里的，你再等一等噢，元旦之后，我陪这边的千纸鹤们去完电影院看小红花包场之后就**去找你**，不要着急 </font>|2020/11/23 13:31|
|366|0|******|我下午就**动手**，**一起做个伴**|2020/11/24 9:59|
|548|1|******|大爷你在那里好好的，我会**过来找你的**，想你了，**我也坚持不了啦** |2020/11/18 1:03|
|6595|1|******|被**抑郁症**困扰了四年了，今天终于**下定决心了**。感谢你，这么久以来每次听到这首歌都会心头一暖。现在是凌晨两点，**我来找你了**，希望在那儿可以亲耳听到你的歌。 |2020/7/27 1:58|
|10360|1|******|<font color='#C0CFCC'>这个**世界有好大好大的恶意啊**……\n后天开学，到了被同学集体针对的第三个学期，直播课的时候又有同学挖苦我呢，我忍也是错，怼回去也是错，被彻底当成了一个没有脾气的傻子呢……**每天一到晚上我就会崩溃**，制止不住地**哭**。但家里有人，不敢被发现呢，每次被发现会被说犯**病**了呢……试图从窗户上**跳下去**了3次，但我家是3**楼**，要是**摔下去死的不彻底**，抢救过来会太难看了呢，一直试图寻找某个时机，能不被人发现的，**死**的透彻一点啊……\n这个现实**世界**到底对我来说**还有什么意义呢**，我告诉其他人还抱有一丝被拯救的**希望**的时候，他们说：“你是不是有**病**啊？”\n**我不配**在这个人间玩耍，大爷，我马上就来**找你玩了**哦 </font>|2020/5/19 21:14|
|10360|1|******|晚安。时隔一年，我又开始吃**药**了。好像很久没有来找你说话了吧？最好的朋友也离我而去了，身体也**越来越不如从前**，药物的副作用也慢慢显现出来，有时候觉得，活着或者死去，就是一念之间，幻想**自己从楼上坠落下来**的样子，会被人看到吗？或者是悄无声息地，和你一样。**晚安**吧，即使在梦里下了无数遍地狱，也要试试今晚的梦会不会甜美一点。 |2019/11/2 22:46|
|37386|1|******|我已经按照某人的约定活到这一年了啊……**这样就够了**。**让我去找你吧** |2019/1/1 14:30|
|37420|1|******|被**一氧化碳**夺走维身的控制权。\n这样的**死**法真的能够**结束痛苦**么，相信我很快就会知道了…… |2019/1/1 14:30|
|48709|1|******|大爷…我的**抑郁症越来越严重啦**…哪天…说不定就会**来找你啦** |2018/3/15 22:37|
|51533|1|******|大爷，我又来找你了，真难过。**我是不是死了**，罪就会被清除呢 |2017/12/13 20:26|

> 里面有一些人已经走了，当然也有人挺了过来，**请不要去打扰他们**，谢谢

不难发现，这些将自身想法表露出来的“倾诉者”，








到了知识盲区了 - 学习去了
> *在鹿🦌上了*

# 参考文献
> 有些已经参考了，有些还在看，先写这，免得忘了
* [World Health Organization. World Health Statistics 2018:monitoring health for the SDGs[EB/OL]. (2018-06-06)[2019-02-06].](https://apps.who.int/iris/bitstream/handle/10665/272596/9789241565585-eng.pdf?ua=1)
* 杨芳，黄智生，杨冰香，等. 基于人工智能技术的微博“树洞”用户自杀意念分析[J]. 护理学杂志，2019，34(24)：42-43.
* 黄智生，胡青，顾进广，等. 网络智能机器人与自杀监控预警[J]. 中国数字医学，2019，14(3)：3-6.
* 黄智生，闵一文，林凤，等．社交媒体中自杀信息的时间特征[J]．中国数字医学，2019，14(3)：7-10．
* 徐玉，赵怀娟．偏差行为理论视角下“网络直播自杀”行为探析[J]．中国青年研究，2017(11)：87-91．
* 管理，郝碧波，刘天俐，等．新浪微博用户中自杀死亡和无自杀意念者特征差异的研究[J]．中华流行病学杂志，2015，36(5)：421-425．
* 管理，郝碧波，程绮瑾，等．不同自杀可能性微博用户行为和语言特征差异解释性研究[J]．中国公共卫生，2015，31(3)：349-352．
* 肖水源，周亮，徐慧兰．危机干预与自杀预防（二）———自杀行为的概念与分类[J]．临床精神医学杂志，2005，15(5) ：298-299．
* 胡德英，柳丽茗，邓先锋，等．568例急诊科自杀未遂患者特征分析与管理对策[J]．护理学杂志，2018，33(18)：15-17．
* 刘瑾．366例自杀死亡案例统计分析[J]．世界中西医结合杂志，2012，7(4)：329-331．
* 张杰．自杀的“压力不协调理论”初探（综述）[J]．中国心理卫生杂志，2005，19(11)：778-782．
* 李玲，廖宗峰．神经内科抑郁症状患者自杀的预警干预[J]．护理学杂志，2017，32(13)：75-76，83．
