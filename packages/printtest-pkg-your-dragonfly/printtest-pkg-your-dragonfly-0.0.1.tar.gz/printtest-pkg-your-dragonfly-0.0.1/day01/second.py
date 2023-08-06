# -*- coding:utf-8 -*-
'''
Created on 2019年5月16日

@author: Administrator
'''
# import sys
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from builtins import sorted


# print(sys.getdefaultencoding())
# reload(sys)
# sys.setdefaultencoding('utf-8')
# print(sys.getdefaultencoding())

# 打印结果
def showresult(em):
    print(em)


# 数据样例
# 7.213.213.208    吉林    2018-03-29    1522294977303    1920936170939152672    www.dangdang.com    Login

# 页面访问量
def pv(lines):
    sitepair = lines.map(lambda line: (line.split("\t")[5], 1))
    result1 = sitepair.reduceByKey(lambda v1, v2: v1 + v2)
    # 排序 降序
    result2 = result1.sortBy(lambda one: one[1], ascending=False)
    result2.foreach(lambda em: showresult(em))


# ('www.baidu.com', 18791)
# ('www.dangdang.com', 18751)
# ('www.suning.com', 18699)
# ('www.mi.com', 18678)
# ('www.taobao.com', 18613)
# ('www.jd.com', 18519)
# ('www.gome.com.cn', 18493)

# 用户访问量
def uv(lines):
    # 同一个IP访问某个网站量要排重
    sitepair = lines.map(lambda line: line.split("\t")[0] + "_" + line.split("\t")[5]).distinct()
    result = sitepair.map(lambda one: (one.split("_")[1], 1)).reduceByKey(lambda v1, v2: v1 + v2).sortBy(
        lambda one: one[1], ascending=False)
    result.foreach(lambda one: showresult(one))


# ('www.baidu.com', 15830)
# ('www.suning.com', 15764)
# ('www.mi.com', 15740)
# ('www.jd.com', 15682)
# ('www.dangdang.com', 15641)
# ('www.taobao.com', 15593)
# ('www.gome.com.cn', 15590)

def uvExceptBJ(lines):
    usiteviews = lines.filter(lambda line: line.split("\t")[1] != "北京").map(
        lambda line: line.split("\t")[0] + "_" + line.split("\t")[5]).distinct()
    result1 = usiteviews.map(lambda one: (one.split("_")[1], 1)).reduceByKey(lambda v1, v2: v1 + v2)
    result2 = result1.sortBy(lambda one: one[1], ascending=False)
    result2.foreach(lambda em: showresult(em))


# ('www.baidu.com', 15399)
# ('www.mi.com', 15341)
# ('www.suning.com', 15294)
# ('www.jd.com', 15255)
# ('www.dangdang.com', 15181)
# ('www.gome.com.cn', 15154)
# ('www.taobao.com', 15131)

def getTop2Location(lines):
    # 按照网站分组
    site_locations = lines.map(lambda line: (line.split("\t")[5], line.split("\t")[1])).groupByKey()
    result = site_locations.map(lambda one: getCurrSiteTop2Location(one)).collect()
    for em in result:
        print(em)


# ('www.suning.com', [('山西', 1102), ('广西', 606)])
# ('www.jd.com', [('山西', 1069), ('湖北', 614)])
# ('www.taobao.com', [('山西', 1065), ('安徽', 601)])
# ('www.gome.com.cn', [('山西', 1029), ('内蒙', 590)])
# ('www.dangdang.com', [('山西', 1083), ('香港', 591)])
# ('www.mi.com', [('山西', 1085), ('广东', 617)])
# ('www.baidu.com', [('山西', 1028), ('台湾', 641)])

def getCurrSiteTop2Location(one):
    site = one[0]
    locations = one[1]

    locationdict = {}
    # 汇总每个网站中location的数量
    for location in locations:
        if location in locationdict:
            locationdict[location] += 1
        else:
            locationdict[location] = 1
    resultlist = []
    # 使用内置函数排序
    sortedList = sorted(locationdict.items(), key=lambda kv: kv[1], reverse=True)
    # 取前两个地区
    if len(sortedList) < 2:
        resultlist = sortedList
    else:
        for i in range(2):
            resultlist.append(sortedList[i])
    return site, resultlist


