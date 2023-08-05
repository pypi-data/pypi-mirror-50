r'''
qq_tr for free

https://cloud.tencent.com/document/api/551/15619
目标语言，参照支持语言列表
zh : 中文
en : 英文
jp : 日语
kr : 韩语
de : 德语
fr : 法语
es : 西班牙文
it : 意大利文
tr : 土耳其文
ru : 俄文
pt : 葡萄牙文
vi : 越南文
id : 印度尼西亚文
ms : 马来西亚文
th : 泰文
auto : 自动识别源语言，只能用于source字段

'''
# pylint: disable=C0103

import logging
import re
from time import time, sleep
from random import random
import uuid

import requests
from .get_qtk_qtv import COOKIES
from .qq_langpair import qq_langpair

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

UUID = uuid.uuid1().int
URL = "https://fanyi.qq.com/api/translate"
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


SESS = requests.Session()
SESS.get('https://fanyi.qq.com')
SESS.headers.update(HEADERS)
SESS.cookies.update(COOKIES)


class EmptyResu(Exception):
    ''' empty result'''
    pass


# QQ_FANYI = QqFanyi()
def _qq_tr(text, from_lang='auto', to_lang='zh'):
    '''
    refactor QqFanyi in qq_fangyi.py

    '''

    trtext = ''
    jdata = {}  # json response
    _qq_tr.suggest = ''

    # refer to https://blog.csdn.net/best_fish/article/details/83997229
    uuid_ = int(time() * 1000)

    data = {
        'source': from_lang,
        'target': to_lang,
        'sourceText': text,
        # 'sessionUuid': UUID,
        # 'sessionUuid': uuid.uuid1().int,
        'sessionUuid': "translate_uuid" + str(uuid_),
    }
    try:
        resp = SESS.post(URL, data=data)
        resp.raise_for_status()
    except Exception as exc:
        LOGGER.error("sess(URL, data=data) exc: %s", exc)
        raise
        # return None

    try:
        jdata = resp.json()
    except Exception as exc:
        LOGGER.error("jdata = resp.json() exc: %s", exc)
        raise
        # return None

    tmp = [elm.get('targetText') for elm in jdata.get('translate').get('records')]
    trtext = ''.join(tmp)
    try:
        _qq_tr.suggest = [elm.get('translate').strip() + ' ' + elm.get('word').strip() for elm in jdata.get('suggest').get('data')]  # NOQA
    except Exception as exc:
        # LOGGER.debug("_qq_tr.suggest = ...exc: %s", exc)
        _qq_tr.suggest = []

    return trtext


def qq_tr(text, from_lang='auto', to_lang='zh', timeout=16):
    '''proxy of _qq_tr

    try timeout=20 seconds, sleep(random()/2)

    >>> qq_tr('this is a test.')
    '这是个测试。'
    >>> len(qq_tr('这是个测试')) > 4
    True
    >>> qq_tr('这是个测试', to_lang='de')
    'Das ist ein Test.'
    >>> qq_tr('这是个测试', to_lang='dde')
    'Das ist ein Test.'
    >>> qq_tr('这是个测试', to_lang='en')
    'This is a test'
    '''

    # refer to sogou_langpair and youdao_langpair
    from_lang, to_lang = qq_langpair(from_lang, to_lang)

    if not text.strip():
        return ''

    resu = _qq_tr(text, from_lang=from_lang, to_lang=to_lang).strip()

    # return QQ_FANYI.translate(text, from_lang=from_lang, to_lang=to_lang)

    # give another try if empty
    # by converting to 'de' first
    if not re.sub(r'[。，！]', '', resu).strip():
        trtext_de = _qq_tr(text, from_lang=from_lang, to_lang='de')
        resu = _qq_tr(trtext_de, from_lang='de', to_lang=to_lang).strip()

    return resu
