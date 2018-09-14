# coding:utf-8
from csv import DictWriter
from datetime import datetime
import requests
import chardet
import json
from collections import OrderedDict
from pyexcel_xls import save_data
# 登录的主方法
from bs4 import BeautifulSoup
from selenium import webdriver


def login():
    # 获取验证码
    codeurl = 'http://new.cnzz.com/v1/images/validate.php'
    valcode = requests.get(codeurl)
    f = open('valcode.png', 'wb')
    # 将response的二进制内容写入到文件中
    f.write(valcode.content)
    # 关闭文件流对象
    f.close()
    code = input('请输入验证码：')
    #u = input('请输入u：')
    #p = input('请输入p：')
    # post需要的表单数据，类型为字典
    login_data = {
        'password': 'qj734748',
        "number": str(code),
    }
    # 使用seesion登录，这样的好处是可以在接下来的访问中可以保留登录信息
    session = requests.session()
    # 登录的URL
    baseurl = "http://new.cnzz.com/v1/login.php?t=login&siteid=1274657921"
    # requests 的session登录，以post方式，参数分别为url、headers、data
    content = session.post(baseurl,  cookies=requests.utils.dict_from_cookiejar(valcode.cookies),data=login_data)
    strHtml = content.content
    r = chardet.detect(strHtml)
    soup = BeautifulSoup(strHtml, 'lxml')

    # res = strHtml.decode("GB2312").encode("utf-8")
    print(soup)
    array = {
        'cookies': requests.utils.dict_from_cookiejar(valcode.cookies),
        'data': login_data
    }
    return array
    # print(content.text)

def cont( cookies=None, data=None,):
    session = requests.session()
    sheet_1 = []
    dic = dict()

    with open('test.csv', 'a') as f:
        fieldnames = ['ip', 'location']
        f_csv = DictWriter(f, fieldnames=fieldnames)
        f_csv.writeheader()
        starttime=datetime.now()
        for page in range(139,500):
            ddic = dict()
            s = session.get("https://web.umeng.com/main.php?c=flow&a=detail&ajax=module%3DfluxData_option%3Dpv%7Cmodule%3DdetailPvList_currentPage%3D"+str(page)+"_pageType%3D100&siteid=1274657921&st=2018-09-14&et=2018-09-14&visitorType=&visitorAgent=&visitorAct=&location=&refererType=&ip=&referer=&keyword=&hour=24&page=&cnzz_eid=&_=1536903726772",cookies=cookies, data=data)
            w = json.loads(s.text)
            b = w['data']['detailPvList']['items']
            for json1 in b:
                if json1['ip'] in dic.keys():
                    continue
                else:
                    ddic["ip"] = json1['ip']
                    ddic["location"] =json1['location']
                    try:
                        f_csv.writerow(ddic)
                        dic[json1['ip']] = "1"
                    except:
                        print("error page:" +page)
                        break
            print(page)
        endtime = datetime.now()
        print((endtime-starttime).seconds)


def main():
    line = login()
    print(line)
    cont( line['cookies'], line['data'])







main()