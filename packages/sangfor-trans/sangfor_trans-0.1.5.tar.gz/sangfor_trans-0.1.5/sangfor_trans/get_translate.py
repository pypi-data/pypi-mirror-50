# -*- coding:utf-8 -*-
# from __future__ import unicode_literals
import json
import importlib
from sangfor_trans.baidu_trans import baidu_api
from sangfor_trans.google_trans import google_crawl

from sangfor_trans.config import (
    GOOGLE, BAIDU, EXCEPT_STATU_CODE, INVALID_TRANS_TYPE, INVALID_PARAMETER, APP_ID, SECRET_KEY, 
    PARAM_STATUE_CODE, CRAWL, API, INVALID_TRANS_MODE, NO_SUCH_MODE, LANG_ERROR, LANG_TYPE_ERROR, 
    TRANS_TYPE_LIST, TRANS_MODE_LIST, LANGUAGES, INVALID_LANG_ERROR
)


class GetTranslator(object):
    """翻译操作类，获取翻译对象
    
    trans_type：翻译器（翻译类型）
    """

    def __init__(self, trans_type=GOOGLE, mode=CRAWL, app_id=APP_ID, secret_key=SECRET_KEY):
        """默认用谷歌翻译器"""
        self.trans_type = trans_type
        self.mode = mode
        self.app_id = app_id
        self.secret_key = secret_key

    def translate(self, from_lang, to_lang, query_text):
        """  
        from_lang：源语言  
        to_lang：译文语言  
        query_text：翻译内容  

        -- 语言列表如下 --
        auto：自动检测（to_lang不支持auto）  
        zh：中文  
        en：英语  
        jp：日语  
        kor：韩语  
        fra：法语  
        de：德语  
        yue：粤语  
        spa：西班牙语  
        th：泰语  
        ru：俄语  
        ara：阿拉伯语  
        ......
        """
        from_lang = from_lang.lower().strip()
        to_lang = to_lang.lower().strip()
        
        # 判读传入字段是否为空
        if not from_lang or not to_lang or not query_text:
            return self.invalid_func(PARAM_STATUE_CODE, INVALID_PARAMETER)

        # 源语言和译文语言不能相同
        if from_lang == to_lang:
            return self.invalid_func(EXCEPT_STATU_CODE, LANG_ERROR)
        
        # 源语言和译文语言类型判断
        if not isinstance(from_lang, str) or not isinstance(to_lang, str):
            return self.invalid_func(EXCEPT_STATU_CODE, LANG_TYPE_ERROR)
        
        # 判断翻译语言是否在支持列表
        if from_lang not in LANGUAGES or to_lang not in LANGUAGES:
            return self.invalid_func(EXCEPT_STATU_CODE, INVALID_LANG_ERROR)
        
        # 判断翻译方式是否在范围内
        if self.mode not in TRANS_MODE_LIST:
            return self.invalid_func(EXCEPT_STATU_CODE, INVALID_TRANS_MODE)

        # 判断翻译器（翻译类型）是否在范围内
        if self.trans_type not in TRANS_TYPE_LIST:
            return self.invalid_func(EXCEPT_STATU_CODE, INVALID_TRANS_TYPE)
        
        if not isinstance(query_text, list) and isinstance(query_text, str):
            query_text = query_text.replace("\n", "")
        
        
        # 翻译方式默认映射
        mode_map = {BAIDU: baidu_api, GOOGLE: google_crawl}
        # 动态导入翻译模块
        trans_module = importlib.import_module("sangfor_trans.{0}_trans".format(self.trans_type))
        trans_module = getattr(trans_module, '{0}_{1}'.format(self.trans_type, self.mode), mode_map[self.trans_type])
        translator = trans_module.Translator(app_id=self.app_id, secret_key=self.secret_key)
        trans_result = translator.translate(from_lang, to_lang, query_text)

        return trans_result

    @staticmethod
    def invalid_func(statu_code, msg):
        trans_result = dict()
        trans_result["statu_code"] = statu_code
        trans_result["msg"] = msg
        return json.dumps(trans_result)
            
