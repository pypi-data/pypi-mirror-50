import requests
import time
import os
import pickle
import zxing
import pyqrcode

user_id = None
uid = None
access_token = None
cookies = requests.cookies.RequestsCookieJar()


def login():
    global user_id, uid, access_token
    load_cookies()
    status = check_login_status()
    if status is False:
        print('cookies过期 请重新登陆')
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        }
        s = requests.session()
        result = get_qrcode()
        imgurl = result[0]
        token = result[1]
        res = s.get(imgurl, headers=headers, cookies=cookies)
        content = res.content
        f = open('image.png', 'wb')
        f.write(content)
        f.close()
        reader = zxing.BarCodeReader()
        raw = reader.decode("image.png").raw
        url = pyqrcode.create(raw)
        print(url.terminal(quiet_zone=1))
        start = time.time()
        while True:
            if time.time() - start < 120:
                url = 'https://www.zhihu.com/api/v3/account/api/login/qrcode/{}/scan_info'.format(token)
                res = s.get(url, headers=headers)
                if res.status_code == 200:
                    content = res.json()
                    if 'status' in content:
                        if content['status'] == 1:
                            print('扫码成功 请确认登陆')
                            continue
                    else:
                        print('成功确认登陆')
                        cookies_dict = res.cookies.get_dict()
                        for key in cookies_dict:
                            cookies.set(key, cookies_dict[key])
                        user_id = content['user_id']
                        uid = content['uid']
                        access_token = content['access_token']
                        q_c0 = content['cookie']['q_c0']
                        z_c0 = content['cookie']['z_c0']
                        cookies.set('q_c0', q_c0)
                        cookies.set('z_c0', z_c0)
                        save_cookies()
                        os.system('cls')
                        return True

            else:
                print('验证码已经过期')
                return False
    else:
        print('成功从文件加载cookies')


def get_qrcode():
    global cookies
    s = requests.session()
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
    }

    url = 'https://www.zhihu.com/signin?next=%2F'
    res = s.get(url=url, headers=headers)
    cookies_dict = res.cookies.get_dict()
    for key in cookies_dict:
        cookies.set(key, cookies_dict[key])

    url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
    res = s.get(url, headers=headers)
    cookies_dict = res.cookies.get_dict()
    for key in cookies_dict:
        cookies.set(key, cookies_dict[key])

    url = 'https://www.zhihu.com/udid'
    res = s.post(url=url, headers=headers)
    cookies_dict = res.cookies.get_dict()
    for key in cookies_dict:
        cookies.set(key, cookies_dict[key])

    url = 'https://www.zhihu.com/api/v3/account/api/login/qrcode'
    res = s.post(url, headers=headers, cookies=cookies, data="")
    token = res.json()['token']
    imgurl = 'https://www.zhihu.com/api/v3/account/api/login/qrcode/{}/image'.format(token)
    result = [imgurl, token]
    return result


def save_cookies():
    f = open('cookies', 'wb')
    pickle.dump(cookies, f)
    f.close()


def load_cookies():
    global cookies
    try:
        f = open('cookies.txt', 'rb')
        data = pickle.load(f)
        cookies = data
    except FileNotFoundError:
        print('cookie文件不存在')


def check_login_status():
    s = requests.session()
    url = 'https://www.zhihu.com/api/v4/me'
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
    }
    res = s.get(url, headers=headers, cookies=cookies)
    content = res.json()
    if 'error'in content:
        return False
    else:
        return True
