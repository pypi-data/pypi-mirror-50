import json
import aiohttp
import asyncio
resps = []


# 为所有的请求构建一个session
async def main(urls,pool,method,params=None, datas=None, headers=None, cookies=None, proxy_str=None, timeout=None): # 启动
    try:
        if isinstance(headers,str):
            headers = str_to_dict(headers)
        if isinstance(params,str):
            params = str_to_dict(params)
        # 如果url是字符串,把其加到列表里
        if isinstance(urls,str):
            urls = [urls,]  # 如果urls 是字符串,放到列表里
            # print(urls,'当前url列表')
        sem = asyncio.Semaphore(pool)  # 限制同时请求数量 ,是一个semaphore对象

        async with aiohttp.ClientSession(cookies=cookies) as session:  # 给所有请求,创建同一个session
            tasks = []
            for url in urls:  # url 列表
                if url:
                    tasks.append(control_sem(sem,url,session,method,params=params,datas=datas,headers=headers, proxy_str=proxy_str, timeout=timeout)) # 放入tasks
            await asyncio.wait(tasks)  # 这个地方写错位置了
    except:
        pass


async def control_sem(sem, url, session,method, params=None, datas=None, headers=None, proxy_str=None, timeout=None):
    try:
        async with sem: # 在这个对象下
            await fetch(url,session,method,params=params, datas=datas, headers=headers, proxy_str=proxy_str, timeout=timeout)
    except:
        pass


async def fetch(url,session, method,params=None, datas=None, headers=None, proxy_str=None, timeout=None):
    try:
        '''
            request 函数,被get post 调用,接收多个参数
            1. 判断method
        '''
        if method in 'GETS':  # 发送url ,返回响应数据
            #  使用的 get
            async with session.get(url,params=params,headers=headers,proxy=proxy_str,timeout=timeout) as resp:
                body = await resp.read()
                resp = Myresponse(body,resp)
                resps.append(resp)
        elif method == 'POST':
            # aiohttp 的post 数据是data 不是datas
            async with session.post(url,data=datas,headers=headers,proxy=proxy_str,timeout=timeout) as resp:
                body = await resp.read()
                resp = Myresponse(body,resp)
                resps.append(resp)
    except:
        pass


def get(url, params=None, datas=None, headers=None, cookies=None, proxy_str=None, timeout=None, pool=100):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls=url,method='GET',params=params,datas=datas,headers=headers,cookies=cookies,proxy_str=proxy_str,timeout=timeout,pool=pool))
    try:
        return resps[0]
    except:
        return None


def gets(urls, params=None, datas=None, headers=None, cookies=None, proxy_str=None, timeout=None, pool=100):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls=urls, method='GETS', params=params, datas=datas, headers=headers, cookies=cookies,proxy_str=proxy_str, timeout=timeout, pool=pool))
    return resps


def post(url, params=None, datas=None, headers=None, cookies=None, proxy_str=None, timeout=None, pool=100):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls=url, method='POST', params=params, datas=datas, headers=headers, cookies=cookies,proxy_str=proxy_str, timeout=timeout, pool=pool))
    try:
        return resps[0]
    except:
        return None


class Myresponse(object):
    def __init__(self,body, resp):
        self.body = body
        self.resp = resp
        self.results = []

    @property
    def text(self):  # text 类型
        try:
            return self.body.decode('utf-8')
        except:
            return self.body.decode('gbk')
    @property
    def content(self):
        return self.body

    def json(self,value):
        text = json.loads(self.body)
        get_v(text,value)
        if len(results) == 1:
            return results[0]  # 如果只有一个元素,直接返回元素,不返回列表套一个元素
        else:
            return results
    @property
    def cookies(self):
        print(self.resp.cookies)
        return self.resp.cookies
    @property
    def headers(self):
        return self.resp.headers
    @property
    def url(self):
        return self.resp.url
    @property
    def status(self):
        return self.resp.status


results = []


def get_v(text, value):
    if not text:
        return results
    if isinstance(text, dict):
        try:
            results.append(text[value])
            if not isinstance(text[value],str):  # 这个地方要考虑到 列表的值也可能是字典
                get_v(text[value],value)
        except:
            for k, v in text.items():
                get_v(text[k], value)
    if isinstance(text, list):
        result = []
        for t in text:
            if t == value:
                result.append(t)
                results.append(t)
        if result:
            return results
        else:
            for i in text:
                get_v(i, value)


def str_to_dict(str1):
    headers = {}
    for i in str1.split('\n'):
        try:
            l = i.split(':', 1)
            headers[l[0].strip()] = l[1].strip()
        except:
            pass
    return headers