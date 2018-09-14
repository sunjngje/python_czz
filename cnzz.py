# coding:utf-8
import urllib

import requests
import chardet
import re
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
     #   'username': u,
    }

    # 设置头信息
    headers_base = {
        'Host': 'web.umeng.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept-Language': 'zh-CN,zh;q:0.8,zh-TW;q:0.7,zh-HK;q:0.5,en-US;q:0.3,en;q:0.2',
        'Cookie': 'PHPSESSID:n6l8tms1vono6vvasjl3ed7ca5; PHPSESSID:n6l8tms1vono6vvasjl3ed7ca5; UM_distinctid:165d5cf50e54f-01a505e84ab7be-4c312878-1fa400-165d5cf50e7250; CNZZDATA30086426:cnzz_eid%3D1482631492-1536887867-https%253A%252F%252Fweb.umeng.com%252F%26ntime%3D1536887867; _cnzz_CV30069868:%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%7C%E6%9F%A5%E7%9C%8B%E5%AF%86%E7%A0%81%E7%99%BB%E5%BD%95%7C1536892258603; CNZZDATA30069868:cnzz_eid%3D50679563-1536886990-https%253A%252F%252Fweb.umeng.com%252F%26ntime%3D1536886266; CNZZDATA33222:cnzz_eid%3D1759931982-1536887468-https%253A%252F%252Fweb.umeng.com%252F%26ntime%3D1536887468; CNZZDATA30001831:cnzz_eid%3D1832564270-1536885496-https%253A%252F%252Fweb.umeng.com%252F%26ntime%3D1536890027; cn_ea1523f470091651998a_dplus:%7B%22distinct_id%22%3A%20%22165d5cf50e54f-01a505e84ab7be-4c312878-1fa400-165d5cf50e7250%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201536890462%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201536890462%7D%2C%22initial_view_time%22%3A%20%221536889081%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Fweb.umeng.com%2Flogin_check.php%3Fsiteid%3D1274657921%26url%3DKDw2SFcsUzBXLSNAYApgCg%253D%253D%26t%3Dlogin%22%2C%22initial_referrer_domain%22%3A%20%22web.umeng.com%22%7D',
        'Connection': 'keep-alive',
        'TE': 'Trailers'
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
    for i in range(1, 7000):
      s = session.get("https://web.umeng.com/main.php?c=flow&a=detail&ajax=module=report&siteid=1274657921&st=2018-09-14&et=2018-09-14&visitorFrom=pv&pageType=100&currentPage="+str(i)+"&visitorType=&visitorAgent=&visitorAct=&location=&refererType=&ip=&referer=&keyword=&hour=24&page=&cnzz_eid=&downloadType=xls",cookies=cookies, data=data)
      print("正在下载第"+str(i)+"页")
      with open('D:/py/demo1/cn_data/'+str(i)+".xls", 'wb') as f:
          f.write(s.content)



def get_page_source(cookies=None , data=None,):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.add_cookie(cookies)
    driver.get("https://web.umeng.com/main.php?c=flow&a=frame&siteid=1274657921#!/1536901756921/flow/detail/1/0/1274657921/2018-09-14/2018-09-14")

    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(1)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

    element = driver.find_element_by_id('rightContainer')
    outerhtml = element.get_attribute("outerHTML")
    driver.quit()
    print(outerhtml)
    return outerhtml


def Schedule(a,b,c):
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)


def main():
    line = login()
    print(line)
    cont( line['cookies'], line['data'])







main()

