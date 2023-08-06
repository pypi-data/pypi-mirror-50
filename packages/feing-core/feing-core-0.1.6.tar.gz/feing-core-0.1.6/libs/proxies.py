# -*- coding:UTF-8 -*-
import datetime
import os
import re
import subprocess as sp
import telnetlib
import time

import requests
from bs4 import BeautifulSoup
from lxml import etree

from wrappers.request import get_simple_header, get_proxy_header

# 西祠代理高匿IP地址
IP_HOST = 'http://www.xicidaili.com'
ROOT_DIR = 'data'
PROXIES_DIR = 'proxies'


def get_proxy(protocol='http', proxies_dir=PROXIES_DIR, total_page=1):
    """
    获取代理：获取本地当日可用代理
    :return: 代理字典
    """
    if os.path.exists(ROOT_DIR) is False:
        os.makedirs(ROOT_DIR)
    save_dir = ROOT_DIR + os.path.sep + proxies_dir
    save_dir = save_dir + '_%s.txt' % time.strftime('%Y-%m-%d')

    # 本地代理文件不存在则生成代理文件
    if not os.path.exists(save_dir):
        generate_proxies(total_page, proxies_dir)

    # 读取本地代理文件
    f = open(save_dir, 'r')
    proxies = f.readlines()
    proxies_count = len(proxies)

    if str(proxies).find(protocol + '#') == -1 or proxies_count == 0:
        generate_proxies(total_page, proxies_dir)
        get_proxy()
        return

    active_proxy = None
    save_proxies = []
    for i in range(0, proxies_count):
        proxy = proxies[i]
        split_proxy = proxy.strip("\n").split('#')
        scheme = split_proxy[0]
        if protocol == scheme:
            ip = split_proxy[1]
            port = split_proxy[2]
            # 检测并重写可用代理
            if test_proxy(ip, port=port, time_out=10):
                active_proxy = {scheme: ip + ':' + port}
                print('可用代理： %s' % active_proxy)
                save_proxies.append(proxies[i])
    f.close()

    f = open(save_dir, 'w')
    for proxy in save_proxies:
        f.write(str(proxy))
    f.close()

    return active_proxy


def generate_proxies(total_page, proxies_dir):
    """
    生成可用代理文件
    """
    print('生成可用代理文件...')
    if os.path.exists(ROOT_DIR) is False:
        os.makedirs(ROOT_DIR)
    save_dir = ROOT_DIR + os.path.sep + proxies_dir
    f = open(save_dir + '_%s.txt' % time.strftime('%Y-%m-%d'), 'a')

    for i in range(1, total_page + 1):
        proxies = get_proxies(i)
        if len(proxies) == 0:
            print('代理列表为空')
            return None

        for proxy in proxies:
            split_proxy = proxy.split('#')
            if test_proxy(split_proxy[1], port=split_proxy[2], time_out=10):
                f.write(str(proxy))
                f.write('\n')
    f.close()
    print('代理已检测完成并保存至\'%s\'' % save_dir)


def get_proxies(page=1):
    """
    获取代理列表
    :param page: 高匿代理页数,默认获取第一页
    :return: 代理列表
    """
    request_session = requests.Session()
    target_url = IP_HOST + '/nn/%d' % page
    target_headers = get_simple_header()
    target_headers.update({
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Referer': IP_HOST + '/nn/',
        'Upgrade-Insecure-Requests': '1'
    })

    print('分析第%s页代理, url：%s' % (page, target_url))
    target_response = request_session.get(url=target_url, headers=target_headers)
    target_response.encoding = 'utf-8'
    target_html = target_response.text
    bf1_ip_list = BeautifulSoup(target_html, 'lxml')
    bf2_ip_list = BeautifulSoup(str(bf1_ip_list.find_all(id='ip_list')), 'lxml')
    ip_list_info = bf2_ip_list.table.contents
    proxies = []

    for index in range(len(ip_list_info)):
        if index % 2 == 1 and index != 1:
            dom = etree.HTML(str(ip_list_info[index]))
            ip = dom.xpath('//td[2]')
            port = dom.xpath('//td[3]')
            protocol = dom.xpath('//td[6]')
            proxies.append(protocol[0].text.lower() + '#' + ip[0].text + '#' + port[0].text)

    return proxies


def test_proxy(ip, port, time_out=20):
    """
    测试代理是否可用
    :param ip: 代理IP
    :param port: 代理IP端口
    :param time_out: 请求超时时间
    :return: True/False
    """
    proxies = {'http': ip + ':' + port}
    year = str(datetime.datetime.now().year)
    url = 'http://' + year + '.ip138.com/ic.asp'
    header = get_proxy_header()
    header.update({
        'Host': 'www.ip138.com'
    })

    try:
        print('%s 检测中...' % proxies)
        response = requests.get(url, headers=header, proxies=proxies, timeout=time_out)
        if response.status_code == 200:
            response.encoding = 'gbk'
            result = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', response.text)
            result = result.group()
            # 验证IP的前面9位
            if result[:9] == ip[:9]:
                print('%s 检测通过' % proxies)
                return True
            else:
                print('%s 检测通过' % proxies)
                return False
        else:
            print('%s 检测未通过' % proxies)
            return False
    except Exception as e:
        print('%s 连接超时: %s' % (proxies, str(e)))
        return False


def telnet_ip(ip, port, time_out=20):
    """
    检测IP的连通性
    :param ip: 代理IP
    :param port: 代理IP端口
    :param time_out: 请求超时时间
    :return: True/False
    """
    try:
        telnetlib.Telnet(ip, port=port, timeout=time_out)
    except:
        print('IP %s 连接超时, 重新获取...' % ip)
        return False
    else:
        print('IP %s 检测通过' % ip)
        return True


def get_ip_elapsed_time(ip, lose_time, waste_time):
    """
    获取IP的平均耗时
    :param ip: IP地址
    :param lose_time: 匹配丢包数
    :param waste_time: 匹配平均时间
    :return average_time: 平均耗时
    """
    # 命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
    cmd = 'ping -n 3 -w 3 %s'
    # 执行命令
    p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    # 获得返回结果并解码
    out = p.stdout.read().decode('gbk')
    # 丢包数
    lose_time = lose_time.findall(out)
    # 当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
    if len(lose_time) == 0:
        lose = 3
    else:
        lose = int(lose_time[0])
    # 如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
    if lose > 2:
        # 返回False
        return 1000
    # 如果丢包数目小于等于2个,获取平均耗时的时间
    else:
        # 平均时间
        average = waste_time.findall(out)
        # 当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
        if len(average) == 0:
            return 1000
        else:
            #
            average_time = int(average[0])
            # 返回平均耗时
            return average_time


def init_pattern():
    """
    初始化正则表达式
    :return lose_time: 匹配丢包数
    :return waste_time: 代匹配平均时间
    """
    # 匹配丢包数
    lose_time = re.compile(u'丢失 = (\d+)', re.IGNORECASE)
    # 匹配平均时间
    waste_time = re.compile(u'平均 = (\d+)ms', re.IGNORECASE)
    return lose_time, waste_time


if __name__ == '__main__':
    print(get_proxy(total_page=2))