def getTopOperation(lines):
    site_operations = lines.map(lambda line: (line.split("\t")[5], line.split("\t")[6])).groupByKey()
    result = site_operations.map(lambda one: getCurrSiteTopOperation(one)).collect()
    for em in result:
        print(em)


# ('www.suning.com', [('View', 3168)])
# ('www.jd.com', [('Login', 3132)])
# ('www.taobao.com', [('Regist', 3196)])
# ('www.gome.com.cn', [('Click', 3170)])
# ('www.dangdang.com', [('Buy', 3179)])
# ('www.mi.com', [('Buy', 3231)])
# ('www.baidu.com', [('Comment', 3207)])

def getCurrSiteTopOperation(one):
    site = one[0]
    operations = one[1]
    operationDict = {}
    for operation in operations:
        if operation in operationDict:
            operationDict[operation] += 1
        else:
            operationDict[operation] = 1

    resultList = []
    sortedList = sorted(operationDict.items(), key=lambda kv: kv[1], reverse=True)
    if len(sortedList) < 1:
        resultList = []
    else:
        resultList.append(sortedList[0])
    return site, resultList


def getTop3User(lines):
    # 另外一种思路 按照用户分组 统计每个用户访问不同网站数量
    site_uid_count = lines.map(lambda line: (line.split("\t")[3], line.split("\t")[5])).groupByKey().flatMap(
        lambda one: getSiteInfo(one))
    # 按照网站分组之后再取前三
    result = site_uid_count.groupByKey().map(lambda one: getCurSiteTop3User(one)).collect()
    for em in result:
        print(em)


# ('www.suning.com', [('1522294989941', 5), ('1522294980028', 5), ('1522294986337', 5)])
# ('www.jd.com', [('1522295002636', 5), ('1522294988631', 5), ('1522294990824', 4)])
# ('www.taobao.com', [('1522294992394', 5), ('1522294982477', 5), ('1522294999369', 5)])
# ('www.gome.com.cn', [('1522294994219', 5), ('1522294988497', 5), ('1522294991142', 5)])
# ('www.dangdang.com', [('1522294994360', 5), ('1522294988712', 5), ('1522294992239', 4)])
# ('www.mi.com', [('1522294987189', 5), ('1522294989540', 5), ('1522294980962', 5)])
# ('www.baidu.com', [('1522294991559', 6), ('1522294989188', 5), ('1522294996021', 5)])

# 统计每个用户访问网站数量 然后返回每个网站对应用户访问量
def getSiteInfo(one):
    uid = one[0]
    sites = one[1]
    siteDict = {}
    for site in sites:
        if site in siteDict:
            siteDict[site] += 1
        else:
            siteDict[site] = 1
    resultList = []
    for site, count in siteDict.items():
        resultList.append((site, (uid, count)))
    return resultList


def getCurSiteTop3User(one):
    site = one[0]
    uid_counts = one[1]
    top3List = ["", "", ""]
    for uid_count in uid_counts:
        for i in range(0, len(top3List)):
            if top3List[i] == "":
                top3List[i] = uid_count
                break
            else:
                if uid_count[1] > top3List[i][1]:
                    for j in range(2, i, -1):
                        top3List[j] = top3List[j - 1]
                    top3List[i] = uid_count
                    break
    return site, top3List


if __name__ == '__main__':
    conf = SparkConf().setMaster("local").setAppName("pvuv")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("WARN")
    lines = sc.textFile('../../data/pvuvdata')
    # 1).统计PV,UV
    pv(lines)
    uv(lines)
    # 2).统计除了北京地区外的UV
    uvExceptBJ(lines)
    # 3).统计每个网站最活跃的top2地区
    getTop2Location(lines)
    # 4).统计每个网站最热门的操作
    getTopOperation(lines)
    # 5).统计每个网站下最活跃的top3用户
    getTop3User(lines)
    # 停止
    sc.stop()
