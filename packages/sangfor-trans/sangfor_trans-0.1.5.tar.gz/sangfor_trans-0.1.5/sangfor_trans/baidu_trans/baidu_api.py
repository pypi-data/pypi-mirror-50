#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import traceback
import json
from hashlib import md5

from sangfor_trans.compat import PY3
from sangfor_trans.compat import quote
from sangfor_trans.compat import HTTPConnection

from sangfor_trans.baidu_trans.setting import (
    API_URL, APP_ID, BASE_URL, SECRET_KEY, STATU_CODE_MAP, RANDOM_LOW, RANDOM_UP
    )
from sangfor_trans.config import (
    SUCCESS_STATUE_CODE, EXCEPT_STATU_CODE, SUCCESS, INVALID_SOURCE_LANG, INVALID_DEST_LANG, 
    LANGMAP, LANGMAP_REVERSED, NETWORK_ERRER, NETWORK_MOVED
)


class Translator(object):
    """
    百度翻译操作类
    """
    def __init__(self, app_id, secret_key):
       self.app_id = app_id
       self.secret_key = secret_key

    def translate(self, from_lang, to_lang, query_text):
        """
        百度翻译api入口
        from_lang:  源语言
        to_lang:    译文语言
        query_text: 翻译文本
        return：    返回翻译结果
        """

        http_client = None
        url = self.get_url(from_lang, to_lang, query_text)
        try:
            # API HTTP请求
            http_client = HTTPConnection(BASE_URL)
            http_client.request('GET', url)
        
            # 创建HTTPResponse对象
            response = http_client.getresponse()
            resp = response.read()

            # 网络错误
            if resp[4:9] == NETWORK_MOVED:
                return json.dumps({'msg': NETWORK_ERRER, 'statu_code': EXCEPT_STATU_CODE})

            result = json.loads(resp)
            # 状态码和信息处理
            error_code = result.pop('error_code', None)
            if error_code:
                result["statu_code"] = STATU_CODE_MAP.get(error_code, EXCEPT_STATU_CODE)
            else:
                result["statu_code"] = SUCCESS_STATUE_CODE
            result["msg"] = result.pop('error_msg', SUCCESS)
            
            return json.dumps(result)
             
        except Exception as e:
            traceback.print_exc()
        finally:
            if http_client:
                http_client.close()

    def get_url(self, from_lang, to_lang, query_text):
        """
        生成请求url
        """
        # 随机生成数据
        salt = random.randint(RANDOM_LOW, RANDOM_UP)
        # MD5生成签名
        sign = self.app_id + query_text + str(salt) + self.secret_key
        m1 = md5()
        if PY3:
            m1.update(sign.encode("utf-8"))
        else:
            m1.update(sign)
        sign = m1.hexdigest()
        # 拼接URL
        # url = API_URL + '?appid=' + self.app_id + '&q=' + quote(query_text) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign
        url = "{}?appid={}&q={}&from={}&to={}&salt={}&sign={}".format(API_URL, self.app_id, quote(query_text), from_lang, to_lang, str(salt), sign)        
        return url

