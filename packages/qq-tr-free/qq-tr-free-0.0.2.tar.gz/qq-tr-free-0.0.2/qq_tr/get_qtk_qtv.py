'''
Visit http://fanyi.qq.com to obtain qtk,qtv from http://fani.qq.com

'''
import re
import requests

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "DNT": "1",
    "Host": "fanyi.qq.com",
    "Origin": "http://fanyi.qq.com",
    "Referer": "http://fanyi.qq.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def get_qtk_qtv():
    ''' Fetch qtk qtv from fanyi.qq.com '''
    sess = requests.Session()
    resp = sess.get('http://fanyi.qq.com/')
    qtk = ''.join(re.findall(r'qtk=.*?==', resp.text))
    qtv = ''.join(re.findall(r'qtv=[^"]*', resp.text))

    temp = tuple(qtk.split('=', 1)), tuple(qtv.split('=', 1))

    return dict(temp)

COOKIES = get_qtk_qtv()
