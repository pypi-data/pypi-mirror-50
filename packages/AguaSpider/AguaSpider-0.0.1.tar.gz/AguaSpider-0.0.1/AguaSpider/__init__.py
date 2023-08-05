import aiohttp
import asyncio
from lxml import etree
import json

loop = asyncio.get_event_loop()   #构建事件循环队列
result = []
def get(url,params={},headers={},cookies={},proxy='',timeout=None):
    return __request(urls=[url],method='GET',params=params,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout)[0]

def gets(urls,params={},headers={},cookies={},proxy='',timeout=None):
    return __request(urls=urls,method='GET',params=params,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout)


def post(url,data={},headers={},cookies={},proxy='',timeout=None):
    return __request(urls=[url],method='POST',params=data,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout)[0]

def __request(urls,method=None,params={},headers={},cookies={},proxy='',timeout=None):
    tasks = []
    for url in urls:
        #向tasks中添加面函数
        tasks.append(main(url,method=method,params=params,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout))
    loop.run_until_complete(asyncio.wait(tasks))   #执行tasks列表中的main函数
    return result

#执行请求，获得响应
async def main(url,method=None,params={},headers={},cookies={},proxy='',timeout=None):
    async with aiohttp.ClientSession() as sess:
        resp = await sess.request(url=url,method=method,params=params,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout)
        body = await resp.read()
        resp = MyResponse(body)
        result.append(resp)


def switch_dict(str):
    #将字符串形式的headers等，转换成字典
    p={}
    # print(str.split('\n'))
    for s in str.split('\n'):
        if s == '':
            continue
        datas=s.split(': ')
        p.update({datas[0].strip():datas[1].strip()})
    return p

class MyResponse():
    def __init__(self,body):
        self.body = body

    @property
    def text(self):
        try:
            return self.body.decode('utf-8')
        except:
            return self.body.decode('gbk')

    @property
    def json(self):
        return json.loads(self.body)


    def get_element_from_xpath(self,str):
        element = etree.HTML(self.body).xpath(str)
        return element[0]   #返回一个str

    def get_elements_from_xpath(self,str):
        return etree.HTML(self.body).xpath(str)   #返回一个list

    def findall(self,f_json, key):
        result = []

        if type(f_json) == dict:
            # print(True)
            for i in f_json:
                if i == key:
                    result.append(f_json[i])

                else:
                    f_json = f_json[i]
                    result += (self.findall(f_json, key))
        elif type(f_json) == list:
            for i in f_json:
                if type(i) == dict:
                    f_json = i
                    result += (self.findall(f_json, key))
                # else:
                #     continue
        else:
            return []
        return result
