#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author  : mundane
# @time    : 2017/5/18 10:51
# @file    : ZhihuLogin.py
# @Software: PyCharm Community Edition

import requests, time
from bs4 import BeautifulSoup
from http import cookiejar
from PIL import Image

session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
}
try:
    # 从本地文件加载cookies
    # ignore_discard的意思是即使cookies将被丢弃也将它保存下来，ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
    session.cookies.load(ignore_discard=True)
except Exception as e:
    print('exception:', e)
    print('还没有cookie信息')


def get_xsrf():
    url = 'https://www.zhihu.com'
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # <input type="hidden" name="_xsrf" value="0448114b8b68c194d9fc9d831d251379">
    tag = soup.find('input', attrs={'name': '_xsrf'})
    return tag['value']


def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    response = session.get(captcha_url, headers=headers)
    captcha_name = 'captcha.gif'
    with open(captcha_name, 'wb') as f:
        f.write(response.content)
    im = Image.open(captcha_name)
    im.show()
    return input('请输入验证码: ')


def get_email():
    return input('请输入邮箱: ')


def get_password():
    return input('请输入密码: ')


def login(email, password, _xsrf, captcha):
    data = {
        '_xsrf': _xsrf,
        'password': password,
        'email': email,
        'captcha': captcha
    }
    login_url = 'https://www.zhihu.com/login/email'
    response = session.post(login_url, data=data, headers=headers)
    print('response.json() =', response.json())
    # 保存cookies到本地
    session.cookies.save()


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    # 这里重定向一定要设置为false, 否则就算没有登录会被重定向到登录的地址去, 然后code就返回200了
    response = session.get(url, headers=headers, allow_redirects=False)
    code = response.status_code
    if code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
        email = get_email()
        password = get_password()
        _xsrf = get_xsrf()
        print('_xsrf =', _xsrf)
        captcha = get_captcha()
        login(email, password, _xsrf, captcha)
