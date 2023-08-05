# -*- coding: UTF-8 -*-
import random
from http import cookiejar
from urllib import request, error

import requests
from selenium import webdriver

import os, sys
sys.path.append(os.path.abspath('.'))
HEADER = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


def get_random_user_agent():
    return random.choice(HEADER)


def get_proxy_header():
    return {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'User-Agent': get_random_user_agent()
    }


def get_simple_header():
    return {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
    }


class RequestBuilder(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.headers = get_simple_header()
        self.request_session = requests.session()  # 自动保持cookie

    def page_source(self, url):
        """
        使用selenium获取源码
        """
        self.driver.get(url)
        return self.driver.page_source

    def execute_source_script(self, js):
        """
        使用selenium执行js
        """
        return self.driver.execute_script(js)

    def get(self, url, retry_count=3, headers=None, proxies=None, data=None):
        """
        :param url: 请求 URL 链接
        :param retry_count: 失败重试次数
        :param headers: http header={'X':'x', 'X':'x'}
        :param proxies: 代理设置 proxies={"https": "http://12.112.122.12:3212"}
        :param data: (optional) Dictionary, bytes, urlencode(post_data), or file-like object to send in the body
        :return: 网页内容 | None
        """
        if url is None:
            return None
        if headers is None:
            headers = self.headers
        try:
            cookie = cookiejar.CookieJar()
            cookie_process = request.HTTPCookieProcessor(cookie)
            opener = request.build_opener(cookie_process)
            if proxies:
                opener.add_handler(request.ProxyHandler(proxies))

            req = request.Request(url, headers=headers, data=data)
            html = opener.open(req).read()
        except error.URLError as e:
            print('>>>Request error:', e.reason)
            html = None
            if retry_count > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # retry when return code is 5xx HTTP erros
                    return self.get(url, retry_count - 1, headers, proxies, data)
        return html

    def get_content(self, url, retry_count=3, headers=None, proxies=None, data=None):
        """
        :param url: 请求 URL 链接
        :param retry_count: 失败重试次数
        :param headers: http header={'X':'x', 'X':'x'}
        :param proxies: 代理设置 proxies={"https": "http://12.112.122.12:3212"}
        :param data: (optional) Dictionary, bytes, urlencode(post_data), or file-like object to send in the body
        :return: 网页内容 | None
        """
        if headers:
            self.request_session.headers.update(headers)
        try:
            if data:
                html = self.request_session.post(url, data, proxies=proxies).content
            else:
                html = self.request_session.get(url, proxies=proxies).content
        except (ConnectionError, requests.Timeout) as e:
            print('>>>Request ConnectionError or Timeout:' + str(e))
            html = None
            if retry_count > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # retry when return code is 5xx HTTP erros
                    self.get_content(url, retry_count - 1, headers, proxies, data)
        except Exception as e:
            print('>>>Request Exception:' + str(e))
            html = None
        return html


def main():
    url = 'http://www.baidu.com'
    content = RequestBuilder().get(url).decode('utf-8')
    print(str(content))

    content = RequestBuilder().get_content(url).decode('utf-8')
    print(str(content))


if __name__ == '__main__':
    main()
