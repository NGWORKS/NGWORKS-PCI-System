# NGWORKS心理危机干预系统
NGWORKS Psychological Crisis Intervention System

## 1.1 什么是NGWORKS心理危机干预系统

自杀是导致全球高疾病负担的一个重要因素。一项全球自杀数据显示，2016年全球自杀死亡人数为81.7万人，1990～2016年全球自杀死亡总数增加了6.7%。据WHO发布的《2018世界卫生统计报告》，中国的自杀死亡率为每10万人中约9.7人。

尽管有自杀倾向者很少寻求帮助，但已有研究表明产生自杀意念的人群在行为及言语表达上存在特定形式。早期识别自杀风险并进行自杀干预有利于降低自杀死亡率。

随着网络社交平台的发展，人们借助网络表达观点的意愿越来越强烈，很多抑郁症患者在萌发自杀意念时也往往通过社交平台表达自身真实想法，这种现象基于渴望得到他人关注和挽回的
心理需求。

本项目主要基于哔哩哔哩社区功能，通过自然语言处理技术，通过理解在“树洞”评论区的评论，对其中潜藏的抑郁症患者行为进行**监控**、**评估**、**预警**、**干预**的系统
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
  > B站up主、唱见；于2014年11月29日中午12时许烧炭自杀一氧化碳中毒死亡

非常**不建议**看到这里的朋友跑去留言，谢谢

两个“树洞”的形成时间差具较大，影响范围也尽不相同，各具代表性。**可以这么推测，任何一个已经逝去的up主的页面，凡是带有评论区的地方，都是一个“树洞”**  

*其实这件事情应该平台去做的，现代任何的社区平台都应该及时的把“心理危机干预”如同“内容安全”一样常态化。*

## 2.2 实现方案
### 2.2.1 查找，发掘树洞
这阶段只能通过海量数据的爬取，人工的发掘，来找到“树洞”

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

* 前面两个请求参数加上**当前时间戳的毫秒数**按照下面的示例拼接成字符串
    ```
    <type>&<id>&<当前时间戳的毫秒数>
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
* 服务器会每2分钟对“树洞”的评论区的评论进行一次扫描，并且根据数据库中记录的评论时间戳进行比较，当现有评论的时间戳大于这个时间戳时，服务器就会爬取大于该时间戳的评论，直到爬取到等于，或者小于这个时间戳的评论，当有相等时间戳时，程序才会判断rid。上述操作执行完毕后，数据库会更新用于下次的时间戳与rid。
    > 这个策略只能发现根评论的更新，**通过时间戳判断是为了防止评论被删除**。
* 服务器每天凌晨会全面抓取一次“树洞”评论。

## 2.2.2 分类，评估
程序通过**6～10**级高自杀风险人群进行自杀风险分级（根据自杀方式的确定性和时间紧迫性[1]）：
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

到了知识盲区了 - 学习去了
> *在鹿🦌上了*

# 参考文献
* World Health Organization.World Health Statistics 2018:monitoring health for the SDGs[EB/OL].(2018-06-06)[2019-02-06].https://apps.who.int/iris/bitstream/handle/10665/272596/9789241565585-eng.pdf?ua=1
* 杨芳，黄智生，杨冰香等基于人工智能技术的微博“树洞”用户自杀意念分析[J],护理学杂志，2019，34(24)：42-43
* 黄智生，胡青，顾进广，等．网络智能机器人与自杀监控
预警［J］．中国数字医学，2019，14(3)：3-6．

